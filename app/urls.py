from django.urls import path
from . import views


urlpatterns = [
	path('register/',views.registerPage, name="register"),
	path('login/',views.loginPage, name="login"),  
	path('logout/',views.logoutUser, name="logout"),
    #path('', views.home, name="home"),
    #path('user/', views.userPage, name="user-page"),
    #path('account/', views.accountSettings, name="account"),
    path('client/', views.clientPage, name="client"),
    path('lawyer/', views.lawyerPage, name="lawyer"),
]