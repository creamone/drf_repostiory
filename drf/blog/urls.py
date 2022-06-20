from django.contrib import admin
from django.urls import path, include
from blog import views

urlpatterns = [
    # blog/
    path('', views.ArticleView.as_view())
]
