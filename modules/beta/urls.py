from django.urls import path
from .views import ArticleListView, ArticleDetailView, ArticleByCategoryListView, ArticleDetailViewMain

urlpatterns = [
    path('', ArticleListView.as_view(), name='home'),
    path('articles/<str:slug>/', ArticleDetailView.as_view(), name='articles_detail'),
    path('articles/<str:slug>/', ArticleDetailViewMain.as_view(), name='articles_detail'),

    path('category/<str:slug>/', ArticleByCategoryListView.as_view(), name="articles_by_category"),
]