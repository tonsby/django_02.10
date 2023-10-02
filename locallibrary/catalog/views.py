from django.shortcuts import render
from .models import Book, BookInstance, Author, Genre
from django.views import generic
from django.contrib import auth
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin # вариант ограничения доступа к страницам ДЛЯ КЛАССОВ
#from django.contrib.auth.decorators import login_required - вариант ограничения доступа к страницам
from django.contrib.auth.decorators import permission_required # -для функций
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Author
import datetime

from .forms import RenewBookForm
from .forms import UpdateAuthorForm



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

#if not request.user.is_authenticated:
    # return redirect ("/accounts/login")

    #title = book.objects.filter().value("title")
    return render(
        request,
        'book_list.html',
        context={'num_books': num_books},
    )#

class BookListView(generic.ListView): #Для отображения моделей книг
    model = Book
    paginate_by = 5
    #context_object_name = 'books_list'  # ваше собственное имя переменной контекста в шаблоне
    #queryset = Book.objects.filter(title__icontains='стория')[:5]  # Получение 5 книг, содержащих слово 'история' в заголовке
    #template_name = 'catalog/book_list.html'  # Определение имени вашего шаблона и его расположения

    #НИЖНЯЯ ЧАСТЬ НЕ РАБОТАЕТ ТАК КАК НУЖНО, ЧТОБЫ УВИДЕТЬ КНИГИ НУЖНО УДАЛИТЬ ЕЁ

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """
    Generic class-based view listing books on loan to current user.
    """
    model = BookInstance
    template_name ='catalog/bookinstance_list_zaemshikov.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(zaemshik=self.request.user).filter(status__exact='o').order_by('due_back')

class BibliotekarsBooksListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name='catalog/bookinstance_list_bibliotekars.html'

    def get_queryset(self):
        return BookInstance.objects.all()


def return_books(request, pk):
    books = BookInstance.objects.filter(id=pk).first()
    setattr(books,"zaemshik", None)
    books.save()

    return redirect ("librarians-books",)


#class BooksLookedByBibliotekarView(LoginRequiredMixin,generic.ListView):
    #permission_required= 'catalog.can_mark_returned'
    #model=BookInstance
    #template_name='bookinstance_list_bibliotekars.html'

#@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    book_inst = get_object_or_404(BookInstance, pk=pk)

    # Если данный запрос типа POST, тогда
    if request.method == 'POST':

        # Создаём экземпляр формы и заполняем данными из запроса (связывание, binding):
        form = RenewBookForm(request.POST) #Здесь происходит заполнение

        # Проверка валидности данных формы:
        if form.is_valid():
            # Обработка данных из form.cleaned_data
            #(здесь мы просто присваиваем их полю due_back)
            book_inst.due_back = form.cleaned_data['renewal_date']
            book_inst.save()

            # Переход по адресу 'all-borrowed':
            return HttpResponseRedirect(reverse('librarians-books') ) #reverse то же самое, что и url

    # Если это GET (или какой-либо ещё), создать форму по умолчанию.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)#Предполагаемая дата (здесь можем ввести те данные которые отобразятся уже для пользователя в качестве подсказки)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date,})

    return render(request, 'catalog/book_renew_librarian.html', {'form': form, 'bookinst':book_inst}) #render объединяет запрос со словарём
#ФОРМЫ ДЛЯ АВТОРОВ, НЕОБХОДИМО ИМПОРТИРОВАТЬ Create, Update, Delete

class AuthorCreate(CreateView):
    model = Author
    fields = '__all__'
    initial={'date_of_death':'12/10/2016',}

def author_update(request, pk):
    author = get_object_or_404(Author, pk=pk)

    if request.method == 'POST':

        form= UpdateAuthorForm(request.POST)  # Здесь происходит заполнение

        # Проверка валидности данных формы:
        if form.is_valid():
            # Обработка данных из form.cleaned_data
            # (здесь мы просто присваиваем их полю due_back)
            author.date_of_death = form.cleaned_data['update_author_date_of_death']
            author.save()

            # Переход по адресу 'authors':
            return HttpResponseRedirect(reverse('authors'))  # reverse то же самое, что и url

    # Если это GET (или какой-либо ещё), создать форму по умолчанию.
    else:
        proposed_date_of_death = datetime.date.today() + datetime.timedelta(weeks=3)  # Предполагаемая дата (здесь можем ввести те данные которые отобразятся уже для пользователя в качестве подсказки)
        form = UpdateAuthorForm(initial={'update_author_date_of_death': proposed_date_of_death, })

    return render(request, 'catalog/book_update_authors.html',
                  {'form': form, 'authors': author})  # render объединяет запрос со словарём


    # ФОРМЫ ДЛЯ АВТОРОВ, НЕОБХОДИМО ИМПОРТИРОВАТЬ Create, Update, Delete

#class AuthorUpdate(UpdateView):
    model = Author
    fields = ['first_name','last_name','date_of_birth','date_of_death']

class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('authors')


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
    paginate_by = 5

class AuthorDetailView(generic.DetailView):
    model = Author

