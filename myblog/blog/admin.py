from django.contrib import admin
from .models import Post, Comment, Category, UserProfile, FavoritePost, FitnessService


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'created_at', 'author', 'category', 'image')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'content', 'created_at', 'email', 'name', 'parent_comment')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'avatar', 'description')


@admin.register(FavoritePost)
class FavoritePostAdmin(admin.ModelAdmin):
    list_display = ('user', 'post')


@admin.register(FitnessService)
class FitnessServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'price', 'author', 'image')

