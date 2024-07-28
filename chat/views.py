from django.contrib.auth.forms import AuthenticationForm
from django.http.response import HttpResponse as HttpResponse
from django.contrib import messages
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

# Create your views here.
class LoginView(LoginView):
    redirect_authenticated_user = True
    template_name = "login/login.html"

    def  get_success_url(self) -> str:
        return reverse_lazy('index')

    def form_invalid(self, form: AuthenticationForm):
        messages.error(self.request,'Invalid username or password')
        return self.render_to_response(self.get_context_data(form=form))


class SearchRoomView(LoginRequiredMixin, TemplateView):
    template_name = 'chat/index.html'


class RoomView(LoginRequiredMixin, TemplateView):

    template_name = "chat/room.html"

    def get_context_data(self, **kwargs) -> dict[str, any]:
        context = super().get_context_data(**kwargs)
        context['room_name'] = self.kwargs['room_name']
        return context

