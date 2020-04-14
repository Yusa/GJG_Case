from django.shortcuts import render
from django.db import IntegrityError
import sys, traceback

# Create your views here.
from GJG_Case.ScoreboardApi.serializers import UserProfileSerializer, LeaderboardSerializer, ScoreSubmitSerializer
from GJG_Case.ScoreboardApi.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import GJG_Case.settings as settings

class UserListNewView(APIView):
    def get(self, request, guid, format=None):
        try:
            # user_id is given as empty string
            if guid.strip() == "":
                return Response({"error": "User ID is not given in the correct format."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                users = User.objects.get(user_id=guid)
                serializer = UserProfileSerializer(users)
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


class LeaderboardView(APIView):
    def get(self, request, country_code=None, format=None):
        try:
            if country_code == None:
                users = User.objects.all().order_by('rank')
                serializer = LeaderboardSerializer(users, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            
            elif len(country_code) != 2 or not country_code.isalpha():
                return Response({"error":"Country code is not valid."}, status=status.HTTP_400_BAD_REQUEST)

            else:
                users = User.objects.filter(country=country_code).order_by('rank')
                if len(users):
                    serializer = LeaderboardSerializer(users, many=True)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response({"result":"No user record exists for the given country code."}, status=status.HTTP_200_OK)

        except Exception as e:
            if settings.DEBUG:
                print(f"Exceptin in {__name__}: {e}")
            return Response({"error": "Unknown"}, status=status.HTTP_400_BAD_REQUEST)



class ScoreView(APIView):
    def post(self, request, format=None):
        try:
            if "user_id" in request.data.keys():
                user = User.objects.get(user_id=request.data["user_id"])
                serializer = ScoreSubmitSerializer(user, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response({"result":"1"}, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error": "user_id is not given."}, status=status.HTTP_400_BAD_REQUEST)        
        except Exception as e:
            if settings.DEBUG:
                print(f"Exceptin in {__name__}: {e}")
                #traceback.print_exc(file=sys.stdout)
            if "matching query does not exist" in str(e):
               return Response({"error":"User with given user_id does not exists."}, status=status.HTTP_400_BAD_REQUEST, content_type=None)               
            return Response({"error": "Unknown"}, status=status.HTTP_400_BAD_REQUEST)



class UserCreateBulkView(APIView):
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