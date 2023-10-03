from django.contrib import admin
from .models import Genre,Author,Book,BookInstance, Language
# Register your models here.
@admin.register (Language)
class LanguageAdmin(admin.ModelAdmin):
    fields = ['name']
class BookInline(admin.TabularInline):
    model = Book
    extra = 0 # Не отображает пустые еще незаполненные поля с книгами

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
    inlines = [BookInline]#Добавляет отображение этих полей на странице Авторов
admin.site.register (Genre)
admin.site.register(Author, AuthorAdmin)
@admin.register(BookInstance)#То же самое если бы написали admin.site.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book','zaemshik', 'status', 'due_back', 'id')
    list_filter = ('status', 'due_back')
    fieldsets = (
        (None, {
            'fields': ('book','imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back','zaemshik')
        }),
    )
class BooksInstanceInline(admin.TabularInline):
        model = BookInstance
        extra = 0 # Не отображает пустые еще незаполненные поля с экземплярами книг
@admin.register(Book) #То же самое если бы написали admin.site.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    inlines = [BooksInstanceInline]
