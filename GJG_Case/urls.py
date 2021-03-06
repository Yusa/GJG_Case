from django.contrib import admin
from django.urls import include, path, re_path
from rest_framework import routers
from GJG_Case.scoreboard_api import views
from rest_framework.urlpatterns import format_suffix_patterns


router = routers.DefaultRouter()

urlpatterns = [
	path('admin/', admin.site.urls),
    path('user/create/', views.UserListNewView.as_view()), # Works with POST request
    re_path(r'user/profile/(?P<guid>([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})|)', views.UserListNewView.as_view()), # Works with GET request
    path('leaderboard/', views.LeaderboardView.as_view()), # Works with GET request    
    path('leaderboard/<country_code>/', views.LeaderboardView.as_view()), # Works with GET request
	path('score/submit/', views.ScoreView.as_view()), # Works with POST request
	path('user/create/bulk/', views.UserCreateBulkView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
