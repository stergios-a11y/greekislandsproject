#!/usr/bin/env python3
"""Trip-cost (Budget) page redesign, Oct 2026: settings bar on top (month, people, style, ferry/fly/
already booked, 'More options' for exact dates, own car, non-EU); compact island rows (nights + one
vehicle button that cycles walk/scooter/car; tap a row for boat day, rooms, guide); total + stacked
bar + the only two booking buttons in a sticky right column, smart swaps under it; empty start with
four ready-made trips. The cost model is untouched."""
import re, sys
from pathlib import Path
R = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
P = R / 'tools/build_trip_cost.py'
s = P.read_text(encoding='utf-8')
if 'NEW_STR' in s:
    print('already'); sys.exit()
D = lambda x: x.replace('{', '{{').replace('}', '}}')   # literal braces inside the f-string


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:90])
    s = s.replace(a, b)


# ---- strings
rep("def render_page(lang, meta, data):\n    t = STR[lang]",
'''NEW_STR = {
    'en': {'more_opts': 'More options', 'gt_booked': 'Already booked', 'gt_ferry_c': '⛴ Ferry', 'gt_fly_c': '✈ Fly',
           'own_sw': '🚙 I\\'m bringing my own car on the ferries', 'start_h': 'Where are you going?',
           'start_p': 'Add your first island, or start from a ready-made trip and change it.',
           'rooms_l': '🛏 Rooms on Booking.com', 'see_prices': 'see prices →', 'guide_l': '📖 {isl} guide', 'open_l': 'open →',
           'cyc_t': 'Tap to change: on foot, scooter or car', 'row_t': 'Tap for boat day, rooms and the guide',
           'trip_k': 'Your trip', 'boat_avail': 'boat day',
           'p1': 'Cyclades classic', 'p2': 'Small Cyclades', 'p3': 'Easy Saronic', 'p4': 'Dodecanese',
           'mshort': {'apr': 'Apr', 'may': 'May', 'jun': 'Jun', 'jul': 'Jul', 'aug': 'Aug', 'sep': 'Sep', 'oct': 'Oct'}},
    'el': {'more_opts': 'Περισσότερα', 'gt_booked': 'Έχω εισιτήρια', 'gt_ferry_c': '⛴ Πλοίο', 'gt_fly_c': '✈ Αεροπλάνο',
           'own_sw': '🚙 Φέρνω το αυτοκίνητό μου με το πλοίο', 'start_h': 'Πού πας;',
           'start_p': 'Πρόσθεσε το πρώτο νησί, ή ξεκίνα από ένα έτοιμο ταξίδι και άλλαξέ το.',
           'rooms_l': '🛏 Δωμάτια στο Booking.com', 'see_prices': 'δες τιμές →', 'guide_l': '📖 Οδηγός: {isl}', 'open_l': 'άνοιγμα →',
           'cyc_t': 'Πάτα για αλλαγή: πεζός, σκούτερ ή αυτοκίνητο', 'row_t': 'Πάτα για ημέρα σκάφους, δωμάτια και οδηγό',
           'trip_k': 'Το ταξίδι σου', 'boat_avail': 'ημέρα σκάφους',
           'p1': 'Κυκλάδες, η κλασική', 'p2': 'Μικρές Κυκλάδες', 'p3': 'Εύκολος Σαρωνικός', 'p4': 'Δωδεκάνησα',
           'mshort': {'apr': 'Απρ', 'may': 'Μάι', 'jun': 'Ιούν', 'jul': 'Ιούλ', 'aug': 'Αύγ', 'sep': 'Σεπ', 'oct': 'Οκτ'}},
}


def render_page(lang, meta, data):
    t = {**STR[lang], **NEW_STR[lang]}''')
rep("""        for m, name in t['months'].items()
    )""", """        for m, name in t['mshort'].items()
    )""")
