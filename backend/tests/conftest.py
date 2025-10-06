import shutil
from pathlib import Path

import pytest
from fastapi import UploadFile
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
from starlette.datastructures import Headers

from app.database import get_session
from app.models.peak import Peak
from app.services.storage.local_storage import LocalFileStorage
from main import app


@pytest.fixture
def client():
    """Creates a TestClient instance for API testing"""
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def client_with_db(test_session):
    """
    Create a test client with a test database session.
    Reuses the test_session fixture for database operations.
    """

    def override_get_session():
        yield test_session

    app.dependency_overrides[get_session] = override_get_session

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture
def test_session():
    """
    Create a test database session with an in-memory SQLite database.
    """
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=False,
    )
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        yield session


@pytest.fixture
def test_peaks(test_session: Session):
    """Create test peaks and save to database"""
    peaks = [
        Peak(
            name="Rysy",
            elevation=2499,
            latitude=49.1795,
            longitude=20.0881,
            range="Tatry",
        ),
        Peak(
            name="Śnieżka",
            elevation=1602,
            latitude=50.7361,
            longitude=15.7400,
            range="Karkonosze",
        ),
        Peak(
            name="Babia Góra",
            elevation=1725,
            latitude=49.5731,
            longitude=19.5297,
            range="Beskidy",
        ),
    ]

    for peak in peaks:
        test_session.add(peak)

    test_session.commit()

    for peak in peaks:
        test_session.refresh(peak)

    return peaks


@pytest.fixture
def test_upload_dir():
    """Creates a temporary upload directory for tests"""
    test_dir = Path("test_uploads")
    test_dir.mkdir(exist_ok=True)
    yield test_dir

    if test_dir.exists():
        shutil.rmtree(test_dir)


@pytest.fixture
def local_storage(test_upload_dir):
    """Creates a LocalFileStorage instance with test directory"""
    return LocalFileStorage(upload_dir=str(test_upload_dir))


@pytest.fixture
def mock_upload_file(tmp_path):
    """Creates a mock UploadFile for testing"""
    test_content = b"test image content"
    test_file = tmp_path / "test.jpg"
    test_file.write_bytes(test_content)

    return UploadFile(
        filename="test.jpg",
        file=open(test_file, "rb"),
        headers=Headers({"content-type": "image/jpeg"}),
    )
