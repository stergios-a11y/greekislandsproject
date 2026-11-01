#!/usr/bin/env python3
"""Trip cost v3 (Oct 2026): 'Your trip' with numbered choices (1 Travellers + Rooms, 2 Style, 3 When,
4 Getting there, 5 Extras: eSIM / insurance) and 6 Islands; 'Your budget' card with a teal header and
a thin bar on each line (car hire + fuel share one). Rooms follow two-per-room until the visitor
changes them (1-4 people a room; triple x1.3, quad x1.5 of the double price). Greek 'Ferry + MY car',
'1 person' grammar."""
import re, sys
from pathlib import Path
R = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
P = R / 'tools/build_trip_cost.py'
s = P.read_text(encoding='utf-8')
if 'tc-bh' in s:
    print('already'); sys.exit()
D = lambda x: x.replace('{', '{{').replace('}', '}}')


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:110])
    s = s.replace(a, b)


# ---- strings
rep("'x_h': 'Add to the estimate',",
    "'x_h': 'Add to the estimate', 'sec_trip': 'Your trip', 'sec_trip_s': 'everything here changes the budget', "
    "'sec_isl': 'Islands', 'sec_isl_s': 'tap an island for boat day, rooms and the guide', 'sec_bud': 'Your budget', "
    "'lbl_rooms': 'Rooms', 'lbl_extras': 'Extras', 'x_esim_c': '📶 eSIM', 'x_ins_c': '🛡 Travel insurance', 'incl_fuel': 'incl. fuel', "
    "'p1w': 'person', 'pNw': 'people', 'r1w': 'room', 'rNw': 'rooms', 'triple': 'triple', 'quad': 'quad', 'auto_r': 'two per room',")
rep("'x_h': 'Πρόσθεσε στην εκτίμηση',",
    "'x_h': 'Πρόσθεσε στην εκτίμηση', 'sec_trip': 'Το ταξίδι σου', 'sec_trip_s': 'ό,τι αλλάζεις εδώ αλλάζει τον προϋπολογισμό', "
    "'sec_isl': 'Νησιά', 'sec_isl_s': 'πάτα ένα νησί για ημέρα σκάφους, δωμάτια και οδηγό', 'sec_bud': 'Ο προϋπολογισμός σου', "
    "'lbl_rooms': 'Δωμάτια', 'lbl_extras': 'Επιπλέον', 'x_esim_c': '📶 eSIM', 'x_ins_c': '🛡 Ταξιδιωτική ασφάλεια', 'incl_fuel': 'μαζί με καύσιμα', "
    "'p1w': 'άτομο', 'pNw': 'άτομα', 'r1w': 'δωμάτιο', 'rNw': 'δωμάτια', 'triple': 'τρίκλινο', 'quad': 'τετράκλινο', 'auto_r': 'δύο ανά δωμάτιο',")
rep("'gt_car_c': '🚗 Πλοίο + αυτοκίνητο'", "'gt_car_c': '🚗 Πλοίο + το αυτοκίνητό μου'")
rep("'x_h', 'eu_roam',", "'x_h', 'eu_roam', 'incl_fuel', 'p1w', 'pNw', 'r1w', 'rNw', 'triple', 'quad', 'auto_r',")

# ---- 'Your trip' heading + numbered rows + rooms + extras
rep('''  <div class="tc-set" id="tc-bar">
    <div class="tc-q"><b>{t['lbl_trav']}</b>''',
    '''  <div class="tc-sec"><b>{t['sec_trip']}</b><small>{t['sec_trip_s']}</small></div>
  <div class="tc-set" id="tc-bar">
    <div class="tc-q"><b><i class="tc-num">1</i>{t['lbl_trav']}</b>''')
rep('''<button type="button" id="tc-pax-plus" aria-label="{'Περισσότεροι ταξιδιώτες' if lang == 'el' else 'More travellers'}">+</button></div><span class="tc-hint">{t['pax_hint']}</span></div></div>''',
    '''<button type="button" id="tc-pax-plus" aria-label="{'Περισσότεροι ταξιδιώτες' if lang == 'el' else 'More travellers'}">+</button></div><span class="tc-rl">{t['lbl_rooms']}</span><div class="tc-step"><button type="button" id="tc-rm-minus" aria-label="−">−</button><span id="tc-rooms" aria-live="polite">1</span><button type="button" id="tc-rm-plus" aria-label="+">+</button></div><span class="tc-hint" id="tc-rhint"></span></div></div>''')
