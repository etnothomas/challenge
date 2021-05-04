from flask import request, jsonify
from flask.views import MethodView
from src.DataTables.Tables import RegionalCapacities, GlobalCapacities, Offers
import json
import decimal
from itertools import groupby
from operator import itemgetter
from collections import defaultdict


# helper method to encode decimals as strings when jsonifying
def _json_encode_decimal(obj):
    if isinstance(obj, decimal.Decimal):
        return str(obj)
    raise TypeError(repr(obj) + " is not JSON serializable")


# since python does not support tail recursion, this probably breaks with big result sets...
def _unpacker(dict, grouped_values, keys):
    if len(keys) == 1:
        dict[keys[0]].extend(grouped_values)
    else:
        a, *b = keys
        if a in dict:
            _unpacker(dict[a], grouped_values, b)
        else:
            dict[a] = defaultdict(list)
            _unpacker(dict[a], grouped_values, b)


# helper method to create a nested dict from a result set
# nesting happens in order of the keys
def _to_nested_dict(dict, *keys):
    d = defaultdict(list)
    grouped = groupby(dict, key=itemgetter(*keys))
    for keys, values in grouped:
        _unpacker(d, values, keys)
    return d


class GetProjectRegionalAndGlobalCaps(MethodView):

    def __init__(self, dal):
        self.dal = dal

    def get(self):
        project_id = request.args.get('project_id')
        result = self.dal.session.query(Offers, GlobalCapacities, RegionalCapacities)\
            .join(GlobalCapacities, GlobalCapacities.supplier == Offers.supplier) \
            .join(RegionalCapacities, RegionalCapacities.supplier == Offers.supplier) \
            .filter(Offers.project_id.like(project_id)) \
            .with_entities(
                Offers.supplier,
                RegionalCapacities.region,
                RegionalCapacities.country_supplier,
                RegionalCapacities.country_destination,
                GlobalCapacities.capacity.label("global_cap"),
                RegionalCapacities.capacity.label("regional_cap")) \
            .all()
        grouped = _to_nested_dict([dict(row) for row in result], "supplier", "region")
        return jsonify(json.dumps({project_id: grouped}, default=_json_encode_decimal)), 200


class GetRegionalAndGlobalCapacitiesWithOffers(MethodView):

    def __init__(self, dal):
        self.dal = dal

    def get(self):
        result = self.dal.session.query(Offers, GlobalCapacities, RegionalCapacities) \
            .join(GlobalCapacities, GlobalCapacities.supplier == Offers.supplier) \
            .join(RegionalCapacities, RegionalCapacities.supplier == Offers.supplier) \
            .with_entities(
                Offers.supplier,
                RegionalCapacities.region,
                RegionalCapacities.country_supplier,
                RegionalCapacities.country_destination,
                GlobalCapacities.capacity.label("global_cap"),
                RegionalCapacities.capacity.label("regional_cap"),
                Offers.item)\
            .all()
        grouped = _to_nested_dict([dict(row) for row in result], "supplier", "region", "item")
        return jsonify(json.dumps(grouped, default=_json_encode_decimal)), 200


class GetOfferCapacities(MethodView):

    def __init__(self, dal):
        self.dal = dal

    def get(self):
        item_id = request.args.get('item_id')
        result = self.dal.session.query(Offers, GlobalCapacities, RegionalCapacities) \
            .join(GlobalCapacities, GlobalCapacities.supplier == Offers.supplier) \
            .join(RegionalCapacities, RegionalCapacities.supplier == Offers.supplier) \
            .filter(Offers.item.like(item_id)) \
            .with_entities(
                Offers.item,
                Offers.supplier,
                Offers.capacity.label("item_cap"),
                RegionalCapacities.region,
                RegionalCapacities.country_supplier,
                RegionalCapacities.country_destination,
                GlobalCapacities.capacity.label("global_cap"),
                RegionalCapacities.capacity.label("regional_cap"),
                Offers.unit_price) \
            .all()
        grouped = _to_nested_dict([dict(row) for row in result], "item", "supplier", "region")
        return jsonify(json.dumps(grouped, default=_json_encode_decimal)), 200


class AddRegionalCapacity(MethodView):

    def __init__(self, dal):
        self.dal = dal

    def post(self):
        json_data = request.get_json(force=True)
        new_datum = {
            'country_supplier': json_data[0].lower(),
            'region': json_data[1].lower(),
            'country_destination': json_data[2].lower(),
            'type': json_data[3].lower(),
            'supplier': json_data[4].lower(),
            'capacity': json_data[5]
            }
        new_model = RegionalCapacities(**new_datum)
        self.dal.insert(new_model)
        return jsonify(new_datum), 201


class AddGlobalCapacity(MethodView):

    def __init__(self, dal):
        self.dal = dal

    def post(self):
        json_data = request.get_json()
        new_datum = {
            'supplier': json_data['supplier'].lower(),
            'capacity': json_data['capacity']
        }
        new_model = GlobalCapacities(**new_datum)
        self.dal.insert([new_model])
        return jsonify(new_datum), 201


class AddItemCapacity(MethodView):

    def __init__(self, dal):
        self.dal = dal

    def post(self):
        json_data = request.get_json(force=True)
        new_datum = {
            'item': json_data['item'],
            'supplier': json_data['supplier'].lower(),
            'unit_price': json_data['unit_price'],
            'project_id': json_data['project_id'],
            'capacity': json_data['capacity']
        }
        new_model = Offers(**new_datum)
        self.dal.insert([new_model])
        return jsonify(new_datum), 201
