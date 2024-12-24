from django.views.generic import TemplateView
from qc.models import Operator

class HomeView(TemplateView):
    template_name = 'core/homepage.html'

class OperatorView(TemplateView):
    model = Operator
    template_name = 'core/operator.html'
    context_object_name = 'operator'
