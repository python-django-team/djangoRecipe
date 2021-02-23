from django.urls import path
from . import views

app_name = "app"
urlpatterns = [
    path("siteUser/login", views.SiteUserLoginView.as_view(), name="site_user_login"),
    path("siteUer/logout", views.SiteUserLogoutView.as_view(), name="site_user_logout"),
    path("siteUser/register", views.SiteUserRegisterView.as_view(), name="site_user_register"),
    path("siteUser/profile", views.SiteUserProfileView.as_view(), name="site_user_profile"),
    path('',views.IndexView.as_view(),name='index'),
	path('result',views.ResultView.as_view(),name='result')
]
