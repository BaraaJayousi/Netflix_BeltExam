from django.urls import path
from . import views
app_name = "auth"
urlpatterns = [
    path('', views.render_auth_page, name='auth_page'),
    path('/register', views.register_user, name='register_user'),
    path('/login', views.login_user, name='login_user'),
    path('/logout', views.logout_user, name='logout_user')
]
