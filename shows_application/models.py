from django.db import models
from authentication_app.models import User

# Create your models here.

class showManager(models.Manager):
  def validate_show(self, post_data, is_update=False):
    errors ={}
    if len(post_data['show_title']) < 3:
        errors['show_title'] = "Title should be at least 3 characters"
    if len(post_data['show_network']) < 3:
        errors['show_network'] = "Network name should be at least 3 characters"
    if len(post_data['show_comment']) < 3 :
        errors['show_comment'] = "Show description should be at least 3 characters"
    if(not is_update):
      if len(self.filter(title=post_data['show_title'])) > 0:
          errors['show_title_duplicate'] = "The title you\'re adding already exists, choose another one"
    return errors

  def create_show(self,post_data, user_id):
    user= User.objects.get_user_by_id(user_id)
    new_show =  self.create(title= post_data['show_title'], network=post_data['show_network'], release_date = post_data['show_release_date'], comment=post_data['show_comment'], user=user)
    return new_show
  def get_all_shows(self):
    return self.all()

  def get_show_by_id(self, show_id):
    try:
        return self.get(id = show_id)
    except:
      print("show Id doesn't exist")

  def update_show(self,post_data):
    show = self.get_show_by_id(show_id=post_data['show_id'])
    show.title = post_data['show_title']
    show.network = post_data['show_network']
    show.release_date = post_data['show_release_date']
    show.comments = post_data['show_comment']
    show.save()


class Show(models.Model):
  title= models.CharField(max_length=255)
  network = models.CharField(max_length=255)
  release_date= models.DateField()
  comments= models.TextField()
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  created_at= models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now= True)

  objects = showManager()

class Comments(models.Model):
  comment = models.TextField()
  user_comments = models.ManyToManyField(User, related_name="user_comments")
  show_comments = models.ManyToManyField(Show, related_name = "show_comments")
  created_at= models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now= True)