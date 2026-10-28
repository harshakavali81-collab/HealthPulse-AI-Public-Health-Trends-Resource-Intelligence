"""Read-only WHO OData availability diagnostics: no persistence or credentials."""
from __future__ import annotations
import json
import httpx
from datetime import datetime,timezone

def main():
    base="https://ghoapi.azureedge.net/api"
    targets=[
      ("indicators",base+"/Indicator",{"$top":"1"}),
      ("life_expectancy_unfiltered",base+"/WHOSIS_000001",{"$top":"1"}),
      ("life_expectancy_filtered",base+"/WHOSIS_000001",{"$top":"1","$filter":"SpatialDim eq 'IND'"}),
      ("country_dimension",base+"/DIMENSION/COUNTRY/DimensionValues",{"$top":"1"}),
    ]
    results=[]
    with httpx.Client(timeout=18.0,follow_redirects=False,headers={"Accept":"application/json"}) as client:
        for name,url,params in targets:
            try:
                r=client.get(url,params=params)
                info={"route":name,"http_status":r.status_code,"content_type":r.headers.get("content-type",""),
                      "request_url":str(r.request.url),"bytes":len(r.content)}
                if r.status_code==200:
                    try:
                        data=r.json()
                        info["json_data"]=isinstance(data,dict)
                        info["records"]=len(data.get("value",[])) if isinstance(data,dict) else None
                    except ValueError:
                        info["json_data"]=False
                results.append(info)
            except httpx.RequestError as e:
                results.append({"route":name,"error":type(e).__name__})
    print(json.dumps({"checked_at":datetime.now(timezone.utc).isoformat(),"source":"WHO GHO official documented OData base","results":results},indent=2))
    if not any(x.get("http_status")==200 and x.get("json_data") for x in results):
        raise SystemExit("No WHO route returned an accessible 200 JSON result; live WHO ingestion remains unverified.")


if __name__=="__main__":
    main()
