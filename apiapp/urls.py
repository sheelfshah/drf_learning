from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('countries/', views.CountryList.as_view(), name="country-list"),
    path('countries/<int:pk>/', views.CountryDetail.as_view(), name="country-detail"),
    path('states/', views.StateList.as_view(), name="state-list"),
    path('states/<int:pk>/', views.StateDetail.as_view(), name="state-detail"),
    path('citytowns/', views.CityTownList.as_view(), name="citytown-list"),
    path('citytowns/<int:pk>/', views.CityTownDetail.as_view(),
         name="citytown-detail"),
    path('persons/', views.PersonList.as_view(), name="person-list"),
    path('persons/<int:pk>/', views.PersonDetail.as_view(),
         name="person-detail"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