rep("""    js_t['months'] = t['months']""", """    js_t['months'] = t['months']
    for _k in ('more_opts', 'gt_booked', 'start_h', 'start_p', 'rooms_l', 'see_prices', 'guide_l', 'open_l', 'cyc_t', 'row_t',
               'trip_k', 'boat_avail', 'p1', 'p2', 'p3', 'p4', 'gt_fly_off'):
        js_t[_k] = t[_k]""")

# ---- CSS
NEW_CSS = r'''
/* ---- Oct 2026 redesign ---- */
.tc-bar{display:flex;flex-wrap:wrap;gap:10px 14px;align-items:center;background:var(--card-bg,#fff);border:1px solid var(--border,#EAE4DC);border-radius:16px;padding:10px 14px;margin:18px 0 0;box-shadow:0 2px 10px rgba(26,35,50,.05)}
.tc-g{display:flex;align-items:center;gap:6px}
.tc-g>small{font-size:10.5px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;color:var(--ink-3,#637080);margin-right:2px}
.tc-bar .tc-chips{gap:5px;flex-wrap:nowrap}
.tc-bar .tc-chip{border-radius:999px;padding:5px 11px;font-size:13px;white-space:nowrap}
.tc-bar .tc-chip.on{background:var(--ink,#1A2332);border-color:var(--ink,#1A2332);color:#fff}
.tc-bar .tc-chip.off{opacity:.45;cursor:not-allowed}
.tc-bar .tc-step{padding:2px;gap:8px}.tc-bar .tc-step button{width:26px;height:26px;font-size:15px}
.tc-morebtn{margin-left:auto;font:inherit;font-size:13px;font-weight:800;color:var(--primary-dark,#076880);background:none;border:0;cursor:pointer;padding:4px 2px;white-space:nowrap}
.tc-more{flex-basis:100%;display:flex;flex-wrap:wrap;gap:12px 26px;align-items:center;padding-top:10px;border-top:1px dashed var(--border,#EAE4DC)}
.tc-more[hidden]{display:none}
.tc-grid{margin-top:18px}
.tc-side{position:sticky;top:16px}.tc-side .tc-sum{position:static}
.tc-trip{padding:6px 0 12px}
.tc-trip .tc-leg{padding:7px 16px}
.tc-row{display:flex;align-items:center;gap:12px;padding:10px 16px;border-top:1px solid var(--border,#EAE4DC);border-bottom:1px solid var(--border,#EAE4DC);background:var(--card-bg,#fff)}
.tc-rh{display:flex;align-items:center;gap:12px;flex:1;min-width:0;cursor:pointer}
.tc-rh img,.tc-rh .ph{width:46px;height:46px;border-radius:10px;object-fit:cover;flex:none;background:#dde8ec;display:block}
.tc-rn{min-width:0}.tc-rn b{display:block;font-family:'Alegreya',serif;font-size:18px;line-height:1.15;color:var(--ink-1,#1A2332)}
.tc-rn small{display:block;font-size:12px;color:var(--ink-3,#637080);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.tc-rn small i{font-style:normal;color:var(--primary,#0B8FAC);font-weight:700}
.tc-rn .chev{color:var(--ink-4,#A0ADB8);font-size:11px;margin-left:5px;display:inline-block;transition:transform .15s;font-family:sans-serif}
.tc-row.open .tc-rn .chev{transform:rotate(180deg)}
.tc-row .tc-n{gap:6px;white-space:nowrap}
.tc-row .tc-n b{font-size:14px;color:var(--ink-1,#1A2332);min-width:14px;text-align:center}
.tc-vc{border:1px solid var(--border-2,#D8CEC2);background:var(--card-bg,#fff);border-radius:999px;padding:5px 10px;font:inherit;font-size:12.5px;font-weight:700;cursor:pointer;white-space:nowrap;color:var(--ink-2,#2E3D50)}
.tc-vc:disabled{cursor:default;opacity:.8}
.tc-exp{background:var(--primary-pale,#E8F7FB);padding:10px 16px 12px 74px;display:grid;gap:7px;font-size:13px;border-bottom:1px solid var(--border,#EAE4DC)}
.tc-exp>div{display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.tc-exp a{margin-left:auto;font-weight:800;color:var(--primary-dark,#076880);text-decoration:none}
.tc-exp .tc-sw{color:var(--ink-2,#2E3D50);font-size:13px}
.tc-exp .amt{margin-left:auto;font-weight:800}
.tc-trip .tc-warn{padding:0 16px 8px 74px;margin:6px 0 0}
.tc-trip .tc-addrow{padding:4px 16px 0;margin-top:10px}
.tc-k{font-size:11px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;color:var(--ink-3,#637080)}
.tc-big{font-family:'Alegreya',serif;font-weight:800;font-size:44px;line-height:1.05;color:var(--ink-1,#1A2332);margin:4px 0 2px}
.tc-pp2{font-size:13px;color:var(--ink-3,#637080);margin-bottom:12px}
.tc-stk{display:flex;height:10px;border-radius:5px;overflow:hidden;margin:0 0 10px;background:var(--border,#EAE4DC)}
.tc-stk i{display:block;height:100%}
.tc-side #tc-swaps .tc-swaps-box{background:var(--card-bg,#fff);margin:14px 0 0;box-shadow:0 4px 18px rgba(26,35,50,.06)}
.tc-start{padding:18px 16px 6px}
.tc-start h3{font-family:'Alegreya',serif;font-size:22px;margin:0 0 4px;text-transform:none;letter-spacing:0;color:var(--ink-1,#1A2332)}
.tc-start p{margin:0 0 12px;color:var(--ink-3,#637080);font-size:13.5px}
.tc-pres{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:10px}
.tc-pre{border:1px solid var(--border,#EAE4DC);border-radius:12px;overflow:hidden;background:var(--card-bg,#fff);cursor:pointer;text-align:left;padding:0;font:inherit;color:inherit}
.tc-pre:hover{border-color:var(--primary,#0B8FAC)}
.tc-pre img,.tc-pre .ph{display:block;width:100%;height:70px;object-fit:cover;background:#dde8ec}
.tc-pre span{display:block;padding:8px 10px;font-size:12px;color:var(--ink-3,#637080)}
.tc-pre b{display:block;font-size:13.5px;color:var(--ink-1,#1A2332)}
html.dark .tc-bar,html.dark .tc-row,html.dark .tc-vc,html.dark .tc-pre{background:#1F2530;border-color:rgba(255,255,255,.12)}
html.dark .tc-bar .tc-chip.on{background:#EEF2F5;color:#1A2332;border-color:#EEF2F5}
html.dark .tc-exp{background:#16303A}
html.dark .tc-big{color:#EEF2F5}
@media(max-width:900px){.tc-side{position:static}}
@media(max-width:640px){
  .tc-bar{flex-wrap:nowrap;overflow-x:auto;-webkit-overflow-scrolling:touch;scrollbar-width:none;padding:8px 10px;gap:12px}
  .tc-bar::-webkit-scrollbar{display:none}
  .tc-g>small{display:none}
  .tc-more{flex-basis:auto;border:0;padding:0;flex-wrap:nowrap}
  .tc-row{gap:8px;padding:10px 12px}.tc-rh{gap:9px}.tc-rh img,.tc-rh .ph{width:40px;height:40px}
  .tc-row .tc-nl{display:none}
  .tc-vc .vl{display:none}
  .tc-exp{padding-left:12px}.tc-trip .tc-warn{padding-left:12px}
  .tc-trip .tc-leg{padding:7px 12px}.tc-trip .tc-addrow{padding:4px 12px 0}
}
'''
rep(".tc-advrow{{display:flex;gap:22px;flex-wrap:wrap;align-items:center;margin-top:16px}}\n</style>",
    ".tc-advrow{{display:flex;gap:22px;flex-wrap:wrap;align-items:center;margin-top:16px}}\n" + D(NEW_CSS) + "</style>")

