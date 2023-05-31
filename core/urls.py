from django.urls import path
from core import views

app_name = 'core'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('add/question/', views.QuestionCreateView.as_view(), name='question-create'),
    path('questions/<int:pk>/choices/', views.add_choices_to_question, name='question-choices'),
    path('questions/<int:pk>/vote/', views.ChoiceSelectView.as_view(), name='question-vote'),
    path('questions/<int:pk>/', views.QuestionDetailView.as_view(), name='question-detail'),
    path('questions/<int:pk>/delete/', views.QuestionDeleteView.as_view(), name='question-delete'),
    path('questions/<int:pk>/edit/', views.QuestionUpdateView.as_view(), name='question-edit'),
]