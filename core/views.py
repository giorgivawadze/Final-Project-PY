from typing import Any

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpRequest, HttpResponse, Http404, HttpResponseBadRequest, HttpResponseRedirect
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy, reverse
from core.models import Question, Choice
from core.forms import QuestionCreateForm
from django.forms import inlineformset_factory
from django.db.models import Q

# CRUD - Create Retrieve Update Delete
# Create your views here.
    
class HomeView(ListView):
    template_name = 'index.html'
    context_object_name = 'questions'
    paginate_by = 5
    
    
    def get_queryset(self) -> QuerySet[Any]:
        query: str = self.request.GET.get('q', '')
        queryset = Question.objects.filter(
            Q(title__icontains=query) | Q(user__username__icontains=query)
        )
        return queryset.order_by('-create_time')



class QuestionDetailView(DetailView):
    model = Question
    queryset = Question.objects.all()
    template_name = 'core/question_detail.html'
    

class QuestionDeleteView(DeleteView):
    model = Question
    success_url = reverse_lazy('core:home')
    template_name = 'core/question_delete.html'

    def get_queryset(self):
        if self.request.user.is_staff:
            return Question.objects.all()

        return Question.objects.filter(
            user=self.request.user
        )


class QuestionUpdateView(LoginRequiredMixin, UpdateView):
    model = Question
    fields = ['title']
    template_name = 'core/question_edit.html'

    def get_success_url(self) -> str:
        return self.get_object().get_absolute_url()

    def get_queryset(self):
        if self.request.user.is_staff:
            return Question.objects.all()

        return Question.objects.filter(
            user=self.request.user
        )


class ChoiceSelectView(LoginRequiredMixin, UpdateView):
    http_method_names = ['post']
    model = Choice
    fields = []
    
    def get_success_url(self) -> str:
        return self.object.question.get_absolute_url()
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
     
        self.object: Choice = self.get_object()
        self.object.votes += 1
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class AboutView(TemplateView):
    template_name = 'about.html'
    

@login_required
def contact_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'contact.html')


# Generics / class based views
class QuestionCreateView(LoginRequiredMixin, CreateView):
    form_class = QuestionCreateForm
    template_name = 'core/question_create.html'
    
    def get_success_url(self) -> str:
        return reverse('core:question-choices', kwargs={'pk': self.object.pk})

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_kwargs['user'] = self.request.user
        return form_kwargs
    
@login_required
def add_choices_to_question(request: HttpRequest, pk: int) -> HttpResponse:
    if not Question.objects.filter(user=request.user, pk=pk).exists() and not request.user.is_staff:
        raise Http404()

    question = get_object_or_404(Question, pk=pk)
    
    ChoiceInlineFormSet = inlineformset_factory(Question, Choice, fields=['text'])
    if request.method == "POST":
        formset = ChoiceInlineFormSet(request.POST, request.FILES, instance=question)
        if formset.is_valid():
            formset.save()
            return HttpResponseRedirect(question.get_absolute_url())
    else:
        formset = ChoiceInlineFormSet(instance=question)
    return render(request, "core/question_choices.html", {"formset": formset})

