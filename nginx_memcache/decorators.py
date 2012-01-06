from django.conf import settings
from django.utils.decorators import decorator_from_middleware_with_args

from .middleware import UpdateCacheMiddleware


# Create decorator.
# This is a similar approach to https://github.com/shaunsephton/djanginxed
# except using middleware instead of writing decorator directly.
def cache_page_nginx(view_fn=None, cache_timeout=settings.CACHE_NGINX_TIME,
                    page_version_fn=None, anonymous_only=False):
    decorator = decorator_from_middleware_with_args(UpdateCacheMiddleware)(
        cache_timeout=cache_timeout, page_version_fn=page_version_fn,
        anonymous_only=anonymous_only)
    if callable(view_fn):
        return decorator(view_fn)
    return decorator
