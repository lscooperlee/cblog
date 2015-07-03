from django.forms import ModelForm, SlugField, TextInput, Textarea
from cblog.models import Entry, Comment

class EntryForm(ModelForm):

    class Meta:
        model=Entry
        fields=['title','pub_date','author','isdraft','categories','body']

    def save(self, commit=True):
        slug=SlugField(required=False)
        super().save(commit)


class CommentForm(ModelForm):
    class Meta:
        model=Comment
        fields=['name','comment']
        widgets={
            'name': TextInput(attrs={"placeholder": 'name'}),
            'comment': Textarea(attrs={"placeholder": 'comment'})
        }


