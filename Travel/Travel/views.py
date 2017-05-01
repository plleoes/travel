# Create your views here.

# from django.utils.translation import ugettext_lazy as _

from django.http import HttpResponse
from django.template import loader
import os

def my_view(request):
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    template = loader.get_template(os.path.join(BASE_DIR, 'templates') + "\\index.html")
    return HttpResponse(template.render())
