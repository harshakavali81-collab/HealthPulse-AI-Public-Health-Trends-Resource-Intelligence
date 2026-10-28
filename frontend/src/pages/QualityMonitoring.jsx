import React,{useEffect,useMemo,useState} from 'react';
import {AlertCircle, CheckCircle2, Info, Database} from 'lucide-react';
import {api} from '../api/client.js';

export default function QualityMonitoring({source,indicator,records,metadata}){
  const [quality,setQuality]=useState(null),[coverage,setCoverage]=useState(null),[error,setError]=useState('');
  useEffect(()=>{let active=true;setQuality(null);setCoverage(null);setError('');
    Promise.all([api('/quality',{source}),api('/coverage',{source,indicator})])
      .then(([q,c])=>{if(active){setQuality(q);setCoverage(c)}})
      .catch(()=>{if(active)setError('Quality endpoints are temporarily unavailable.')});
    return()=>{active=false};
  },[source,indicator]);
  const countries=coverage?.countries||[];
  const gaps=countries.filter(r=>r.missing_years_within_span>0).length;
  return <>
    <div className="kpi-grid">
      <div className="kpi-card"><div className="kpi-top"><span>Stored observations</span><Database size={19}/></div><strong>{quality?.rows??'—'}</strong><div className="kpi-small">All indicators · {source}</div></div>
      <div className="kpi-card"><div className="kpi-top"><span>Duplicate keys</span></div><strong>{quality?.duplicate_keys??'—'}</strong><div className="kpi-small">Within source & year</div></div>
      <div className="kpi-card"><div className="kpi-top"><span>Missing numeric values</span></div><strong>{quality?.missing??'—'}</strong><div className="kpi-small">After validation</div></div>
      <div className="kpi-card"><div className="kpi-top"><span>Country series with gaps</span></div><strong>{coverage?gaps:'—'}</strong><div className="kpi-small">Within first–last available year</div></div>
    </div>
    {error&&<div className="error-banner" role="alert">{error}</div>}
    <section className="panel section-gap"><div className="panel-header"><div><h2>Year coverage audit</h2><p>{metadata.name} · {source} · gaps are measured only within each country's observed span</p></div><Info size={20}/></div>
      {countries.length?<div className="data-table-wrap"><table className="data-table"><thead><tr><th>Country</th><th>First year</th><th>Last year</th><th>Years observed</th><th>Internal gaps</th><th>Review</th></tr></thead><tbody>{countries.map(r=><tr key={r.country}><td>{r.country_name} ({r.country})</td><td>{r.first_year}</td><td>{r.last_year}</td><td>{r.observed_years}</td><td>{r.missing_years_within_span}</td><td>{r.missing_years_within_span?<span className="hp-status warn"><AlertCircle size={14}/> Check gaps</span>:<span className="hp-status"><CheckCircle2 size={14}/> No internal gaps</span>}</td></tr>)}</tbody></table></div>:<div className="empty-state">No country-year coverage available for the selected source.</div>}
      <p className="method-footer">Missing early or late years are not inferred. Zero database missing values does not guarantee completeness or source reliability.</p>
    </section>
    <section className="panel section-gap"><div className="panel-header"><div><h2>Source coverage by indicator</h2><p>Counts of countries with at least one observation</p></div></div>
      <div className="hp-text-block">{quality?.coverage?.length?quality.coverage.map(r=><p key={r.indicator}><strong>{r.indicator.replaceAll('_',' ')}</strong>: {r.countries} countries</p>):<p>No source records yet.</p>}</div>
    </section>
  </>;
}
