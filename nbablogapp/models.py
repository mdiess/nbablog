from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    following = models.ManyToManyField('User', blank=True, related_name='users_following')
    followers = models.ManyToManyField('User', blank=True, related_name='users_followers')
    blocked_users = models.ManyToManyField('User', blank=True, related_name='users_blocked')
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    is_private = models.BooleanField(default=False)

    def __str__(self):
        return self.username
    
    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'
    
    def liked_post(self, post):
        return Like.objects.filter(user=self, post=post).exists()
    
    def reposted_post(self, post):
        return Repost.objects.filter(user=self, post=post).exists()
    
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
    
    def get_reply_count(self):
        return self.replies.count()
    
    def get_like_count(self):
        return self.likes.count()
    
    def get_repost_count(self):
        return self.reposts.count()
    
    def can_repost(self):
        return not self.author.is_private

class Reply(Post):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='replies')

    def __str__(self):
        return f'Reply to {self.post.title} by {self.author.__str__()}'
    
    def get_time_since_posted(self):
        time_gap = timezone.now() - self.date_posted
        if time_gap < timezone.timedelta(hours=1):
            return f'{time_gap.seconds // 60}m'
        elif time_gap < timezone.timedelta(days=1):
            return f'{time_gap.seconds // 3600}h'
        else:
            return f'{time_gap.days}d'

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')

class Repost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='reposts')
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f'{self.user.username} reposted {self.post.title}'
