from django.forms import ModelForm, SlugField
from cblog.models import Entry

class EntryForm(ModelForm):

    class Meta:
        model=Entry
        fields=['title','pub_date','author','isdraft','categories','body']

    def save(self, commit=True):
        slug=SlugField(required=False)
        super().save(commit)