"""SmartBinDB core implementation with sync and async support.

This module provides the SmartBinDB class for high-performance offline BIN
lookups. All public methods are available in both synchronous and asynchronous
variants, allowing seamless integration with any application architecture.

The database loads once at instantiation and maintains in-memory indices for
O(1) lookups across all query types.
"""

import os
import time
import pickle
import logging
from functools import lru_cache
from typing import Optional, Dict, Any

import pycountry
import pycountry_convert

logger = logging.getLogger(__name__)

API_OWNER = "@ISmartCoder"
API_CHANNEL = "@TheSmartDev"


class SmartBinDB:
    """High-performance offline BIN lookup database with sync/async support.

    Loads bundled BIN database into memory with fast in-memory indices. Supports
    both synchronous and asynchronous method calls for flexible integration.

    Attributes:
        COUNTRY_JSON_DIR (str): Directory containing bundled binary database.
        BINARY_DB (str): Absolute path to binary database file.
        BIN_INDEX (dict): O(1) lookup mapping from BIN string to entry tuples.
        COUNTRY_DATA (dict): Mapping from country code to BIN entry lists.
        START_TIME (float): Process start time in epoch seconds.

    Example:
        .. code-block:: python

            from smartbindb import SmartBinDB

            db = SmartBinDB()

            result = db.get_bin_info("457173")
            print(result)

            result_async = await db.aget_bin_info("457173")
            print(result_async)
    """

    def __init__(self) -> None:
        """Initialize and load bundled BIN database into memory.

        Reads the pickle file once at construction. Reuse the same instance
        across requests in long-running processes to avoid reload overhead.
        """
        self.COUNTRY_JSON_DIR = os.path.join(os.path.dirname(__file__), "data")
        self.BINARY_DB = os.path.join(self.COUNTRY_JSON_DIR, "smartbin.db")
        self.BIN_INDEX: Dict[str, Any] = {}
        self.COUNTRY_DATA: Dict[str, Any] = {}
        self.START_TIME = time.time()
        self.load_data()

    def load_data(self) -> None:
        """Load bundled binary database into memory.

        If the database file is missing or unreadable, the error is logged
        and in-memory structures remain empty. Public calls will attempt
        reload before returning an error envelope.

        Example:
            .. code-block:: python

                db = SmartBinDB()
                db.COUNTRY_DATA.clear()
                db.load_data()
                assert db.COUNTRY_DATA
        """
        if not os.path.exists(self.BINARY_DB):
            logger.error("Binary DB not found: %s", self.BINARY_DB)
            return
        try:
            with open(self.BINARY_DB, "rb") as f:
                data = pickle.load(f)
            self.COUNTRY_DATA = data.get("country_data", {})
            self.BIN_INDEX = data.get("bin_index", {})
            logger.info(
                "Loaded SmartBinDB: %d countries, %d BINs",
                len(self.COUNTRY_DATA),
                len(self.BIN_INDEX),
            )
        except Exception as exc:
            logger.exception("Error loading binary DB: %s", exc)

    @lru_cache(maxsize=256)
    def get_country_info(self, country_code: str) -> Dict[str, str]:
        """Return ISO country metadata for alpha-2 country code.

        Wrapped with LRU cache (256 max). Repeated calls for same country
        are essentially free after first lookup.

        Args:
            country_code: 2-letter country code. Special values "US1" and
                "US2" are normalized to "US".

        Returns:
            Dictionary with A2, A3, N3, Name, and Cont keys. Unknown codes
            return empty strings for all fields except A2.

        Example:
            .. code-block:: python

                db = SmartBinDB()
                print(db.get_country_info("BD"))
                print(db.get_country_info("ZZ"))
        """
        country_code = country_code.upper()
        lookup_code = "US" if country_code in ("US1", "US2") else country_code
        country = pycountry.countries.get(alpha_2=lookup_code)
        if not country:
            return {"A2": country_code, "A3": "", "N3": "", "Name": "", "Cont": ""}
        try:
            continent_code = pycountry_convert.country_alpha2_to_continent_code(
                country.alpha_2
            )
            continent = pycountry_convert.convert_continent_code_to_continent_name(
                continent_code
            )
        except Exception as exc:
            logger.debug("Continent lookup failed for %s: %s", country_code, exc)
            continent = ""
        return {
            "A2": country.alpha_2,
            "A3": country.alpha_3,
            "N3": country.numeric,
            "Name": country.name,
            "Cont": continent,
        }

    def format_entry(self, entry: Dict[str, Any], country_code: str) -> Dict[str, Any]:
        """Normalize raw BIN record into public response schema.

        Raw entries from pickle are partially typed with possible missing fields.
        This produces the stable public shape documented in response schema.

        Args:
            entry: Raw BIN entry from database. May have bin, brand, category,
                type, issuer, phone, website, country_code_alpha3 keys.
            country_code: Country code for entry. Passed to get_country_info.

        Returns:
            Normalized BIN record with complete response schema.

        Example:
            .. code-block:: python

                db = SmartBinDB()
                raw = {"bin": "457173", "brand": "VISA", "type": "credit"}
                print(db.format_entry(raw, "BD"))
        """
        country_info = self.get_country_info(country_code)
        return {
            "bin": entry.get("bin", ""),
            "brand": entry.get("brand", ""),
            "category": entry.get("category", ""),
            "CardTier": f"{entry.get('category', '')} {entry.get('brand', '')}".strip(),
            "country_code": country_code,
            "Type": entry.get("type", ""),
            "country_code_alpha3": entry.get("country_code_alpha3", ""),
            "Country": country_info,
            "issuer": entry.get("issuer", ""),
            "phone": entry.get("phone", ""),
            "type": entry.get("type", ""),
            "website": entry.get("website", ""),
        }

    def _error(self, message: str) -> Dict[str, Any]:
        """Build uniform error response payload."""
        return {
            "status": "error",
            "message": message,
            "api_owner": API_OWNER,
            "api_channel": API_CHANNEL,
        }

    def _success(self, data: list, filtered_by: str) -> Dict[str, Any]:
        """Build uniform success response payload."""
        return {
            "status": "SUCCESS",
            "data": data,
            "count": len(data),
            "filtered_by": filtered_by,
            "api_owner": API_OWNER,
            "api_channel": API_CHANNEL,
            "Luhn": True,
        }

    def get_bins_by_bank(
        self, bank: str, limit: Optional[int] = None
    ) -> Dict[str, Any]:
        """Return BIN records from banks matching substring (sync).

        Case-insensitive substring match against issuer field across all
        country buckets. Scan short-circuits when limit is reached.

        Args:
            bank: Case-insensitive issuer substring. "chase", "Chase", and
                "CHASE BANK" all match same records.
            limit: Optional cap on returned records. Reduces CPU work.

        Returns:
            Standard response. filtered_by set to "bank" on success.

        Example:
            .. code-block:: python

                db = SmartBinDB()
                result = db.get_bins_by_bank("Chase", limit=5)
                for row in result["data"]:
                    print(row["bin"], row["issuer"])
        """
        if not self.COUNTRY_DATA:
            self.load_data()
            if not self.COUNTRY_DATA:
                return self._error(
                    f"Binary database not found or empty: {self.BINARY_DB}"
                )
        matching_bins = []
        needle = bank.lower()
        for country_code, data in self.COUNTRY_DATA.items():
            for entry in data:
                issuer = entry.get("issuer", "")
                if issuer and needle in issuer.lower():
                    matching_bins.append(self.format_entry(entry, country_code))
                    if limit and len(matching_bins) >= limit:
                        break
            if limit and len(matching_bins) >= limit:
                break
        if not matching_bins:
            return self._error(f"No matches found for bank: {bank}")
        return self._success(matching_bins, "bank")

    def get_bins_by_country(
        self, country: str, limit: Optional[int] = None
    ) -> Dict[str, Any]:
        """Return BIN records for country code (sync).

        Pseudo country "US" aggregates US, US1, US2 regional buckets and
        caps at 8000 records per call to keep payloads bounded.

        Args:
            country: Alpha-2 country code (case-insensitive).
            limit: Optional cap on returned records.

        Returns:
            Standard response. filtered_by set to "country" on success.

        Example:
            .. code-block:: python

                db = SmartBinDB()
                result = db.get_bins_by_country("BD", limit=20)
                print(result["count"])
        """
        if not self.COUNTRY_DATA:
            self.load_data()
            if not self.COUNTRY_DATA:
                return self._error(
                    f"Binary database not found or empty: {self.BINARY_DB}"
                )
        country = country.upper()
        if country == "US":
            matching_bins = []
            for code in ("US", "US1", "US2"):
                if code in self.COUNTRY_DATA:
                    for entry in self.COUNTRY_DATA[code]:
                        matching_bins.append(self.format_entry(entry, code))
                        if limit and len(matching_bins) >= limit:
                            break
                if limit and len(matching_bins) >= limit:
                    break
            if not matching_bins:
                return self._error("No data found for country code: US")
            if limit is None:
                limit = 1000
            if limit > 8000:
                return self._error("Maximum limit allowed for US is 8000")
            return self._success(matching_bins[:limit], "country")
        if country not in self.COUNTRY_DATA:
            return self._error(f"No data found for country code: {country}")
        data = []
        for entry in self.COUNTRY_DATA[country]:
            data.append(self.format_entry(entry, country))
            if limit and len(data) >= limit:
                break
        return self._success(data, "country")

    def get_bin_info(self, bin: str) -> Dict[str, Any]:
        """Look up single BIN record by exact match (sync).

        Hot path with single BIN_INDEX[key] access. Argument converted to
        string and whitespace stripped before lookup.

        Args:
            bin: BIN to lookup, typically first 6-8 card digits. Whitespace
                trimmed automatically.

        Returns:
            Standard response with single entry on success. Error envelope
            on miss with message echoing original query.

        Example:
            .. code-block:: python

                db = SmartBinDB()
                result = db.get_bin_info("457173")
                if result["status"] == "SUCCESS":
                    row = result["data"][0]
                    print(row["brand"], row["issuer"], row["Country"]["Name"])
        """
        if not self.BIN_INDEX:
            self.load_data()
            if not self.BIN_INDEX:
                return self._error(
                    f"Binary database not found or empty: {self.BINARY_DB}"
                )
        key = str(bin).strip()
        if key in self.BIN_INDEX:
            country_code, entry = self.BIN_INDEX[key]
            return self._success([self.format_entry(entry, country_code)], "bin")
        return self._error(f"No matches found for BIN: {bin}")

    async def aget_bins_by_bank(
        self, bank: str, limit: Optional[int] = None
    ) -> Dict[str, Any]:
        """Return BIN records from banks matching substring (async).

        Async wrapper around synchronous get_bins_by_bank.

        Args:
            bank: Case-insensitive issuer substring.
            limit: Optional cap on returned records.

        Returns:
            Standard response. filtered_by set to "bank" on success.
        """
        return self.get_bins_by_bank(bank, limit)

    async def aget_bins_by_country(
        self, country: str, limit: Optional[int] = None
    ) -> Dict[str, Any]:
        """Return BIN records for country code (async).

        Async wrapper around synchronous get_bins_by_country.

        Args:
            country: Alpha-2 country code (case-insensitive).
            limit: Optional cap on returned records.

        Returns:
            Standard response. filtered_by set to "country" on success.
        """
        return self.get_bins_by_country(country, limit)

    async def aget_bin_info(self, bin: str) -> Dict[str, Any]:
        """Look up single BIN record by exact match (async).

        Async wrapper around synchronous get_bin_info.

        Args:
            bin: BIN to lookup, typically first 6-8 card digits.

        Returns:
            Standard response with single entry on success.
        """
        return self.get_bin_info(bin)
