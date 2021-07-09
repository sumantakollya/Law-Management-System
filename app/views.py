
from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

# Create your views here.
from .models import *
from .forms import *
from .decorators import unauthenticated_user, allowed_users, admin_only

@unauthenticated_user
def registerPage(request):

	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            if form.cleaned_data.get('is_lawyer'):
                group = Group.objects.get(name='lawyer')
                user.groups.add(group)
                Lawyer.objects.create(
                    user=user,
                    name=user.username,
                    )

                messages.success(request, 'Account was created for lawyer ' + username)
                return redirect('login')
            else:
                group = Group.objects.get(name='client')
                user.groups.add(group)
                Client.objects.create(
                    user=user,
                    name=user.username,
                    )

                messages.success(request, 'Account was created for client ' + username)
                return redirect('login')
		

	context = {'form':form}
	return render(request, 'app/register.html', context)


@unauthenticated_user
def loginPage(request):

	if request.method == 'POST':
		username = request.POST.get('username')
		password =request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user is not None and user.is_lawyer == True:
			login(request, user)
			return redirect('lawyer')

		elif user is not None and user.is_lawyer == False:
			login(request, user)
			return redirect('client')
        
		else:
			messages.info(request, 'Username OR password is incorrect')

	context = {}
	return render(request, 'app/login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('login')

