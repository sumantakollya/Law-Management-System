
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


def registerPage(request):

	form = CreateUserForm()
	if request.method == 'POST':
		user_form = CreateUserForm(request.POST)
		if user_form.is_valid():
            user = user_form.save()
            username = user_form.cleaned_data.get('username')
            if user_form.cleaned_data.get('is_lawyer'):
                lawyer_form = LawyerForm(request.POST,request.FILES)
                type_form = lawyer_form
                lawyer = lawyer_form.save(commit=False)
                lawyer.user = user
                lawyer.save()
                messages.success(request, 'Account was created for lawyer ' + username)
                return redirect('login')
            else:
                client_form = ClientForm(request.POST,request.FILES)
                type_form = client_form
                client = client_form.save(commit=False)
                client.user = user
                client.save()
                messages.success(request, 'Account was created for client ' + username)
                return redirect('login')
		

	context = {'user_form':user_form,'type_form':type_form}
	return render(request, 'app/register.html', context)



def loginPage(request):

	if request.method == 'POST':
		username = request.POST.get('username')
		password =request.POST.get('password')
		user = authenticate(request, username=username, password=password)

		if user is not None :
            login(request, user)
            lawyer_obj = Lawyer.objects.filter(user=user).first()
            client_obj = Client.objects.filter(user=user).first()
            if user.is_authenticated and lawyer_obj != None:
                return redirect('lawyer')
            else:
                return redirect('client')

		else:
			messages.info(request, 'Username OR password is incorrect')

	return render(request, 'app/login.html')

def logoutUser(request):
	logout(request)
	return redirect('login')



def clientPage(request):
    client = request.user.client
    legalservices = request.user.client.legalservice_set.all()
    total_legalservices = legalservices.count()
    completed = legalservices.filter(status='Completed').count()
    pending = legalservices.filter(status='Pending').count()

    print('LEGALSERVICES:', legalservices)

    context = {'client':client,'legalservices':legalservices, 'total_orders':total_legalservices,'completed':completed,'pending':pending}
    return render(request, 'app/client.html', context)


def lawyerPage(request):
    lawyer = request.user.lawyer
    legalservices = request.user.lawyer.legalservice_set.all()
    total_legalservices = legalservices.count()
    completed = legalservices.filter(status='Completed').count()
    pending = legalservices.filter(status='Pending').count()

    print('LEGALSERVICES:', legalservices)

    context = {'lawyer':lawyer,'legalservices':legalservices, 'total_orders':total_legalservices,'completed':completed,'pending':pending}
    return render(request, 'app/lawyer.html', context)


def updateLawyer(request):
	lawyer = request.user.lawyer
	form = LawyerForm(instance=lawyer)

	if request.method == 'POST':
		form = LawyerForm(request.POST, request.FILES,instance=lawyer)
		if form.is_valid():
			form.save()


	context = {'form':form}
	return render(request, 'app/lawyer_update.html', context)


def updateClient(request):
	client = request.user.client
	form = ClientForm(instance=client)

	if request.method == 'POST':
		form = ClientForm(request.POST, request.FILES,instance=client)
		if form.is_valid():
			form.save()


	context = {'form':form}
	return render(request, 'app/client_update.html', context)

