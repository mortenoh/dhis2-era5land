"""Value transformation functions for ERA5-Land data."""

from collections.abc import Callable
from enum import StrEnum
from typing import Any


class Transform(StrEnum):
    """Available value transforms."""

    METERS_TO_MILLIMETERS = "meters_to_millimeters"
    IDENTITY = "identity"


def meters_to_millimeters(value: float) -> float:
    """Convert precipitation from meters to millimeters."""
    return value * 1000


def identity(value: float) -> float:
    """Return value unchanged."""
    return value


# Map of transform names to functions
TRANSFORMS: dict[Transform, Callable[[Any], Any]] = {
    Transform.METERS_TO_MILLIMETERS: meters_to_millimeters,
    Transform.IDENTITY: identity,
}


def get_transform(name: Transform) -> Callable[[Any], Any]:
    """Get a transform function by name."""
    return TRANSFORMS[name]
