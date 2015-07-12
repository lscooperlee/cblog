from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
from django.forms import ModelForm, SlugField, TextInput, Textarea, ModelMultipleChoiceField, FileField, Form
from cblog.models import Entry, Comment, Category


class TextInputModelMultipleChoiceField(ModelMultipleChoiceField):
    widget = TextInput

    def clean(self, value):
        if value is None:
            raise ValidationError(_('not empty: %s') % value)
        return value

class EntryForm(ModelForm):
    category=TextInputModelMultipleChoiceField(required=True, queryset=Category.objects.filter(),to_field_name='categories')

    class Meta:
        model=Entry
        fields=['title','pub_date','author','isdraft','category','body']

        labels={
            'pub_date': 'date',
            'isdraft': 'draft',
        }

        help_texts={
            'title':'',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        try:
            cc=self.instance.categories.all()
            s=','.join([ str(c) for c in cc ])
            self.fields['category'].initial=s
        except ValueError:
            pass

    def save(self, commit=True):
        slug=SlugField(required=False)
#        e=super().save(commit=False) #error
        e=super().save()
        category_list=self.cleaned_data.get('category',"").strip()
        category_list=category_list if category_list else "Uncategorized"
        e.categories.clear()
        for c in category_list.split(','):
            cateobj=Category.objects.get_or_create(title=c)[0]
            e.categories.add(cateobj)

        return e.save()

class CommentForm(ModelForm):
    class Meta:
        model=Comment
        fields=['name','content']
        widgets={
            'name': TextInput(attrs={"placeholder": 'name'}),
            'content': Textarea(attrs={"placeholder": 'comment'})
        }
        labels={
            'name':'',
            'content':'',
        }

