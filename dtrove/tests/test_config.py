
from .base import *


class ConfigTests(DtroveTest):

    def setUp(self):
        from dtrove import _get
        self._get = _get

    def test_get_config(self):
        found = self._get('SECRET_KEY')
        self.assertEqual(settings.SECRET_KEY, found)

    def test_get_default(self):
        default = self._get('MISSING_CONFIG_OPTION', 'gone')
        self.assertEqual('gone', default)

    def test_get_warning(self):
        default = self._get('MISSING_CONFIG_OPTION', 'gone', warn=True)
        self.assertEqual('gone', default)
