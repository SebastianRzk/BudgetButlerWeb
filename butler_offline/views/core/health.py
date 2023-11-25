from butler_offline.viewcore import request_handler
from butler_offline.viewcore.context.builder import generate_page_context, PageContext


class HealthContext:
    pass


def handle_request(_, context: HealthContext) -> PageContext:
    return generate_page_context('dashboard')


def index(request):
    return request_handler.handle(
        request=request,
        handle_function=handle_request,
        context_creator=lambda db: HealthContext(),
        html_base_page='core/health.html'
    )
