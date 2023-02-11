from django.urls import path

from . import views


urlpatterns = [
	path('cards/', views.CardsListAPIView.as_view()),
    path('cards/search/', views.CardsSearchAPIView.as_view()),
	path('card/', views.CardAPIView.as_view()),
    path('card/update-status/', views.UpdateStatusAPIView.as_view()),
    path('card/create/', views.CreateCardAPIView.as_view()),
    path('card/delete/', views.DeleteCardAPIView.as_view()),
    path('order/create/', views.AddOrderAPIView.as_view()),
]
