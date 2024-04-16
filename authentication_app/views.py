from django.shortcuts import render, redirect
from django.urls import reverse
from .models import User
from django.contrib import messages

# Create your views here.

#renders authentication page
def render_auth_page(request):
  if request.method == "GET":
    #render auth template
    return render(request, 'auth_page.html')


#Register new user, upon successful registration input new user id in user_id session to login
def register_user(request):
  if request.method == 'POST':
    errors = User.objects.validate_user(request.POST)
    if errors:
      for key, val in errors.items():
        messages.error(request, val, extra_tags="register_error")

      return redirect(reverse('auth:auth_page'))
    else:
      new_user = User.objects.create_user(first_name = request.POST['f_name'], last_name=request.POST['l_name'], email = request.POST['email'], password = request.POST['password'])
      request.session['user_id'] = new_user.id
      return redirect(reverse('shows:render_shows'))
  else:
    return redirect(reverse('auth:auth_page'))
  

def login_user(request):
  if request.method == 'POST':
    user = User.objects.login_user(email = request.POST['email'], password= request.POST['password'])
    if user:
      request.session['user_id'] = user.id
      return redirect(reverse('shows:render_shows'))
    else:
      msg = "Your email or password do not match our records"
      messages.error(request, msg, extra_tags="login_error")
      return redirect(reverse("auth:auth_page"))
    

def logout_user(request):
  del request.session['user_id']
  return redirect(reverse('auth:auth_page'))