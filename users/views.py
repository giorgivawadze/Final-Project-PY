from django.shortcuts import render

from django.urls import reverse_lazy
from django.views.generic import CreateView
from users.forms import CustomUserCreateForm


class SingUpView(CreateView):
    form_class = CustomUserCreateForm
    template_name = 'registration/user_create_form.html'
    success_url = reverse_lazy('users:login')