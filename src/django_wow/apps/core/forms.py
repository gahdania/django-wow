from django import forms
from .models import Character, Realm


class CharacterAddForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Character
        fields = ('name', 'realm', 'account')

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['account'].queryset = user.account_set.all()
        self.fields['account'].widget.attrs['class'] = 'form-select'
        self.fields['realm'].queryset = Realm.objects.filter(region=user.region).order_by('slug')
        self.fields['realm'].widget.attrs['class'] = 'form-select'


class CharacterUpdateForm(forms.ModelForm):

    template_name = 'core/character_update.html'

    class Meta:
        model = Character
        fields = ('name', 'realm')
