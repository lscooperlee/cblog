from django.contrib import admin

# Register your models here.
from cblog.models import Entry, Category, Comment

@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    pass

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass

