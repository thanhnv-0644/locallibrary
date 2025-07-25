from django.contrib import admin
from .models import Author, Genre, Book, BookInstance


admin.site.register(Genre)

# Định nghĩa lớp quản trị


class AuthorAdmin(admin.ModelAdmin):
    list_display = (
        'last_name',
        'first_name',
        'date_of_birth',
        'date_of_death',
    )
    fields = [
        'first_name',
        'last_name',
        ('date_of_birth', 'date_of_death')
    ]


# Đăng ký lớp quản trị với model tương ứng
admin.site.register(Author, AuthorAdmin)


class BooksInstanceInline(admin.TabularInline):
    model = BookInstance

# Đăng ký lớp quản trị cho Book bằng decorator

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    inlines = [BooksInstanceInline]


# Đăng ký lớp quản trị cho BookInstance bằng decorator
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_filter = ('status', 'due_back')

    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back')
        }),
    )
