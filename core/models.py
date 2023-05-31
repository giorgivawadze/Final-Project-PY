from typing import Iterable, Optional
from django.db import models
from django.utils import timezone
import datetime
from django.urls import reverse
from users.models import User

class Tag(models.Model):
    text = models.CharField(max_length=255, unique=True)
    
    def save(self, *args, **kwargs) -> None:
        self.text = self.text.lower()
        return super().save(*args, **kwargs)

  
    def __str__(self) -> str:
        return self.text


class Question(models.Model):
    tags = models.ManyToManyField(Tag, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, unique=True)
    create_time = models.DateTimeField(auto_now_add=True)
    edit_time = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
       
        return self.title
    
    def is_recent(self) -> bool:
      
        time_since: datetime.timedelta = timezone.now() - self.create_time
        return time_since.days < 1
    
    def get_absolute_url(self):
        return reverse("core:question-detail", kwargs={"pk": self.pk})
    


class Choice(models.Model):
  
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=60)
    votes = models.PositiveIntegerField(default=0)

    def __str__(self) -> str:
        return self.text


