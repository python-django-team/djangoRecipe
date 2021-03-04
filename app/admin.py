from django.contrib import admin
from  .models import SiteUser, Recipe
# Register your models here.


admin.site.register(SiteUser)
admin.site.register(Recipe)
