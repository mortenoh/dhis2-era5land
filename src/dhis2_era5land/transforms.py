"""Value transformation functions for ERA5-Land data."""

from collections.abc import Callable
from enum import StrEnum
from typing import Any


class Transform(StrEnum):
    """Available value transforms."""

    METERS_TO_MILLIMETERS = "meters_to_millimeters"
    METERS_TO_CENTIMETERS = "meters_to_centimeters"
    KELVIN_TO_CELSIUS = "kelvin_to_celsius"
    KELVIN_TO_FAHRENHEIT = "kelvin_to_fahrenheit"
    IDENTITY = "identity"


def meters_to_millimeters(value: float) -> float:
    """Convert precipitation from meters to millimeters."""
    return value * 1000


def meters_to_centimeters(value: float) -> float:
    """Convert from meters to centimeters."""
    return value * 100


def kelvin_to_celsius(value: float) -> float:
    """Convert temperature from Kelvin to Celsius."""
    return value - 273.15


def kelvin_to_fahrenheit(value: float) -> float:
    """Convert temperature from Kelvin to Fahrenheit."""
    return (value - 273.15) * 9 / 5 + 32


def identity(value: float) -> float:
    """Return value unchanged."""
    return value


# Map of transform names to functions
TRANSFORMS: dict[Transform, Callable[[Any], Any]] = {
    Transform.METERS_TO_MILLIMETERS: meters_to_millimeters,
    Transform.METERS_TO_CENTIMETERS: meters_to_centimeters,
    Transform.KELVIN_TO_CELSIUS: kelvin_to_celsius,
    Transform.KELVIN_TO_FAHRENHEIT: kelvin_to_fahrenheit,
    Transform.IDENTITY: identity,
}


def get_transform(name: Transform) -> Callable[[Any], Any]:
    """Get a transform function by name."""
    return TRANSFORMS[name]
