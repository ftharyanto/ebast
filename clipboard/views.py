from django.shortcuts import redirect
from django.utils import timezone
from datetime import timedelta
from django.views.generic import ListView, CreateView
from .models import Clipboard
from .forms import ClipboardForm

class ClipboardView(ListView, CreateView):
    model = Clipboard
    context_object_name = 'clipboard_items'
    template_name = 'clipboard/clipboard.html'
    form_class = ClipboardForm
    success_url = '/clipboard/'

    def get_queryset(self):
        # Remove expired entries
        # Clipboard.objects.filter(created_at__lt=timezone.now() - timedelta(days=1)).delete()
        return Clipboard.objects.all()

    def form_valid(self, form):
        form.save()
        return redirect(self.success_url)
