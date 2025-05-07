from django.urls import path
from . import views
from .views import ArticleListView, ArticleDetailView, ArticleByCategoryListView, ArticleDetailViewMain, SingleCourseView

urlpatterns = [
    path('', ArticleListView.as_view(), name='home'),
    path('articles/<str:slug>/', ArticleDetailView.as_view(), name='articles_detail'),
    path('articles/main/<str:slug>/', ArticleDetailViewMain.as_view(), name='articles_detail_main'),  # Изменили путь
    path('category/<str:slug>/', ArticleByCategoryListView.as_view(), name="articles_by_category"),
    path('course/<int:pk>/', SingleCourseView.as_view(), name='single_course'),
]