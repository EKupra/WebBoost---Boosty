from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('analyze/', views.analyze, name='analyze'),
    path('pricing/', views.pricing, name='pricing'),
    path('register/', views.register, name='register'),
    path('premium-dashboard/', views.premium_dashboard, name='premium_dashboard'),
    path('logout/', views.logout, name='logout'),
]