# ---- HTML body
m = re.search(r'  <div class="tc-grid">\n.*?\n</main>', s, re.S)
assert m
HTML = '''  <div class="tc-bar" id="tc-bar">
    <div class="tc-g"><small>{t['lbl_month']}</small><div class="tc-chips" id="tc-months">{months_html}</div></div>
    <div class="tc-g"><small>{t['lbl_trav']}</small><div class="tc-step"><button type="button" id="tc-pax-minus" aria-label="{'Λιγότεροι ταξιδιώτες' if lang == 'el' else 'Fewer travellers'}">−</button><span id="tc-pax" aria-live="polite">2</span><button type="button" id="tc-pax-plus" aria-label="{'Περισσότεροι ταξιδιώτες' if lang == 'el' else 'More travellers'}">+</button></div></div>
    <div class="tc-g"><small>{t['lbl_style']}</small><div class="tc-chips" id="tc-tiers"><button type="button" class="tc-chip" data-t="budget" title="{t['tier_budget_s']}">{t['tier_budget']}</button><button type="button" class="tc-chip on" data-t="mid" title="{t['tier_mid_s']}">{t['tier_mid']}</button><button type="button" class="tc-chip" data-t="comfort" title="{t['tier_comfort_s']}">{t['tier_comfort']}</button></div></div>
    <div class="tc-g"><small>{t['lbl_gt']}</small><div class="tc-chips" id="tc-gt"><button type="button" class="tc-chip on" data-gt="ferry" title="{t['gt_ferry_s']}">{t['gt_ferry_c']}</button><button type="button" class="tc-chip" data-gt="fly" title="{t['gt_fly_s']}">{t['gt_fly_c']}</button><button type="button" class="tc-chip" data-gt="skip" title="{t['skip_tr']}">{t['gt_booked']}</button></div></div>
    <button type="button" class="tc-morebtn" id="tc-more-btn" aria-expanded="false" aria-controls="tc-more">{t['more_opts']} ▾</button>
    <div class="tc-more" id="tc-more" hidden>
      <div class="tc-daterow" style="margin:0"><button class="tc-link" id="tc-exact">{t['exact_link']}</button><input type="date" id="tc-date" class="tc-date" hidden></div>
      <button type="button" role="switch" aria-checked="false" class="tc-sw" id="tc-own"><span class="s" aria-hidden="true"></span> {t['own_sw']}</button>
      <button type="button" role="switch" aria-checked="false" class="tc-sw" id="tc-noneu"><span class="s" aria-hidden="true"></span> {t['noneu']} <small style="font-weight:600;color:var(--ink-4,#A0ADB8)">{t['noneu_small']}</small></button>
    </div>
  </div>

  <div class="tc-grid">
    <div>
      <section class="tc-ctrl tc-trip">
        <div id="tc-route"></div>
        <div class="tc-addrow" id="tc-addrow">
          <div class="tc-f tc-f-isl">
            <input class="tc-search" id="tc-search" placeholder="＋ {t['add_ph']}" autocomplete="off">
            <div class="tc-sug" id="tc-sug"></div>
          </div>
          <span id="tc-quick"></span>
        </div>
      </section>
    </div>
    <div class="tc-side">
      <div class="tc-sum" id="tc-summary"></div>
      <div id="tc-swaps"></div>
    </div>
    <a class="tc-stick" id="tc-stick" href="#tc-summary"><span><span class="k">{'Your estimate' if lang == 'en' else 'Η εκτίμησή σου'}</span><br><span class="v" id="tc-stick-v"></span> <span class="s" id="tc-stick-s"></span></span><span class="go">{'Breakdown ↓' if lang == 'en' else 'Ανάλυση ↓'}</span></a>
  </div>
</main>'''
s = s[:m.start()] + HTML + s[m.end():]

