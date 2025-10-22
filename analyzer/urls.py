from django.urls import path
from .views import AnalyzeStringView, GetStringView, GetStringsView, DeleteStringView, NaturalLanguageFilterView

urlpatterns = [
    path('strings', AnalyzeStringView.as_view()),  # POST
    path('strings/<str:value>', GetStringView.as_view()),  # GET single
    path('strings/', GetStringsView.as_view()),  # GET all with filters
    path('strings/filter-by-natural-language', NaturalLanguageFilterView.as_view()),  # GET natural query
    path('strings/<str:value>/delete', DeleteStringView.as_view()),  # DELETE
]
