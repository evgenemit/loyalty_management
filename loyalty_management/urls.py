from django.urls import path

from . import views


urlpatterns = [
	path('', views.cards, name='cards'),
    path('card/<str:serial_number>/<str:number>/', views.card_profile, name='card_profile'),
    path('generator/', views.generator, name='generator'),
    path('trash/', views.trash, name='trash'),
]