# ---- JS: settings sync at the top of render()
a0 = s.index("  document.getElementById('tc-noneu').classList.toggle('on',state.nonEU);")
a1 = s.index("  const sR=CFG.season_room[state.month]")
s = s[:a0] + D('''  document.getElementById('tc-noneu').classList.toggle('on',state.nonEU);
  document.getElementById('tc-own').classList.toggle('on',state.own);
  {const f0=state.trip[0],l0=state.trip[state.trip.length-1];
   const canFly=!!(state.trip.length&&(ISL[f0.k].air||ISL[l0.k].air));
   const cur=state.skip?'skip':(state.fly?'fly':'ferry');
   document.querySelectorAll('#tc-gt .tc-chip').forEach(o=>{o.classList.toggle('on',o.dataset.gt===cur);
     if(o.dataset.gt==='fly'){o.classList.toggle('off',!canFly||state.own);o.title=canFly?T.gt_fly_s:T.gt_fly_off;}});}
''') + s[a1:]

# ---- JS: empty state with ready-made trips
a0 = s.index("  if(!state.trip.length){{\n    document.getElementById('tc-route').innerHTML")
a1 = s.index("    sync();return;\n  }}", a0) + len("    sync();return;\n  }}")
s = s[:a0] + D('''  if(!state.trip.length){
    const img=k=>ISL[k]&&ISL[k].img?`<img src="${ISL[k].img}" alt="" loading="lazy">`:'<i class="ph"></i>';
    document.getElementById('tc-route').innerHTML=`<div class="tc-start"><h3>${T.start_h}</h3><p>${T.start_p}</p><div class="tc-pres">`+
      PRESETS.map((p,j)=>`<button type="button" class="tc-pre" data-preset="${j}">${img(p.t[1][0])}<span><b>${T[p.n]}</b>${p.t.map(x=>iname(x[0])).join(' · ')} · ${p.t.reduce((a,x)=>a+x[1],0)} ${T.nights}</span></button>`).join('')+`</div></div>`;
    document.getElementById('tc-quick').innerHTML='';
    document.getElementById('tc-summary').innerHTML=`<div class="tc-k">${T.estimate}</div><div class="tc-pp2" style="margin-top:6px">${T.empty_trip}</div>`;
    {const st=document.getElementById('tc-stick');if(st)st.classList.remove('on');}
    renderSwaps();sync();return;
  }''') + s[a1:]

