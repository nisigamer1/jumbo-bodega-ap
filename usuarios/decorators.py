from django.shortcuts import redirect

def role_required(role_name):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if request.user.is_authenticated and request.user.groups.filter(name=role_name).exists():
                return view_func(request, *args, **kwargs)
            return redirect('login')
        return wrapper
    return decorator