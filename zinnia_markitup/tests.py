"""Test cases for zinnia-markitup"""
from django.test import TestCase
from django.test import RequestFactory
from django.contrib.admin.sites import AdminSite
from django.test.utils import restore_template_loaders
from django.test.utils import setup_test_template_loader

from zinnia.models.entry import Entry
from zinnia.signals import disconnect_entry_signals

from zinnia_markitup.admin import EntryAdminMarkItUp


class BaseAdminTestCase(TestCase):

    def setUp(self):
        disconnect_entry_signals()
        self.site = AdminSite()
        self.admin = EntryAdminMarkItUp(
            Entry, self.site)

    def tearDown(self):
        try:
            restore_template_loaders()
        except AttributeError:
            pass


class EntryAdminMarkItUpTestCase(BaseAdminTestCase):
    """Test case for Entry Admin with MarkItUp"""

    def setUp(self):
        super(EntryAdminMarkItUpTestCase, self).setUp()
        self.request_factory = RequestFactory()
        self.request = self.request_factory.get('/')

    def test_markitup(self):
        template_to_use = 'admin/zinnia/entry/markitup.js'
        setup_test_template_loader({template_to_use: ''})
        response = self.admin.markitup(self.request)
        self.assertTemplateUsed(response, template_to_use)
        self.assertEqual(len(response.context_data['lang']), 2)
        self.assertEqual(response['Content-Type'], 'application/javascript')

    def test_medias(self):
        medias = self.admin.media
        self.assertEqual(
            medias._css,
            {'all': ['/static/zinnia/css/jquery.autocomplete.css']})
        self.assertEqual(
            medias._js,
            ['/static/admin/js/core.js',
             '/static/admin/js/admin/RelatedObjectLookups.js',
             '/static/admin/js/jquery.min.js',
             '/static/admin/js/jquery.init.js',
             '/static/admin/js/actions.min.js',
             '/static/admin/js/urlify.js',
             '/static/admin/js/prepopulate.min.js',
             '/static/zinnia/js/jquery.js',
             '/static/zinnia/js/jquery.bgiframe.js',
             '/static/zinnia/js/jquery.autocomplete.js',
             '/admin/zinnia/entry/autocomplete_tags/',
             '/static/zinnia_wymeditor/js/wymeditor/jquery.wymeditor.pack.js',
             '/static/zinnia_wymeditor/js/wymeditor/'
             'plugins/hovertools/jquery.wymeditor.hovertools.js',
             '/admin/zinnia/entry/wymeditor/'])
