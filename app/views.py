from django.shortcuts import render, redirect
from django.http import HttpResponse, QueryDict
import requests
from django.views.generic import View
from django.views.generic.base import TemplateView
from django.views import View
from .models import Recipe, SiteUser
from .forms import SiteUserRegisterForm, SiteUserLoginForm, MyRecipe
from django.contrib import messages
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.mixins import LoginRequiredMixin
import ast


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
			

class MyRecipeView(View):
	def get(self, request, *args, **kwargs):
		'''myrecipe.html get処理'''
		context = {
			# select処理
			'myrecipes': Recipe.objects.filter(userRecipe=self.request.user).order_by('-id')
		}
		return render(request, 'home/myrecipe.html', context)

	def post(self, request, *args, **kwargs):
		'''searchRusult.html post処理'''
		recipes = self.request.POST.getlist('recipe[]',[])

		# 1つ以上選択された時
		if recipes != []:
			for recipe in recipes:
				# string -> dict -> querydict
				r = ast.literal_eval(recipe)
				qd = QueryDict('title='+r["recipeTitle"]+'&link='+r["recipeUrl"]+'&img='+r["foodImageUrl"])

				form = MyRecipe(qd)
				print(form)

				# insert処理
				if form.is_valid():
					create_myrecipe = Recipe(
						title=qd['title'],
						link=qd['link'],
						img=qd['img'],
						userRecipe=self.request.user
					)
					create_myrecipe.save()
				else:
					return HttpResponse("None")

			messages.success(request, 'マイレシピに保存されました')
			context = {
			# select処理
			'myrecipes': Recipe.objects.filter(userRecipe=self.request.user).order_by('-id')
			}
			return render(request, 'home/myrecipe.html', context)

		# 1つも選択されなかった時
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

        return redirect("app:index")


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
