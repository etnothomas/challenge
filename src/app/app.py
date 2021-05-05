from flask import Flask
from src.app.views import AddGlobalCapacity, AddItemCapacity, AddRegionalCapacity, GetRegionalAndGlobalCapacitiesWithOffers, GetOfferCapacities, GetProjectRegionalAndGlobalCaps
from src.Dal.DataAccessLayer import DataAccessLayer
from src.DataTables.Tables import Base
from src.Parser.Populate import Populate
from pathlib import Path
from src.Logging.Logging import Logger


def create_app():
    # get main logger
    logger = Logger.get_logger("Main")
    # get the root dir of the code
    parentdir = Path().resolve().parent.parent
    # import the sql alchemy Base that will hold the table metadata
    base = Base
    dal = DataAccessLayer(base)
    pop = Populate(dal)
    dal.connect(f"sqlite:///{parentdir}/db/archlet.db")
    logger.info("Created Sqlite3 database")
    # so that we start from scratch
    dal.destroy_db()
    # create tables and populate them
    dal.create_all()
    logger.info("Start populating tables...")
    pop.populate_global_capacity(f"{parentdir}/data/global_capacities.txt")
    pop.populate_offers(f"{parentdir}/data/offers.csv")
    pop.populate_regional_capacity(f"{parentdir}/data/bundle_capacities.txt")
    logger.info("Done populating tables")
    # setup flask app
    logger.info("Instantiating Flask app")
    app = Flask(__name__)
    app.add_url_rule('/archlet/v1/postglobalcapacity',
                     view_func=AddGlobalCapacity.as_view('postglobalcapacity', dal))
    app.add_url_rule('/archlet/v1/postregionalcapacity',
                     view_func=AddRegionalCapacity.as_view('postregionalcapacity', dal))
    app.add_url_rule('/archlet/v1/postitemcapacity',
                     view_func=AddItemCapacity.as_view('postitemcapacity', dal))
    app.add_url_rule('/archlet/v1/getprojectregionalandglobalcaps',
                     view_func=GetProjectRegionalAndGlobalCaps.as_view('GetProjectRegionalAndGlobalCaps', dal))
    app.add_url_rule('/archlet/v1/getregionalandglobalcapacitieswithoffers',
                     view_func=GetRegionalAndGlobalCapacitiesWithOffers.as_view('getregionalandglobalcapacitieswithoffers', dal))
    app.add_url_rule('/archlet/v1/getoffercapacities',
                     view_func=GetOfferCapacities.as_view('getoffercapacities', dal))
    logger.info("App ready")
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', debug=True, port=5050)

