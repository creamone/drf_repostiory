

from datetime import datetime
from django.utils import timezone
from django.db import models
from user.models import User

# Create your models here.


class Category(models.Model):
    name = models.CharField("이름", max_length=70, default='')
    description = models.TextField("설명")

    def __str(self):
        return f'{self.name}'


class Article(models.Model):
    user = models.ForeignKey(
        'user.User', verbose_name="작성자", on_delete=models.CASCADE)
    title = models.CharField("제목", max_length=50)
    category = models.ManyToManyField(Category, verbose_name="카테고리")
    contents = models.TextField("본문")
    # show_start_date =models.DateTimeField(auto_now_add = True) # 노출 시작일자
    # show_end_date = models.DateTimeField(default="datetime.now()+timedelta(days=7)") # 노출 종료 일자 #timezone.now()+timedelta(days=7)
    exposure_start_date = models.DateField("노출 시작 일자", default=timezone.now)
    exposure_end_date = models.DateField("노출 종료 일자", default=timezone.now)

    def __str__(self):
        return f"{self.user.username} 님이 작성하신 글입니다."


class Comment(models.Model):
    user = models.ForeignKey(
        'user.User', verbose_name="작성자", on_delete=models.CASCADE)
    article = models.ForeignKey(
        Article, verbose_name="게시글", on_delete=models.CASCADE)
    contents = models.TextField("본문")

    def __str__(self):
        return f"{self.article.title} / {self.contents}"
