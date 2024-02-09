from django.shortcuts import redirect

def redirect_authenticated_user(function):
    def _function(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')  # Change 'index' to the desired URL name if needed
        return function(request, *args, **kwargs)
    return _function