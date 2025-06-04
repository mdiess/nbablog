from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    liked_posts = models.ManyToManyField('Post', blank=True)
    following = models.ManyToManyField('User', blank=True, related_name='users_following')
    followers = models.ManyToManyField('User', blank=True, related_name='users_followers')

    def __str__(self):
        return self.username
    
    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'
    
class Post(models.Model):
    title = models.CharField(max_length=100, blank=True)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title if self.title else f'Post created by {self.author.__str__()} on {self.date_posted}'
    
    def get_time_since_posted(self):
        time_gap = timezone.now() - self.date_posted
        if time_gap < timezone.timedelta(hours=1):
            return f'{time_gap.seconds // 60}m'
        elif time_gap < timezone.timedelta(days=1):
            return f'{time_gap.seconds // 3600}h'
        else:
            return f'{time_gap.days}d'