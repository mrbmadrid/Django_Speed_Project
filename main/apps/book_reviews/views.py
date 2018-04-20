# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from bcrypt import hashpw, gensalt
from django.shortcuts import render, redirect, HttpResponse
from models import *

# Create your views here.

def landing(request):
	return render(request, "book_reviews/login_register.html")

def books(request):
	if not request.session['id']:
		return redirect(landing)

	context = {}
	user = User.objects.get(id=request.session['id'])
	context['name'] = user.name
	context['books'] = Book.objects.all().order_by('-created_at')
	context['all_books'] = Book.objects.all().order_by('title')
	context['reviews'] = []
	reviews = Review.objects.all().order_by('-created_at')
	for review in reviews:
		book = Book.objects.get(id=review.book_id)
		user = User.objects.get(id=review.user_id)
		rating = Rating.objects.filter(book=book).filter(user=user).first()
		context['reviews'].append({
			'book_title' : book.title,
			'book_id' : book.id,
			'rating' : rating.value,
			'content' : review.content,
			'user' : user.name,
			'user_id' : user.id,
			'date' : review.created_at
			})
		if len(context['reviews']) > 2:
			break

	return render(request, "book_reviews/index.html", context)

def add_book(request):
	if request.POST:
		author = request.POST['new_author']
		if not len(author):
			author = request.POST['existing_author']
		Book.objects.create(title=request.POST['title'], author=Author.objects.create(name=author))
		book = Book.objects.last()
		Review.objects.create(content = request.POST['review'], book=book, user = User.objects.get(id=request.session['id']))
		Rating.objects.create(value = request.POST['rating'], book=book, user = User.objects.get(id=request.session['id']))
		return redirect(books)
	authors = Author.objects.all()
	return render(request, "book_reviews/add_book_review.html", {'authors':authors})

def add_review(request):
	if request.POST:
		book = Book.objects.get(id=request.POST['book_id'])
		Review.objects.create(content = request.POST['review'], book=book, user = User.objects.get(id=request.session['id']))
		Rating.objects.create(value = request.POST['rating'], book=book, user = User.objects.get(id=request.session['id']))
		return redirect(books)
	authors = Author.objects.all()
	return render(request, "book_reviews/add_book_review.html", {'authors':authors})

def delete(request, id):
	if Review.objects.get(id=id).user == User.objects.get(id=request.session['id']):
		print id
		print request.session['id']
		Review.objects.get(id=id).delete()
		Rating.objects.get(id=id).delete()
	return redirect(books)

def book_reviews(request, id):
	context = {}
	context['book'] = Book.objects.get(id=id)
	context['ratings'] = Rating.objects.filter(book=context['book'])
	context['reviews'] = Review.objects.filter(book=context['book'])
	return render(request, "book_reviews/reviews_for_book.html", context)

def user_reviews(request, id):
	context = {}
	context['user'] = User.objects.get(id=id)
	context['reviews'] = Review.objects.filter(user=context['user'])
	context['num_reviews'] = len(context['reviews'])
	return render(request, "book_reviews/reviews_by_user.html", context)

def register(request):
	register_errors={}
	if request.POST:
		if len(User.objects.filter(email=request.POST['email'])):
   			register_errors['email_duplicate'] = "This email has already been registered."
   			return render(request, "book_reviews/login_register.html", {'register_errors' : register_errors})
   		else:
   			register_errors = User.objects.registration_validator(request.POST)
	        if len(register_errors):
	            return render(request, "book_reviews/login_register.html", {'register_errors' : register_errors})
	        else:
	        	salt = gensalt()
	        	pw = hashpw(request.POST['password'].encode(), salt)
	        	User.objects.create(name = request.POST['name'], alias = request.POST['alias'], email = request.POST['email'], salt = salt, pw = pw)
	        	request.session['id'] = User.objects.get(email=request.POST['email']).id
	        	return redirect(books)
	return redirect(landing)

def login(request):
	login_errors={}
	if request.POST:
		if len(User.objects.filter(email=request.POST['email'])):
			user = User.objects.get(email=request.POST['email'])
			pw = user.pw
			salt = user.salt
			if hashpw(request.POST['password'].encode(), salt.encode()) == pw:
				request.session['id'] = User.objects.get(email=request.POST['email']).id
				return redirect(books)
			else:
				login_errors['exists'] = "Check your email or password."
		else:
			login_errors['exists'] = "Check your email or password."
	return render(request, "book_reviews/login_register.html", {'login_errors':login_errors})

def logout(request):
	request.session.clear()
	return redirect(landing)













