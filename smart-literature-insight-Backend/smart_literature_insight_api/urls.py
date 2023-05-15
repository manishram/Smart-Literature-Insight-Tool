from django.urls import path
from smart_literature_insight_api import views

urlpatterns = [
    path('',views.index),
    path('ask', views.giveAnswer),
]