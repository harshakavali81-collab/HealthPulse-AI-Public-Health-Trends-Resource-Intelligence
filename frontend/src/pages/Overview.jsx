import React, {useMemo,useState} from 'react';
import {Activity, ArrowDownRight, ArrowUpRight, Globe2, HeartPulse, Layers, ShieldCheck, TrendingUp, UsersRound, Info, ArrowRight} from 'lucide-react';
import {TrendChart, RegionChart, CountryBars} from '../components/Charts.jsx';
const fmt=(v,unit)=>v==null?'—':new Intl.NumberFormat('en-US',{maximumFractionDigits:1}).format(v)+(unit==='%'?'%':'');
export default function Overview({indicator,source,country,records,metadata,loading}) {
  const latest=useMemo(()=>Math.max(...records.map(r=>r.year),0),[records]);
  const last=useMemo(()=>records.filter(r=>r.year===latest),[records,latest]);
  const countries=new Set(records.map(r=>r.country)).size;
  const avg=last.length?last.reduce((a,r)=>a+r.value,0)/last.length:null;
  const prev=records.filter(r=>r.year===latest-1);
  const prevAvg=prev.length?prev.reduce((a,r)=>a+r.value,0)/prev.length:null;
  const delta=avg!=null&&prevAvg!=null?avg-prevAvg:null;
  const annual=useMemo(()=>Object.values(records.reduce((m,r)=>{(m[r.year]??={year:r.year,total:0,n:0}).total+=r.value;m[r.year].n++;return m},{})).map(r=>({year:r.year,value:+(r.total/r.n).toFixed(2)})).sort((a,b)=>a.year-b.year),[records]);
  const regional=useMemo(()=>Object.values(last.reduce((m,r)=>{(m[r.region]??={region:r.region,total:0,n:0}).total+=r.value;m[r.region].n++;return m},{})).map(r=>({...r,value:+(r.total/r.n).toFixed(2)})).sort((a,b)=>b.value-a.value),[last]);
  const featured=useMemo(()=>last.slice().sort((a,b)=>b.value-a.value).slice(0,7).map(r=>({country:r.country,value:r.value})),[last]);
  const spot=last.find(r=>r.country===country);
  return <>
    <div className="kpi-grid">
      <div className="kpi-card"><div className="kpi-top"><span>Latest country mean</span><span className="kpi-icon mint"><Activity size={19}/></span></div><strong>{fmt(avg,metadata.unit)}</strong><div className="kpi-small">{metadata.unit} <span className="tiny-divider">·</span> {latest||'No data'}</div><div className="kpi-foot"><span className={`delta ${delta!=null&&delta>=0?'positive':'negative'}`}>{delta==null?'—':delta>=0?<ArrowUpRight size={13}/>:<ArrowDownRight size={13}/>} {delta==null?'No comparison':Math.abs(delta).toFixed(2)+' vs prior year'}</span></div></div>
      <div className="kpi-card"><div className="kpi-top"><span>Countries covered</span><span className="kpi-icon blue"><Globe2 size={19}/></span></div><strong>{countries}</strong><div className="kpi-small">Distinct countries in dataset</div><div className="kpi-foot"><span className="subtle-tag">Coverage view</span></div></div>
      <div className="kpi-card"><div className="kpi-top"><span>Data observations</span><span className="kpi-icon purple"><Layers size={19}/></span></div><strong>{records.length.toLocaleString()}</strong><div className="kpi-small">Validated aggregate records</div><div className="kpi-foot"><span className="subtle-tag">{records.length?'Available':'Not synced'}</span></div></div>
      <div className="kpi-card"><div className="kpi-top"><span>Country spotlight</span><span className="kpi-icon orange"><HeartPulse size={19}/></span></div><strong>{spot?fmt(spot.value,metadata.unit):'—'}</strong><div className="kpi-small">{spot?.country_name||'Select a country'} · {latest||'—'}</div><div className="kpi-foot"><span className="subtle-tag">{metadata.unit}</span></div></div>
    </div>
    <div className="dash-grid"><section className="panel wide"><div className="panel-header"><div><h2>Indicator trends <span className="soft-label">ANNUAL</span></h2><p>Unweighted average across available countries</p></div><span className="legend"><i/> Time series</span></div>{annual.length?<TrendChart data={annual}/>:<Empty/>}<div className="panel-bottom"><span><Info size={14}/> Mean of countries, not population weighted</span><span>{annual.length?`${annual[0].year} – ${annual.at(-1).year}`:'No data'}</span></div></section>
    <section className="panel"><div className="panel-header"><div><h2>Regional snapshot</h2><p>Latest reporting year · {metadata.unit}</p></div></div>{regional.length?<RegionChart data={regional}/>:<Empty/>}<div className="panel-bottom"><span>Region labels reflect dataset mappings</span></div></section></div>
    <div className="dash-grid second-grid"><section className="panel wide"><div className="panel-header"><div><h2>Country comparison</h2><p>Higher values are not always better — interpret by indicator</p></div></div>{featured.length?<CountryBars data={featured}/>:<Empty/>}</section><section className="panel insight-card"><div className="insight-icon"><ShieldCheck size={22}/></div><h2>Data with context</h2><p>HealthPulse separates demo data from WHO observations, tracks provenance and flags limited coverage before trends are interpreted.</p><ul><li><span/> Indicator-specific units and definitions</li><li><span/> Sequential holdout forecasting</li><li><span/> Robust change-point anomaly flags</li></ul><div className="insight-note">Not a clinical decision-support or resource-allocation system.</div></section></div>
  </>
}
function Empty(){return <div className="empty-state">No records for this source. Configure the backend and authorized WHO sync to populate official datasets.</div>}