rep('''    <div class="tc-q"><b>{t['lbl_style']}</b>''', '''    <div class="tc-q"><b><i class="tc-num">2</i>{t['lbl_style']}</b>''')
rep('''    <div class="tc-q"><b>{t['lbl_when']}</b>''', '''    <div class="tc-q"><b><i class="tc-num">3</i>{t['lbl_when']}</b>''')
rep('''    <div class="tc-q"><b>{t['lbl_gt']}</b>''', '''    <div class="tc-q"><b><i class="tc-num">4</i>{t['lbl_gt']}</b>''')
rep('''<button type="button" class="tc-chip" data-gt="skip" title="{t['skip_tr']}">{t['gt_booked']}</button></div></div>
  </div>''',
    '''<button type="button" class="tc-chip" data-gt="skip" title="{t['skip_tr']}">{t['gt_booked']}</button></div></div>
    <div class="tc-q"><b><i class="tc-num">5</i>{t['lbl_extras']}</b><div class="tc-c tc-chips" id="tc-extras"><button type="button" class="tc-chip tc-tg" data-x="esim" role="switch" aria-checked="false"><i aria-hidden="true"></i>{t['x_esim_c']}<small>{t['x_esim_s']}</small></button><button type="button" class="tc-chip tc-tg" data-x="ins" role="switch" aria-checked="false"><i aria-hidden="true"></i>{t['x_ins_c']}<small>{t['x_ins_s']}</small></button></div></div>
  </div>''')
rep('''    <div>
      <section class="tc-ctrl tc-trip">''', '''    <div>
      <div class="tc-sec"><i class="tc-num">6</i><b>{t['sec_isl']}</b><small>{t['sec_isl_s']}</small></div>
      <section class="tc-ctrl tc-trip">''')
rep('''    <div class="tc-side">
      <div class="tc-sum" id="tc-summary"></div>''', '''    <div class="tc-side">
      <div class="tc-sec"><b>{t['sec_bud']}</b></div>
      <div class="tc-sum" id="tc-summary"></div>''')

CSS = r'''
.tc-sec{display:flex;align-items:center;gap:10px;margin:22px 0 8px;flex-wrap:wrap}
.tc-sec>b{font-family:'Alegreya',serif;font-size:21px;color:var(--ink-1,#1A2332)}
.tc-sec>small{font-size:12.5px;color:var(--ink-3,#637080)}
.tc-side .tc-sec,.tc-grid>div>.tc-sec{margin-top:0}
.tc-set{margin-top:0}
.tc-num{width:22px;height:22px;border-radius:50%;background:var(--primary,#0B8FAC);color:#fff;font:800 12px/22px var(--font-ui,sans-serif);text-align:center;font-style:normal;display:inline-block;letter-spacing:0;margin-right:8px;flex:none}
.tc-q>b{display:flex;align-items:center}
.tc-rl{font-size:12.5px;font-weight:700;color:var(--ink-2,#2E3D50);margin:0 2px 0 12px}
.tc-tg{display:inline-flex;align-items:center;gap:7px}
.tc-tg>i{width:26px;height:15px;border-radius:8px;background:#d5dbe0;position:relative;display:inline-block;flex:none}
.tc-tg>i:after{content:"";position:absolute;left:2px;top:2px;width:11px;height:11px;border-radius:50%;background:#fff;transition:left .15s}
.tc-tg.on>i{background:#2ec4e6}.tc-tg.on>i:after{left:13px}
.tc-set .tc-tg small{font-size:11px;font-weight:600;color:var(--ink-3,#637080);margin-left:2px}
.tc-set .tc-tg.on small{color:#cfd6de}
.tc-sum{padding:0!important;overflow:hidden;box-shadow:0 10px 30px rgba(7,104,128,.18)!important}
.tc-bh{background:linear-gradient(135deg,#076880,#0C3442);color:#fff;padding:16px 20px 18px}
.tc-bh .tc-k{color:#bfe8f2}
.tc-bh .tc-big{color:#fff}
.tc-bh .tc-pp2{color:#d6eef4;margin:0}.tc-bh .tc-pp2 small{color:#a9d6e2}
.tc-bb{padding:6px 20px 18px}
.tc-li .tr{grid-column:2/4;display:flex;align-items:center;gap:8px;margin-top:5px}
.tc-li .tr i{display:block;height:6px;border-radius:3px;min-width:4px}
.tc-li .tr em{font-style:normal;font-size:11.5px;font-weight:800;color:var(--ink-3,#637080);white-space:nowrap}
html.dark .tc-bh{background:linear-gradient(135deg,#0C4556,#0A2530)}
@media(max-width:640px){.tc-rl{margin-left:6px}.tc-set .tc-tg small{display:none}.tc-sec>small{display:none}}
'''
rep("#tc-months[hidden],.tc-when .tc-date[hidden]{{display:none!important}}",
    "#tc-months[hidden],.tc-when .tc-date[hidden]{{display:none!important}}\n" + D(CSS))

