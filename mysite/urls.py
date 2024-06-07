"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
# from . import views
from django.urls import include
from demo.views.index.book import book_search
# import demo.views.index as view_api
from demo.views.index.login import login_view
# from demo.views.index.review import add_review
from . import testdb
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('demo.urls')),
    path('testdb/',testdb.testdb),
    path('booktest/',testdb.booktest),
    path('search/',book_search,name='book_search'),
    path('', login_view,name='login'),
    # path('add/',add_review,name='add_review')
    # path("",views.hello,name="hello")
    # path('hello/', views.hello)
]
