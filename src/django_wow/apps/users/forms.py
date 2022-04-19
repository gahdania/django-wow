from django import forms
from django.core.exceptions import ValidationError

from . import models


class UserCreationForm(forms.ModelForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class': 'form-control'}))
    display_name = forms.CharField(label='Display Name', widget=forms.TextInput(attrs={'class': 'form-control'}),
                                   required=False)
    battle_tag = forms.CharField(label='BattleTag', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Password confirmation',
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    link_bnet = forms.BooleanField(label='Link Battle.net Account',
                                   widget=forms.CheckboxInput(), required=False)

    class Meta:
        model = models.User
        fields = ('username', 'display_name', 'email', 'password1', 'password2', 'battle_tag', 'preferred_locale',
                  'link_bnet')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    display_name = forms.CharField(label='Display Name', widget=forms.TextInput(attrs={'class': 'form-control'}),
                                   required=False)
    battle_tag = forms.CharField(label='BattleTag', widget=forms.TextInput(attrs={'class': 'form-control'}))
    bnet_id = forms.CharField(label='Battle.net ID', widget=forms.TextInput(attrs={'class': 'form-control'}),
                              required=False)
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    preferred_locale = forms.ModelChoiceField(label='Preferred Locale',
                                              widget=forms.Select(attrs={'class': 'form-control'}),
                                              queryset=models.Locale.objects.all())

    class Meta:
        model = models.User
        fields = ('email', 'display_name', 'battle_tag', 'bnet_id', 'region', 'preferred_locale')


class UserLoginForm(forms.ModelForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = models.User
        fields = ('username', 'password')


class AccountChangeForm(forms.ModelForm):

    account_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), disabled=True)
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = models.Account
        fields = ('account_number', 'name')
