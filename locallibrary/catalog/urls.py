from django.urls import path
from . import views
from django.urls import re_path as url

urlpatterns = [
    path('', views.index, name='index'),
    #path('catalog/book_list', views.book_list, name='book_list'),
    url(r'^books/$', views.BookListView.as_view(), name='books'),
    url(r'^book/(?P<pk>\d+)$', views.BookDetailView.as_view(), name='book-detail'),
    url(r'^authors/$', views.AuthorListView.as_view(), name='authors'),
    url(r'^author/(?P<pk>\d+)$', views.AuthorDetailView.as_view(), name='author-detail'),
    url (r'^mybooks/$', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    url (r'^librariansbooks/$', views.BibliotekarsBooksListView.as_view(), name='librarians-books'),
    url(r'^book/(?P<pk>[-\w]+)/renew/$', views.renew_book_librarian, name='renew-book-librarian'),
    url(r'^author/create/$', views.AuthorCreate.as_view(), name='author_create'),
    url(r'^author/(?P<pk>\d+)/update/$', views.author_update, name='author_update'),
    url(r'^author/(?P<pk>\d+)/delete/$', views.delete_author, name='author_delete'),
    path (r'^returnedbooks/<str:pk>', views.return_books, name='return-books'),
]