from django.urls import path
from django.views.decorators.cache import cache_page

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('<int:year>/<str:month>/', views.home, name='home'),
    path('characters/', cache_page(0)(views.CharacterListView.as_view()), name='character-list'),
    path('characters/<int:pk>/', cache_page(0)(views.CharacterDetailView.as_view()), name='character-detail'),
    path('characters/add/', views.CharacterAddView.as_view(), name='character-add'),
    path('characters/import/', views.CharacterImportView.as_view(), name='characters-import'),
]
