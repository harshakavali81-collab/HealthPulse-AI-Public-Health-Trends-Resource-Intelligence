import React, {useMemo} from 'react';
import {Database, ExternalLink, Info, ShieldCheck} from 'lucide-react';

export default function DataProvenance({records, source, indicator, metadata}) {
  const summary=useMemo(()=>{
    const years=records.map(r=>r.year);
    const countryCount=new Set(records.map(r=>r.country)).size;
    const sources=new Set(records.map(r=>r.source));
    return {countries:countryCount, first:years.length?Math.min(...years):null, last:years.length?Math.max(...years):null, sources:[...sources]};
  },[records]);
  const sample=records.slice(-15).reverse();
  return <>
    <div className="kpi-grid">
      <div className="kpi-card"><div className="kpi-top"><span>Selected source</span><Database size={20}/></div><strong style={{fontSize:24}}>{source==='synthetic'?'Synthetic':source==='WorldBank'?'World Bank WDI':'WHO GHO'}</strong><div className="kpi-small">Never pooled across sources</div></div>
      <div className="kpi-card"><div className="kpi-top"><span>Countries</span></div><strong>{summary.countries}</strong><div className="kpi-small">Observed for this indicator</div></div>
      <div className="kpi-card"><div className="kpi-top"><span>Year range</span></div><strong style={{fontSize:23}}>{summary.first==null?'—':summary.first+'–'+summary.last}</strong><div className="kpi-small">Available observations only</div></div>
      <div className="kpi-card"><div className="kpi-top"><span>Aggregate rows</span></div><strong>{records.length}</strong><div className="kpi-small">No individual patient records</div></div>
    </div>
    <section className="panel section-gap"><div className="panel-header"><div><h2>Source provenance</h2><p>Selected indicator: {metadata.name} ({metadata.unit})</p></div><ShieldCheck size={21}/></div>
      <div className="hp-text-block"><p><strong>{source==='synthetic'?'Fabricated demonstration observations':source==='WorldBank'?'Imported World Bank World Development Indicators':'Imported WHO Global Health Observatory aggregates'}</strong></p>
        <p>{source==='synthetic'?'All displayed values were generated with a fixed random seed for teaching, visual demonstrations and automated tests. They do not represent official population estimates.':source==='WorldBank'?'These public aggregates come from World Bank WDI. They are not directly imported from the WHO GHO API. Check each series methodology, coverage, revisions and publishing institution.':'Values are returned by the optional server-side WHO GHO OData importer. Always check official indicator metadata, revisions, dimensions and reporting periods before using them.'}</p>
        <p>Indicator definitions, source URLs and import timestamps are retained in SQLite. The import is admin-controlled; the website cannot submit data.</p>
        {source==='WorldBank'&&<p><a href="https://datahelpdesk.worldbank.org/knowledgebase/articles/889392" target="_blank" rel="noreferrer">World Bank Indicators API guidance <ExternalLink size={13}/></a></p>}
        {source==='WHO'&&<p><a href="https://www.who.int/data/gho/info/gho-odata-api" target="_blank" rel="noreferrer">WHO GHO API guidance <ExternalLink size={13}/></a></p>}
      </div>
    </section>
    <section className="panel section-gap"><div className="panel-header"><div><h2>Observation lineage</h2><p>Sample of up to 15 stored aggregate records</p></div></div>
      {sample.length?<div className="data-table-wrap"><table className="data-table"><thead><tr><th>Country</th><th>Year</th><th>Value</th><th>Data source</th><th>Imported at</th><th>Reference</th></tr></thead><tbody>{sample.map((r,i)=><tr key={r.country+'-'+r.year+'-'+i}><td>{r.country_name}</td><td>{r.year}</td><td>{r.value} {r.unit}</td><td>{r.source}</td><td>{r.ingested_at||'—'}</td><td>{r.source==='WHO'&&r.source_url?.startsWith('https://ghoapi.azureedge.net/api/')?<a target="_blank" rel="noopener noreferrer" href={r.source_url}>WHO GHO ↗</a> :r.source==='WorldBank'&&r.source_url?.startsWith('https://api.worldbank.org/v2/')?<a target="_blank" rel="noopener noreferrer" href={r.source_url}>World Bank WDI ↗</a>:'Synthetic'}</td></tr>)}</tbody></table></div>:<div className="empty-state">No observations for this indicator and source.</div>}
      <p className="method-footer"><Info size={15}/> Sample only. Export CSV for the selected indicator or query the API for source and lineage fields.</p>
    </section>
  </>;
}
