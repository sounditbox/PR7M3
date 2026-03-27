from django.contrib import messages


class ErrorMessageMixin:
    """
    Add an error message on invalid form submission.
    """

    error_message = 'Что-то пошло не так :('

    def form_invalid(self, form):
        response = super().form_invalid(form)
        error_message =  self.error_message
        if error_message:
            messages.error(self.request, error_message)
        return response