# ---- JS: island rows
a0 = s.index("    h+=`<div class=\"tc-card\">")
a1 = s.index("    const next=state.trip[i+1];", a0)
s = s[:a0] + D('''    const open=OPEN.has(t.k);
    const vlab={'':T.veh_walk,m:T.veh_scoot,c:T.veh_hire}[t.v||''];
    const sp=x=>[x.split(' ')[0],x.split(' ').slice(1).join(' ')];
    const vbtn=isl.car?(state.own?`<button type="button" class="tc-vc" disabled title="${T.veh_ownc_t}">${sp(T.veh_ownc)[0]}<span class="vl"> ${sp(T.veh_ownc)[1]}</span></button>`
      :`<button type="button" class="tc-vc" data-a="vc" data-i="${i}" title="${T.cyc_t}">${sp(vlab)[0]}<span class="vl"> ${sp(vlab)[1]}</span></button>`):'';
    h+=`<div class="tc-row${open?' open':''}">
      <div class="tc-rh" data-a="tog" data-i="${i}" role="button" tabindex="0" aria-expanded="${open}" title="${T.row_t}">
        ${isl.img?`<img src="${isl.img}" alt="" loading="lazy">`:'<i class="ph"></i>'}
        <div class="tc-rn"><b>${iname(t.k)}<span class="chev" aria-hidden="true">▾</span></b><small>${eur(rnd(rn))}${T.per_night}${ld?' · '+fmtD(ld[0])+' – '+fmtD(ld[1]):''}${isl.boat?' · <i>'+(t.b?'✓ ':'⛵ ')+T.boat_avail+'</i>':''}</small></div>
      </div>
      <span class="tc-n"><button type="button" data-a="n-" data-i="${i}" aria-label="${(LANG==='el'?'Μία νύχτα λιγότερη: ':'One night fewer: ')+iname(t.k)}">−</button><b>${t.n}</b><span class="tc-nl">${t.n===1?T.night:T.nights}</span><button type="button" data-a="n+" data-i="${i}" aria-label="${(LANG==='el'?'Μία νύχτα ακόμα: ':'One more night: ')+iname(t.k)}">+</button></span>
      ${vbtn}
      <button class="tc-x" data-a="rm" data-i="${i}" title="${T.remove}">✕</button>
    </div>`;
    if(open){h+=`<div class="tc-exp">
      ${isl.boat?`<div><button type="button" role="switch" aria-checked="${t.b?'true':'false'}" class="tc-sw ${t.b?'on':''}" data-a="boat" data-i="${i}"><span class="s" aria-hidden="true"></span> ${LANG==='el'?(isl.boat.nel||T.boat_day):(isl.boat.n||T.boat_day)}</button><span class="amt">€${isl.boat.pp} pp</span></div>`:''}
      <div>${T.rooms_l}<a href="${bookUrl(i)}" target="_blank" rel="noopener sponsored">${T.see_prices}</a></div>
      <div>${T.guide_l.replace('{isl}',iname(t.k))}<a href="${guide}">${T.open_l}</a></div></div>`;}
    if(state.own&&NO_CAR[t.k])h+=`<div class="tc-warn">🚫 ${T.no_car_note.replace('{isl}',iname(t.k))}</div>`;
    if(!state.own&&!t.v&&isl.cn>=4&&isl.car)h+=`<div class="tc-warn">${T.carless_note.replace('{n}',iname(t.k)).replace('{p}',Math.round((CFG.carless_central_premium-1)*100))}</div>`;
''') + s[a1:]

