from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin


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


class AuthorRequiredMixin(UserPassesTestMixin):
    """
    Restrict access to objects owned by the current user.
    """

    def test_func(self):
        obj = self.get_object()
        return bool(
            self.request.user.is_authenticated
            and getattr(obj, 'author', None) is not None
            and obj.author.user_id == self.request.user.id
        )
