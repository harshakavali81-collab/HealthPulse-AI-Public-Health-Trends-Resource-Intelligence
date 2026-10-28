import React,{useEffect,useState} from 'react';
import {Bed, Info, ShieldCheck} from 'lucide-react';
import {api} from '../api/client.js';

export default function ResourceContext({source}){
  const [rows,setRows]=useState([]),[unit,setUnit]=useState('beds per 1,000'),[note,setNote]=useState(''),[error,setError]=useState('');
  useEffect(()=>{let active=true;setRows([]);setError('');
    api('/resources',{source}).then(x=>{if(active){setRows(x.countries||[]);setUnit(x.unit||'beds per 1,000');setNote(x.note||'')}}).catch(()=>{if(active)setError('Resource context is unavailable.')});
    return()=>{active=false};
  },[source]);
  const max=Math.max(1,...rows.map(r=>r.value));
  return <>
    <div className="alert-banner"><ShieldCheck size={20}/><div><strong>Context only — not a resource-gap classifier</strong><span>Bed density by itself cannot establish shortages, capacity, service quality or allocation priorities. Synthetic, WHO GHO and World Bank WDI sources must never be conflated.</span></div></div>
    {error&&<div className="error-banner" role="alert">{error}</div>}
    <section className="panel"><div className="panel-header"><div><h2>Hospital-bed density comparison</h2><p>Selected source: {source==='synthetic'?'fabricated demo':source==='WorldBank'?'World Bank WDI':'WHO GHO'} · {unit} · latest observation per country</p></div><Bed size={21}/></div>
      {rows.length?<div className="hp-resource-list">{rows.map(r=><div className="hp-resource-row" key={r.country}><div><strong>{r.country_name}</strong><small>{r.country} · {r.year}</small></div><div className="hp-resource-track"><span style={{width:(100*r.value/max).toFixed(1)+'%'}} /></div><b>{r.value}</b></div>)}</div>:<div className="empty-state">No hospital-bed observations for this source. The example dataset does not imply any actual health-system capacity.</div>}
      <p className="method-footer"><Info size={15}/> {note||'These examples do not quantify healthcare supply or unmet medical need.'}</p>
    </section>
    <section className="panel section-gap"><div className="hp-text-block"><h2>How to interpret</h2><p>These are separate annual country observations. The list is ordered by observed density, not by healthcare effectiveness, inequity or need. Without population denominators, demand, facility distribution, staffing and validated country metadata, automated resource recommendations would be misleading.</p><p>For real policy work, validate the source indicator definition and consult the public-health experts responsible for the geography.</p></div></section>
  </>;
}