# ---- rooms model
rep("function roomsFor(p){{return Math.max(1,Math.ceil((p||1)/2));}}",
    D("""function roomsFor(p){return roomsN();}
// Rooms follow two-per-room until the visitor sets them (1 to 4 people a room).
function roomsAuto(){return Math.max(1,Math.ceil(state.pax/2));}
function roomsN(){const lo=Math.ceil(state.pax/4),hi=state.pax;return state.rooms?Math.min(hi,Math.max(lo,state.rooms)):roomsAuto();}
function occs(){const r=roomsN(),q=Math.floor(state.pax/r),x=state.pax%r;return Array.from({length:r},(_,i)=>q+(i<x?1:0));}
// price of the party's rooms in double-room units: a triple ~1.3, a quad ~1.5 of a double
function roomMult(){return occs().reduce((a,n)=>a+(n<=2?1:n===3?1.3:1.5),0);}
const pw=n=>n===1?T.p1w:T.pNw, rw=n=>n===1?T.r1w:T.rNw;
function roomDesc(){const o=occs(),mx=Math.max(...o);const kind=mx===3?T.triple:mx===4?T.quad:'';
  return `${o.length} ${rw(o.length)}, ${state.pax} ${pw(state.pax)}${kind?' ('+kind+')':''}`;}"""))
rep("    rsum+=rn*t.n*mult*roomsFor(state.pax);}});", "    rsum+=rn*t.n*mult*roomMult();}});")
rep("  let c=rn*n*mult*roomsFor(state.pax) + mealDay(k)*state.pax*n;", "  let c=rn*n*mult*roomMult() + mealDay(k)*state.pax*n;")
rep("${{T.li_rooms}} — ${{nightsTotal}} ${{T.nights}}${{roomsFor(state.pax)>1?' · '+roomsFor(state.pax)+' '+T.rooms_word:''}}`,state.trip.map(",
    "${{T.li_rooms}} — ${{nightsTotal}} ${{T.nights}}`,roomDesc()+' · '+state.trip.map(")
# island row: price for the party's rooms per night
rep("<small>${{eur(rnd(rn))}}${{T.per_night}}", "<small>${{eur(rnd(rn*roomMult()))}}${{T.per_night}}")
# '1 person' grammar
s = s.replace("${{state.pax}} ${{T.li_pax}}", "${{state.pax}} ${{pw(state.pax)}}")

# ---- state, URL, settings render, events
rep("  if(q.get('pax'))state.pax=Math.min(8,Math.max(1,parseInt(q.get('pax'))||2));",
    "  if(q.get('pax'))state.pax=Math.min(8,Math.max(1,parseInt(q.get('pax'))||2));\n  if(q.get('rooms'))state.rooms=Math.min(8,Math.max(1,parseInt(q.get('rooms'))||0))||null;")
rep("(state.esim?'&esim=1':'')", "(state.rooms?'&rooms='+state.rooms:'')+(state.esim?'&esim=1':'')")
rep("  document.getElementById('tc-pax').textContent=state.pax;",
    D("""  document.getElementById('tc-pax').textContent=state.pax;
  {const r=roomsN();document.getElementById('tc-rooms').textContent=r;
   document.getElementById('tc-rhint').textContent=state.rooms&&r!==roomsAuto()?roomDesc():T.auto_r;
   document.querySelectorAll('#tc-extras .tc-tg').forEach(b=>{const on=!!state[b.dataset.x];b.classList.toggle('on',on);b.setAttribute('aria-checked',String(on));});}"""))
