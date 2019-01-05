def set_success_message(context, message):
    context['message'] = True
    context['message_type'] = 'success'
    context['message_content'] = message
    return context

def set_error_message(context, message):
    context['message'] = True
    context['message_type'] = 'error'
    context['message_content'] = message
    return context
