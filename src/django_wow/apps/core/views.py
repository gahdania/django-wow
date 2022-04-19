from datetime import datetime
from time import sleep

from battlenet_client.wow import profile
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, FormView, DetailView, RedirectView, CreateView
from requests.exceptions import HTTPError

from apps.users.views import oauth
from . import models
from .forms import CharacterUpdateForm, CharacterAddForm
from .tasks import process_character, process_characters


def home(request, year=datetime.now().year, month=datetime.now().month):
    return render(request, 'core/home.html', {'user': request.user, 'year': year, 'month': month})


class CharacterListView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = models.Character
    paginate_by = 10

    def get_ordering(self):
        ordering = []

        def set_order_list(name, value):
            if value == 'asc':
                ordering.append(name)
            if value == 'desc':
                ordering.append(f"-{name}")

        set_order_list('name', self.request.GET.get('sortName'))
        set_order_list('realm__slug', self.request.GET.get('sortRealm'))
        set_order_list('level', self.request.GET.get('sortLevel'))
        set_order_list('cls__slug', self.request.GET.get('sortClass'))
        set_order_list('spec__slug', self.request.GET.get('sortSpec'))
        set_order_list('race__slug', self.request.GET.get('sortRace'))
        set_order_list('gender__slug', self.request.GET.get('sortGender'))

        if not ordering:
            return 'realm__slug', 'name'

        return ordering

    def get_queryset(self):
        return models.Character.objects.filter(account__in=self.request.user.account_set.all()).order_by(
            *self.get_ordering())

    def get_context_data(self, *, object_list=None, **kwargs):

        context = super().get_context_data(object_list=object_list, **kwargs)
        name = self.request.GET.get('sortName') if self.request.GET.get('sortName') else 'none'
        realm = self.request.GET.get('sortRealm') if self.request.GET.get('sortRealm') else 'none'
        level = self.request.GET.get('sortLevel') if self.request.GET.get('sortLevel') else 'none'
        cls = self.request.GET.get('sortClass') if self.request.GET.get('sortClass') else 'none'
        spec = self.request.GET.get('sortSpec') if self.request.GET.get('sortSpec') else 'none'
        race = self.request.GET.get('sortRace') if self.request.GET.get('sortRace') else 'none'
        gender = self.request.GET.get('sortGender') if self.request.GET.get('sortGender') else 'none'
        context.update({'sortName': name, 'sortRealm': realm, 'sortLevel': level, 'sortClass': cls,
                        'sortSpec': spec, 'sortRace': race, 'sortGender': gender})

        return context


class CharacterDetailView(LoginRequiredMixin, DetailView):

    login_url = reverse_lazy('login')
    model = models.Character
    template_name = 'core/character_detail.html'


class CharacterAddView(LoginRequiredMixin, CreateView):

    form_class = CharacterAddForm
    template_name = 'core/character_add.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, user=request.user)

        if form.is_valid():
            args = (form.cleaned_data['account'].account_number, form.cleaned_data['realm'].slug,
                    form.cleaned_data['name'])
            process_character.apply_async(args)
            messages.success(request, 'Successfully added character for import')

            return redirect('character-list')


class CharacterImportView(LoginRequiredMixin, RedirectView):
    login_url = reverse_lazy('oauth-login')

    def get_redirect_url(self, *args, **kwargs):

        url, params = profile.account_profile_summary(self.request.user.region.tag,
                                                      locale=self.request.user.preferred_locale.__str__())
        user_data = {}
        for _ in range(5):
            try:
                response = oauth.battlenet.get(url, params=params, token=self.request.user.token)
                response.raise_for_status()
            except HTTPError as error:
                if error.response.status_code == 429:
                    sleep(1)
                    continue
                if error.response.status_code == 404:
                    user_data = None
                    break
            else:
                user_data = response.json()
                break

        if user_data:
            return_val = process_characters.apply_async(args=(user_data['wow_accounts'],))
            if return_val:
                messages.success(self.request, 'Import request added to queue')
            else:
                messages.warning(self.request, 'Unable to import')

            return reverse_lazy('character-list')
        else:
            messages.warning(self.request, 'Something happened.  You need to relogin with Blizzard')
            return self.login_url


class CharacterUpdateView(LoginRequiredMixin, FormView):
    login_url = reverse_lazy('login')
    form_class = CharacterUpdateForm

    template_name = 'core/character_add.html'
    success_url = reverse_lazy('character-list')
