from django.shortcuts import render, redirect
from django.urls import reverse
from authentication_app.models import User
from .models import Show
from django.contrib import messages

# Create your views here.

def render_shows(request):
  if "user_id" in request.session:
    context = {
      "logged_user" : User.objects.get_user_by_id(request.session['user_id']),
      "shows": Show.objects.get_all_shows(),
    }
    if request.method == "GET":
      return render(request, 'dashboard.html', context)
  else:
    return redirect(reverse('auth:auth_page'))
  
def render_new_show_form(request):
  if "user_id" in request.session:
    context = {
      "logged_user" : User.objects.get_user_by_id(request.session['user_id'])
    }
    if request.method == "GET":
      return render(request, "new_show.html", context)
  else:
    return redirect(reverse('auth:auth_page'))
  
def create_new_show(request):
  if "user_id" in request.session:
    if request.method == 'POST':
      errors = Show.objects.validate_show(request.POST)
      if errors:
        for key, val in errors.items():
          messages.error(request, val, extra_tags="new_show_error")
        return redirect(reverse("shows:render_new_show_form"))
      else:
        Show.objects.create_show(request.POST, request.session['user_id'])
    return redirect(reverse("shows:render_shows"))


def render_show_edit_form(request, show_id):
  if "user_id" in request.session:
    context={
      'show': Show.objects.get_show_by_id(show_id=show_id),
      "logged_user" : User.objects.get_user_by_id(request.session['user_id'])
    }
    return render(request, 'new_show.html', context)
  

def update_show(request):
  if "user_id" in request.session:
    if request.method == 'POST':
      errors = Show.objects.validate_show(post_data = request.POST, is_update=True)
      if errors:
        for key, val in errors.items():
          messages.error(request, val, extra_tags="new_show_error")
        return redirect(reverse("shows:render_show_edit_form", args=[request.POST['show_id']]))
      else:
        Show.objects.update_show(post_data= request.POST)
    return redirect(reverse("shows:render_shows"))
  
def render_show_details(request, show_id):
  if "user_id" in request.session:
    context={
      'show': Show.objects.get_show_by_id(show_id=show_id),
      "logged_user" : User.objects.get_user_by_id(request.session['user_id']),
    }
    if request.method == "GET":
      return render(request, 'show_details.html', context)
    
