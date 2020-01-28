from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('logout', views.logout),
    path('books', views.books),
    path('books/<int:book_id>', views.show),
    path('delete/<int:book_id>', views.delete),
    path('favorite/<int:book_id>', views.favorite),
    path('unfavorite/<int:book_id>', views.unfavorite),
]