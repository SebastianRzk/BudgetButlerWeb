from butler_offline.viewcore import template

from flask import render_template

RENDERER = None
BASE_THEME_PATH = 'theme/'


def theme(page):
    return template.BASE_THEME_PATH + page


def renderer_instance():
    if not template.RENDERER:
        template.RENDERER = Renderer()
    return template.RENDERER


class Renderer:
    def render(self, html, **context):
        return render_template(theme(html), **context)
