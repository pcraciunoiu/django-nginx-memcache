from django.http import HttpResponse
from django.test import TestCase
from django.test.client import RequestFactory

from nginx_memcache.cache import nginx_cache as cache, get_cache_key
from nginx_memcache.decorators import cache_page_nginx


class CachePageDecoratorTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_default_args(self):
        def my_view(request):
            return HttpResponse('content')

        # Clear the cache before we do anything.
        request = self.factory.get('/')
        cache.clear()
        cache_key = get_cache_key(request.get_full_path())
        assert not cache.get(cache_key)

        # Cache the view
        my_view_cached = cache_page_nginx(my_view)
        self.assertEqual(my_view_cached(request).content, 'content')

        assert cache.get(cache_key)
