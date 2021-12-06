from .models import Comment, Category
import django.forms as forms


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']


class SortFiltForm(forms.Form):
    SORT_BY = (('dates', "Creation date"),
            ('comments', "Most commented"),
            ("views", "Most viewed"))
    sort_by = forms.ChoiceField(choices=SORT_BY)
    category_filt = forms.ModelChoiceField(Category.objects.all(), required=False)


