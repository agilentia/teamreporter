from django.http import Http404
from django.shortcuts import get_object_or_404

from .models import Survey


def survey_completed(view_func):
    """
    Allow updating only surveys which haven't been completed. In other case point to 404 page.
    """
    def decorator(request, *args, **kwargs):
        if get_object_or_404(Survey, pk=kwargs['uuid']).completed is not None:
            raise Http404()
        else:
            return view_func(request, *args, **kwargs)
    return decorator