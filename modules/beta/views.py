### Исправленный код представлений (`views.py`)


from django.views.generic import ListView, DetailView, TemplateView
from .models import Article, Category, Course
from django.shortcuts import get_object_or_404

class ArticleListView(TemplateView):
    template_name = 'industrie/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['articles'] = Article.objects.all()  # Изменил `context['article']` на `context['articles']`
        context['courses'] = Course.objects.all()  # Изменил `context['course']` на `context['courses']`
        return context

class SingleCourseView(DetailView):
    model = Course
    template_name = 'industrie/bottom_menu.html'
    context_object_name = 'course'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['courses'] = Course.objects.all()  # Изменил `context['course']` на `context['courses']`
        return context

class ArticleDetailViewMain(DetailView):
    model = Article
    template_name = 'industrie/site.html'
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['courses'] = Course.objects.all()
        context['title'] = self.object.title  # Заголовок статьи
        return context

class ArticleDetailView(DetailView):
    model = Article
    template_name = 'industrie/site.html'
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['courses'] = Course.objects.all()
        context['title'] = self.object.title
        return context

class ArticleByCategoryListView(ListView):
    model = Article
    template_name = 'industrie/index.html'
    context_object_name = 'articles'

    def get_queryset(self):
        category_slug = self.kwargs['slug']
        return Article.objects.filter(category__slug=category_slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['courses'] = Course.objects.all()
        context['title'] = f'Статьи из категории: {self.get_category_title()}'
        return context

    def get_category_title(self):
        category_slug = self.kwargs['slug']
        category = get_object_or_404(Category, slug=category_slug)
        return category.title