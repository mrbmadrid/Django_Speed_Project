from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.landing),
	url(r'^register$', views.register),
	url(r'^login$', views.login),
	url(r'^logout$', views.logout),
	url(r'^books$', views.books),
	url(r'^books/add$', views.add_book),
	url(r'^addreview$', views.add_review),
	url(r'^book/(?P<id>\d+)$', views.book_reviews),
	url(r'^user/(?P<id>\d+)$', views.user_reviews),
	url(r'^delete/(?P<id>\d+)$', views.delete)
]