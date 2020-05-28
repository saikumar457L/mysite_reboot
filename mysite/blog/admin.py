from django.contrib import admin

from .models import Post,Comment

# Register your models here.

class CommentPostAdmin(admin.StackedInline):
    model = Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title","slug","author","publish","created","updated","status"]
    search_fields = ["title","slug","body"]
    prepopulated_fields = {"slug":("title",)}
    date_hierarchy="publish"
    list_filter = ["author","status","publish","created"]
    inlines = [CommentPostAdmin]

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["post","email","active"]
    list_filter = ["active","name","created"]
    search_fields = ["name","email","body"]
