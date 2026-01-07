"""Tests for value transforms."""

from dhis2_era5land.transforms import (
    Transform,
    get_transform,
    identity,
    kelvin_to_celsius,
    kelvin_to_fahrenheit,
    meters_to_centimeters,
    meters_to_millimeters,
)


def test_meters_to_millimeters() -> None:
    assert meters_to_millimeters(1.0) == 1000.0
    assert meters_to_millimeters(0.001) == 1.0


def test_meters_to_centimeters() -> None:
    assert meters_to_centimeters(1.0) == 100.0
    assert meters_to_centimeters(0.01) == 1.0


def test_kelvin_to_celsius() -> None:
    assert kelvin_to_celsius(273.15) == 0.0
    assert kelvin_to_celsius(373.15) == 100.0


def test_kelvin_to_fahrenheit() -> None:
    assert kelvin_to_fahrenheit(273.15) == 32.0
    assert kelvin_to_fahrenheit(373.15) == 212.0


def test_identity() -> None:
    assert identity(42.0) == 42.0
    assert identity(-10.5) == -10.5


def test_get_transform() -> None:
    assert get_transform(Transform.METERS_TO_MILLIMETERS) == meters_to_millimeters
    assert get_transform(Transform.KELVIN_TO_CELSIUS) == kelvin_to_celsius
    assert get_transform(Transform.IDENTITY) == identity
