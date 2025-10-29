import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app, get_db
from app.schemas import Base, Sailing

# not using the file-based DB for tests
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"


@pytest.fixture(scope="session")
def db_engine():
    """
    The engine for testing, using in-memory db.
    """
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
    
    # using dependency_base() from app.schemas here 
    Base.metadata.create_all(bind=engine)
    yield engine
    # The engine will remove itself after the tests are done.


@pytest.fixture(scope="function")
def db_session(db_engine):
    """
    Will create a new database session for each test function.
    It handles rolling back after the test completes.
    """
    connection = db_engine.connect()
    trans = connection.begin()
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=connection)
    db = SessionLocal()

    def seed_data_factory(sailings_data):
        db.query(Sailing).delete()
        db.commit()
        db.add_all(sailings_data)
        db.commit()

    yield db, seed_data_factory

    db.close()
    trans.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(db_session):
    """
    TestClient, which provides the seeding factory to the test.
    """
    db, seed_data_factory = db_session

    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app), seed_data_factory

    del app.dependency_overrides[get_db]
