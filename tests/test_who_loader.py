from healthpulse.ingestion.who_loader import fetch_who_indicator
class DummyResponse:
    def raise_for_status(self): pass
    def json(self):
        return {"value": [
            {"SpatialDim":"IND","TimeDim":2020,"NumericValue":69.8,"Dim1":"BTSX"},
            {"SpatialDim":"IND","TimeDim":2020,"NumericValue":70.1,"Dim1":"MLE"},
            {"SpatialDim":"XX","TimeDim":2020,"NumericValue":70,"Dim1":"BTSX"}
        ]}
class DummyClient:
    def get(self,url,params=None):
        assert 'WHOSIS_000001' in url
        return DummyResponse()

def test_total_only_and_country_code():
    r=fetch_who_indicator('life_expectancy',client=DummyClient())
    assert len(r['records'])==1
    assert r['records'][0]['value']==69.8
    assert r['rejected_count']==1