rep("document.getElementById('tc-summary').addEventListener('click',e=>{{const b=e.target.closest('[data-x]');if(!b)return;const k=b.dataset.x;state[k]=!state[k];render();}});",
    D("""document.getElementById('tc-extras').addEventListener('click',e=>{const b=e.target.closest('[data-x]');if(!b)return;const k=b.dataset.x;state[k]=!state[k];render();});
document.getElementById('tc-rm-minus').addEventListener('click',()=>{state.rooms=Math.max(Math.ceil(state.pax/4),roomsN()-1);render();});
document.getElementById('tc-rm-plus').addEventListener('click',()=>{state.rooms=Math.min(state.pax,roomsN()+1);render();});"""))

# ---- budget card: teal header, a thin bar on each line
rep("  const line=(ic,lbl,small,amt,book,url,nc)=>`<div class=\"tc-li${{nc?' nc':''}}\">",
    "  const GRP={{'⛴':'tr','🚌':'tr','✈':'tr','🛏':'rooms','🚗':'car','⛽':'car','🚙':'car','⛵':'boat','🍴':'food','📶':'x','🛡':'x'}};\n"
    "  const line=(ic,lbl,small,amt,book,url,nc)=>`<div class=\"tc-li${{nc?' nc':''}}\"${{nc?'':` data-amt=\"${{amt}}\" data-g=\"${{GRP[ic]||ic}}\"`}}>")
a0 = s.index("  {{const tr=Math.max(0,tot-rsum-msum-csumAll-bsum);")
a1 = s.index("  document.getElementById('tc-summary').innerHTML=`", a0)
s = s[:a0] + s[a1:]
rep('''    <div class="tc-k">${{T.trip_k}} · ${{nightsTotal}} ${{T.nights}} · ${{state.pax}} ${{pw(state.pax)}}</div>
    <div class="tc-big">${{eur(rnd(tot))}}</div>''',
    '''    <div class="tc-bh"><div class="tc-k">${{nightsTotal}} ${{T.nights}} · ${{state.pax}} ${{pw(state.pax)}} · ${{roomsN()}} ${{rw(roomsN())}} · ${{whenTxt}}</div>
    <div class="tc-big">${{eur(rnd(tot))}}</div>''')
rep('''<br><small>${{state.fly?T.total_fly:T.total}}</small></div>
    <div class="tc-stk">${{window._tcStk}}</div><div class="tc-leg2">${{window._tcLeg}}</div>
    ${{li}}''', '''<br><small>${{state.fly?T.total_fly:T.total}}</small></div></div>
    <div class="tc-bb">${{li}}''')
a0 = s.index('    <div class="tc-xtra"><div class="tc-k">${{T.x_h}}</div>')
a1 = s.index('    <div class="tc-ctas">', a0)
s = s[:a0] + s[a1:]
rep('''<div class="tc-honest">${{T.honest}}</div></details>`;''', '''<div class="tc-honest">${{T.honest}}</div></details></div>`;
''' + D('''  {const COL={rooms:'#0B8FAC',food:'#E8522A',tr:'#3D8B6F',car:'#C98A00',boat:'#8A7AA0',x:'#7A8794'};
   const ls=[...document.querySelectorAll('#tc-summary .tc-li[data-amt]')],sum={},cnt={};
   ls.forEach(l=>{const g=l.dataset.g;sum[g]=(sum[g]||0)+(+l.dataset.amt);cnt[g]=(cnt[g]||0)+1;});
   const seen=new Set();ls.forEach(l=>{const g=l.dataset.g;if(seen.has(g)||!tot)return;seen.add(g);
     const pc=Math.round(sum[g]/tot*100);
     l.insertAdjacentHTML('beforeend',`<div class="tr"><i style="width:${Math.max(2,pc)}%;background:${COL[g]||'#7A8794'}"></i><em>${pc}%${cnt[g]>1&&g==='car'?' '+T.incl_fuel:''}</em></div>`);});}'''))
P.write_text(s, encoding='utf-8')
print('ok')
