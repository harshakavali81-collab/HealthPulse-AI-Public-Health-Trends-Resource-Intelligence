import React, { useEffect, useMemo, useState } from 'react';
import { createRoot } from 'react-dom/client';
import { Activity, BarChart3, Bell, ChevronDown, CircleHelp, Database, Download, Globe2, HeartPulse, LayoutDashboard, Microscope, Search, ShieldCheck, TrendingUp, UsersRound, MapPinned, Layers, Menu, X, ArrowUpRight } from 'lucide-react';
import Overview from './pages/Overview.jsx';
import Indicators from './pages/Indicators.jsx';
import RegionalComparison from './pages/RegionalComparison.jsx';
import Trends from './pages/Trends.jsx';
import { api } from './api/client.js';
import './styles.css';

const nav = [{title:'Overview',icon:LayoutDashboard},{title:'Indicators',icon:BarChart3},{title:'Regional comparison',icon:MapPinned},{title:'Trends & forecast',icon:TrendingUp}];
const catalogue = [
  {id:'life_expectancy',name:'Life expectancy at birth',unit:'years'},
  {id:'immunization',name:'DTP3 immunization coverage',unit:'%'},
  {id:'physicians',name:'Physician density',unit:'per 1,000'},
  {id:'hospital_beds',name:'Hospital bed density',unit:'per 1,000'},
  {id:'under5_mortality',name:'Under-five mortality rate',unit:'per 1,000 live births'},
];
function App(){
  const [page,setPage]=useState('Overview');
  const [indicator,setIndicator]=useState('life_expectancy');
  const [source,setSource]=useState('synthetic');
  const [country,setCountry]=useState('IND');
  const [mobileNav,setMobileNav]=useState(false);
  const [allRecords,setAllRecords]=useState([]);
  const [loading,setLoading]=useState(true);
  const [error,setError]=useState('');
  const metadata = catalogue.find(i=>i.id===indicator);
  useEffect(()=>{
    let active=true; setLoading(true);setError('');
    api('/records',{source,indicator,limit:5000}).then(x=>{if(active){setAllRecords(x.records);setLoading(false)}})
      .catch(()=>{if(active){setError('API unavailable. Start the backend or use Docker Compose.');setAllRecords([]);setLoading(false)}});
    return ()=>{active=false};
  },[source,indicator]);
  const countries=useMemo(()=>Array.from(new Map(allRecords.map(r=>[r.country,r.country_name])).entries()).sort((a,b)=>a[1].localeCompare(b[1])),[allRecords]);
  useEffect(()=>{if(countries.length && !countries.some(([code])=>code===country))setCountry(countries[0][0])},[countries,country]);
  function exportCSV(){
    const columns=['country','country_name','region','year','indicator','value','unit','source'];
    const lines=[columns.join(','),...allRecords.map(row=>columns.map(k=>`"${String(row[k]??'').replace(/"/g,'""')}"`).join(','))];
    const blob=new Blob([lines.join('\n')],{type:'text/csv;charset=utf-8'});
    const url=URL.createObjectURL(blob);const a=document.createElement('a');a.href=url;a.download=`healthpulse-${indicator}-${source}.csv`;a.click();URL.revokeObjectURL(url);
  }
  const shared={indicator,source,country,records:allRecords,metadata,countries,loading};
  return <div className="app-shell">
    <aside className={`sidebar ${mobileNav?'visible':''}`}>
      <div className="brand"><div className="brand-mark"><HeartPulse size={23} strokeWidth={2.5}/></div><span>HealthPulse<span className="brand-ai">AI</span><small>PUBLIC HEALTH INTELLIGENCE</small></span></div>
      <div className="nav-label">WORKSPACE</div>
      <nav aria-label="Main navigation">{nav.map(({title,icon:Icon})=><button key={title} className={`nav-item ${page===title?'active':''}`} onClick={()=>{setPage(title);setMobileNav(false)}}><Icon size={18}/><span>{title}</span>{page===title&&<span className="active-dot"/>}</button>)}</nav>
      <div className="nav-label nav-label-extra">DATA & GOVERNANCE</div>
      <div className="nav-static"><Database size={17}/> Data provenance</div>
      <div className="nav-static"><ShieldCheck size={17}/> Quality monitoring</div>
      <div className="sidebar-bottom"><div className="tiny-signal"><span/> Demo environment</div><div className="sidebar-info"><strong>Built for transparency.</strong><p>Aggregate indicators only. No personal health records or individual predictions.</p></div><a href="https://www.who.int/data/gho/info/gho-odata-api" target="_blank" rel="noreferrer">Explore WHO GHO <ArrowUpRight size={14}/></a></div>
    </aside>
    {mobileNav&&<div className="nav-overlay" onClick={()=>setMobileNav(false)}/>}
    <div className="main-column">
      <header className="topbar"><button className="mobile-menu icon-button" onClick={()=>setMobileNav(!mobileNav)} aria-label="Toggle sidebar">{mobileNav?<X size={21}/>:<Menu size={21}/>}</button><div className="breadcrumbs">Workspace <span>/</span> <strong>{page}</strong></div><div className="topbar-right"><span className="source-pill"><span className="pulse-dot"/> {source==='synthetic'?'Synthetic demo data':'WHO GHO data'}</span><a className="top-icon" href="https://www.who.int/data/gho" target="_blank" rel="noreferrer" aria-label="WHO data"><CircleHelp size={19}/></a><span className="avatar">HP</span></div></header>
      <main className="workspace">
        <div className="heading-row"><div><div className="eyebrow"><Globe2 size={14}/> GLOBAL HEALTH OBSERVATORY</div><h1>{page==='Overview'?'Health at a glance':page}</h1><p className="subtitle">Explore public health indicators with meaningful context, transparent data and reproducible analytics.</p></div><button onClick={exportCSV} className="export-btn" disabled={!allRecords.length}><Download size={17}/> Export CSV</button></div>
        <div className="alert-banner"><ShieldCheck size={19}/><div><strong>{source==='synthetic'?'Demonstration dataset — not official health statistics':'WHO GHO dataset — definitions and coverage vary'}</strong><span>{source==='synthetic'?'All numbers shown are fabricated for software demonstration. Switch to WHO after an authorized ingestion.':'WHO data are historical aggregates; verify indicator metadata, disaggregation and reporting delays.'}</span></div></div>
        <section className="filter-panel"><div className="filter-control"><label>Indicator</label><select value={indicator} onChange={e=>setIndicator(e.target.value)}>{catalogue.map(i=><option key={i.id} value={i.id}>{i.name}</option>)}</select></div><div className="filter-control"><label>Data source</label><select value={source} onChange={e=>setSource(e.target.value)}><option value="synthetic">Synthetic demo</option><option value="WHO">WHO GHO (if synced)</option></select></div><div className="filter-control"><label>Country spotlight</label><select value={country} onChange={e=>setCountry(e.target.value)} disabled={!countries.length}>{countries.map(([code,name])=><option key={code} value={code}>{name}</option>)}</select></div></section>
        {error&&<div className="error-banner" role="alert">{error}</div>}
        {page==='Overview'&&<Overview {...shared}/>}
        {page==='Indicators'&&<Indicators {...shared}/>}
        {page==='Regional comparison'&&<RegionalComparison {...shared}/>}
        {page==='Trends & forecast'&&<Trends {...shared}/>}
        <footer><span>© 2026 HealthPulse AI • A portfolio demonstration</span><span>Source transparency · Non-clinical use · Reproducible methods</span></footer>
      </main>
    </div>
  </div>
}
createRoot(document.getElementById('root')).render(<App/>);
