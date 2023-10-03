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
    url(r'^mybooks/$', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    url(r'^allbooks/$', views.LibrariansBooksListView.as_view(),name = 'all-books'),
    #url(r'^ubratzaemshika/(?P<pk>\d+)$', views.ubrat_zaemshika, name = 'ubrat-zaemshika'),
    path('ubratzaemshika/<str:pk>/', views.ubrat_zaemshika, name = 'ubrat-zaemshika'),
]