# ---- JS: summary (header, stacked bar, no per-line booking links)
rep("li+=line('⛴',T.li_ferries,`${{portsTxt}}${{legs.filter(([a,b])=>!legInfo(a,b).road).length}} ${{T.li_legs}} × ${{state.pax}} ${{T.li_pax}}`,fsum,SK?null:T.book_ferry,'https://www.ferryhopper.com/'+(LANG==='el'?'el/':'en/'),SK);",
    "li+=line('⛴',T.li_ferries,`${{portsTxt}}${{legs.filter(([a,b])=>!legInfo(a,b).road).length}} ${{T.li_legs}} × ${{state.pax}} ${{T.li_pax}}`,fsum,null,null,SK);")
rep(",rsum,state.trip.length===1?T.book_room:null,state.trip.length===1?bookUrl(0):null);", ",rsum,null,null);")
rep(",csum,T.book_car,'https://www.discovercars.com/?a_aid=antaran2');tot+=csum;", ",csum,null,null);tot+=csum;")
rep("  let csum=0,cd=0,fuelSum=0;", "  csumAll=0;let csum=0,cd=0,fuelSum=0;")
rep("  if(cd){{li+=line('🚗'", "  csumAll=csum+fuelSum;\n  if(cd){{li+=line('🚗'")
rep("  const nightsTotal=state.trip.reduce((a,t)=>a+t.n,0);\n  let tot=0,li='';",
    "  const nightsTotal=state.trip.reduce((a,t)=>a+t.n,0);\n  let tot=0,li='',csumAll=0;")
