// Execute every classic script from the archived page, in page order.
// The DOM is a test double; this is not browser or screenshot evidence.
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const crypto = require('node:crypto');
const [pageArg, casesArg, outputArg] = process.argv.slice(2);
if (!outputArg) throw Error('Usage: node replay.cjs PAGE CASES_JSON OUTPUT_JSON');
const page = path.resolve(pageArg);
const html = fs.readFileSync(page, 'utf8');
const els = new Map();
function element(id='') {
  return {id, value:'', checked:false, validity:{badInput:false}, innerHTML:'', textContent:'',
    dataset:{}, style:{}, listeners:{}, children:[],
    addEventListener(event,fn) {(this.listeners[event]??=[]).push(fn);},
    replaceChildren() {this.innerHTML='';this.children=[];},
    setAttribute(){}, closest(){return null;},
    appendChild(e){this.children.push(e);e.parentNode=this;},
    insertBefore(){}, parentNode:{insertBefore(){}}
  };
}
for (const match of html.matchAll(/<[^>]+\bid="([^"]+)"[^>]*>/g)) {
  const e=element(match[1]);
  e.value=match[0].match(/\bvalue="([^"]*)"/)?.[1]??'';
  els.set(e.id,e);
}
els.get('measure').value='RR';
const domEvents={};
const document={readyState:'loading',
  getElementById(id) {if(!els.has(id)) throw Error('Unknown DOM id '+id);return els.get(id);},
  querySelectorAll(selector){if(selector!=='.footer-note') throw Error('Unknown selector '+selector);return [];},
  createElement:element, addEventListener(event,fn){(domEvents[event]??=[]).push(fn);}
};
const ctx={document,console};
ctx.window=ctx;ctx.globalThis=ctx;
vm.createContext(ctx);
const scripts=[];
for (const [index,match] of [...html.matchAll(/<script\b([^>]*)>([\s\S]*?)<\/script>/gi)].entries()) {
  const src=match[1].match(/\bsrc="([^"]+)"/i)?.[1];
  if(src && /^(https?:|\/\/)/.test(src)) throw Error('Remote script refused');
  const filename=src?path.resolve(path.dirname(page),src):`${page}#inline-${index}`;
  const code=src?fs.readFileSync(filename,'utf8'):match[2];
  scripts.push({file:src??`inline-${index}`,sha256:crypto.createHash('sha256').update(code).digest('hex')});
  vm.runInContext(code,ctx,{filename,timeout:5000});
}
document.readyState='complete';
for(const fn of domEvents.DOMContentLoaded??[]) fn();
const cases=JSON.parse(fs.readFileSync(casesArg,'utf8'));
if(!Array.isArray(cases)||!cases.length) throw Error('Empty corpus');
const rows=cases.map(c=>{
  // Seed a valid prior result so refusal probes must clear stale output.
  for(const [id,value] of Object.entries({point:2,lo:1.5,hi:2.7,measure:'RR'})) {
    els.get(id).value=String(value);els.get(id).validity.badInput=false;
  }
  els.get('rare').checked=false;ctx.run();
  for(const id of ['measure','point','lo','hi']) {
    els.get(id).value=c[id]==null?'':String(c[id]);
    els.get(id).validity.badInput=(c.badInput??[]).includes(id);
  }
  els.get('rare').checked=!!c.rare;
  const clicks=els.get('btn-run').listeners.click;
  if(clicks.length!==1) throw Error('Expected one page compute handler');
  clicks[0]();
  const result=ctx.__almLastEValue();
  if(result===null && (!els.get('tbody').textContent.startsWith('Analysis refused:') ||
      els.get('interp').textContent!=='' || els.get('plot').innerHTML!=='')) throw Error('Stale refusal UI');
  if(result!==null && /NaN|Infinity/.test(els.get('plot').innerHTML)) throw Error('Nonfinite plot');
  return {id:c.id,accepted:result!==null,values:result===null?null:
    {point:result.point,ci:result.ci,rr_point:result.rr.point,rr_lo:result.rr.lo,rr_hi:result.rr.hi}};
});
// Prevent JSON.stringify from disguising NaN/Infinity as null.
for(const row of rows) if(row.values) for(const value of Object.values(row.values))
  if(value!==null && !Number.isFinite(value)) throw Error('Nonfinite result');
fs.writeFileSync(outputArg,JSON.stringify({runtime:process.version,scripts,rows},null,2)+'\n');
console.log(`${rows.length} page configurations replayed (simulated DOM)`);
