from django.urls import path
from . import views

urlpatterns = [
    path('', views.tour_list, name='tour_list'),
    path('book/<int:tour_id>/', views.book_tour, name='book_tour'),
]