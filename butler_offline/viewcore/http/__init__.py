from flask import redirect, Response


class Redirector:
    def temporary_redirect(self, destination: str) -> Response:
        return redirect(destination, code=301)


class Request:
    def __init__(self, values: dict, args: dict, method: str):
        self.values = values
        self.args = args
        self.method = method

    def is_post_request(self):
        return self.method == 'POST'

    def post_action_is(self, action_name: str) -> bool:
        if not self.is_post_parameter_set( 'action'):
            return False
        return self.values['action'] == action_name

    def get_post_parameter_or_default(self, key, default, mapping_function=lambda x: x):
        if not self.is_post_parameter_set(key):
            return default
        return mapping_function(self.values[key])

    def is_post_parameter_set(self, parameter):
        if self.method != 'POST':
            return False
        return parameter in self.values.keys()

