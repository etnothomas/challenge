from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from contextlib import contextmanager


class DataAccessLayer(object):

    def __init__(self, base):
        self.base = base
        self.engine = None
        self.session = None

    def connect(self, url):
        self.engine = create_engine(url)
        self.session = scoped_session(sessionmaker(bind=self.engine))

    @contextmanager
    def transaction(self):
        session = self.session()
        try:
            yield session
            session.commit()
        except Exception as e:
            print(e)
            session.rollback()
            raise e
        finally:
            session.close()
            self.session.remove()
            print("session closed")

    def insert(self, data):
        for datum in data:
            try:
                with self.transaction() as session:
                    session.merge(datum)
            except Exception as e:
                print(e)
                continue

    def bulk_insert(self, data):
        with self.transaction() as session:
            session.bulk_save_objects(data)

    def create_all(self):
        self.base.metadata.create_all(self.engine)

    def destroy_db(self):
        self.base.metadata.drop_all(self.engine)
