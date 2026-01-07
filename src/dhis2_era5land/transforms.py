"""Value transformation functions for ERA5-Land data."""


def meters_to_millimeters(value: float) -> float:
    """Convert precipitation from meters to millimeters."""
    return value * 1000
