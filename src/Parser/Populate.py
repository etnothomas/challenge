from src.Parser.Parser import Parser
from src.Logging.Logging import Logger


class Populate:

    def __init__(self, dal):
        self.dal = dal
        self.logger = Logger.get_logger("Populate")

    def populate_offers(self, file_path):
        parser = Parser('offers', None, ',', True)
        objects = parser.parser(file_path)
        self.dal.bulk_insert(objects)
        self.logger.info(f"Inserted {len(objects)} rows into Offers")

    def populate_global_capacity(self, file_path):
        parser = Parser('global_capacity', {1: lambda s: str(s).replace(" ", "")}, ':', False)
        objects = parser.parser(file_path)
        self.dal.bulk_insert(objects)
        self.logger.info(f"Inserted {len(objects)} rows into global capacity")

    def populate_regional_capacity(self, file_path):
        parser = Parser('regional_capacity', {0: lambda s: Parser.parse_bundle_data(str(s))}, '@', False)
        objects = parser.parser(file_path)
        self.dal.bulk_insert(objects)
        self.logger.info(f"Inserted {len(objects)} rows into regional_capacity")
