from django.http import HttpResponse
from viewcore import configuration_provider

THEMECSS = """:root {
    --main-color: THEME_COLOR;
}
"""

def index(request):
    return HttpResponse(THEMECSS.replace('THEME_COLOR', configuration_provider.get_configuration('THEME_COLOR')), content_type='text/css')
