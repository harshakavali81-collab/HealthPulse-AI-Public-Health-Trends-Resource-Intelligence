"""WHO integration tests never require network or personal health data."""
import pytest
from healthpulse.ingestion.who_loader import fetch_who_indicator

ROW = {"SpatialDim":"IND","TimeDim":2020,"NumericValue":69.8,"Dim1":"BTSX"}

class DummyResponse:
    def __init__(self,payload):
        self.payload=payload
    def raise_for_status(self): pass
    def json(self): return self.payload

class DummyClient:
    def __init__(self,pages):
        self.pages=list(pages)
        self.calls=[]
    def get(self,url,params=None):
        self.calls.append((url,params))
        return DummyResponse(self.pages.pop(0))

def test_total_only_and_country_code():
    client=DummyClient([{"value":[ROW,
        {**ROW,"Dim1":"MLE","NumericValue":71.1},
        {**ROW,"Dim2":"MLE","NumericValue":70}]}])
    result=fetch_who_indicator("life_expectancy",client=client)
    assert len(result["records"])==1
    assert result["records"][0]["value"]==69.8
    assert result["rejected_count"]==0
    assert result["complete"] is True
    assert result["pages_fetched"]==1

def test_second_page_success():
    nxt="https://ghoapi.azureedge.net/api/WHOSIS_000001?$skip=1000"
    client=DummyClient([{"value":[ROW],"@odata.nextLink":nxt},
                        {"value":[{**ROW,"TimeDim":2021,"NumericValue":70.0}]}])
    result=fetch_who_indicator("life_expectancy",client=client,max_pages=2)
    assert len(result["records"])==2
    assert result["pages_fetched"]==2

def test_reject_cross_host_redirect_before_second_request():
    client=DummyClient([{"value":[ROW],"@odata.nextLink":"https://evil.example/api/WHOSIS_000001"}])
    with pytest.raises(ValueError, match="Untrusted"):
        fetch_who_indicator("life_expectancy",client=client)
    assert len(client.calls)==1

def test_reject_partial_paginated_import():
    client=DummyClient([{"value":[ROW],"@odata.nextLink":"https://ghoapi.azureedge.net/api/WHOSIS_000001?$skip=1000"}])
    with pytest.raises(ValueError,match="not fully retrieved"):
        fetch_who_indicator("life_expectancy",max_pages=1,client=client)

def test_reject_conflicting_duplicate_observations():
    client=DummyClient([{"value":[ROW,{**ROW,"NumericValue":70.1}]}])
    with pytest.raises(ValueError, match="Conflicting"):
        fetch_who_indicator("life_expectancy",client=client)

def test_reject_empty_compatible_result():
    client=DummyClient([{"value":[{**ROW,"Dim1":"MLE"}]}])
    with pytest.raises(ValueError,match="no compatible"):
        fetch_who_indicator("life_expectancy",client=client)

def test_country_filter_is_applied_and_record_source_is_who():
    client=DummyClient([{"value":[ROW,{**ROW,"SpatialDim":"USA"}]}])
    result=fetch_who_indicator("life_expectancy",client=client,country="IND")
    assert len(result["records"])==1
    assert result["records"][0]["source"]=="WHO"
    assert client.calls[0][1]["$filter"]=="SpatialDim eq 'IND'"

def test_invalid_country_filter():
    with pytest.raises(ValueError):
        fetch_who_indicator("life_expectancy",client=DummyClient([]),country="India")

def test_invalid_shape():
    with pytest.raises(ValueError,match="structure"):
        fetch_who_indicator("life_expectancy",client=DummyClient([{"items":[]}]))


def test_invalid_total_population_observation_fails_whole_who_batch():
    client=DummyClient([{"value":[ROW,{**ROW,"SpatialDim":"XX","NumericValue":70}]}])
    with pytest.raises(ValueError,match="invalid aggregate observations"):
        fetch_who_indicator("life_expectancy",client=client)


def test_total_and_non_total_records_are_never_mixed():
    client=DummyClient([{"value":[ROW,{**ROW,"Dim1":"FMLE","NumericValue":100}]}])
    data=fetch_who_indicator("life_expectancy",client=client)
    assert data["records"][0]["value"]==ROW["NumericValue"]
    assert len(data["records"])==1
