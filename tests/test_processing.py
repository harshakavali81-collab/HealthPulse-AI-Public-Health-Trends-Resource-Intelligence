import pytest
from healthpulse.processing.clean import normalize_record
from healthpulse.processing.validate import validate_records
from healthpulse.ingestion.public_dataset_loader import make_demo_data

valid = dict(indicator="life_expectancy", country="IND", year=2022, value=73, source="synthetic")

def test_normalize():
    r = normalize_record(valid)
    assert r["unit"] == "years" and r["country"] == "IND"

@pytest.mark.parametrize("changes", [
    {"indicator": "happiness"}, {"country": "India"}, {"year": 1200}, {"value": 600},
    {"value": float("nan")}, {"source": "private"}, {"value": float("inf")},
])
def test_rejected(changes):
    with pytest.raises(ValueError):
        normalize_record({**valid, **changes})

def test_validator():
    good, bad = validate_records([valid, {**valid, "value": -1}])
    assert len(good) == 1 and len(bad) == 1

def test_synthetic_reproducible():
    assert make_demo_data() == make_demo_data()
    assert len(make_demo_data()) == 18 * 13 * 5
    assert {x["source"] for x in make_demo_data()} == {"synthetic"}
