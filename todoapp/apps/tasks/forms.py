from django import forms
# from django.forms.widgets import SelectDateWidget

from tasks.models import TodoItem

# class AddTaskForm(forms.Form):
#     description = forms.CharField(max_length=64, label='', initial='')


# BIRTH_YEAR_CHOICES = ('1980', '1981', '1982')
# FAVORITE_COLORS_CHOICES = (('blue', 'Blue'),
#                             ('green', 'Green'),
#                             ('black', 'Black'))

# class SimpleForm(forms.Form):
#     birth_year = forms.DateField(widget=SelectDateWidget(years=BIRTH_YEAR_CHOICES))
#     favorite_colors = forms.MultipleChoiceField(required=False,
#         widget=forms.CheckboxSelectMultiple, choices=FAVORITE_COLORS_CHOICES)


# class CommentForm(forms.Form):
#     name = forms.CharField(widget=forms.TextInput(attrs={'class': 'special'}))
#     url = forms.URLField()
#     comment = forms.CharField(widget=forms.TextInput(attrs={'size': '40'}))


class AddTaskForm(forms.ModelForm):
    class Meta:
        model = TodoItem
        fields = ('description', 'priority', 'tags',)
        labels = {
            'description': '', 
            'priority': '', 
            'tags': 'теги',
        }
        help_texts = {
            # 'tags': '',
        }


class TodoItemExportForm(forms.Form):
    prio_high = forms.BooleanField(label='высокой важности', initial=True, required=False)
    prio_med = forms.BooleanField(label='средней важности', initial=True, required=False)
    prio_low = forms.BooleanField(label='низкой важности', initial=False, required=False)


class TodoItemImportTrelloForm(forms.ModelForm):
    class Meta:
        model = TodoItem
        fields = ('trello_id_board',)
        labels = {
            'trello_id_board': 'id доски', 
        }
