
from flask import Blueprint, request, jsonify
from app.models import db
from app.models.address import Address
from app.utils import is_valid_btc_address

address_bp = Blueprint('address', __name__)

@address_bp.route('/addresses', methods=['POST'])
def add_address():
    data = request.get_json()
    address = data.get('address')

    if not address:
        return jsonify({'error': 'Address is required'}), 400
    if not is_valid_btc_address(address):
        return jsonify({'error': 'Invalid Bitcoin address format'}), 400
    if Address.query.filter_by(address=address).first():
        return jsonify({'error': 'Address already exists'}), 400

    new_address = Address(address=address)
    db.session.add(new_address)
    db.session.commit()
    return jsonify(new_address.as_dict()), 201

@address_bp.route('/addresses/<address>', methods=['DELETE'])
def remove_address(address):
    addr = Address.query.filter_by(address=address).first()
    if not addr:
        return jsonify({'error': 'Address not found'}), 404

    db.session.delete(addr)
    db.session.commit()

    return jsonify({'message': 'Address removed'}), 200

@address_bp.route('/addresses', methods=['GET'])
def list_addresses():
    addresses = Address.query.all()
    return jsonify([a.as_dict() for a in addresses])
