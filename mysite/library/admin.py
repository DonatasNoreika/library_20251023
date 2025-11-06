from django.contrib import admin
from .models import Author, Genre, Book, BookInstance, BookReview, CustomUser
from django.contrib.auth.admin import UserAdmin

class BookInstanceInLine(admin.TabularInline):
    model = BookInstance
    extra = 0
    can_delete = False
    readonly_fields = ['uuid']
    fields = ['uuid', 'due_back', 'reader', 'status']


class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'isbn', 'display_genre']
    inlines = [BookInstanceInLine]

class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ['uuid', 'book', 'due_back', 'reader', 'status', 'is_overdue']
    list_filter = ['book', 'book__author', 'reader', 'due_back']
    search_fields = ['uuid', 'book__title']
    list_editable = ['due_back', 'reader', 'status']
    fieldsets = [
        ('General', {'fields': ('uuid', 'book')}),
        ('Availability', {'fields': ('status', 'reader', 'due_back')}),
    ]

class AuthorAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'display_books']

class BookReviewAdmin(admin.ModelAdmin):
    list_display = ['book', 'reviewer', 'date_created']

class CustomUserAdmin(admin.ModelAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('photo',)}),
    )
admin.site.register(Author, AuthorAdmin)
admin.site.register(Genre)
admin.site.register(Book, BookAdmin)
admin.site.register(BookInstance, BookInstanceAdmin)
admin.site.register(BookReview, BookReviewAdmin)
admin.site.register(CustomUser, CustomUserAdmin)