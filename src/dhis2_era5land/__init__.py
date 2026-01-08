"""Import ERA5-Land climate data into DHIS2."""

try:
    from importlib.metadata import version as _get_version

    __version__ = _get_version("dhis2-era5land")
except Exception:
    __version__ = "unknown"
