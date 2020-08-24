from cal.models import Event
from django.forms import DateInput, ModelForm , TimeInput
from django import forms
class EventForm(ModelForm):
    class Meta:
        model = Event
    # datetime-local is a HTML5 input type, format to make date time show on fields
        widgets = {
        'date': DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
        'time': TimeInput(attrs={'type': 'time'}, format='T%H:%M'),
        }
        fields = ('title', 'author', 'body', 'time', 'date')

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        # input_formats to parse HTML5 datetime-local input to datetime field
        self.fields['date'].input_formats = ('%Y-%m-%d',)
        self.fields['time'].input_formats = ('%H:%M',)
        self.fields['body'].required = False
        
class SearchForm(forms.Form):
    query = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'جستوجو . . .'}))