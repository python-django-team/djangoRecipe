from django.urls import path
from . import views


app_name = "app"
urlpatterns = [
    path("siteUser/login", views.SiteUserLoginView.as_view(), name="site_user_login"),
    path("siteUer/logout", views.SiteUserLogoutView.as_view(), name="site_user_logout"),
    path("siteUser/register", views.SiteUserRegisterView.as_view(), name="site_user_register"),
    path("siteUser/profile", views.SiteUserProfileView.as_view(), name="site_user_profile"),

    # トップページ
    path('',views.TopView.as_view(), name='top'),
    path('top',views.TopView.as_view(), name='top'),
    # レシピ検索
    path('index',views.IndexView.as_view(),name='index'),
    # 結果表示
	path('result',views.ResultView.as_view(),name='result'),
    # ランダムレシピ
    path('random', views.RandomView.as_view(), name='random'),
    # マイレシピ(ログイン必要)
    path("myrecipe", views.MyRecipeView.as_view(), name='myrecipe'),
    # マイレシピ削除(ログイン必要)
    path("myrecipe/delete", views.DeleteMyRecipeView.as_view(), name='myrecipe_delete'),
]
