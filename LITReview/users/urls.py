from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.loginUser, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerUser, name="register"),

    path('', views.profiles, name="profiles"),
    path('profile/<str:pk>/', views.userProfile, name="user-profile"),
    path('account/', views.userAccount, name="account"),

    path('edit-account/', views.editAccount, name="edit-account"),

    path('create-interest/', views.createInterest, name="create-interest"),
    path('update-interest/<str:pk>/', views.updateInterest, name="update-interest"),
    path('delete-interest/<str:pk>/', views.deleteInterest, name="delete-interest"),
    path('favourite/<str:pk>/', views.favourite, name='favourite'),
]