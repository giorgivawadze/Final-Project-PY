from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from users.views import SingUpView

app_name = 'users'

urlpatterns = [
    path('login/', LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', SingUpView.as_view(), name='signup'),
]