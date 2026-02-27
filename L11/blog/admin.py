from django import forms
from django.contrib import admin
from unfold.admin import ModelAdmin
from django.db import models

from .models import Author, Post, Comment, Tag

admin.site.register(Tag)


class CommentInline(admin.StackedInline):
    model = Comment
    can_delete = True
    extra = 1


@admin.register(Post)
class PostAdmin(ModelAdmin):
    list_display = ('id', 'title', 'comments_count', 'published', 'author', 'views', 'created_at')
    list_display_links = ('id',)
    list_filter = ('published', 'created_at')
    search_fields = ('title', 'content', 'author__user__username')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

    formfield_overrides = {
        models.TextField: {'widget': forms.Textarea(attrs={'rows': 15})},
    }
    inlines = (CommentInline,)

    fieldsets = (
        ('Основная информация', {  # Первый филдсет
            'fields': ('title', 'author', 'published')
        }),
        ('Содержимое поста', {  # Второй филдсет
            'fields': ('content', 'tags'),
            'classes': ('collapse',),  # Сделать блок сворачиваемым
            'description': 'Основной текст и теги для поста.'
        }),
        ('Даты (Авто)', {  # Третий филдсет
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at', 'updated_at')
    actions = ('publish', 'unpublish')

    @admin.action(description='Опубликовать выбранные посты')
    def publish(self, request, queryset):
        count = queryset.update(published=True)
        self.message_user(request, f'Опубликовано {count} постов')

    @admin.action(description='Распубликовать выбранные посты')
    def unpublish(self, request, queryset):
        count = queryset.update(published=False)
        self.message_user(request, f'Распубликовано {count} постов')

    @admin.display(description='Комментарии')
    def comments_count(self, obj: Post):
        return obj.comments.count()


@admin.register(Author)
class AuthorAdmin(ModelAdmin):
    list_display = ('id', 'user')
    list_display_links = ('id',)


@admin.register(Comment)
class CommentAdmin(ModelAdmin):
    list_display = ('id', 'content', 'author', 'post', 'created_at')
    list_display_links = ('id',)
    list_filter = ('post', 'created_at')
    search_fields = ('content', 'author__user__username')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
