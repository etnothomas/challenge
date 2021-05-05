from numpy import genfromtxt
from src.DataTables.Tables import Offers, GlobalCapacities, RegionalCapacities
import re
from src.Logging.Logging import Logger


class Parser:

    def __init__(self, model_name, func, delimiter, skip_header):
        self.delimiter = delimiter
        self.model_name = model_name
        self.func = func
        self.skip_header = skip_header
        self.parser = self.get_parser()
        self.logger = Logger.get_logger("Parser")

    def get_parser(self):
        if self.model_name == 'offers':
            return self.parse_offers
        elif self.model_name == 'global_capacity':
            return self.parse_global_capacities
        elif self.model_name == 'regional_capacity':
            return self.parse_regional_capacities
        else:
            return None

    @staticmethod
    def parse_bundle_data(s):
        country_destination = re.search("CountryDestination = (.+?)(,|\\s)", s)
        country_supplier = re.search("CountrySupplier = (.+?)(,|\\s)", s)
        region = re.search("Region = (.+?)(,|\\s)", s)
        type = re.search("Type = (.+?)(,|\\s)", s)
        supplier = re.search("supplier (.+?)\\s", s)
        capacity = re.search("max capacity of (.*)", s)
        return [v.group(1) if v else None for v in [country_supplier, region, country_destination, type, supplier, capacity]]

    def _read_data(self, file_path):
        data = genfromtxt(file_path, delimiter=self.delimiter, dtype=None, encoding=None, skip_header=self.skip_header, converters=self.func)
        return data.tolist()

    def parse_offers(self, file_path):
        data = self._read_data(file_path)
        offers = []
        for datum in data:
            offer = Offers(**{
                'item': datum[0],
                'supplier': datum[1].lower(),
                'unit_price': datum[2],
                'project_id': datum[3],
                'capacity': None
            })
            offers.append(offer)
        return offers

    def parse_global_capacities(self, file_path):
        data = self._read_data(file_path)
        global_capacities = []
        for datum in data:
            global_capacity = GlobalCapacities(**{
                'supplier': datum[0].lower(),
                'capacity': datum[1]
            })
            global_capacities.append(global_capacity)
        return global_capacities

    def parse_regional_capacities(self, file_path):
        data = self._read_data(file_path)
        bundle_capacities = []
        for datum in data:
            bundle_capacity = RegionalCapacities(**{
                'country_supplier': datum[0].lower(),
                'region': datum[1].lower(),
                'country_destination': datum[2].lower(),
                'type': datum[3].lower(),
                'supplier': datum[4].lower(),
                'capacity': datum[5]
            })
            bundle_capacities.append(bundle_capacity)
        return bundle_capacities


