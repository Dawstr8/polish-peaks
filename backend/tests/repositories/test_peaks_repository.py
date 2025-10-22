"""
Tests for the PeaksRepository
"""

import pytest

from src.peaks.repository import PeaksRepository


@pytest.fixture()
def test_repository(test_db):
    """Create a PeaksRepository instance for testing"""
    return PeaksRepository(test_db)


def test_get_all(test_repository, test_peaks):
    """Test retrieving all peaks"""
    peaks = test_repository.get_all()

    assert len(peaks) == 3
    assert any(peak.name == "Rysy" for peak in peaks)
    assert any(peak.name == "Śnieżka" for peak in peaks)
    assert any(peak.name == "Babia Góra" for peak in peaks)


def test_get_by_id(test_repository, test_peaks):
    """Test retrieving a peak by ID"""
    peak_id = test_peaks[0].id

    peak = test_repository.get_by_id(peak_id)

    assert peak is not None
    assert peak.name == "Rysy"
    assert peak.elevation == 2499

    peak = test_repository.get_by_id(999999)
    assert peak is None
