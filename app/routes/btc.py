
from flask import Blueprint, jsonify, request
from app.models.address import Address
from app.integration.bitcoin_api import BitcoinAPI

btc_bp = Blueprint('btc', __name__)

@btc_bp.route('/addresses/<address>/balance', methods=['GET'])
def get_balance(address):
    addr = Address.query.filter_by(address=address).first()
    if not addr:
        return jsonify({'error': 'Address not found'}), 404

    balance, error = BitcoinAPI.get_balance(address)
    if error or balance is None:
        return jsonify({'error': error or 'Unable to fetch balance'}), 500

    return jsonify({'address': address, 'balance': balance})

@btc_bp.route('/addresses/<address>/transactions', methods=['GET'])
def get_transactions(address):
    addr = Address.query.filter_by(address=address).first()

    if not addr:
        return jsonify({'error': 'Address not found'}), 404
    try:
        limit = int(request.args.get('limit', 20))
    except ValueError:
        limit = 20

    try:
        offset = int(request.args.get('offset', 0))
    except ValueError:
        offset = 0

    txs, error, total_count = BitcoinAPI.get_transactions(address, limit=limit, offset=offset)
    if error or txs is None:
        return jsonify({'error': error or 'Unable to fetch transactions'}), 500
    return jsonify({'address': address, 'transactions': txs, 'total': total_count, 'offset': offset, 'limit': limit})
