#!/usr/bin/env python3
"""Trip cost settings, Oct 2026: one question per line (Travellers, Style, When, Getting there).
When = Month | Start date. Getting there = Ferry / Ferry + my car / Fly / Already booked (no own-car
switch); road-reached islands (Lefkada, central Evia) read Bus / My car and get a KTEL bus fare from
Athens instead of EUR 0. The ferries line notes what fast boats would cost (~1.8x on longer legs)."""
import re, sys
from pathlib import Path
R = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
P = R / 'tools/build_trip_cost.py'
s = P.read_text(encoding='utf-8')
if 'tc-set' in s:
    print('already'); sys.exit()
D = lambda x: x.replace('{', '{{').replace('}', '}}')


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:100])
    s = s.replace(a, b)


# ---- strings
rep("'x_h': 'Add to the estimate',",
    "'x_h': 'Add to the estimate', 'lbl_when': 'When', 'w_month': 'Month', 'w_date': 'Start date', "
    "'d_hint': '→ {n} nights, back {d}', 'pax_hint': 'two people share a room', 'gt_car_c': '🚗 Ferry + my car', "
    "'gt_bus': '🚌 Bus', 'gt_mycar': '🚗 My car', 'fast_note': 'fast boats where they run: ~{x}',")
rep("'x_h': 'Πρόσθεσε στην εκτίμηση',",
    "'x_h': 'Πρόσθεσε στην εκτίμηση', 'lbl_when': 'Πότε', 'w_month': 'Μήνας', 'w_date': 'Ημερομηνία', "
    "'d_hint': '→ {n} νύχτες, επιστροφή {d}', 'pax_hint': 'δύο άτομα ανά δωμάτιο', 'gt_car_c': '🚗 Πλοίο + αυτοκίνητο', "
    "'gt_bus': '🚌 Λεωφορείο', 'gt_mycar': '🚗 Με το αυτοκίνητο', 'fast_note': 'με ταχύπλοα όπου υπάρχουν: ~{x}',")
rep("'x_h', 'x_esim',", "'x_h', 'lbl_when', 'w_month', 'w_date', 'd_hint', 'gt_car_c', 'gt_ferry_c', 'gt_bus', 'gt_mycar', 'fast_note', 'x_esim',")
rep("'li_bus': 'Buses between regions'", "'li_bus': 'Buses'")
rep("'li_bus': 'Λεωφορεία μεταξύ περιοχών'", "'li_bus': 'Λεωφορεία'")

# ---- settings box
m = re.search(r'  <div class="tc-bar" id="tc-bar">\n.*?\n  </div>\n\n  <div class="tc-grid">', s, re.S)
assert m
HTML = '''  <div class="tc-set" id="tc-bar">
    <div class="tc-q"><b>{t['lbl_trav']}</b><div class="tc-c"><div class="tc-step"><button type="button" id="tc-pax-minus" aria-label="{'Λιγότεροι ταξιδιώτες' if lang == 'el' else 'Fewer travellers'}">−</button><span id="tc-pax" aria-live="polite">2</span><button type="button" id="tc-pax-plus" aria-label="{'Περισσότεροι ταξιδιώτες' if lang == 'el' else 'More travellers'}">+</button></div><span class="tc-hint">{t['pax_hint']}</span></div></div>
    <div class="tc-q"><b>{t['lbl_style']}</b><div class="tc-c tc-chips" id="tc-tiers"><button type="button" class="tc-chip" data-t="budget">{t['tier_budget']}<small>{t['tier_budget_s']}</small></button><button type="button" class="tc-chip on" data-t="mid">{t['tier_mid']}<small>{t['tier_mid_s']}</small></button><button type="button" class="tc-chip" data-t="comfort">{t['tier_comfort']}<small>{t['tier_comfort_s']}</small></button></div></div>
    <div class="tc-q"><b>{t['lbl_when']}</b><div class="tc-c tc-when"><span class="tc-seg2" id="tc-when"><button type="button" data-w="m" class="on">{t['w_month']}</button><button type="button" data-w="d">{t['w_date']}</button></span><div class="tc-chips" id="tc-months">{months_html}</div><input type="date" id="tc-date" class="tc-date" hidden><span class="tc-hint" id="tc-dhint"></span></div></div>
    <div class="tc-q"><b>{t['lbl_gt']}</b><div class="tc-c tc-chips" id="tc-gt"><button type="button" class="tc-chip on" data-gt="ferry" title="{t['gt_ferry_s']}">{t['gt_ferry_c']}</button><button type="button" class="tc-chip" data-gt="car">{t['gt_car_c']}</button><button type="button" class="tc-chip" data-gt="fly" title="{t['gt_fly_s']}">{t['gt_fly_c']}</button><button type="button" class="tc-chip" data-gt="skip" title="{t['skip_tr']}">{t['gt_booked']}</button></div></div>
  </div>

  <div class="tc-grid">'''
