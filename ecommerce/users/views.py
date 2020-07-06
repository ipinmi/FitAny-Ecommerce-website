from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

# Create your views here.
from users.models import *
from store.models import *
from users.forms import  CreateUserForm
from .decorators import unauthenticated_user, allowed_users, admin_only

def index(request):
	return HttpResponse('user')

@unauthenticated_user
def registerPage(request):
	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			form.save()
			user = form.cleaned_data.get('username')

			# group = Group.objects.get(name='customer')
			# user.groups.add(group)
			# #Added username after video because of error returning customer name if not added
			# Customer.objects.create(
			# 	user=user,
			# 	name=user.username,
			# )
			messages.success(request, 'Account was created for ' + user)

			return redirect('login')
		
	category = Category.objects.all()
	context = {'form':form,'category': category}
	return render(request, 'accounts/register.html', context)

@unauthenticated_user
def loginPage(request):
	# if request.user.is_authenticated:
	# 	return redirect('home')
	# else:
	if request.method == 'POST':
		username = request.POST.get('username')
		password =request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('home')
		else:
			messages.info(request, 'Username OR password is incorrect')
			
	category = Category.objects.all()
	context = {'category': category}
	return render(request, 'accounts/login.html', context)


def logoutUser(request):
	logout(request)
	return redirect('login')