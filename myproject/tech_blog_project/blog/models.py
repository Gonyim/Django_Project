# blog/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # Removed default=1
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)  # 기본값으로 현재 시간을 사용
    modified_date = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)  # 삭제 여부를 나타내는 필드

    def __str__(self):
        return self.title
