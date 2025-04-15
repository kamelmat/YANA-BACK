import os
from django.test.runner import DiscoverRunner

class CustomTestRunner(DiscoverRunner):
    def setup_test_environment(self, **kwargs):
        os.environ['DJANGO_SETTINGS_MODULE'] = 'test_settings'
        super().setup_test_environment(**kwargs) 