# accounts/views.py
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ImproperlyConfigured
from django.urls import reverse_lazy
from django.views import generic
from django.contrib import messages

class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

    def get_success_url(self):
        """Return the URL to redirect to after processing a valid form."""
        if not self.success_url:
            raise ImproperlyConfigured("No URL to redirect to. Provide a success_url.")

        messages.success(self.request, 'Your account have been created. You can now login.')
        return str(self.success_url)  # success_url may be lazy
