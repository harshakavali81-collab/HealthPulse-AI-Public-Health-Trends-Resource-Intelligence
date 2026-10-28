import React,{useMemo} from 'react';
import {Globe2, Info} from 'lucide-react';
import {RegionChart, CountryBars} from '../components/Charts.jsx';
export default function RegionalComparison({records,metadata}){
  const year=Math.max(0,...records.map(r=>r.year));
  const latest=records.filter(r=>r.year===year);
  const regions=useMemo(()=>Object.values(latest.reduce((acc,r)=>{(acc[r.region]??={region:r.region,total:0,n:0}).total+=r.value;acc[r.region].n++;return acc},{})).map(r=>({region:r.region,value:+(r.total/r.n).toFixed(2),count:r.n})).sort((a,b)=>b.value-a.value),[records]);
  return <><div className="panel"><div className="panel-header"><div><h2>Regional comparison</h2><p>Latest data year {year||'—'} · {metadata.unit} · country-average (unweighted)</p></div><span className="pill muted">{regions.length} groups</span></div>{regions.length?<RegionChart data={regions}/>:<div className="empty-state">No regional data available.</div>}</div><div className="panel section-gap"><div className="panel-header"><div><h2>Region detail</h2><p>Coverage should be examined before interpreting regional differences</p></div></div><div className="data-table-wrap"><table className="data-table"><thead><tr><th>Region</th><th>Country count</th><th>Country mean ({metadata.unit})</th><th>Coverage note</th></tr></thead><tbody>{regions.map(r=><tr key={r.region}><td>{r.region}</td><td>{r.count}</td><td><strong>{r.value}</strong></td><td>{r.count<3?'Small sample':'Unweighted mean'}</td></tr>)}</tbody></table></div><p className="method-footer"><Info size={15}/> These are unweighted comparisons of available countries, not WHO population-weighted regional estimates. WHO-imported observations without trusted region mappings display as “Unmapped”.</p></div></>
}
