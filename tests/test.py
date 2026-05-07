"""SmartBinDB test suite with sync and async coverage."""

import pytest
import asyncio

from smartbindb import SmartBinDB, __version__


@pytest.fixture(scope="module")
def db():
    """Module-scoped SmartBinDB instance."""
    return SmartBinDB()


def test_version():
    """Package version is non-empty string."""
    assert isinstance(__version__, str) and __version__


def test_data_loaded(db):
    """Bundled database populates both indices."""
    assert db.COUNTRY_DATA, "COUNTRY_DATA should not be empty"
    assert db.BIN_INDEX, "BIN_INDEX should not be empty"


def test_country_info_known(db):
    """Known country codes return full ISO metadata."""
    info = db.get_country_info("US")
    assert info["A2"] == "US"
    assert info["A3"] == "USA"
    assert info["Name"]


def test_country_info_unknown(db):
    """Unknown country codes return empty-but-shaped record."""
    info = db.get_country_info("ZZ")
    assert info["A2"] == "ZZ"
    assert info["A3"] == ""


def test_format_entry(db):
    """format_entry produces documented response schema."""
    formatted = db.format_entry(
        {"bin": "457173", "issuer": "Test", "type": "credit"}, "US"
    )
    assert formatted["bin"] == "457173"
    assert formatted["issuer"] == "Test"
    assert formatted["Country"]["A2"] == "US"


def test_get_bin_info_unknown(db):
    """Invalid BIN lookup returns error response."""
    res = db.get_bin_info("000000xyz")
    assert res["status"] == "error"


def test_get_bin_info_known(db):
    """First known BIN lookup returns success."""
    sample_bin = next(iter(db.BIN_INDEX))
    res = db.get_bin_info(sample_bin)
    assert res["status"] == "SUCCESS"
    assert res["count"] == 1


def test_get_bins_by_country_known(db):
    """Known country returns at least one record."""
    sample_country = next(iter(db.COUNTRY_DATA))
    res = db.get_bins_by_country(sample_country, limit=2)
    assert res["status"] == "SUCCESS"
    assert res["count"] >= 1


def test_get_bins_by_country_unknown(db):
    """Unknown country code returns error."""
    res = db.get_bins_by_country("ZZ", limit=1)
    assert res["status"] == "error"


def test_get_bins_by_country_us_limit(db):
    """US bucket rejects limits above 8000."""
    res = db.get_bins_by_country("US", limit=9000)
    assert res["status"] == "error"


def test_get_bins_by_bank_unknown(db):
    """Unknown bank substring returns error."""
    res = db.get_bins_by_bank("zzz_definitely_not_a_bank_zzz", limit=1)
    assert res["status"] == "error"


def test_get_bins_by_bank_known(db):
    """Existing issuer substring returns matches."""
    sample_issuer = ""
    for entries in db.COUNTRY_DATA.values():
        for entry in entries:
            if entry.get("issuer"):
                sample_issuer = entry["issuer"]
                break
        if sample_issuer:
            break
    res = db.get_bins_by_bank(sample_issuer[:4], limit=3)
    assert res["status"] == "SUCCESS"


@pytest.mark.asyncio
async def test_aget_bin_info_unknown(db):
    """Async invalid BIN lookup returns error."""
    res = await db.aget_bin_info("000000xyz")
    assert res["status"] == "error"


@pytest.mark.asyncio
async def test_aget_bin_info_known(db):
    """Async first known BIN lookup returns success."""
    sample_bin = next(iter(db.BIN_INDEX))
    res = await db.aget_bin_info(sample_bin)
    assert res["status"] == "SUCCESS"
    assert res["count"] == 1


@pytest.mark.asyncio
async def test_aget_bins_by_country_known(db):
    """Async known country returns at least one record."""
    sample_country = next(iter(db.COUNTRY_DATA))
    res = await db.aget_bins_by_country(sample_country, limit=2)
    assert res["status"] == "SUCCESS"
    assert res["count"] >= 1


@pytest.mark.asyncio
async def test_aget_bins_by_bank_known(db):
    """Async existing issuer substring returns matches."""
    sample_issuer = ""
    for entries in db.COUNTRY_DATA.values():
        for entry in entries:
            if entry.get("issuer"):
                sample_issuer = entry["issuer"]
                break
        if sample_issuer:
            break
    res = await db.aget_bins_by_bank(sample_issuer[:4], limit=3)
    assert res["status"] == "SUCCESS"
