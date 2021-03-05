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
from django.conf import settings
import ast


import json
import random

#envファイル→settings.pyファイルで読み込む
REQUEST_URL = settings.REQUEST_URL
APP_ID = settings.APP_ID

# ランダムレシピ
class Random(View):
	def get(self, request, *args, **kwargs):
	# jsonファイルから読み込む(必要なデータを取り出す)
		passdatas = [] # 連想配列の配列
		passdata = {} # 連想配列
		category_numbers = [ # カテゴリid
				"10-66", "10-67", "10-68", "10-69", "10-275", "10-277", "10-278",
				"11-70", "11-71", "11-72", "11-73", "11-74", "11-77", "11-78"
			]
		with open('static/json/mydata.json', mode='rt', encoding='utf-8') as file:
			data = json.load(file)
			# data[result_カテゴリ番号_カテゴリ内のレシピ番号][0] -----

			# 表示するレシピの数
			show_num = 5
			passdata = {}
			# カテゴリidをランダムに5個選ぶ
			choose_id = random.sample(range(len(category_numbers)), k=show_num)
			for i in range(show_num):
				r = random.randint(0,3) # カテゴリ内のレシピ番号(0~3)
				passdata = {}
				passdata["recipeUrl"] = data["result_"+category_numbers[choose_id[i]]+"_"+str(r)][0]["recipeUrl"]
				passdata["foodImageUrl"] = data["result_"+category_numbers[choose_id[i]]+"_"+str(r)][0]["foodImageUrl"]
				passdata["recipeTitle"] = data["result_"+category_numbers[choose_id[i]]+"_"+str(r)][0]["recipeTitle"]
				passdata["recipePublishday"] = data["result_"+category_numbers[choose_id[i]]+"_"+str(r)][0]["recipePublishday"]
				passdata["recipeIndication"] = data["result_"+category_numbers[choose_id[i]]+"_"+str(r)][0]["recipeIndication"]
				passdata["recipeDescription"] = data["result_"+category_numbers[choose_id[i]]+"_"+str(r)][0]["recipeDescription"]
				passdatas.append(passdata)

		return render(request, 'home/random_recipe.html', {'data': passdatas})

# 食材のジャンル選択画面
class IndexView(TemplateView):
	template_name = 'home/index.html'
	
# 結果表示画面
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
				# データを取得する
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
	

# マイレシピ保存
class MyRecipeView(View):
	# マイレシピ画面
	def get(self, request, *args, **kwargs):
		'''myrecipe.html get処理'''
		context = {
			# select処理
			'myrecipe': Recipe.objects.filter(userRecipe=self.request.user).order_by('-id')
		}
		return render(request, 'home/myrecipe.html', context)

	# レシピ保存
	def post(self, request, *args, **kwargs):
		'''searchRusult.html post処理'''
		recipes = self.request.POST.getlist('recipe[]',[])

		# 1つ以上選択された時
		if recipes != []:
			for recipe in recipes:
				# string -> dict -> querydict
				r = ast.literal_eval(recipe)
				qd = QueryDict(
					'title='+r["recipeTitle"]+
					'&link='+r["recipeUrl"]+
					'&img='+r["foodImageUrl"]
				)

				form = MyRecipe(user=self.request.user, data=qd)
				print(type(self.request.user))

				# insert処理
				if form.is_valid():
					create_myrecipe = Recipe(
						title=qd['title'],
						link=qd['link'],
						img=qd['img'],
						userRecipe=self.request.user
					)
					create_myrecipe.save()
					messages.success(request, r["recipeTitle"]+'をマイレシピに保存しました')
				else:
					messages.error(request, r["recipeTitle"]+"は既に保存されています")

			context = {
			# select処理
			'myrecipe': Recipe.objects.filter(userRecipe=self.request.user).order_by('-id')
			}
			return render(request, 'home/myrecipe.html', context)

		# 1つも選択されなかった時
		else:
			messages.error(request,"最低1つ以上選択してください")
			return redirect('app:index')

# マイレシピ削除
class DeleteMyRecipeView(View):
	def post(self, request, *args, **kwargs):
		'''searchRusult.html post処理'''
		recipes = self.request.POST.getlist('recipe[]',[])

		# 1つ以上選択された時
		if recipes != []:
			for recipe in recipes:
				selected_title = Recipe.objects.get(id=recipe).title
				Recipe.objects.filter(id=recipe).delete()
				messages.success(request, selected_title+'をマイレシピから削除しました')

			context = {
			# select処理
			'myrecipe': Recipe.objects.filter(userRecipe=self.request.user).order_by('-id')
			}
			return render(request, 'home/myrecipe.html', context)
			return HttpResponse(status=204)

		# 1つも選択されなかった時
		else:
			messages.error(request,"最低1つ以上選択してください")
			return redirect('app:myrecipe')



# ログイン
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

# ログアウト
class SiteUserLogoutView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):

        if request.user.is_authenticated:
            auth_logout(request)

        messages.success(request, "ログアウトしました")

        return redirect("app:site_user_login")

        
# 会員登録
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
