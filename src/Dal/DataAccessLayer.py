from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from contextlib import contextmanager
from src.Logging.Logging import Logger


class DataAccessLayer(object):

    def __init__(self, base):
        self.base = base
        self.engine = None
        self.session = None
        self.logger = Logger.get_logger("DataAccessLayer")

    def connect(self, url):
        self.engine = create_engine(url)
        self.session = scoped_session(sessionmaker(bind=self.engine))

    @contextmanager
    def transaction(self):
        session = self.session()
        try:
            self.logger.info("session started")
            yield session
            session.commit()
        except Exception as e:
            self.logger.error(e)
            session.rollback()
            raise e
        finally:
            session.close()
            self.session.remove()
            self.logger.info("session closed")

    def insert(self, data):
        for datum in data:
            try:
                with self.transaction() as session:
                    session.merge(datum)
            except Exception as e:
                self.logger.error(e)
                continue

    def bulk_insert(self, data):
        with self.transaction() as session:
            session.bulk_save_objects(data)

    def create_all(self):
        self.base.metadata.create_all(self.engine)

    def destroy_db(self):
        self.base.metadata.drop_all(self.engine)
