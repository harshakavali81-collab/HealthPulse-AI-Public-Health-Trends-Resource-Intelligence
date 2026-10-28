"""Fully mocked World Bank API contracts: no live network in CI."""
import pytest
from healthpulse.ingestion.worldbank_loader import fetch_worldbank_indicator, WB_CODES

C={"id":"IND","name":"India","region":{"id":"SAS","value":"South Asia"}}
R={"indicator":{"id":"SP.DYN.LE00.IN"}, "countryiso3code":"IND","date":"2022",
   "value":70.5,"obs_status":""}

class Response:
    def __init__(self, payload): self.payload = payload
    def raise_for_status(self): return None
    def json(self): return self.payload

class Client:
    def __init__(self, metadata=None, data=None):
        self.metadata=metadata if metadata is not None else [{"page":1,"pages":1},[C]]
        self.data=data if data is not None else [{"page":1,"pages":1},[R]]
        self.calls=[]
    def get(self,url,params=None):
        self.calls.append((url,params))
        return Response(self.data if "/indicator/" in url else self.metadata)


def test_wdi_uses_distinct_provider_and_authoritative_region():
    x=fetch_worldbank_indicator("life_expectancy",countries=["IND"],client=Client())
    assert x["complete"] and x["observations"]==1 and x["provider"]=="World Bank WDI"
    r=x["records"][0]
    assert r["source"]=="WorldBank" and r["region"]=="South Asia"
    assert r["unit"]=="years" and r["country"]=="IND"
    assert "/SP.DYN.LE00.IN" in r["source_url"]


def test_correct_wdi_indicator_codes():
    assert WB_CODES["immunization"]=="SH.IMM.IDPT"
    assert WB_CODES["under5_mortality"]=="SH.DYN.MORT"
    assert WB_CODES["hospital_beds"]=="SH.MED.BEDS.ZS"
    assert WB_CODES["physicians"]=="SH.MED.PHYS.ZS"


def test_reject_invalid_country_list():
    with pytest.raises(ValueError, match="ISO3"):
        fetch_worldbank_indicator("life_expectancy",countries=["India"],client=Client())


def test_reject_api_unexpected_json():
    with pytest.raises(ValueError, match="documented"):
        fetch_worldbank_indicator("life_expectancy",countries=["IND"],client=Client(metadata={"broken":1}))


def test_reject_missing_country_metadata():
    with pytest.raises(ValueError, match="country metadata"):
        fetch_worldbank_indicator("life_expectancy",countries=["IND"],client=Client(metadata=[{"page":1,"pages":1},[]]))


def test_reject_partial_page_batch():
    bad=[{"page":1,"pages":10},[R]]
    with pytest.raises(ValueError, match="pagination"):
        fetch_worldbank_indicator("life_expectancy",countries=["IND"],max_pages=2,client=Client(data=bad))


def test_reject_wrong_indicator():
    wrong={**R,"indicator":{"id":"WRONG"}}
    with pytest.raises(ValueError, match="indicator"):
        fetch_worldbank_indicator("life_expectancy",countries=["IND"],client=Client(data=[{"page":1,"pages":1},[wrong]]))


def test_reject_conflicting_country_year_duplicates():
    conflict={**R,"value":99.9}
    with pytest.raises(ValueError, match="Conflicting"):
        fetch_worldbank_indicator("life_expectancy",countries=["IND"],client=Client(data=[{"page":1,"pages":1},[R,conflict]]))


def test_drops_missing_and_provider_forecasts():
    forecast={**R,"date":"2023","obs_status":"F","value":71}
    null={**R,"date":"2024","value":None}
    x=fetch_worldbank_indicator("life_expectancy",countries=["IND"],client=Client(data=[{"page":1,"pages":1},[R,forecast,null]]))
    assert x["observations"]==1


def test_fails_closed_for_all_bad_values():
    negative={**R,"value":200}
    with pytest.raises(ValueError,match="No valid"):
        fetch_worldbank_indicator("life_expectancy",countries=["IND"],client=Client(data=[{"page":1,"pages":1},[negative]]))


def test_fails_closed_for_mixed_valid_invalid_rows():
    negative={**R,"date":"2021","value":200}
    with pytest.raises(ValueError,match="invalid observations"):
        fetch_worldbank_indicator("life_expectancy",countries=["IND"],client=Client(data=[{"page":1,"pages":1},[R,negative]]))


def test_country_metadata_rejects_aggregate():
    wrong={"id":"IND","name":"Aggregated","region":{"id":"NA","value":"Aggregates"}}
    with pytest.raises(ValueError,match="country metadata"):
        fetch_worldbank_indicator("life_expectancy",countries=["IND"],client=Client(metadata=[{"page":1,"pages":1},[wrong]]))


def test_admin_endpoint_disabled_by_default(client):
    assert client.post("/api/admin/sync-worldbank/life_expectancy").status_code==503


def test_admin_endpoint_rejects_invalid_key(client, monkeypatch):
    monkeypatch.setenv("ADMIN_API_KEY","do-not-use-me")
    assert client.post("/api/admin/sync-worldbank/life_expectancy",headers={"X-Admin-Key":"bad"}).status_code==403


def test_admin_endpoint_rejects_unmapped_indicator(client, monkeypatch):
    monkeypatch.setenv("ADMIN_API_KEY","some-long-secret")
    assert client.post("/api/admin/sync-worldbank/no-such-indicator",headers={"X-Admin-Key":"some-long-secret"}).status_code==422
