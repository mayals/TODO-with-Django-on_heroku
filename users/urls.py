from django.urls import path
from . import views 


app_name = 'users'
urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='UserLogin'),
    path('logout/', views.UserLogoutView.as_view(),name='UserLogout'),
    path('signup/', views.UserFormView.as_view(), name='UserForm'),
    path('profileupdate/', views.profile_user_edit, name='profile_user_edit'),
    path('profile/', views.profile_view, name='profile_view'),
]
