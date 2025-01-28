from django.http import HttpResponse
import traceback
import logging


class ExceptionMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
        except Exception as e:
            self.process_exception(request, exception=e)
            return HttpResponse("Oops! Something went wrong.", status=500)
        return response

    def process_exception(self, request, exception):
        if exception:
            tb = traceback.extract_tb(exception.__traceback__)
            short_tb = "".join(traceback.format_list(tb[-3:]))

            message = "url: {url}\n[ERROR]: {error}\n[TRACEBACK]: {tb}\n\n".format(
                url=request.build_absolute_uri(),
                error=repr(exception),
                tb=short_tb
            )

            logging.error(f"{message}")
