import unittest
from unittest.mock import patch, MagicMock
from app import app

class BtcApiUnitTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        app.config['TESTING'] = True

    @patch('app.routes.btc.Address')
    @patch('app.integration.bitcoin_api.BitcoinAPI.get_balance')
    def test_get_balance_success(self, mock_get_balance, mock_address):
        mock_address.query.filter_by.return_value.first.return_value = MagicMock()
        mock_get_balance.return_value = (123456, None)
        resp = self.app.get('/addresses/addr1/balance')
        self.assertEqual(resp.status_code, 200)
        self.assertIn('balance', resp.get_json())

    @patch('app.routes.btc.Address')
    def test_get_balance_address_not_found(self, mock_address):
        mock_address.query.filter_by.return_value.first.return_value = None
        resp = self.app.get('/addresses/addr1/balance')
        self.assertEqual(resp.status_code, 404)
        self.assertIn('error', resp.get_json())

    @patch('app.routes.btc.Address')
    @patch('app.integration.bitcoin_api.BitcoinAPI.get_balance')
    def test_get_balance_api_error(self, mock_get_balance, mock_address):
        mock_address.query.filter_by.return_value.first.return_value = MagicMock()
        mock_get_balance.return_value = (None, 'API error')
        resp = self.app.get('/addresses/addr1/balance')
        self.assertEqual(resp.status_code, 500)
        self.assertIn('error', resp.get_json())

    @patch('app.routes.btc.Address')
    @patch('app.integration.bitcoin_api.BitcoinAPI.get_transactions')
    def test_get_transactions_success(self, mock_get_transactions, mock_address):
        mock_address.query.filter_by.return_value.first.return_value = MagicMock()
        mock_get_transactions.return_value = ([{'hash': 'tx1'}, {'hash': 'tx2'}], None, 2)
        resp = self.app.get('/addresses/addr1/transactions?limit=2')
        self.assertEqual(resp.status_code, 200)
        self.assertIn('transactions', resp.get_json())
        self.assertEqual(len(resp.get_json()['transactions']), 2)

    @patch('app.routes.btc.Address')
    def test_get_transactions_address_not_found(self, mock_address):
        mock_address.query.filter_by.return_value.first.return_value = None
        resp = self.app.get('/addresses/addr1/transactions')
        self.assertEqual(resp.status_code, 404)
        self.assertIn('error', resp.get_json())

    @patch('app.routes.btc.Address')
    @patch('app.integration.bitcoin_api.BitcoinAPI.get_transactions')
    def test_get_transactions_api_error(self, mock_get_transactions, mock_address):
        mock_address.query.filter_by.return_value.first.return_value = MagicMock()
        mock_get_transactions.return_value = (None, 'API error', 0)
        resp = self.app.get('/addresses/addr1/transactions')
        self.assertEqual(resp.status_code, 500)
        self.assertIn('error', resp.get_json())

if __name__ == '__main__':
    unittest.main()
