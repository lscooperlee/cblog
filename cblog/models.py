from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from markdown import markdown


class Category(models.Model):
    title=models.CharField(max_length=250)

    class Meta:
        verbose_name_plural="Categories"

    def __str__(self):
        return self.title

class Entry(models.Model):
    title=models.CharField(max_length=250,help_text="maximum 250 characterrs")
    slug=models.SlugField(unique=True)
    exerpt=models.TextField(blank=True)
    body=models.TextField()
    body_html=models.TextField(editable=False,blank=True)
    pub_date=models.DateTimeField(default=datetime.now)
    author=models.ForeignKey(User)
    isdraft=models.BooleanField(default=True)
    categories=models.ManyToManyField(Category)

    class Meta:
        verbose_name_plural="Entries"

    def __str__(self):
        return self.title

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.slug=str(self.title).replace(' ','-')
        self.body_html=markdown(self.body)
        super().save(force_insert,force_update,using,update_fields)


class Comment(models.Model):
    name=models.CharField(max_length=128)
    email=models.EmailField(blank=True)
    content=models.TextField()
    entry=models.ForeignKey(Entry)
    pub_date=models.DateTimeField(default=datetime.now)
    replyto_comment=models.ForeignKey('self',blank=True, null=True)

