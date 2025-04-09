import os
from django.test.runner import DiscoverRunner

class PostgresTestRunner(DiscoverRunner):
    def setup_test_environment(self, **kwargs):
        os.environ['DJANGO_SETTINGS_MODULE'] = 'site_app.settings.test'
        super().setup_test_environment(**kwargs) 