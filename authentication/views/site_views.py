import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, DetailView
from pyexpat.errors import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.utils.translation import gettext_lazy as _

from authentication.forms import LoginForm, CustomUserForm, CustomUserCreationForm
from authentication.models import CustomUser
from logger.utils import log_addition

log = logging.getLogger(__name__)


class LoginView(View):
    @classmethod
    def get(cls, request):
        form = LoginForm()
        return render(request, 'authentication/login.html', {'form': form})

    @classmethod
    def post(cls, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.add_message(request, messages.SUCCESS, f'{_("Welcome,")} {user.username}')
                    return HttpResponseRedirect(reverse('administration:index'))
                else:
                    messages.add_message(request, messages.ERROR, _('Account is inactive'))
            else:
                messages.add_message(request, messages.ERROR, _('Wrong username or password'))
        else:
            log.error(form.errors)
        return render(request, 'authentication/login.html', {'form': form})


class CustomUserListView(LoginRequiredMixin, ListView):
    model = CustomUser

    def __init__(self, **kwargs):
        super(CustomUserListView, self).__init__(**kwargs)

    def get_context_data(self, **kwargs):
        context = super(CustomUserListView, self).get_context_data(**kwargs)
        context['users'] = self.get_queryset()
        return context

    def get_queryset(self):
        qs = super(CustomUserListView, self).get_queryset().order_by('-id')
        return qs


class CustomUserCreateView(LoginRequiredMixin, CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm

    def __init__(self, **kwargs):
        super(CustomUserCreateView, self).__init__(**kwargs)
        self.object = None

    def post(self, request, *args, **kwargs):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            log_addition(request, form.instance)
            kwargs.update({'pk': form.instance.pk})
            x = redirect(reverse('authentication:user_detail', kwargs=kwargs))
        else:
            log.warning(form.errors)
            x = redirect(reverse('authentication:users_list'))
        return x

    def form_valid(self, form):
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class CustomUserDetailView(LoginRequiredMixin, DetailView):
    model = CustomUser
    extra_context = {"title": _('User details')}

    def __init__(self, **kwargs):
        super(CustomUserDetailView, self).__init__(**kwargs)
        self.object = None

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CustomUserForm(request.POST, instance=self.object)
        if form.is_valid() and form.changed_data:
            form.save()
        elif form.errors:
            log.warning(form.errors)
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context=context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

