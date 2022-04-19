from django.contrib.auth import views as auth_views
from django.urls import path
from django.urls import reverse_lazy
from django.views.decorators.cache import cache_page

from . import views
from .forms import UserChangeForm

urlpatterns = [
    path('login_user/', views.UserLoginView.as_view(), name='login'),
    path('login_oauth/', views.oauth_login, name='oauth-login'),
    path('callback/', views.oauth_callback, name='oauth-callback'),
    path('logout_user/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('register_user/', views.RegisterNewUserView.as_view(), name='register-user'),
    path('change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html',
                                                          form_class=UserChangeForm,
                                                          success_url=reverse_lazy('login')), name='password-change'),
    path('change/done/',
         auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'),
         name='password-change-done'),
    path('reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html'),
         name='password-reset'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
         name='password-reset-confirmation'),
    path('reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password-reset-done'),
    path('edit/', views.ProfileView.as_view(), name='user-profile'),
    path('accounts/', views.AccountListView.as_view(), name='accounts-list'),
    path('accounts/edit/<int:pk>/', cache_page(0)(views.AccountEditView.as_view()), name='account-edit')
]
