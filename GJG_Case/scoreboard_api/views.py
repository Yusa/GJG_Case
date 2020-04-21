from django.shortcuts import render
from django.db import IntegrityError
import sys, traceback

from GJG_Case.scoreboard_api.serializers import UserProfileSerializer, LeaderboardSerializer, ScoreSubmitSerializer, BulkUserSerializer
from GJG_Case.scoreboard_api.models import User, ScoreSubmitHistory
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination, CursorPagination
from GJG_Case.scoreboard_api.pagination import LeaderboardPagination
from rest_framework.response import Response
from rest_framework import status

import GJG_Case.settings as settings
from django.utils import timezone

class UserListNewView(APIView):
    def get(self, request, guid, format=None):
        try:
            # user_id is given as empty string
            if guid.strip() == "":
                return Response({"error": "User ID is not given in the correct format."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                user = User.objects.get(user_id=guid)
                need_update = ScoreSubmitHistory.objects.filter(created_at__gt=user.updated_at, min_rank__lte=user.rank, max_rank__gte=user.rank).count()
                if need_update:
                    rank_new = User.objects.filter(points__gte=user.points).exclude(user_id=user.user_id).count() + 1
                    user.rank = rank_new
                    user.save()
                serializer = UserProfileSerializer(user)
                return Response(serializer.data, status=status.HTTP_200_OK)
    
        except Exception as e:
            if settings.DEBUG:
                print(f"Exception in {__name__}: {e}")            
            if "matching query does not exist" in str(e):
                return Response({"error": "User doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)
            else:               
                return Response({"error": "Unknown"}, status=status.HTTP_400_BAD_REQUEST)


    def post(self, request, format=None):
        try:
            serializer = UserProfileSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"result":"1"}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError as e:
            if 'unique constraint' in str(e).lower():
                return Response({"error":"User already exists."}, status=status.HTTP_400_BAD_REQUEST, content_type=None)
            else:
                if settings.DEBUG:
                    print("Integrity error:", e)
                return Response({"error": e}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            if settings.DEBUG:
                print(f"Exception in {__name__}: {e}")
            return Response({"error": "Unknown"}, status=status.HTTP_400_BAD_REQUEST)


class LeaderboardView(APIView, LeaderboardPagination):
    def get(self, request, country_code=None, format=None):
        try:
            # Main Leaderboard without Country Code
            if country_code == None:
                users = User.objects.all()
                results = self.paginate_queryset(users, request, view=self)
                ranks = [user.rank for user in results]
                ranks_u = list(set(ranks))

                # Since every score.submit possibly cause rank duplication if rank of the player changes.
                # So that we are checking duplicated ranks in the page. If exists, the ranks in the page is 
                # re-evaluated and saved to database.
                if len(ranks) != len(ranks_u) or ranks[0] != self.page_size * (self.page.number - 1) + 1 or ranks[-1] != self.page_size * (self.page.number - 1) + len(results):
                    page_start_rank = (self.page.number-1) * self.page_size + 1
                    for ctr, user in enumerate(results):
                        user.rank = page_start_rank + ctr
                        user.updated_at = timezone.now()

                    User.objects.bulk_update(results, ['rank', 'updated_at']) #This one speeded up 10x compared tu user.save()

                serializer = LeaderboardSerializer(results, many=True)
                return self.get_paginated_response(serializer.data)

            elif len(country_code) != 2 or not country_code.isalpha():
                return Response({"error":"Country code is not valid."}, status=status.HTTP_400_BAD_REQUEST)

            else: # If there is a country code given.
                users = User.objects.filter(country=country_code).order_by("-points")
                if len(users):
                    update_needed = False
                    results = self.paginate_queryset(users, request, country_code, view=self)
                    # hist = ScoreSubmitHistory.objects.all()
                    users_to_update = []
                    for user in results:
                        hist_check = ScoreSubmitHistory.objects.filter(created_at__gt=user.updated_at, min_rank__lt=user.rank, max_rank__gt=user.rank).exists()
                        if hist_check:
                            rank_new = User.objects.filter(points__gte=user.points, rank__lt=user.rank).count() + 1
                            user.rank = rank_new
                            user.updated_at = timezone.now()
                            users_to_update.append(user)
                            update_needed = True

                    if update_needed:
                        User.objects.bulk_update(users_to_update, ['rank','updated_at'])

                    serializer = LeaderboardSerializer(results, many=True)
                    return self.get_paginated_response(serializer.data)
                else:
                    return Response({"result":"No user record exists for the given country code."}, status=status.HTTP_200_OK)

        except Exception as e:
            if settings.DEBUG:
                print(f"Exception in {__name__}: {e}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)



class ScoreView(APIView):
    def post(self, request, format=None):
        try:
            if "user_id" in request.data.keys():
                user = User.objects.get(user_id=request.data["user_id"])
                user_serializer = ScoreSubmitSerializer(user, data=request.data)
                if user_serializer.is_valid():
                    user_serializer.save()
                    return Response({"result":"1"}, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error": "user_id is not given."}, status=status.HTTP_400_BAD_REQUEST)        
        except Exception as e:
            if settings.DEBUG:
                print(f"Exception in {__name__}: {e}")
                #traceback.print_exc(file=sys.stdout)
            if "matching query does not exist" in str(e):
               return Response({"error":"User with given user_id does not exists."}, status=status.HTTP_400_BAD_REQUEST, content_type=None)               
            return Response({"error": "Unknown"}, status=status.HTTP_400_BAD_REQUEST)



class UserCreateBulkView(APIView):
    def post(self, request, format=None):
        if 'count' in request.data.keys():
            count = request.data['count']
            if count == len(request.data['users']):
                errors = []
                for user in request.data['users']:
                    try:
                        serializer = BulkUserSerializer(data=user)
                        if serializer.is_valid():
                            serializer.save()
                        else:
                            errors.append({"error":serializer.errors, 'user':user})
                    except IntegrityError as e:
                        if 'unique constraint' in str(e).lower():
                            errors.append({"error":"User already exists.", "user":user})
                        else:
                            if settings.DEBUG:
                                print("Integrity error:", e)
                            errors.append({"error": e, "user":user})
                    except Exception as e:
                        if settings.DEBUG:
                            print(f"Exception in {__name__}: {e}")
                        errors.append({"error": "Unknown", "user":user})
                return Response(errors, status=status.HTTP_200_OK)
            else:
                return Response({"error": "count-amount mismatch."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "count is not specified."}, status=status.HTTP_400_BAD_REQUEST)
