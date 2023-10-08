from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.contrib.auth.models import AbstractUser
from embed_video.fields import EmbedVideoField


class Category(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField( null=True,max_length=200)
    duration = models.DurationField(null=True)
    thumbnail = models.ImageField(default=None, blank = True,null=True)
    @property
    def time(self):
        total_seconds = int(self.duration.total_seconds())
        # hours = total_seconds // 3600
        # minutes = (total_seconds % 3600) // 60

        # return '{} hours {} min'.format(hours, minutes)
        days = total_seconds // 86400
        remaining_hours = total_seconds % 86400
        remaining_minutes = remaining_hours % 3600
        hours = remaining_hours // 3600
        minutes = remaining_minutes // 60
        seconds = remaining_minutes % 60

        days_str = f'{days}d ' if days else ''
        hours_str = f'{hours}h ' if hours else ''
        minutes_str = f'{minutes}m ' if minutes else ''
        seconds_str = f'{seconds}s' if seconds and not hours_str else ''

        return f'{days_str}{hours_str}{minutes_str}{seconds_str}'
    def __str__(self):
        return self.name

class Sub_course(models.Model):
    main = models.ForeignKey(Category, on_delete=models.CASCADE)
    extra_details = models.CharField(max_length = 100,default = "",blank=True)
    topic_name = models.CharField(max_length=100)
    def __str__(self):
        return self.topic_name


class Sub_Topic(models.Model):
    main = models.ForeignKey(Sub_course, on_delete=models.CASCADE)
    topic_name = models.CharField(max_length=100)
    extra_details = models.CharField(max_length = 30,default = "",blank = True)
    tutorial_Video = EmbedVideoField()
    duration = models.DurationField(null=True)
    @property
    def time(self):
        total_seconds = int(self.duration.total_seconds())
        days = total_seconds // 86400
        remaining_hours = total_seconds % 86400
        remaining_minutes = remaining_hours % 3600
        hours = remaining_hours // 3600
        minutes = remaining_minutes // 60
        seconds = remaining_minutes % 60

        days_str = f'{days}d ' if days else ''
        hours_str = f'{hours}h ' if hours else ''
        minutes_str = f'{minutes}m ' if minutes else ''
        seconds_str = f'{seconds}s' if seconds and not hours_str else ''

        return f'{days_str}{hours_str}{minutes_str}{seconds_str}'
    def __str__(self):
        return self.topic_name

class DefaultTopic(models.Model):
    main = models.ForeignKey(Category, on_delete=models.CASCADE)
    extra_details = models.CharField(max_length = 100,default = "")
    topic_name = models.CharField(max_length=100)
    def __str__(self):
        return self.topic_name

class Default_Subtopics(models.Model):
    main = models.ForeignKey(DefaultTopic, on_delete=models.CASCADE)
    topic_name = models.CharField(max_length=100)
    extra_details = models.CharField(max_length = 30,default = "")
    tutorial_Video = EmbedVideoField()
    duration = models.DurationField(null=True)
    @property
    def time(self):
        total_seconds = int(self.duration.total_seconds())
        days = total_seconds // 86400
        remaining_hours = total_seconds % 86400
        remaining_minutes = remaining_hours % 3600
        hours = remaining_hours // 3600
        minutes = remaining_minutes // 60
        seconds = remaining_minutes % 60

        days_str = f'{days}d ' if days else ''
        hours_str = f'{hours}h ' if hours else ''
        minutes_str = f'{minutes}m ' if minutes else ''
        seconds_str = f'{seconds}s' if seconds and not hours_str else ''

        return f'{days_str}{hours_str}{minutes_str}{seconds_str}'
    def __str__(self):
        return self.topic_name

class UserSelectedCourse(models.Model):
    host = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Category, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.course.name
    
class UserSelected_Sub(models.Model):
    host = models.ForeignKey(User, on_delete=models.CASCADE)
    main = models.ForeignKey(Sub_course, on_delete=models.CASCADE)
    def __str__(self):
            return self.main.topic_name