s = s[:m.start()] + HTML + s[m.end():]

CSS = r'''
.tc-set{background:var(--card-bg,#fff);border:1px solid var(--border,#EAE4DC);border-radius:16px;padding:4px 18px;margin:18px 0 0;box-shadow:0 2px 10px rgba(26,35,50,.05)}
.tc-q{display:grid;grid-template-columns:130px minmax(0,1fr);align-items:center;gap:12px;padding:10px 0;border-top:1px solid var(--border,#EAE4DC)}
.tc-q:first-child{border-top:0}
.tc-q>b{font-size:11px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;color:var(--ink-3,#637080)}
.tc-c{display:flex;flex-wrap:wrap;gap:6px;align-items:center}
.tc-set .tc-chips{gap:6px}
.tc-set .tc-chip{border-radius:999px;padding:6px 12px;font-size:13px;white-space:nowrap}
.tc-set .tc-chip.on{background:var(--ink,#1A2332);border-color:var(--ink,#1A2332);color:#fff}
.tc-set .tc-chip.off{opacity:.45;cursor:not-allowed}
.tc-set .tc-chip[hidden]{display:none}
#tc-tiers .tc-chip{border-radius:12px;text-align:left;padding:6px 14px}
#tc-tiers .tc-chip small{display:block;font-size:11px;font-weight:600;color:var(--ink-3,#637080);line-height:1.25}
#tc-tiers .tc-chip.on small{color:#cfd6de}
.tc-set .tc-step{padding:3px;gap:10px}.tc-set .tc-step button{width:26px;height:26px;font-size:15px}
.tc-hint{font-size:12.5px;color:var(--ink-3,#637080);margin-left:4px}
.tc-seg2{display:inline-flex;background:var(--primary-pale,#E8F7FB);border-radius:999px;padding:3px;margin-right:4px}
.tc-seg2 button{border:0;background:none;font:inherit;font-size:12.5px;font-weight:700;color:var(--ink-3,#637080);padding:4px 11px;border-radius:999px;cursor:pointer;white-space:nowrap}
.tc-seg2 button.on{background:var(--card-bg,#fff);color:var(--primary-dark,#076880);box-shadow:0 1px 4px rgba(26,35,50,.2)}
.tc-when .tc-date{font-size:13.5px;padding:6px 10px}
html.dark .tc-set{background:#1F2530;border-color:rgba(255,255,255,.12)}
html.dark .tc-q{border-top-color:rgba(255,255,255,.08)}
html.dark .tc-set .tc-chip.on{background:#EEF2F5;color:#1A2332;border-color:#EEF2F5}
html.dark #tc-tiers .tc-chip.on small{color:#3a4656}
html.dark .tc-seg2{background:rgba(255,255,255,.07)}html.dark .tc-seg2 button.on{background:#283040;color:#60D8F0}
@media(max-width:640px){
  .tc-set{padding:2px 14px}
  .tc-q{grid-template-columns:1fr;gap:6px}
  #tc-tiers .tc-chip small{display:none}
  .tc-hint{display:none}
  .tc-when{flex-wrap:nowrap;overflow-x:auto;scrollbar-width:none}.tc-when::-webkit-scrollbar{display:none}
  .tc-when .tc-chips{flex-wrap:nowrap}
}
'''
rep(".tc-more[hidden]{{display:none}}", ".tc-more[hidden]{{display:none}}\n" + D(CSS))

# ---- render: settings state
rep("""  {{const ex=document.getElementById('tc-exact');if(ex){{ex.textContent=state.date?T.exact_close:T.exact_link;}}
   if(_di&&state.date)_di.hidden=false;}}""",
D("""  {const dm=DMODE||!!state.date;
   document.querySelectorAll('#tc-when button').forEach(b=>b.classList.toggle('on',(b.dataset.w==='d')===dm));
   document.getElementById('tc-months').hidden=dm;if(_di)_di.hidden=!dm;
   if(!dm)document.getElementById('tc-dhint').textContent='';}"""))
rep("""  document.getElementById('tc-own').classList.toggle('on',state.own);
""", "")
rep("""   const cur=state.skip?'skip':(state.fly?'fly':'ferry');
   document.querySelectorAll('#tc-gt .tc-chip').forEach(o=>{{o.classList.toggle('on',o.dataset.gt===cur);
     if(o.dataset.gt==='fly'){{o.classList.toggle('off',!canFly||state.own);o.title=canFly?T.gt_fly_s:T.gt_fly_off;}}}});}}""",
D("""   const cur=state.skip?'skip':(state.own?'car':(state.fly?'fly':'ferry'));
   const roadTrip=!!(state.trip.length&&LOCAL_PORTS[f0.k]&&isRoad(LOCAL_PORTS[f0.k].f)&&LOCAL_PORTS[l0.k]&&isRoad(LOCAL_PORTS[l0.k].f));
   document.querySelectorAll('#tc-gt .tc-chip').forEach(o=>{o.classList.toggle('on',o.dataset.gt===cur);
     if(o.dataset.gt==='ferry')o.textContent=roadTrip?T.gt_bus:T.gt_ferry_c;
     if(o.dataset.gt==='car')o.textContent=roadTrip?T.gt_mycar:T.gt_car_c;
     if(o.dataset.gt==='fly'){o.hidden=roadTrip;o.classList.toggle('off',!canFly);o.title=canFly?T.gt_fly_s:T.gt_fly_off;}});}"""))

