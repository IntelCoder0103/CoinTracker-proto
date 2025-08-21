import unittest
from unittest.mock import patch, MagicMock
from app import app

class AddressApiUnitTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        app.config['TESTING'] = True

    @patch('app.routes.address.Address')
    @patch('app.routes.address.db')
    @patch('app.routes.address.is_valid_btc_address')
    def test_add_address_success(self, mock_is_valid, mock_db, mock_address):
        mock_is_valid.return_value = True
        mock_address.query.filter_by.return_value.first.return_value = None
        mock_address_obj = MagicMock()
        mock_address_obj.as_dict.return_value = {'address': 'addr1'}
        mock_address.return_value = mock_address_obj
        resp = self.app.post('/addresses', json={'address': 'addr1'})
        self.assertEqual(resp.status_code, 201)
        self.assertIn('address', resp.get_json())
        mock_db.session.add.assert_called_once()
        mock_db.session.commit.assert_called_once()

    @patch('app.routes.address.is_valid_btc_address')
    def test_add_address_invalid(self, mock_is_valid):
        mock_is_valid.return_value = False
        resp = self.app.post('/addresses', json={'address': 'badaddr'})
        self.assertEqual(resp.status_code, 400)
        self.assertIn('error', resp.get_json())

    def test_add_address_missing(self):
        resp = self.app.post('/addresses', json={})
        self.assertEqual(resp.status_code, 400)
        self.assertIn('error', resp.get_json())

    @patch('app.routes.address.Address')
    def test_add_address_duplicate(self, mock_address):
        mock_address.query.filter_by.return_value.first.return_value = MagicMock()
        resp = self.app.post('/addresses', json={'address': 'addr1'})
        self.assertEqual(resp.status_code, 400)
        self.assertIn('error', resp.get_json())

    @patch('app.routes.address.Address')
    @patch('app.routes.address.db')
    def test_remove_address_success(self, mock_db, mock_address):
        mock_addr = MagicMock()
        mock_address.query.filter_by.return_value.first.return_value = mock_addr
        resp = self.app.delete('/addresses/addr1')
        self.assertEqual(resp.status_code, 200)
        self.assertIn('message', resp.get_json())
        mock_db.session.delete.assert_called_once_with(mock_addr)
        mock_db.session.commit.assert_called_once()

    @patch('app.routes.address.Address')
    def test_remove_address_not_found(self, mock_address):
        mock_address.query.filter_by.return_value.first.return_value = None
        resp = self.app.delete('/addresses/addr1')
        self.assertEqual(resp.status_code, 404)
        self.assertIn('error', resp.get_json())

    @patch('app.routes.address.Address')
    def test_list_addresses(self, mock_address):
        mock_addr1 = MagicMock()
        mock_addr1.as_dict.return_value = {'address': 'addr1'}
        mock_addr2 = MagicMock()
        mock_addr2.as_dict.return_value = {'address': 'addr2'}
        mock_address.query.all.return_value = [mock_addr1, mock_addr2]
        resp = self.app.get('/addresses')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_json(), [{'address': 'addr1'}, {'address': 'addr2'}])

if __name__ == '__main__':
    unittest.main()
