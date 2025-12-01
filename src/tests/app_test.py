import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import app as app_module


class TestApp(unittest.TestCase):
    def setUp(self):
        app_module.app.config['TESTING'] = True
        self.client = app_module.app.test_client()
        app_module.varastot.clear()
        app_module.next_id = 1

    def tearDown(self):
        app_module.varastot.clear()
        app_module.next_id = 1

    def test_index_empty(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Warehouse Management', response.data)
        self.assertIn(b'No storages created yet', response.data)

    def test_create_page_get(self):
        response = self.client.get('/create')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Create New Storage', response.data)

    def test_create_storage(self):
        response = self.client.post('/create', data={
            'name': 'Test Storage',
            'tilavuus': '100',
            'alku_saldo': '10'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Storage', response.data)
        self.assertEqual(len(app_module.varastot), 1)

    def test_create_storage_empty_name(self):
        response = self.client.post('/create', data={
            'name': '',
            'tilavuus': '100',
            'alku_saldo': '10'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Name is required', response.data)

    def test_create_storage_invalid_tilavuus(self):
        response = self.client.post('/create', data={
            'name': 'Test',
            'tilavuus': '-10',
            'alku_saldo': '0'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Capacity must be positive', response.data)

    def test_create_storage_invalid_numbers(self):
        response = self.client.post('/create', data={
            'name': 'Test',
            'tilavuus': 'abc',
            'alku_saldo': '0'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid numeric values', response.data)

    def test_view_storage(self):
        self.client.post('/create', data={
            'name': 'Test Storage',
            'tilavuus': '100',
            'alku_saldo': '10'
        })
        response = self.client.get('/view/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Storage', response.data)
        self.assertIn(b'100', response.data)

    def test_view_nonexistent_storage(self):
        response = self.client.get('/view/999', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Warehouse Management', response.data)

    def test_add_to_storage(self):
        self.client.post('/create', data={
            'name': 'Test Storage',
            'tilavuus': '100',
            'alku_saldo': '10'
        })
        response = self.client.post('/add/1', data={'maara': '20'}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(app_module.varastot[1]['varasto'].saldo, 30)

    def test_add_invalid_amount(self):
        self.client.post('/create', data={
            'name': 'Test Storage',
            'tilavuus': '100',
            'alku_saldo': '10'
        })
        response = self.client.post('/add/1', data={'maara': 'abc'}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        # Should redirect to view with unchanged saldo
        self.assertEqual(app_module.varastot[1]['varasto'].saldo, 10)

    def test_add_to_nonexistent_storage(self):
        response = self.client.post('/add/999', data={'maara': '20'}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Warehouse Management', response.data)

    def test_remove_from_storage(self):
        self.client.post('/create', data={
            'name': 'Test Storage',
            'tilavuus': '100',
            'alku_saldo': '50'
        })
        response = self.client.post('/remove/1', data={'maara': '20'}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(app_module.varastot[1]['varasto'].saldo, 30)

    def test_remove_invalid_amount(self):
        self.client.post('/create', data={
            'name': 'Test Storage',
            'tilavuus': '100',
            'alku_saldo': '50'
        })
        response = self.client.post('/remove/1', data={'maara': 'abc'}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        # Should redirect to view with unchanged saldo
        self.assertEqual(app_module.varastot[1]['varasto'].saldo, 50)

    def test_remove_from_nonexistent_storage(self):
        response = self.client.post('/remove/999', data={'maara': '20'}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Warehouse Management', response.data)

    def test_delete_storage(self):
        self.client.post('/create', data={
            'name': 'Test Storage',
            'tilavuus': '100',
            'alku_saldo': '10'
        })
        self.assertEqual(len(app_module.varastot), 1)
        response = self.client.post('/delete/1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(app_module.varastot), 0)

    def test_delete_nonexistent_storage(self):
        response = self.client.post('/delete/999', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Warehouse Management', response.data)

    def test_index_with_storages(self):
        self.client.post('/create', data={
            'name': 'Storage 1',
            'tilavuus': '100',
            'alku_saldo': '10'
        })
        self.client.post('/create', data={
            'name': 'Storage 2',
            'tilavuus': '50',
            'alku_saldo': '25'
        })
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Storage 1', response.data)
        self.assertIn(b'Storage 2', response.data)
