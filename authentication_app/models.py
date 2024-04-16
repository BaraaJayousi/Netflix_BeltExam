from django.db import models
import bcrypt
import re

# Create your models here.


class UserManager(models.Manager):

  def validate_user(self, user_data):
    messages={}
    email_pattern = re.compile('^[\w\-\.]+@([\w-]+\.)+[\w-]{2,}$')
    if len(user_data['f_name']) < 2:
        messages['f_name'] = "First name must be more than 2 characters"
    if len(user_data['l_name']) < 2:
        messages['l_name'] = "Last name must be more than 2 characters"
    if not email_pattern.match(user_data['email']):
        messages['email'] = "please provide a valid email address e.g. example@domain.com"
    if self.filter(email=user_data['email']):
        messages['email_duplicate'] = "This email is already taken"
    if len(user_data['password']) < 8:
        messages['password'] = "Password must be at least 8 characters long"
    if user_data['password'] != user_data['confirm_pw']:
        messages['confirm_pw'] = "Passwords do not match"
    
    return messages
  
  def create_user(self, first_name, last_name, email, password):
    hashed_pwd = self.hash_user_input(password)
    return self.create(first_name=first_name, last_name=last_name, email= email, password = hashed_pwd)

  # authenticate user, returns boolean if user credentials match
  def login_user(self, email, password):
    user = self.filter(email = email).first()
    if user:
      if self.check_login_pw(password, user):
        return user
    else:
      return False
  
  def get_user_by_id(self, user_id):
    return  self.get(id = user_id)

  def hash_user_input(self,pw):
    return  bcrypt.hashpw(pw.encode(), bcrypt.gensalt(12)).decode()
    
  def check_login_pw(self, pw, user) : # Returns a boolean => True if password match and False if it doesn't
    return bcrypt.checkpw(pw.encode(), user.password.encode())

class User(models.Model):
  first_name= models.CharField(max_length=100)
  last_name = models.CharField(max_length=100)
  email= models.EmailField(max_length=254, unique=True)
  password = models.CharField(max_length=255)

  objects = UserManager()



