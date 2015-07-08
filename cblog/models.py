from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from markdown import markdown
import re


class Category(models.Model):
    title=models.CharField(max_length=250)

    class Meta:
        ordering=['title']
        verbose_name_plural="Categories"

    def __str__(self):
        return self.title

class Entry(models.Model):
    title=models.CharField(max_length=250,help_text="maximum 250 characterrs")
    slug=models.SlugField(unique=True,max_length=250)
    exerpt=models.TextField(blank=True)
    body=models.TextField()
    body_html=models.TextField(editable=False,blank=True)
    pub_date=models.DateTimeField(default=timezone.now)
    author=models.ForeignKey(User)
    isdraft=models.BooleanField(default=True)
    categories=models.ManyToManyField(Category)

    class Meta:
        verbose_name_plural="Entries"
        ordering=['-pub_date','title']

    def __str__(self):
        return self.title

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.slug=re.sub(r'[^_\w\d]','_',str(self.title))
        self.body_html=markdown(self.body)
        super().save(force_insert,force_update,using,update_fields)


class Comment(models.Model):
    name=models.CharField(max_length=128)
    email=models.EmailField(blank=True)
    content=models.TextField()
    entry=models.ForeignKey(Entry)
    pub_date=models.DateTimeField(default=timezone.now)
    replyto_comment=models.ForeignKey('self',blank=True, null=True)

