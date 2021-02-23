from django.shortcuts import render, redirect
from django.http import HttpResponse
import requests
from django.views.generic import View
from django.views.generic.base import TemplateView
from django.views import View
from .forms import SiteUserRegisterForm, SiteUserLoginForm
from django.contrib import messages
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.mixins import LoginRequiredMixin

REQUEST_URL = "https://app.rakuten.co.jp/services/api/Recipe/CategoryRanking/20170426"
APP_ID = "1008575362204726338"

class IndexView(TemplateView):
	template_name = 'home/index.html'
	
	
class ResultView(View):
	
	def get(self, request, *args, **kwargs):
		categories = self.request.GET.getlist('categories[]',[])
		if categories != []:
			recipes = []
			recipe_id = []
			recipe_num_dict = []
			result = []
			i = 0
			for category in categories:
				search_param = {
					"applicationId":[APP_ID],
					#"formatVersion":2,
					"categoryId":category
				}
				responses = requests.get(REQUEST_URL, search_param).json()
				if 'error' in responses:
					break
				recipes.append(responses["result"])
				j = 0
				for recipe in responses["result"]:
					recipe_num = {
						"cat_rank":i,
						"res_rank":j
					}
					if recipe["recipeId"] in recipe_id:
						head_id = recipe["recipeId"]
						recipe_num_dict.pop(recipe_id.index(head_id))
						recipe_id.pop(recipe_id.index(head_id))
						recipe_num_dict.insert(0,recipe_num)
						recipe_id.insert(0,head_id)
					else:
						recipe_num_dict.append(recipe_num)
						recipe_id.append(recipe["recipeId"])
					j += 1
				i += 1
			for recipes_num in recipe_num_dict:
				result.append(recipes[recipes_num["cat_rank"]][recipes_num["res_rank"]])
			return render(request,'home/searchResult.html',{ "result":result })
		else:
			messages.error(request,"最低1つ以上選択してください")
			return redirect('app:index')
			
		
class SiteUserLoginView(View):
    def get(self, request, *args, **kwargs):
        context = {
            "form": SiteUserLoginForm(),
        }
        return render(request, "app/siteUser/login.html", context)

    def post(self, request, *args, **kwargs):
        form = SiteUserLoginForm(request.POST)
        if not form.is_valid():
            return render(request, "app/siteUser/login.html", {"form": form})

        login_site_user = form.get_site_user()

        auth_login(request, login_site_user)

        messages.success(request, "ログインしました")

        return redirect("app:site_user_profile")


class SiteUserLogoutView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):

        if request.user.is_authenticated:
            auth_logout(request)

        messages.success(request, "ログアウトしました")

        return redirect("app:site_user_login")
        

class SiteUserRegisterView(View):
    def get(self, request, *args, **kwargs):
        context = {
            "form": SiteUserRegisterForm(),
        }
        return render(request, "app/siteUser/register.html", context)

    def post(self, request, *args, **kwargs):
        form = SiteUserRegisterForm(request.POST)
        if not form.is_valid():
            return render(request, "app/siteUser/register.html", {"form": form})

        new_site_user = form.save(commit=False)
        new_site_user.set_password(form.cleaned_data["password"])

        new_site_user.save()
        messages.success(request, "会員登録が完了しました")
        return redirect("app:site_user_login")


class SiteUserProfileView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):

        return render(request, "app/siteUser/profile.html")

