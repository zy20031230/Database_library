from django.urls import path
from demo import views
# from views.index import review

app_name = "demo"
urlpatterns = [
    # path('', views.index.hello_world.index,),
    path('', views.index.hello_world.load_in),
    path('home/books/', views.index.book.show),
    # path('')
    path('login/',views.login.login_view,name='login'),
    path('home/',views.index.hello_world.index,name='home'),
    # path('search/', views.index.book.book_search,name='book_search'),
    path('register/', views.index.login.register,name='register'),
    path('review/<int:book_id>', views.review.add_review, name='add_review'),
    path('delete_review/<int:book_id>', views.review.delete_review, name='delete_review'),
    path('reserve/<int:book_id>', views.index.reserve.reserve_book, name='reserve'),
    path('home/Person/', views.index.reserve.person_init, name='person_init'),
    path('home/logout/', views.index.reserve.logout, name='logout'),
    path('reserve_cancel/<int:book_id>', views.index.reserve.reserve_cancel, name='reserve_cancel'),
    path('borrow_book/<int:book_id>', views.index.reserve.borrow_book, name='borrow_book'),
    # path('')
    path('home/return_book/<int:book_id>', views.index.reserve.return_book, name='return_book'),
]