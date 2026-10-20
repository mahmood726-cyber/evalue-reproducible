// HOST ONLY. Real-page capture in installed Microsoft Edge (never Chrome). No external requests allowed.
// Usage: node capture_figure.cjs < NUL   -> paper/figures/figure{1,2}.png + capture.json
const fs=require('node:fs'),path=require('node:path'),{pathToFileURL}=require('node:url');
const {chromium}=require('playwright-core');
const EDGE='C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
const FIGURES=[{figure:'figure1',id:'bcg-001-RR-FALSE'},{figure:'figure2',id:'normand1999-001-SMD'}];
const VIEWPORT={width:1200,height:900};
(async()=>{
  const root=__dirname, archive=path.join(root,'evalue-reproducible');
  const corpus=JSON.parse(fs.readFileSync(path.join(archive,'data/corpus.json'),'utf8'));
  const refCsv=fs.readFileSync(path.join(archive,'evidence/fresh/run-1-original-page/reference.csv'),'utf8').trim().split(/\r?\n/);
  const head=refCsv[0].replace(/"/g,'').split(',');
  const reference=Object.fromEntries(refCsv.slice(1).map(l=>{const v=l.split(',');const id=v[0].replace(/"/g,'');
    return [id,Object.fromEntries(head.slice(1).map((k,i)=>[k,v[i+1]===''?null:Number(v[i+1])]))];}));
  const out=path.join(root,'paper/figures');
  fs.mkdirSync(out,{recursive:true});
  for(const f of FIGURES) if(fs.existsSync(path.join(out,f.figure+'.png'))) throw Error('Preserve existing capture before rerun: '+f.figure);
  const browser=await chromium.launch({executablePath:EDGE,headless:true});
  const captures=[];
  try {
    for(const f of FIGURES) {
      const input=corpus.find(c=>c.id===f.id);
      if(!input) throw Error('Preregistered real-data case missing: '+f.id);
      const page=await browser.newPage({viewport:VIEWPORT,deviceScaleFactor:2,colorScheme:'light'});
      const blocked=[];
      await page.route(/^https?:/,route=>{blocked.push(route.request().url());return route.abort();});
      const errors=[];page.on('pageerror',e=>errors.push(e.message));
      const url=pathToFileURL(path.join(archive,'app-original/evalue/index.html')).href;
      await page.goto(url,{waitUntil:'load'});
      await page.locator('#measure').selectOption(input.measure);
      for(const id of ['point','lo','hi']) await page.locator('#'+id).fill(String(input[id]));
      await page.locator('#rare').setChecked(input.rare);
      await page.locator('#btn-run').click();
      const result=await page.evaluate(()=>window.__almLastEValue());
      if(!result||errors.length) throw Error(JSON.stringify({result,errors}));
      const ref=reference[f.id];
      const pairs={point:[result.point,ref.point],ci:[result.ci,ref.ci],rr_point:[result.rr.point,ref.rr_point],
        rr_lo:[result.rr.lo,ref.rr_lo],rr_hi:[result.rr.hi,ref.rr_hi]};
      for(const [k,[a,b]] of Object.entries(pairs))
        if(Math.abs(a-b)/Math.max(1,Math.abs(b))>1e-9) throw Error(`Browser result differs from EValue: ${f.id} ${k} ${a} vs ${b}`);
      const table=await page.locator('#tbody').innerText();
      const file=path.join(out,f.figure+'.png');
      await page.evaluate(()=>window.scrollTo(0,0));await page.waitForTimeout(200);
      await page.screenshot({path:file,fullPage:true});
      captures.push({figure:f.figure,input,result,evalue_reference:ref,displayed_table:table,
        interpretation:await page.locator('#interp').innerText(),url,blocked_requests:blocked,errors});
      await page.close();
    }
    fs.writeFileSync(path.join(out,'capture.json'),JSON.stringify({
      browser:'Microsoft Edge '+browser.version(),executable:EDGE,headless:true,viewport:VIEWPORT,deviceScaleFactor:2,
      driver:'playwright-core 1.59.1',command:'node capture_figure.cjs < NUL',captured_utc:new Date().toISOString(),
      captures,note:'Real archived page in Edge on metadat data; values asserted equal to fresh EValue 4.1.4 reference (1e-9).'
    },null,2)+'\n');
    console.log('Captured',captures.map(c=>c.figure).join(', '),'in Edge',browser.version());
  } finally {await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
