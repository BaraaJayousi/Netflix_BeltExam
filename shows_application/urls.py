from django.urls import path
from . import views

app_name = "shows"
urlpatterns = [
  path('/', views.render_shows, name="render_shows"),
  path('/new/', views.render_new_show_form, name="render_new_show_form"),
  path('/new/create_new', views.create_new_show, name="create_new_show"),
  path('/edit/<int:show_id>', views.render_show_edit_form, name="render_show_edit_form"),
  path('/edit_show', views.update_show, name='update_show'),
  path('/<int:show_id>', views.render_show_details, name='render_show_details'),
]
