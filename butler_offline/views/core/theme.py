from butler_offline.viewcore import configuration_provider
from flask import Response

THEMECSS = """:root {
    --main-color: THEME_COLOR;
}
"""

def index(request):
    return Response(THEMECSS.replace('THEME_COLOR', configuration_provider.get_configuration('THEME_COLOR')), mimetype='text/css')
