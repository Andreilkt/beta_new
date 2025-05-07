### Исправленный код `models.py`


from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth import get_user_model
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey
from modules.services.utils import unique_slugify
from django.utils import timezone

User = get_user_model()

class Category(MPTTModel):
    """Модель категорий с вложенностью"""
    title = models.CharField(max_length=255, verbose_name='Название категории')
    slug = models.SlugField(max_length=255, verbose_name='URL категории', blank=True, unique=True)
    description = models.TextField(verbose_name='Описание категории', max_length=300)
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        db_index=True,
        related_name='children',
        verbose_name='Родительская категория'
    )

    class MPTTMeta:
        order_insertion_by = ('title',)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        db_table = 'app_categories'

    def get_absolute_url(self):
        return reverse('articles_by_category', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

class Article(models.Model):
    """Модель материалов для сайта с установкой категории"""
    STATUS_OPTIONS = (
        ('published', 'Опубликовано'),
        ('draft', 'Черновик')
    )

    title = models.CharField(verbose_name='Заголовок', max_length=255)
    slug = models.SlugField(verbose_name='URL', max_length=255, blank=True, unique=True)
    short_description = models.TextField(verbose_name='Краткое описание', max_length=500)
    full_description = models.TextField(verbose_name='Полное описание')
    thumbnail = models.ImageField(
        verbose_name='Превью поста',
        blank=True,
        upload_to='images/thumbnails/%Y/%m/%d/',
        validators=[FileExtensionValidator(allowed_extensions=('png', 'jpg', 'webp', 'jpeg', 'gif'))]
    )
    status = models.CharField(choices=STATUS_OPTIONS, default='published', verbose_name='Статус материала', max_length=10)
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время добавления')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время обновления')
    category = TreeForeignKey('Category', on_delete=models.PROTECT, related_name='articles', verbose_name='Категория')
    author = models.ForeignKey(to=User, verbose_name='Автор', on_delete=models.SET_DEFAULT, related_name='author_posts', default=1)
    updater = models.ForeignKey(to=User, verbose_name='Обновил', on_delete=models.SET_NULL, null=True, related_name='updater_posts', blank=True)
    fixed = models.BooleanField(verbose_name='Зафиксировано', default=False)

    class Meta:
        db_table = 'app_articles'
        ordering = ['-fixed', '-time_create']
        indexes = [models.Index(fields=['-fixed', '-time_create', 'status'])]
        verbose_name = 'Материал'
        verbose_name_plural = 'Материалы'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('articles_detail_main', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, self.title)
        super().save(*args, **kwargs)

class CategoryBottom(models.Model):
    """Модель для нижнего меню категорий"""
    title = models.CharField(max_length=300)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

class Course(models.Model):
    """Модель курса"""
    title = models.CharField(max_length=255, null=True, blank=True)
    descp = models.CharField(max_length=255, null=True, blank=True)
    descp_full = models.TextField(max_length=255)
    category_bottom = models.ForeignKey(CategoryBottom, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    thumbnail_bottom = models.ImageField(
        verbose_name='Превью поста',
        blank=True,
        upload_to='images/thumbnails/%Y/%m/%d/',
        validators=[FileExtensionValidator(allowed_extensions=('png', 'jpg', 'webp', 'jpeg', 'gif'))]
    )

    def __str__(self):
        return f"{self.title} ({self.descp_full} студентов)"

    def get_absolute_url(self):
        """Возвращает URL для просмотра деталей этого курса."""
        return reverse('single_course', kwargs={'pk': self.pk})