a0 = s.index("  document.getElementById('tc-summary').innerHTML=`\n    <h2>${{T.estimate}}</h2>")
a1 = s.index("    ${{li}}", a0)
s = s[:a0] + D('''  {const tr=Math.max(0,tot-rsum-msum-csumAll-bsum);
   const cat=[['#0B8FAC',rsum],['#E8522A',msum],['#3D8B6F',tr],['#C98A00',csumAll],['#8A7AA0',bsum]].filter(x=>x[1]>0);
   const ct=cat.reduce((a,x)=>a+x[1],0)||1;
   window._tcStk=cat.map(x=>`<i style="width:${(x[1]/ct*100).toFixed(1)}%;background:${x[0]}"></i>`).join('');}
  document.getElementById('tc-summary').innerHTML=`
    <div class="tc-k">${T.trip_k} · ${nightsTotal} ${T.nights} · ${state.pax} ${T.li_pax}</div>
    <div class="tc-big">${eur(rnd(tot))}</div>
    <div class="tc-pp2">${eur(rnd(tot/state.pax))} ${T.pp} · ${whenTxt} · ${({budget:T.tier_budget,mid:T.tier_mid,comfort:T.tier_comfort})[state.tier]}<br><small>${state.fly?T.total_fly:T.total}</small></div>
    <div class="tc-stk">${window._tcStk}</div>
''') + s[a1:]

# ---- JS: presets + open rows, events
rep("const QUICK=['santorini','milos','ios','folegandros','sifnos'];",
    "const QUICK=['santorini','milos','ios','folegandros','sifnos'];\n" + D('''const PRESETS=[{n:'p1',t:[['naxos',4],['paros',3],['santorini',3]]},{n:'p2',t:[['naxos',3],['koufonisia',3],['iraklia',3]]},
  {n:'p3',t:[['aegina',2],['poros',2],['hydra',2]]},{n:'p4',t:[['rhodes',4],['symi',2],['kos',4]]}].filter(p=>p.t.every(x=>ISL[x[0]]));
const OPEN=new Set();'''))
a0 = s.index("document.getElementById('tc-skip').addEventListener")
a1 = s.index("document.getElementById('tc-pax-minus')")
s = s[:a0] + D('''document.getElementById('tc-own').addEventListener('click',()=>{state.own=!state.own;if(state.own)state.fly=false;render();});
document.getElementById('tc-more-btn').addEventListener('click',e=>{const m=document.getElementById('tc-more');m.hidden=!m.hidden;e.currentTarget.setAttribute('aria-expanded',String(!m.hidden));});
document.getElementById('tc-gt').addEventListener('click',e=>{
  const o=e.target.closest('.tc-chip');if(!o||o.classList.contains('off'))return;
  const g=o.dataset.gt;state.skip=g==='skip';if(g==='fly'){state.fly=true;state.own=false;}else if(g==='ferry')state.fly=false;
  render();});
''') + s[a1:]
rep("  else if(el.dataset.a==='veh'){{if(el.dataset.v==='own'){{state.own=true;state.fly=false;}}else{{state.own=false;t.v=el.dataset.v;}}}}",
    "  else if(el.dataset.a==='veh'){{if(el.dataset.v==='own'){{state.own=true;state.fly=false;}}else{{state.own=false;t.v=el.dataset.v;}}}}\n"
    "  else if(el.dataset.a==='vc')t.v={{'':'m',m:'c',c:''}}[t.v||''];\n"
    "  else if(el.dataset.a==='tog'){{OPEN.has(t.k)?OPEN.delete(t.k):OPEN.add(t.k);}}")
rep("  else if(el.dataset.a==='rm')state.trip.splice(i,1);\n  render();}});",
    "  else if(el.dataset.a==='rm')state.trip.splice(i,1);\n  render();}});\n"
    + D('''document.getElementById('tc-route').addEventListener('keydown',e=>{const el=e.target.closest('[data-a="tog"]');if(el&&(e.key==='Enter'||e.key===' ')){e.preventDefault();el.click();}});
document.getElementById('tc-route').addEventListener('click',e=>{const b=e.target.closest('[data-preset]');if(!b)return;
  const p=PRESETS[+b.dataset.preset];state.trip=p.t.map(x=>({k:x[0],n:x[1],v:'',b:false}));render();});'''))
# the old radio handler (.tc-gopt) goes
if "// Getting there: Ferry or Fly." in s:
    a0 = s.index("// Getting there: Ferry or Fly.")
    a1 = s.index("  render();}});", a0) + len("  render();}});")
    s = s[:a0] + s[a1:]
P.write_text(s, encoding='utf-8')
print('ok')
