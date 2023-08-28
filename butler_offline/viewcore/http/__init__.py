from flask import redirect, Response


class Redirector:
    def temporary_redirect(self, destination: str) -> Response:
        return redirect(destination, code=301)
