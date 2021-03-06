from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View

from account.forms import LoginForm


class LoginView(View):

    def get(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        context = {'form': form}
        return render(request, "account/login.html", context)

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect('/admin')
        return render(request, 'account/login.html', {'form': form})


def logout_user(request):
    logout(request)
    return redirect('account:login')
