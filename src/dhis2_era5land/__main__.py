"""Entry point for python -m dhis2_era5land."""

from dhis2_era5land.main import (
    client,
    data_element_id,
    end_date,
    import_era5_land_to_dhis2,
    org_unit_level,
    spatial_aggregation,
    start_date,
    temporal_aggregation,
    timezone_offset,
    value_col,
    value_processing,
    variable,
)

import_era5_land_to_dhis2(
    client,
    variable=variable,
    data_element_id=data_element_id,
    value_col=value_col,
    value_func=value_processing,
    temporal_aggregation=temporal_aggregation,
    spatial_aggregation=spatial_aggregation,
    start_date=start_date,
    end_date=end_date,
    timezone_offset=timezone_offset,
    org_unit_level=org_unit_level,
)
