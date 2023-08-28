from flask import Response

from butler_offline.core import configuration_provider

THEMECSS = """:root {
    --main-color: THEME_COLOR;
}
"""


def index(request):
    return Response(THEMECSS.replace(
        'THEME_COLOR', configuration_provider.get_configuration('THEME_COLOR')), mimetype='text/css')
