from authlib.integrations.django_client import OAuth
from battlenet_client.utils import auth_host
from battlenet_client.wow import profile
from django.conf import settings
from django.contrib.auth import login  # , authenticate
from django.contrib.auth import views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.views import generic
from . import forms
from . import models


oauth = OAuth()
oauth.register(
    name='battlenet',
    server_metadata_url=f'{auth_host(settings.REGION)}/oauth/.well-known/openid-configuration',
    client_kwargs={'scope': 'wow.profile openid'}
)


def oauth_login(request):
    request.session['link'] = request.GET.get('link')
    request.session['next_page'] = request.GET.get('next')

    redirect_url = request.build_absolute_uri(reverse('oauth-callback'))
    return oauth.battlenet.authorize_redirect(request, redirect_url)


def oauth_callback(request):
    token = oauth.battlenet.authorize_access_token(request)

    if 'link' in request.session:
        user = request.user
        url, params = profile.account_profile_summary(user.region.tag, locale=user.preferred_locale.__str__())
        user_data = oauth.battlenet.get(url, params=params, token=token).json()
        user.bnet_id = token['sub']
        user.save()

        if len(models.Account.objects.filter(user=user)) == 0:
            models.Account.objects.bulk_create(
                [models.Account(user=user, account_number=acct['id']) for acct in user_data['wow_accounts']]
            )
    else:
        user = models.User.objects.get(bnet_id=token['sub'])

    if user:
        user.token = token
        user.save()
        login(request, user)

    redirect_to = request.session['next_page']
    if redirect_to:
        return redirect(redirect_to)

    return redirect('home')


class UserLoginView(views.LoginView):
    template_name = 'registration/login.html'
    next_page = reverse_lazy('oauth-login')

    def get_success_url(self):
        if self.request.user.bnet_id:
            return self.next_page
        return reverse_lazy('user-profile')


class RegisterNewUserView(generic.CreateView):
    template_name = 'registration/register_user.html'
    form_class = forms.UserCreationForm
    success_url = reverse_lazy('user-profile')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            if 'link_bnet' in form.cleaned_data:
                self.request.session['link'] = True
                return redirect('oauth-login')

            self.request.session.pop('link', None)
            return redirect('user-profile')


class ProfileView(LoginRequiredMixin, generic.UpdateView):
    form_class = forms.UserChangeForm
    success_url = reverse_lazy('user-profile')
    template_name = 'registration/user_form.html'

    def get_object(self, queryset=None):
        return self.request.user

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, instance=request.user)

        if form.is_valid():
            form.preferred_locale = form.cleaned_data['preferred_locale']
            form.save()

        return render(request, self.template_name, {'form': form})


class AccountListView(LoginRequiredMixin, generic.ListView):
    paginate_by = 10
    template_name = 'registration/accounts_list.html'

    def get_queryset(self):
        return self.request.user.account_set.all()


class AccountEditView(LoginRequiredMixin, generic.UpdateView):

    form_class = forms.AccountChangeForm
    success_url = reverse_lazy('accounts-list')
    pk_url_kwarg = 'pk'
    model = models.Account
    template_name = 'registration/account_form.html'

