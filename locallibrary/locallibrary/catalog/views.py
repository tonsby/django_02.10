from django.shortcuts import render
from .models import Book, BookInstance, Author, Genre
from django.views import generic
from django.contrib import auth
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required
from django import forms
#ф-ия render генерирует HTML запросы

# GITHUB

# Create your views here. # Создайте ваше отображение здесь

def index(request):
    """
    Функция отображения для домашней страницы сайта.
    """
    #if not request.user.is_authenticated:
     #   return redirect ("/accounts/login")

    # Генерация "количеств" некоторых главных объектов
    num_books=Book.objects.all().count() # с помощью objects получаем записи из моделей
    num_instances=BookInstance.objects.all().count()
    # Доступные книги (статус = 'a')
    num_instances_available=BookInstance.objects.filter(status__exact='a').count()
    num_authors=Author.objects.count()  # Метод 'all()' применён по умолчанию.
    num_genres=Genre.objects.all().count()
    num_char_books=Book.objects.filter(title__icontains='').count()
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    # Отрисовка HTML-шаблона index.html с данными внутри
    # переменной контекста context
    return render(
        request,
        'index.html',
        context={'num_books':num_books,'num_instances':num_instances,'num_instances_available':num_instances_available,'num_authors':num_authors, 'num_genres':num_genres, 'num_char_books':num_char_books,'num_visits':num_visits},
    )
#Можно было бы написать такую же функцию как ВЫШЕ, но это экономит нам время и страницы кода
#def book_list(request):

    if not request.user.is_authenticated:
        return redirect ("/accounts/login")

    title = book.objects.filter().value("title")
    return render(
        request,
        'book_list.html',
        context={'num_books': num_books},
    )
class BookListView(generic.ListView): #Для отображения моделей книг
    model = Book
    paginate_by = 5
    #context_object_name = 'books_list'  # ваше собственное имя переменной контекста в шаблоне
    #queryset = Book.objects.filter(title__icontains='стория')[:5]  # Получение 5 книг, содержащих слово 'история' в заголовке
    #template_name = 'catalog/book_list.html'  # Определение имени вашего шаблона и его расположения

    #НИЖНЯЯ ЧАСТЬ НЕ РАБОТАЕТ ТАК КАК НУЖНО, ЧТОБЫ УВИДЕТЬ КНИГИ НУЖНО УДАЛИТЬ ЕЁ

class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):

    """
    Generic class-based view listing books on loan to current user.
    """
    permission_required = 'catalog.can_mark_returned'
    model = BookInstance
    template_name ='catalog/bookinstance_list_zaemshikov.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(zaemshik=self.request.user).filter(status__exact='o').order_by('due_back')

class LibrariansBooksListView(LoginRequiredMixin, generic.ListView):

    model = BookInstance
    template_name='catalog/bookinstance_list_bibliotekarey.html'

    def get_queryset(self):
        return BookInstance.objects.all()
def ubrat_zaemshika(request,pk):
    book=BookInstance.objects.filter(id=pk).first()
    setattr(book, "zaemshik", None)
    book.save()

    return redirect(
        'all-books',)

class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text="Введите дату различающуюся на 3 недели .")

def get_context_data(self, **kwargs):
        # В первую очередь получаем базовую реализацию контекста
        context = super(BookListView, self).get_context_data(**kwargs)
        # Добавляем новую переменную к контексту и инициализируем её некоторым значением
        context['some_data'] = 'This is just some data'
        return context

class BookDetailView(generic.DetailView):
    model = Book

class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 2

class AuthorDetailView(generic.DetailView):
    model = Author

