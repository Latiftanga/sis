from django.shortcuts import redirect
from django.urls import reverse

EXEMPT_URLS = [
    reverse('verify-token'),
    reverse('signup'),
    reverse('signin')
]

class LoginRequiredMiddleware:
    """
    Middleware that requires a user to be authenticated to view any page except
    for the login, signup, and token verification pages.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # If the user is not authenticated and the request path is not in EXEMPT_URLS
        if not request.user.is_authenticated and request.path not in EXEMPT_URLS:
            return redirect(f"{reverse('signin')}?next={request.path}")

        response = self.get_response(request)
        return response


class RoleBasedRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            if request.path == '':
                if request.user.is_student:
                    return redirect('student_dashboard')
                elif request.user.is_teacher:
                    return redirect('teacher_dashboard')
                elif request.user.is_admin:
                    return redirect('admin_dashboard')

        return self.get_response(request)