# ---- road-reached islands: KTEL bus from Athens (one way, per person)
rep("  'evia-central':{{f:[0,0],   en:", "  'evia-central':{{f:[0,0],bus:9,   en:")
rep("  'lefkada':     {{f:[0,0],   en:", "  'lefkada':     {{f:[0,0],bus:37,   en:")
rep("    if(lp)return{{f:lp.f,label:lp[LANG],fly:false}};", "    if(lp)return{{f:lp.f,label:lp[LANG],fly:false,road:isRoad(lp.f),bus:lp.bus||0}};")
rep("<span class=\"fp\">${{fareTxt(dep.f)}}", "<span class=\"fp\">${{(dep.road&&!state.own&&dep.bus)?'🚌 €'+dep.bus+' pp':fareTxt(dep.f)}}")
rep("<span class=\"fp\">${{fareTxt(ret.f)}}", "<span class=\"fp\">${{(ret.road&&!state.own&&ret.bus)?'🚌 €'+ret.bus+' pp':fareTxt(ret.f)}}")
rep("  {{const rl=legs.filter(([a,b])=>a!=='M'&&b!=='M'&&legInfo(a,b).road);",
    "  {{const rl=legs.filter(([a,b])=>{{const l=legInfo(a,b);return l.road&&l.bus;}});")

# ---- fast boats note on the ferries line
rep("    if(fsum>0){{li+=line('⛴',T.li_ferries,`${{portsTxt}}${{legs.filter(([a,b])=>!legInfo(a,b).road).length}} ${{T.li_legs}} × ${{state.pax}} ${{T.li_pax}}`,fsum,null,null,SK);if(!SK)tot+=fsum;}}}}",
    D("""    let fast=0;legs.forEach(([a,b])=>{const l=legInfo(a,b);if(l.road)return;const m=mid(l.f);fast+=(m>=20?m*1.8:m)*state.pax;});
    const fastTxt=(fast-fsum>=20)?'<br>⚡ '+T.fast_note.replace('{x}',eur(rnd(fast))):'';""") + "\n"
    "    if(fsum>0){{li+=line('⛴',T.li_ferries,`${{portsTxt}}${{legs.filter(([a,b])=>!legInfo(a,b).road).length}} ${{T.li_legs}} × ${{state.pax}} ${{T.li_pax}}${{fastTxt}}`,fsum,null,null,SK);if(!SK)tot+=fsum;}}}}")

# ---- start-date hint
rep("  if(_ts){{const _e=new Date(_ts);_e.setDate(_e.getDate()+nightsTotal);whenTxt=fmtD(_ts)+' – '+fmtD(_e);}}",
    "  if(_ts){{const _e=new Date(_ts);_e.setDate(_e.getDate()+nightsTotal);whenTxt=fmtD(_ts)+' – '+fmtD(_e);\n"
    "    document.getElementById('tc-dhint').textContent=T.d_hint.replace('{{n}}',nightsTotal).replace('{{d}}',fmtD(_e));}}\n"
    "  else if(DMODE)document.getElementById('tc-dhint').textContent='';")

# ---- events
rep("""document.getElementById('tc-exact').addEventListener('click',()=>{{const d=document.getElementById('tc-date');
  if(state.date){{state.date=null;d.hidden=true;render();return;}}
  d.hidden=!d.hidden;if(!d.hidden)d.focus();}});""",
D("""document.getElementById('tc-when').addEventListener('click',e=>{const b=e.target.closest('[data-w]');if(!b)return;
  DMODE=b.dataset.w==='d';if(!DMODE)state.date=null;render();
  if(DMODE){const d=document.getElementById('tc-date');try{d.showPicker&&d.showPicker();}catch(_){}d.focus();}});"""))
rep("document.getElementById('tc-own').addEventListener('click',()=>{{state.own=!state.own;if(state.own)state.fly=false;render();}});\n", "")
rep("  const g=o.dataset.gt;state.skip=g==='skip';if(g==='fly'){{state.fly=true;state.own=false;}}else if(g==='ferry')state.fly=false;",
    "  const g=o.dataset.gt;state.skip=g==='skip';state.own=g==='car';state.fly=g==='fly';")
rep("function sync(){{", "let DMODE=!!state.date;\nfunction sync(){{")
P.write_text(s, encoding='utf-8')
print('ok')
