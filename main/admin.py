from django.contrib import admin

from main.models import *

# Register your models here.
@admin.register(Questions)
class QuestionsAdmin(admin.ModelAdmin):
    prepopulated_fields = {}