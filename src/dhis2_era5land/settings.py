"""Configuration for ERA5-Land to DHIS2 import."""

from pydantic_settings import BaseSettings, SettingsConfigDict

from dhis2_era5land.transforms import Transform


class Settings(BaseSettings):
    """Settings for ERA5-Land to DHIS2 import.

    All settings can be overridden via environment variables with DHIS2_ prefix.
    For example: DHIS2_BASE_URL, DHIS2_USERNAME, DHIS2_PASSWORD, etc.
    """

    model_config = SettingsConfigDict(env_prefix="DHIS2_", env_file=".env")

    # DHIS2 connection
    base_url: str = "https://play.im.dhis2.org/stable-2-42-3-1"
    username: str = "admin"
    password: str = "district"

    # ERA5 variable config
    variable: str = "total_precipitation"
    data_element_id: str = "bMoGyfJoH9c"
    value_col: str = "tp"
    value_transform: Transform = Transform.METERS_TO_MILLIMETERS

    # Aggregation settings
    temporal_aggregation: str = "sum"
    spatial_aggregation: str = "mean"

    # Date range
    start_date: str = "2025-10-01"
    end_date: str = "2025-12-30"

    # Other settings
    timezone_offset: int = 0
    org_unit_level: int = 2


# Default settings instance
settings = Settings()
