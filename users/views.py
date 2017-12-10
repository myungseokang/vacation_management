from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.shortcuts import render, redirect
from django.views import View


class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            redirect('vacations:index')

        return render(request, 'users/login.html')

    def post(self, request):
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)
        next_ = request.POST.get('next', 'vacations:index')

        if user is not None:
            auth_login(request, user)
        return redirect(next_)


class LogoutView(View):
    def get(self, request):
        auth_logout(request)
        return render(request, 'users/logout.html')
