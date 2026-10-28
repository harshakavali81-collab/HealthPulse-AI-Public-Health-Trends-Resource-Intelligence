import pytest

def test_health(client):
    assert client.get('/api/health').json()['status']=='ok'

def test_indicators(client):
    assert len(client.get('/api/indicators').json())==5

def test_summary(client):
    d=client.get('/api/summary').json()
    assert d['observations']==234 and d['source']=='synthetic'

def test_records(client):
    d=client.get('/api/records',params={'indicator':'life_expectancy','country':'IND'}).json()
    assert d['total']==13 and d['records'][0]['source']=='synthetic'

def test_trends(client):
    d=client.get('/api/trends',params={'country':'IND'}).json()
    assert len(d['data'])==13

def test_regional(client):
    d=client.get('/api/regional-comparison').json()
    assert len(d['regions'])==5 and 'unweighted' in d['aggregation']

def test_forecast(client):
    d=client.get('/api/forecast').json()
    assert d['status']=='ok' and len(d['forecast'])==3

def test_anomalies(client):
    assert isinstance(client.get('/api/anomalies').json()['flags'],list)

def test_clusters(client):
    assert len(client.get('/api/clusters').json()['clusters'])==18

def test_quality(client):
    assert client.get('/api/quality').json()['duplicate_keys']==0

def test_resources(client):
    d=client.get('/api/resources').json()
    assert 'Synthetic' in d['note'] and len(d['countries'])==12

def test_no_admin_without_key(client):
    assert client.post('/api/admin/sync-who/life_expectancy').status_code==503

def test_admin_denied_with_wrong_key(client,monkeypatch):
    monkeypatch.setenv('ADMIN_API_KEY','strong-secret')
    assert client.post('/api/admin/sync-who/life_expectancy',headers={'X-Admin-Key':'wrong'}).status_code==403

def test_invalid_indicator(client):
    assert client.get('/api/summary',params={'indicator':'doesnotexist'}).status_code==422

def test_invalid_source(client):
    assert client.get('/api/summary',params={'source':'patient_data'}).status_code==422

def test_invalid_horizon(client):
    assert client.get('/api/forecast',params={'horizon':100}).status_code==422

def test_empty_who(client):
    assert client.get('/api/records',params={'source':'WHO'}).json()['total']==0
