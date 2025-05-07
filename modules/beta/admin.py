from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from .models import Category, Article, CategoryBottom, Course

@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    """Админ-панель модели категорий"""
    list_display = ('tree_actions', 'indented_title', 'id', 'title')
    list_display_links = ('title',)
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    """Админ-панель модели статей"""
    prepopulated_fields = {'slug': ('title',)}

@admin.register(CategoryBottom)
class CategoryBottomAdmin(admin.ModelAdmin):
    """Админ-панель модели категорий в нижнем меню"""
    list_display = ('title', 'created_at')
    # Удалено поле slug из prepopulated_fields

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """Админ-панель модели курсов"""
    list_display = ('title', 'descp', 'descp_full', 'category_bottom')
    list_filter = ('category_bottom',)  # Фильтр по категориям, если это необходимо