from src.Parser.Parser import Parser


class Populate:

    def __init__(self, dal):
        self.dal = dal

    def populate_offers(self, file_path):
        parser = Parser('offers', None, ',', True)
        objects = parser.parser(file_path)
        self.dal.bulk_insert(objects)

    def populate_global_capacity(self, file_path):
        parser = Parser('global_capacity', {1: lambda s: str(s).replace(" ", "")}, ':', False)
        objects = parser.parser(file_path)
        self.dal.bulk_insert(objects)

    def populate_regional_capacity(self, file_path):
        parser = Parser('regional_capacity', {0: lambda s: Parser.parse_bundle_data(str(s))}, '@', False)
        objects = parser.parser(file_path)
        self.dal.bulk_insert(objects)
