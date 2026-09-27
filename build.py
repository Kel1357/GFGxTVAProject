#!/usr/bin/env python3
"""
build.py — generates the NEXUS PROTOCOL event site.

Reads event_data.json (content only — no markup) and renders it into a
single self-contained index.html (HTML + CSS + JS inline). Run:

    python3 build.py

Output: index.html in the same folder.
"""
import base64
import json
import pathlib

HERE = pathlib.Path(__file__).parent
DATA = json.loads((HERE / "event_data.json").read_text(encoding="utf-8"))

CLOCK_ART_DATA = "data:image/png;base64," + base64.b64encode((HERE / "tva_clock.png").read_bytes()).decode("ascii")
GOS_IMAGE_DATA = "data:image/png;base64," + base64.b64encode((HERE / "tva_god_of_stories.png").read_bytes()).decode("ascii")
SYLVIE_IMAGE_DATA = "data:image/png;base64," + base64.b64encode((HERE / "tva_sylvie.png").read_bytes()).decode("ascii")
LOKI_LAUFEYSON_IMAGE_DATA = "data:image/png;base64," + base64.b64encode((HERE / "tva_loki_laufeyson.png").read_bytes()).decode("ascii")
CLASSIC_LOKI_IMAGE_DATA = "data:image/png;base64," + base64.b64encode((HERE / "tva_classic_loki.png").read_bytes()).decode("ascii")
FROST_GIANT_LOKI_IMAGE_DATA = "data:image/png;base64," + base64.b64encode((HERE / "tva_frost_giant_loki_enhanced.png").read_bytes()).decode("ascii")
TOUR_DE_FRANCE_LOKI_IMAGE_DATA = "data:image/png;base64," + base64.b64encode((HERE / "tva_tour_de_france_loki_enhanced.png").read_bytes()).decode("ascii")


def esc(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


# ---------------------------------------------------------------------------
# Render repeating blocks from JSON data
# ---------------------------------------------------------------------------

def render_stats(stats):
    out = []
    for s in stats:
        out.append(f"""
        <div class="stat">
          <span class="stat__value">{esc(s['value'])}<span class="stat__unit">{esc(s['unit'])}</span></span>
          <span class="stat__label">{esc(s['label'])}</span>
        </div>""")
    return "".join(out)


def render_tracks(tracks):
    out = []
    for t in tracks:
        out.append(f"""
        <article class="file" tabindex="0">
          <div class="file__tab">
            <span class="file__code">{esc(t['code'])}</span>
            <span class="file__stamp">OPEN</span>
          </div>
          <h3 class="file__name">{esc(t['name'])}</h3>
          <p class="file__desc">{esc(t['desc'])}</p>
        </article>""")
    return "".join(out)


def render_timeline(items):
    out = []
    for i, item in enumerate(items):
        side = "left" if i % 2 == 0 else "right"
        out.append(f"""
        <div class="tl__node tl__node--{side}">
          <div class="tl__dot"></div>
          <div class="tl__card">
            <span class="tl__time">{esc(item['time'])}</span>
            <h4 class="tl__title">{esc(item['title'])}</h4>
            <p class="tl__desc">{esc(item['desc'])}</p>
          </div>
        </div>""")
    return "".join(out)


def render_faq(items):
    out = []
    for i, item in enumerate(items):
        out.append(f"""
        <div class="faq__item">
          <button class="faq__q" aria-expanded="false">
            <span>{esc(item['q'])}</span>
            <span class="faq__icon" aria-hidden="true"></span>
          </button>
          <div class="faq__a"><p>{esc(item['a'])}</p></div>
        </div>""")
    return "".join(out)


ev = DATA["event"]

CSS = r"""
:root{
  --bg:#0e0b08;
  --bg-soft:#161009;
  --paper:#e9ddc0;
  --paper-dim:#d9cba8;
  --ink:#221a10;
  --cream:#f4ecd7;
  --amber:#e8a33d;
  --amber-deep:#b9761f;
  --rust:#b0432a;
  --teal:#3c6e64;
  --line: rgba(233,221,192,0.14);
  --font-display:"Fraunces", Georgia, serif;
  --font-mono:"IBM Plex Mono", ui-monospace, Menlo, monospace;
  --safe-t: env(safe-area-inset-top,0px);
  --safe-b: env(safe-area-inset-bottom,0px);
  color-scheme: dark;
}
*{box-sizing:border-box;}
html{scroll-behavior:smooth; scroll-padding-top:78px;}
html,body{margin:0; padding:0;}
body{
  background:var(--bg);
  color:var(--cream);
  font-family:var(--font-mono);
  font-size:15px;
  line-height:1.6;
  -webkit-font-smoothing:antialiased;
  overflow-x:hidden;
  padding-top:var(--safe-t);
  padding-bottom:var(--safe-b);
}
img{max-width:100%; display:block;}
a{color:inherit;}
h1,h2,h3,h4{font-family:var(--font-display); margin:0; font-weight:600; letter-spacing:-0.01em;}
p{margin:0;}
.tag{
  display:inline-block;
  font-family:var(--font-mono);
  font-size:12px;
  letter-spacing:.08em;
  color:var(--amber);
  border:1px solid var(--amber-deep);
  padding:5px 10px;
  border-radius:2px;
  margin-bottom:18px;
  background:rgba(232,163,61,0.06);
}
.tag--light{color:var(--ink); border-color:var(--ink); background:rgba(34,26,16,0.06);}

/* texture overlays */
.grain{
  position:fixed; inset:0; pointer-events:none; z-index:40; opacity:.05; mix-blend-mode:overlay;
  background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='90' height='90'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='2' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
}
.scanline{
  position:fixed; inset:0; pointer-events:none; z-index:41; opacity:.035;
  background:repeating-linear-gradient(to bottom, transparent 0 2px, #000 2px 4px);
  mix-blend-mode:multiply;
}


/* ---------- cinematic atmosphere (visual-only pass; layout/design unchanged) ---------- */
.cinema-vignette{
  position:fixed; inset:0; pointer-events:none; z-index:38;
  background:
    radial-gradient(ellipse at center, transparent 42%, rgba(0,0,0,.16) 72%, rgba(0,0,0,.42) 100%);
  opacity:.78;
}
.cinema-light{
  position:fixed; inset:-18%; pointer-events:none; z-index:39;
  background:radial-gradient(circle at var(--cinema-x,50%) var(--cinema-y,28%), rgba(232,163,61,.13), transparent 24%);
  mix-blend-mode:screen; opacity:.52;
  filter:blur(26px);
  transition:opacity .7s ease;
}
.cinema-light::after{
  content:""; position:absolute; inset:0;
  background:linear-gradient(105deg, transparent 25%, rgba(244,236,215,.025) 48%, transparent 64%);
  transform:translateX(-45%);
  animation:cinemaSweep 12s ease-in-out infinite;
}
@keyframes cinemaSweep{
  0%,18%{transform:translateX(-55%);opacity:0;}
  30%{opacity:.7;}
  52%{transform:translateX(55%);opacity:.15;}
  70%,100%{transform:translateX(80%);opacity:0;}
}

.hero__branches{
  transform:translate3d(var(--branch-drift-x,0px),var(--branch-drift-y,0px),0) scale(1.015);
  transform-origin:center;
  transition:transform .9s cubic-bezier(.2,.7,.2,1);
  will-change:transform;
}
.hero__inner{will-change:transform,filter;}
.hero::after{
  content:""; position:absolute; inset:0; pointer-events:none; z-index:1;
  background:radial-gradient(ellipse at 50% 42%, transparent 24%, rgba(14,11,8,.22) 78%, rgba(14,11,8,.48) 100%);
}

/* Slow, almost imperceptible motion makes the existing surfaces feel photographed rather than static. */
.tva-panel{
  isolation:isolate;
}
.tva-panel::after{
  content:""; position:absolute; top:-20%; bottom:-20%; left:-45%; width:22%;
  pointer-events:none; z-index:3;
  background:linear-gradient(90deg, transparent, rgba(244,236,215,.055), transparent);
  transform:skewX(-12deg) translateX(0);
  animation:panelSweep 11s ease-in-out infinite;
}
@keyframes panelSweep{
  0%,55%{transform:skewX(-12deg) translateX(0);opacity:0;}
  62%{opacity:1;}
  76%,100%{transform:skewX(-12deg) translateX(720%);opacity:0;}
}
.tva-clock::before{
  animation:clockOrbit 22s linear infinite;
}
.tva-clock::after{
  animation:clockBreath 4.8s ease-in-out infinite;
}
@keyframes clockOrbit{to{transform:rotate(360deg);}}
@keyframes clockBreath{0%,100%{opacity:.55;}50%{opacity:1;}}
.tva-clock__hand--second{filter:drop-shadow(0 0 5px rgba(176,67,42,.35));}
.tva-live-dot i{animation:pulse 1.2s ease-in-out infinite, liveGlow 2.8s ease-in-out infinite;}
@keyframes liveGlow{0%,100%{box-shadow:0 0 8px rgba(232,163,61,.35);}50%{box-shadow:0 0 20px rgba(232,163,61,.9);}}

/* A tiny cinematic focus shift as sections enter the viewport. */
.cinema-focus{
  animation:cinemaFocus .9s cubic-bezier(.2,.7,.2,1) both;
}
@keyframes cinemaFocus{
  from{filter:brightness(.86) saturate(.82);}
  to{filter:brightness(1) saturate(1);}
}

@media (prefers-reduced-motion: reduce){
  .cinema-light,.cinema-light::after,.tva-panel::after,.tva-clock::before,.tva-clock::after,.tva-live-dot i{animation:none !important;}
  .hero__branches{transform:none;transition:none;}
}

/* ---------- top bar ---------- */
.bar{
  position:fixed; top:var(--safe-t); left:0; right:0; z-index:50;
  display:flex; align-items:center; gap:28px;
  padding:16px 32px;
  background:linear-gradient(to bottom, rgba(14,11,8,0.92), rgba(14,11,8,0.75));
  backdrop-filter:blur(6px);
  border-bottom:1px solid var(--line);
}
.bar__seal{display:flex; align-items:center; gap:8px; color:var(--amber);}
.seal__ring{width:26px; height:26px;}
.bar__mark{font-family:var(--font-mono); font-size:12px; letter-spacing:.12em; font-weight:600;}
.bar__nav{display:flex; gap:24px; margin-left:12px; flex:1;}
.bar__nav a{font-size:13px; letter-spacing:.03em; opacity:.8; text-decoration:none; position:relative; padding-bottom:3px;}
.bar__nav a:hover{opacity:1;}
.bar__nav a::after{content:""; position:absolute; left:0; right:100%; bottom:0; height:1px; background:var(--amber); transition:right .25s ease;}
.bar__nav a:hover::after{right:0;}
.bar__cta{
  font-size:12px; letter-spacing:.05em; text-decoration:none;
  border:1px solid var(--amber); color:var(--amber);
  padding:9px 16px; border-radius:2px; white-space:nowrap;
  transition:background .2s ease, color .2s ease;
}
.bar__cta:hover{background:var(--amber); color:var(--bg);}
.bar__burger{display:none; flex-direction:column; gap:5px; background:none; border:none; padding:6px; cursor:pointer;}
.bar__burger span{width:20px; height:2px; background:var(--cream);}
.mobilenav{
  position:fixed; top:60px; right:12px; z-index:49;
  background:var(--bg-soft); border:1px solid var(--line); border-radius:4px;
  display:none; flex-direction:column; padding:10px 0; min-width:180px;
  transform:translateY(-8px); opacity:0; pointer-events:none; transition:.2s ease;
}
.mobilenav.is-open{transform:translateY(0); opacity:1; pointer-events:auto;}
.mobilenav a{padding:10px 18px; text-decoration:none; font-size:13px; letter-spacing:.03em;}
.mobilenav a:hover{background:rgba(232,163,61,0.08); color:var(--amber);}

/* ---------- hero ---------- */
.hero{
  position:relative;
  min-height:100svh;
  display:flex; flex-direction:column; align-items:center; justify-content:center;
  text-align:center;
  padding:120px 24px 80px;
  overflow:hidden;
  background:
    radial-gradient(ellipse at 50% 18%, rgba(232,163,61,0.14), transparent 55%),
    var(--bg);
}
.hero__branches{position:absolute; inset:0; width:100%; height:100%; z-index:0; opacity:.9;}
.hero__inner{position:relative; z-index:2; max-width:760px;}
.hero__case{
  font-size:12px; letter-spacing:.14em; color:var(--amber-deep);
  margin:0 0 22px; text-transform:uppercase;
}
.hero__title{
  font-size:clamp(40px, 8vw, 84px);
  line-height:.98;
  color:var(--cream);
}
.hero__title .line{display:block;}
.hero__variant{color:var(--amber); font-style:italic; font-weight:500;}
.hero__tagline{
  font-family:var(--font-mono); font-size:15px; color:var(--paper-dim);
  max-width:480px; margin:26px auto 0; line-height:1.7;
}
.hero__meta{
  display:flex; flex-wrap:wrap; justify-content:center; gap:0;
  margin:40px auto 0; max-width:640px;
  border:1px solid var(--line); border-radius:3px; overflow:hidden;
}
.hero__metaitem{
  flex:1; min-width:160px; padding:14px 18px; text-align:left;
  border-right:1px solid var(--line);
  display:flex; flex-direction:column; gap:4px;
}
.hero__metaitem:last-child{border-right:none;}
.hero__metaitem span{font-size:10px; letter-spacing:.1em; text-transform:uppercase; color:var(--amber-deep);}
.hero__metaitem strong{font-family:var(--font-display); font-weight:600; font-size:15px; color:var(--cream);}
.hero__actions{display:flex; gap:14px; justify-content:center; margin:38px 0 0; flex-wrap:wrap;}
.btn{
  font-family:var(--font-mono); font-size:13px; letter-spacing:.05em;
  padding:14px 26px; border-radius:2px; text-decoration:none; cursor:pointer;
  border:1px solid transparent; display:inline-flex; align-items:center; justify-content:center;
  transition:transform .15s ease, background .2s ease, color .2s ease, border-color .2s ease;
}
.btn--primary{background:var(--amber); color:#1a1207; border-color:var(--amber); font-weight:600;}
.btn--primary:hover{background:var(--amber-deep); border-color:var(--amber-deep); transform:translateY(-1px);}
.btn--ghost{border-color:var(--line); color:var(--cream);}
.btn--ghost:hover{border-color:var(--amber); color:var(--amber);}
.btn--block{width:100%;}

.countdown{margin:52px auto 0; display:inline-block;}
.countdown__label{font-size:10px; letter-spacing:.14em; text-transform:uppercase; color:var(--amber-deep); margin-bottom:12px;}
.countdown__row{display:flex; gap:10px;}
.countdown__unit{
  background:var(--bg-soft); border:1px solid var(--line); border-radius:3px;
  padding:12px 16px; min-width:64px; display:flex; flex-direction:column; align-items:center; gap:4px;
}
.countdown__unit span{font-family:var(--font-display); font-size:26px; font-weight:600; color:var(--amber); font-variant-numeric:tabular-nums;}
.countdown__unit small{font-size:9px; letter-spacing:.1em; text-transform:uppercase; color:var(--paper-dim);}

.hero__scroll{
  position:absolute; bottom:28px; left:50%; transform:translateX(-50%);
  font-size:10px; letter-spacing:.12em; text-transform:uppercase; color:var(--amber-deep);
  display:flex; flex-direction:column; align-items:center; gap:8px; z-index:2;
}
.hero__scroll span{width:1px; height:34px; background:linear-gradient(to bottom, var(--amber), transparent); animation:scrolldrop 1.8s ease-in-out infinite;}
@keyframes scrolldrop{0%{opacity:0; transform:translateY(-6px);} 40%{opacity:1;} 100%{opacity:0; transform:translateY(10px);}}

/* ---------- TVA x NEXUS lore bridge ---------- */
.loki-bridge{padding:92px 32px 86px;max-width:1180px;margin:0 auto;position:relative;}
.loki-bridge::before{content:"";position:absolute;left:50%;top:0;width:1px;height:100%;background:linear-gradient(180deg,transparent,rgba(232,163,61,.22),transparent);opacity:.65;}
.loki-bridge__head{max-width:760px;margin:0 auto 38px;text-align:center;position:relative;z-index:1;}
.loki-bridge__head h2{font-size:clamp(27px,3.4vw,40px);line-height:1.12;color:var(--cream);margin:10px 0 12px;}
.loki-bridge__head p{max-width:62ch;margin:0 auto;color:var(--paper-dim);font-size:13px;line-height:1.75;}
.loki-bridge__grid{display:grid;grid-template-columns:repeat(3,1fr);gap:1px;background:var(--line);border:1px solid var(--line);position:relative;z-index:1;}
.loki-bridge__card{min-height:210px;padding:24px;background:rgba(14,11,8,.86);position:relative;overflow:hidden;}
.loki-bridge__card::after{content:"";position:absolute;inset:auto -20% 0;height:1px;background:linear-gradient(90deg,transparent,rgba(232,163,61,.55),transparent);transform:translateX(-20%);transition:.35s ease;}
.loki-bridge__card:hover::after{transform:translateX(20%);}
.loki-bridge__code{font-size:8px;letter-spacing:.14em;color:var(--amber-deep);text-transform:uppercase;}
.loki-bridge__card h3{font-family:var(--font-display);font-size:18px;color:var(--cream);margin:9px 0 10px;}
.loki-bridge__card p{font-size:12px;line-height:1.7;color:#9e927f;margin:0;}
.loki-bridge__card strong{color:var(--amber);font-weight:500;}
.loki-bridge__fact{margin-top:16px;padding-top:10px;border-top:1px solid rgba(232,163,61,.12);font-size:9px;line-height:1.55;color:#766956;text-transform:uppercase;letter-spacing:.06em;}
@media(max-width:900px){.loki-bridge{padding:72px 22px;}.loki-bridge__grid{grid-template-columns:1fr;}.loki-bridge::before{display:none;}}
/* ---------- briefing ---------- */
.briefing{padding:120px 32px 60px; max-width:1180px; margin:0 auto;}
.briefing__grid{display:grid; grid-template-columns:1.5fr 1fr; gap:60px; align-items:start;}
.briefing__doc h2{font-size:clamp(28px,3.6vw,42px); line-height:1.12; margin:0 0 22px; color:var(--cream);}
.briefing__doc p{font-size:14.5px; color:var(--paper-dim); max-width:62ch; margin-bottom:16px;}
.briefing__doc p:last-child{margin-bottom:0;}
.briefing__stamp{
  color:var(--rust); opacity:.85; justify-self:center; align-self:center;
  width:180px; transform:rotate(-9deg);
}
.stamptext{
  font-family:var(--font-mono); font-size:15px; letter-spacing:.06em; fill:currentColor; font-weight:700;
}

.stats{
  margin-top:80px; display:grid; grid-template-columns:repeat(4,1fr);
  border-top:1px solid var(--line); border-bottom:1px solid var(--line);
}
.stat{padding:30px 20px; border-right:1px solid var(--line); display:flex; flex-direction:column; gap:6px;}
.stat:last-child{border-right:none;}
.stat__value{font-family:var(--font-display); font-size:clamp(26px,3vw,38px); font-weight:600; color:var(--amber);}
.stat__unit{font-size:14px; margin-left:2px; color:var(--amber-deep);}
.stat__label{font-size:12px; color:var(--paper-dim); max-width:20ch;}

/* ---------- section head shared ---------- */
.section__head{max-width:640px; margin-bottom:56px;}
.section__head h2{font-size:clamp(28px,3.6vw,42px); line-height:1.12; color:var(--cream);}
.section__head--center{margin-left:auto; margin-right:auto; text-align:center;}

/* ---------- case files (tracks) ---------- */
.files{padding:100px 32px; max-width:1180px; margin:0 auto;}
.files__grid{display:grid; grid-template-columns:repeat(3,1fr); gap:1px; background:var(--line); border:1px solid var(--line);}
.file{
  background:var(--bg); padding:30px 26px; min-height:220px;
  display:flex; flex-direction:column; gap:14px;
  transition:background .25s ease;
  outline:none;
}
.file:hover, .file:focus-visible{background:var(--bg-soft);}
.file__tab{display:flex; justify-content:space-between; align-items:center;}
.file__code{font-size:12px; letter-spacing:.1em; color:var(--amber-deep); font-weight:600;}
.file__stamp{
  font-size:9px; letter-spacing:.1em; color:var(--teal); border:1px solid var(--teal);
  padding:3px 8px; border-radius:2px; opacity:0; transform:translateX(4px);
  transition:opacity .25s ease, transform .25s ease;
}
.file:hover .file__stamp, .file:focus-visible .file__stamp{opacity:1; transform:translateX(0);}
.file__name{font-size:19px; color:var(--cream); font-weight:600;}
.file__desc{font-size:13.5px; color:var(--paper-dim); line-height:1.65;}

/* ---------- timeline ---------- */
.tl{padding:100px 32px 60px; max-width:980px; margin:0 auto;}
.tl__spine{position:relative; padding:20px 0;}
.tl__spine::before{
  content:""; position:absolute; left:50%; top:0; bottom:0; width:1px;
  background:linear-gradient(to bottom, transparent, var(--amber-deep) 8%, var(--amber-deep) 92%, transparent);
  transform:translateX(-50%);
}
.tl__node{position:relative; width:50%; padding:0 44px 64px; }
.tl__node--left{left:0; text-align:right;}
.tl__node--right{left:50%; text-align:left;}
.tl__dot{
  position:absolute; top:4px; width:9px; height:9px; border-radius:50%;
  background:var(--amber); box-shadow:0 0 0 4px rgba(232,163,61,0.18);
}
.tl__node--left .tl__dot{right:-4.5px;}
.tl__node--right .tl__dot{left:-4.5px;}
.tl__time{font-size:11px; letter-spacing:.08em; color:var(--amber-deep); display:block; margin-bottom:6px;}
.tl__title{font-size:18px; color:var(--cream); margin-bottom:6px;}
.tl__desc{font-size:13px; color:var(--paper-dim); line-height:1.6;}

/* ---------- recruit ---------- */
.recruit{background:var(--paper); color:var(--ink); padding:110px 32px;}
.recruit__grid{max-width:1180px; margin:0 auto; display:grid; grid-template-columns:1fr 1fr; gap:70px; align-items:start;}
.recruit__copy h2{font-size:clamp(28px,3.4vw,40px); line-height:1.14; margin:0 0 16px; color:var(--ink);}
.recruit__copy > p{font-size:14.5px; color:#4b4026; max-width:50ch; margin-bottom:36px;}

.faq__item{border-top:1px solid rgba(34,26,16,0.18);}
.faq__item:last-child{border-bottom:1px solid rgba(34,26,16,0.18);}
.faq__q{
  width:100%; display:flex; justify-content:space-between; align-items:center; gap:16px;
  background:none; border:none; text-align:left; font-family:var(--font-mono);
  font-size:14px; font-weight:600; color:var(--ink); padding:18px 2px; cursor:pointer;
}
.faq__icon{position:relative; width:14px; height:14px; flex:none;}
.faq__icon::before, .faq__icon::after{content:""; position:absolute; background:var(--ink); top:50%; left:50%; transform:translate(-50%,-50%);}
.faq__icon::before{width:14px; height:1.4px;}
.faq__icon::after{width:1.4px; height:14px; transition:transform .2s ease;}
.faq__q[aria-expanded="true"] .faq__icon::after{transform:translate(-50%,-50%) rotate(90deg) scaleX(0);}
.faq__a{max-height:0; overflow:hidden; transition:max-height .3s ease;}
.faq__a p{font-size:13.5px; color:#4b4026; padding:0 2px 18px; max-width:52ch; line-height:1.65;}

.recruit__form{
  background:var(--bg); color:var(--cream); border-radius:4px; padding:34px 32px;
  border:1px solid #3a2f1c;
}
.recruit__formhead{margin-bottom:22px;}
.form__casecode{font-size:11px; letter-spacing:.1em; color:var(--amber-deep);}
.recruit__formhead h3{font-size:22px; color:var(--cream); margin-top:6px;}
.field{display:flex; flex-direction:column; gap:6px; margin-bottom:16px; font-size:12px;}
.field span{letter-spacing:.05em; color:var(--paper-dim);}
.field input, .field select{
  background:var(--bg-soft); border:1px solid var(--line); color:var(--cream);
  padding:11px 12px; border-radius:2px; font-family:var(--font-mono); font-size:13.5px;
  outline:none; transition:border-color .2s ease;
}
.field input:focus, .field select:focus{border-color:var(--amber);}
.field--row{flex-direction:row; gap:14px; margin-bottom:0;}
.field--row .field{flex:1; margin-bottom:16px;}
.recruit__form .btn--block{margin-top:8px; position:relative; overflow:hidden;}
.btn__stamped{display:none;}
.recruit__form.is-sent .btn__label{display:none;}
.recruit__form.is-sent .btn__stamped{display:inline-flex;}
.recruit__form.is-sent .btn--primary{background:var(--teal); border-color:var(--teal); color:var(--cream);}
.recruit__note{font-size:11px; color:var(--paper-dim); opacity:.7; margin-top:12px; line-height:1.6;}

/* ---------- footer ---------- */
.foot{padding:50px 32px 40px; max-width:1180px; margin:0 auto;}
.foot__top{display:flex; justify-content:space-between; align-items:flex-end; flex-wrap:wrap; gap:24px; padding-bottom:28px; border-bottom:1px solid var(--line);}
.foot__brand p{font-size:13px; color:var(--paper-dim); margin-top:8px; max-width:32ch;}
.foot__links{display:flex; gap:22px;}
.foot__links a{font-size:12.5px; text-decoration:none; opacity:.75;}
.foot__links a:hover{opacity:1; color:var(--amber);}
.foot__bottom{display:flex; justify-content:space-between; padding-top:20px; font-size:11px; letter-spacing:.08em; color:var(--amber-deep); text-transform:uppercase;}

/* ---------- reveal-on-scroll ---------- */
.reveal{opacity:0; transform:translateY(18px); transition:opacity .7s ease, transform .7s ease;}
.reveal.is-visible{opacity:1; transform:translateY(0);}

@media (prefers-reduced-motion: reduce){
  *{animation-duration:.001ms !important; animation-iteration-count:1 !important; transition-duration:.001ms !important; scroll-behavior:auto !important;}
}

/* ---------- responsive ---------- */
@media (max-width:900px){
  .briefing__grid{grid-template-columns:1fr;}
  .briefing__stamp{justify-self:start; margin-top:20px;}
  .files__grid{grid-template-columns:repeat(2,1fr);}
  .stats{grid-template-columns:repeat(2,1fr);}
  .stat:nth-child(2){border-right:none;}
  .stat{border-bottom:1px solid var(--line);}
  .recruit__grid{grid-template-columns:1fr; gap:50px;}
}
@media (max-width:720px){
  .bar__nav{display:none;}
  .bar__cta{display:none;}
  .bar__burger{display:flex;}
  .mobilenav{display:flex;}
  .hero{padding-top:110px;}
  .hero__meta{flex-direction:column;}
  .hero__metaitem{border-right:none; border-bottom:1px solid var(--line); text-align:center; align-items:center;}
  .hero__metaitem:last-child{border-bottom:none;}
  .files__grid{grid-template-columns:1fr;}
  .tl__spine::before{left:14px;}
  .tl__node, .tl__node--left, .tl__node--right{width:100%; left:0; text-align:left; padding:0 0 44px 40px;}
  .tl__node--left .tl__dot, .tl__node--right .tl__dot{left:9.5px; right:auto;}
  .field--row{flex-direction:column; gap:0;}
  .foot__bottom{flex-direction:column; gap:6px;}
}


/* ================= LOKI TVA EASTER-EGG LAYER ================= */
.tva-easter-hint{position:relative;cursor:help}
.tva-easter-hint::after{content:"";position:absolute;left:50%;bottom:calc(100% + 8px);transform:translate(-50%,4px);opacity:0;pointer-events:none;white-space:nowrap;padding:5px 8px;border:1px solid rgba(232,163,61,.22);background:#0b0906;color:var(--amber);font:7px var(--font-mono);letter-spacing:.1em;text-transform:uppercase;transition:.18s ease;z-index:80}
.tva-easter-hint:hover::after,.tva-easter-hint:focus-visible::after{opacity:1;transform:translate(-50%,0)}
.tva-easter-console{position:fixed;right:22px;bottom:22px;width:min(330px,calc(100vw - 44px));z-index:180;pointer-events:none;opacity:0;transform:translateY(14px);transition:.35s ease}
.tva-easter-console.is-visible{opacity:1;transform:none}
.tva-easter-console__inner{border:1px solid rgba(232,163,61,.35);background:rgba(12,9,6,.94);box-shadow:0 18px 55px rgba(0,0,0,.6),inset 0 0 30px rgba(232,163,61,.035);padding:13px}
.tva-easter-console__head{display:flex;justify-content:space-between;gap:10px;color:var(--amber);font:7px var(--font-mono);letter-spacing:.14em;text-transform:uppercase}
.tva-easter-console__body{margin-top:9px;color:var(--paper-dim);font:9px/1.65 var(--font-mono)}
.tva-easter-console__body b{color:var(--cream);font-weight:500}
.tva-easter-console__sig{display:inline-block;margin-top:8px;color:var(--amber);font-size:7px;letter-spacing:.12em}
.tva-artifact{position:relative}
.tva-artifact::before{content:"CLASSIFIED TVA ARTIFACT";position:absolute;top:8px;right:8px;color:rgba(232,163,61,.18);font:6px var(--font-mono);letter-spacing:.13em;pointer-events:none;transform:rotate(-4deg)}
.tva-hidden-trigger{position:relative}
.tva-hidden-trigger::after{content:"?";position:absolute;right:7px;top:7px;width:13px;height:13px;border:1px solid rgba(232,163,61,.18);border-radius:50%;display:grid;place-items:center;color:rgba(232,163,61,.32);font:7px var(--font-mono);opacity:.35;transition:.2s}
.tva-hidden-trigger:hover::after{opacity:1;color:var(--amber);border-color:rgba(232,163,61,.5);box-shadow:0 0 14px rgba(232,163,61,.12)}
@media(max-width:720px){.tva-easter-console{right:12px;bottom:12px;width:calc(100vw - 24px)}}

/* ================= creative pass ================= */

/* custom cursor (desktop, fine-pointer only) */
html.has-cursor, html.has-cursor body{cursor:none;}
html.has-cursor a, html.has-cursor button, html.has-cursor input,
html.has-cursor select, html.has-cursor .file, html.has-cursor .faq__q{cursor:none;}
.cursor{
  position:fixed; top:0; left:0; width:16px; height:16px; border-radius:50%;
  border:1px solid var(--amber); pointer-events:none; z-index:200;
  transform:translate(-50%,-50%); transition:width .18s ease, height .18s ease, border-color .18s ease, background .18s ease;
  mix-blend-mode:screen;
}
.cursor::after{
  content:""; position:absolute; inset:0; margin:auto; width:2px; height:2px; border-radius:50%; background:var(--amber);
}
.cursor.is-hover{width:44px; height:44px; background:rgba(232,163,61,0.08);}
.emberCanvas{position:fixed; inset:0; pointer-events:none; z-index:199;}
@media (hover:none), (pointer:coarse){
  .cursor, .emberCanvas{display:none;}
}

/* HUD ticker */
.ticker{
  position:relative; overflow:hidden; border-top:1px solid var(--line); border-bottom:1px solid var(--line);
  background:var(--bg-soft); padding:12px 0;
}
.ticker__track{
  display:flex; width:max-content; gap:60px; white-space:nowrap;
  animation:tickermove 32s linear infinite;
}
.ticker__track span{
  font-size:11px; letter-spacing:.12em; text-transform:uppercase; color:var(--amber-deep);
  display:inline-flex; align-items:center; gap:10px;
}
.ticker__track span::before{content:"◆"; font-size:8px; color:var(--amber);}
.ticker__live{color:var(--amber) !important; font-weight:600;}
@keyframes tickermove{
  from{transform:translateX(0);}
  to{transform:translateX(-50%);}
}
@media (prefers-reduced-motion: reduce){
  .ticker__track{animation:none;}
}

/* redacted text (briefing) */
.redact{
  position:relative; cursor:pointer; display:inline; border-radius:2px;
}
.redact__bar{
  position:absolute; inset:-1px -3px; background:var(--ink); background:#1c150c;
  border-radius:2px; transition:opacity .35s ease, transform .35s ease;
  transform-origin:left center;
}
.redact.is-open .redact__bar{opacity:0; transform:scaleX(0.02);}
.redact:hover .redact__bar, .redact:focus-visible .redact__bar{opacity:0; transform:scaleX(0.02);}
.redact__tag{
  font-size:9px; letter-spacing:.08em; color:var(--rust); opacity:0; vertical-align:super;
  transition:opacity .3s ease .1s; margin-left:3px;
}
.redact.is-open .redact__tag, .redact:hover .redact__tag{opacity:1;}

/* card tilt (JS sets --rx/--ry) */
.file{
  --rx:0deg; --ry:0deg;
  transform:perspective(700px) rotateX(var(--rx)) rotateY(var(--ry));
  transition:transform .25s ease, background .25s ease;
  will-change:transform;
}

/* magnetic buttons: JS sets --mx/--my */
.btn--primary, .bar__cta{
  --mx:0px; --my:0px;
  transform:translate(var(--mx), var(--my));
}
.btn--primary{transition:transform .18s cubic-bezier(.2,.7,.3,1), background .2s ease, border-color .2s ease;}
.bar__cta{transition:transform .18s cubic-bezier(.2,.7,.3,1), background .2s ease, color .2s ease;}

/* hero glitch word */
.glitch{position:relative; display:inline-block;}
.glitch__ghost{
  position:absolute; left:0; top:0; width:100%; height:100%;
  opacity:0; pointer-events:none;
}
.glitch.is-glitching .glitch__ghost--cyan{
  opacity:.75; color:#5fd5e0; transform:translate(-3px,1px); mix-blend-mode:screen;
}
.glitch.is-glitching .glitch__ghost--red{
  opacity:.75; color:#e0505a; transform:translate(3px,-1px); mix-blend-mode:screen;
}
.glitch.is-glitching{animation:glitchjitter .18s steps(2) 2;}
@keyframes glitchjitter{
  0%{transform:translate(0,0);}
  50%{transform:translate(-1px,1px);}
  100%{transform:translate(0,0);}
}

/* torn paper seam where recruit (light) meets the void above */
.recruit{position:relative;}
.recruit::before{
  content:""; position:absolute; top:0; left:0; right:0; height:14px; transform:translateY(-13px);
  background:
    linear-gradient(135deg, var(--paper) 50%, transparent 50%) 0 0/16px 16px repeat-x,
    linear-gradient(-135deg, var(--paper) 50%, transparent 50%) 0 0/16px 16px repeat-x;
  background-position:0 0, 8px 0;
}

/* live variant counter accent */
.stat__live{
  display:inline-flex; align-items:center; gap:5px; font-size:9px; letter-spacing:.1em;
  color:var(--amber); margin-top:2px; text-transform:uppercase;
}
.stat__live i{
  width:5px; height:5px; border-radius:50%; background:var(--amber); display:inline-block;
  animation:pulse 1.6s ease-in-out infinite;
}
@keyframes pulse{0%,100%{opacity:1;} 50%{opacity:.25;}}




/* ================= TVA CINEMATIC ACCESS OPENING ================= */
.tva-gate{overflow:hidden;}
.tva-gate__prelude{
  position:absolute; inset:0; z-index:12; display:grid; place-items:center;
  background:#070604; color:var(--amber); overflow:hidden;
  transition:opacity .9s ease, visibility .9s ease;
}
.tva-gate__prelude::before{
  content:""; position:absolute; inset:0; opacity:.35;
  background:
    repeating-linear-gradient(0deg, transparent 0 3px, rgba(232,163,61,.035) 3px 4px),
    radial-gradient(circle at 50% 50%, rgba(232,163,61,.10), transparent 35%);
}
.tva-gate__prelude.is-done{opacity:0; visibility:hidden; pointer-events:none;}
.tva-prelude__door{position:absolute;inset:0;display:grid;place-items:center;pointer-events:none;opacity:.95;}
.tva-prelude__door::before,.tva-prelude__door::after{content:"";position:absolute;width:min(76vw,820px);height:min(76vw,820px);border:1px solid rgba(232,163,61,.18);border-radius:50%;box-shadow:0 0 80px rgba(232,163,61,.04),inset 0 0 80px rgba(232,163,61,.03);animation:tvaDoorExpand 3.8s cubic-bezier(.2,.7,.2,1) both;}
.tva-prelude__door::after{width:min(54vw,580px);height:min(54vw,580px);border-color:rgba(232,163,61,.32);animation-delay:.35s;}
.tva-prelude__door span{width:min(34vw,360px);height:min(34vw,360px);border-radius:50%;border:2px solid var(--amber);box-shadow:0 0 40px rgba(232,163,61,.16),inset 0 0 50px rgba(232,163,61,.08);animation:tvaDoorPulse 2.2s ease-in-out infinite;}
.tva-prelude__door i{position:absolute;width:1px;height:78vh;background:linear-gradient(transparent,rgba(232,163,61,.8),transparent);transform:rotate(35deg);animation:tvaDoorSweep 2.4s linear infinite;}
.tva-prelude__door b{position:absolute;bottom:9%;font:7px var(--font-mono);letter-spacing:.2em;color:rgba(232,163,61,.55);font-weight:400;}
@keyframes tvaDoorExpand{0%{transform:scale(.55);opacity:0}25%{opacity:1}100%{transform:scale(1.08);opacity:.35}}
@keyframes tvaDoorPulse{0%,100%{transform:scale(.86);opacity:.55}50%{transform:scale(1);opacity:1}}
@keyframes tvaDoorSweep{0%{transform:rotate(20deg) translateY(-30%);opacity:0}30%{opacity:.7}100%{transform:rotate(20deg) translateY(30%);opacity:0}}
.tva-prelude__core{position:relative; width:min(72vw,620px); aspect-ratio:1; display:grid; place-items:center;}
.tva-prelude__ring{position:absolute; inset:8%; border:1px solid rgba(232,163,61,.34); border-radius:50%; box-shadow:0 0 70px rgba(232,163,61,.06), inset 0 0 40px rgba(232,163,61,.04);}
.tva-prelude__ring::before,.tva-prelude__ring::after{content:"";position:absolute;inset:12%;border:1px dashed rgba(232,163,61,.18);border-radius:50%;}
.tva-prelude__ring::after{inset:24%;border-style:solid;border-color:rgba(176,67,42,.28);}
.tva-prelude__dial{position:absolute;inset:34%;border:2px solid var(--amber);border-radius:50%;animation:tvaDialSpin 12s linear infinite;}
.tva-prelude__dial::before{content:"";position:absolute;left:50%;top:-18px;width:1px;height:36px;background:var(--amber);box-shadow:0 0 12px var(--amber);}
.tva-prelude__dial::after{content:"";position:absolute;left:50%;top:50%;width:8px;height:8px;transform:translate(-50%,-50%);border-radius:50%;background:var(--amber);box-shadow:0 0 24px var(--amber);}
@keyframes tvaDialSpin{to{transform:rotate(360deg);}}
.tva-prelude__copy{position:relative;text-align:center;font-family:var(--font-mono);text-transform:uppercase;letter-spacing:.18em;}
.tva-prelude__brand{font-size:clamp(28px,5vw,54px);font-weight:600;line-height:1;color:var(--cream);text-shadow:0 0 25px rgba(232,163,61,.22);}
.tva-prelude__sub{font-size:9px;color:var(--amber-deep);margin-top:14px;}
.tva-prelude__telemetry{position:absolute;left:50%;bottom:9%;transform:translateX(-50%);font-size:8px;letter-spacing:.14em;color:rgba(233,221,192,.55);white-space:nowrap;}
.tva-prelude__telemetry b{color:var(--amber);font-weight:500;}
.tva-prelude__scanline{position:absolute;left:8%;right:8%;top:50%;height:1px;background:linear-gradient(90deg,transparent,rgba(232,163,61,.6),transparent);box-shadow:0 0 18px rgba(232,163,61,.22);animation:tvaScanline 2.8s ease-in-out infinite;}
@keyframes tvaScanline{0%,100%{transform:translateY(-120px);opacity:.15}50%{transform:translateY(120px);opacity:.9}}
.tva-prelude__stamp{position:absolute;border:1px solid rgba(176,67,42,.55);color:rgba(232,163,61,.65);padding:8px 10px;font-size:7px;letter-spacing:.14em;line-height:1.55;text-transform:uppercase;background:rgba(12,9,6,.38);box-shadow:inset 0 0 14px rgba(232,163,61,.025);}
.tva-prelude__stamp--left{left:5%;top:17%;transform:rotate(-4deg);}
.tva-prelude__stamp--right{right:5%;top:24%;transform:rotate(4deg);}
.tva-prelude__stamp--bottom{right:7%;bottom:17%;transform:rotate(-3deg);}
.tva-prelude__stamp b{color:var(--cream);font-weight:500;}
.tva-prelude__needle{position:absolute;left:50%;top:50%;width:min(31vw,250px);height:1px;background:linear-gradient(90deg,transparent,rgba(232,163,61,.7));transform-origin:0 50%;animation:tvaNeedle 4.2s cubic-bezier(.55,.1,.3,.9) infinite;}
@keyframes tvaNeedle{0%{transform:rotate(-34deg);opacity:.15}35%{opacity:.85}100%{transform:rotate(326deg);opacity:.15}}
.tva-prelude__field{position:absolute;left:50%;top:50%;width:9px;height:9px;border-radius:50%;background:var(--amber);box-shadow:0 0 18px var(--amber),0 0 50px rgba(232,163,61,.35);transform:translate(-50%,-50%);animation:tvaField 1.7s ease-in-out infinite;}
@keyframes tvaField{0%,100%{transform:translate(-50%,-50%) scale(.7);opacity:.65}50%{transform:translate(-50%,-50%) scale(1.25);opacity:1}}
/* temporal rupture: time breaks before the TVA console appears */
.tva-gate__prelude::after{content:"";position:absolute;inset:-12%;pointer-events:none;opacity:.72;background:linear-gradient(92deg,transparent 0 45%,rgba(232,163,61,.08) 45.2%,transparent 46%),linear-gradient(87deg,transparent 0 56%,rgba(176,67,42,.10) 56.2%,transparent 57%);mix-blend-mode:screen;animation:temporalTear 1.9s steps(2,end) infinite;}
.tva-prelude__fracture{position:absolute;inset:0;pointer-events:none;overflow:hidden;}
.tva-prelude__fracture::before{content:"";position:absolute;left:50%;top:50%;width:2px;height:145%;background:linear-gradient(transparent,rgba(244,236,215,.9) 35%,var(--amber) 50%,rgba(176,67,42,.75) 66%,transparent);box-shadow:0 0 22px rgba(232,163,61,.75),0 0 70px rgba(232,163,61,.25);transform:translate(-50%,-50%) rotate(7deg);animation:timeCrack .95s cubic-bezier(.15,.7,.2,1) both;}
.tva-prelude__fracture::after{content:"";position:absolute;left:50%;top:50%;width:118vw;height:1px;background:linear-gradient(90deg,transparent,rgba(244,236,215,.75),var(--amber),rgba(176,67,42,.7),transparent);box-shadow:0 0 28px rgba(232,163,61,.5);transform:translate(-50%,-50%) rotate(-11deg);animation:timeCrackH 1.15s .22s cubic-bezier(.15,.7,.2,1) both;}
.tva-prelude__breaktext{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);z-index:4;font:600 clamp(12px,2vw,18px) var(--font-mono);letter-spacing:.42em;text-transform:uppercase;color:var(--cream);text-shadow:0 0 18px rgba(232,163,61,.65);white-space:nowrap;animation:breakText 1.9s ease both;}
.tva-prelude__breaktext small{display:block;text-align:center;margin-top:10px;font-size:7px;letter-spacing:.22em;color:var(--amber);}
@keyframes temporalTear{0%,100%{transform:translateX(0);opacity:.25}18%{transform:translateX(-2%);opacity:.8}20%{transform:translateX(3%);opacity:.45}55%{transform:translateX(-1%);opacity:.75}58%{transform:translateX(2%);opacity:.3}}
@keyframes timeCrack{0%{transform:translate(-50%,-50%) rotate(7deg) scaleY(0);opacity:0}35%{opacity:1}100%{transform:translate(-50%,-50%) rotate(7deg) scaleY(1);opacity:.9}}
@keyframes timeCrackH{0%{transform:translate(-50%,-50%) rotate(-11deg) scaleX(0);opacity:0}35%{opacity:1}100%{transform:translate(-50%,-50%) rotate(-11deg) scaleX(1);opacity:.7}}
@keyframes breakText{0%{opacity:0;letter-spacing:.8em;filter:blur(8px)}28%{opacity:1;filter:none}68%{opacity:1}100%{opacity:0;transform:translate(-50%,-50%) scale(1.15);filter:blur(3px)}}
.tva-gate.is-breaking .tva-gate__prelude{animation:preludeCollapse .82s cubic-bezier(.2,.8,.2,1) both;}
@keyframes preludeCollapse{0%{opacity:1;clip-path:inset(0)}55%{opacity:1;clip-path:polygon(0 0,48% 0,49% 48%,51% 48%,52% 0,100% 0,100% 100%,52% 100%,51% 52%,49% 52%,48% 100%,0 100%)}100%{opacity:0;clip-path:polygon(0 0,49% 0,49% 100%,0 100%,0 100%,51% 100%,51% 0,100% 0,100% 100%,0 100%);visibility:hidden}}
.tva-prelude__micro{position:absolute;left:50%;top:calc(50% + min(24vw,190px));transform:translateX(-50%);font-size:7px;letter-spacing:.11em;color:rgba(233,221,192,.38);white-space:nowrap;}
.tva-prelude__micro i{display:inline-block;width:22px;height:3px;margin:0 5px;background:linear-gradient(90deg,var(--rust),var(--amber),var(--teal));vertical-align:middle;opacity:.8;}
.tva-gate__diagnostics{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:18px 0 0;}
.tva-diagnostic{border:1px solid rgba(232,163,61,.16);background:rgba(8,7,5,.38);padding:10px 11px;min-height:52px;}
.tva-diagnostic__top{display:flex;justify-content:space-between;gap:10px;font-size:7px;letter-spacing:.12em;text-transform:uppercase;color:var(--amber-deep);}
.tva-diagnostic__value{font-size:9px;color:var(--cream);letter-spacing:.08em;margin-top:7px;}
.tva-diagnostic__meter{height:2px;background:#2a2012;margin-top:8px;overflow:hidden;}
.tva-diagnostic__meter i{display:block;width:72%;height:100%;background:linear-gradient(90deg,var(--rust),var(--amber));animation:diagPulse 1.9s ease-in-out infinite;}
.tva-diagnostic:nth-child(2) .tva-diagnostic__meter i{width:43%;animation-delay:.25s;}
.tva-diagnostic:nth-child(3) .tva-diagnostic__meter i{width:91%;animation-delay:.5s;}
.tva-diagnostic:nth-child(4) .tva-diagnostic__meter i{width:58%;animation-delay:.75s;}
@keyframes diagPulse{0%,100%{opacity:.45;transform:scaleX(.88);transform-origin:left}50%{opacity:1;transform:scaleX(1)}}
.tva-gate__casefile{margin-top:16px;border-top:1px solid rgba(232,163,61,.15);border-bottom:1px solid rgba(232,163,61,.15);padding:9px 0;display:flex;justify-content:space-between;gap:14px;font-size:7px;letter-spacing:.11em;text-transform:uppercase;color:rgba(233,221,192,.5);}
.tva-gate__casefile b{color:var(--amber);font-weight:500;}
.tva-gate__serial{position:absolute;left:18px;bottom:16px;font-size:6px;letter-spacing:.16em;color:rgba(233,221,192,.25);writing-mode:vertical-rl;transform:rotate(180deg);}
.tva-gate__noise{position:absolute;inset:0;pointer-events:none;opacity:.09;background:repeating-radial-gradient(circle at 20% 30%,rgba(255,255,255,.15) 0 1px,transparent 1px 4px);mix-blend-mode:screen;animation:tvaNoise .18s steps(2) infinite;}
@keyframes tvaNoise{0%{transform:translate(0,0)}25%{transform:translate(2px,-1px)}50%{transform:translate(-1px,2px)}75%{transform:translate(1px,1px)}100%{transform:translate(-2px,-1px)}}
.tva-gate__frame{opacity:0;transform:translateY(16px) scale(.985);transition:opacity .8s ease, transform .8s cubic-bezier(.2,.8,.2,1);}
.tva-gate.is-ready .tva-gate__frame{opacity:1;transform:none;}
.tva-gate__aperture{position:absolute;inset:0;z-index:11;pointer-events:none;opacity:0;background:radial-gradient(circle at 50% 50%, transparent 0 2%, rgba(232,163,61,.2) 3%, rgba(232,163,61,.05) 10%, transparent 20%);}
.tva-gate.is-firing .tva-gate__aperture{animation:tvaAperture 1.15s cubic-bezier(.25,.7,.1,1) both;}
@keyframes tvaAperture{0%{opacity:0;transform:scale(.15)}15%{opacity:1}70%{opacity:.85;transform:scale(1.5)}100%{opacity:0;transform:scale(3.2)}}
.tva-gate__frame.is-scanning{animation:tvaFrameScan .55s steps(2) 2;}
@keyframes tvaFrameScan{0%,100%{filter:none}45%{filter:brightness(1.45) sepia(.2)}50%{filter:brightness(.7)}}
.tva-gate__sound{font-size:8px;letter-spacing:.12em;text-transform:uppercase;color:var(--amber-deep);margin-top:8px;text-align:center;}
.tva-gate__sound i{display:inline-block;width:5px;height:5px;border-radius:50%;background:var(--rust);margin-right:6px;vertical-align:middle;}
.tva-gate.is-firing .tva-gate__sound i{background:var(--amber);box-shadow:0 0 10px var(--amber);}
body.tva-transit main,body.tva-transit footer,body.tva-transit .bar{filter:blur(9px) brightness(.45);transform:scale(1.025);transition:filter .9s ease, transform .9s ease;}
@media (prefers-reduced-motion:reduce){
  .tva-prelude__door::before,.tva-prelude__door::after,.tva-prelude__door span,.tva-prelude__door i{animation:none;}
  .tva-prelude__dial{animation:none;}
  .tva-gate__frame{transition:none;}
  .tva-gate__frame.is-scanning,.tva-gate.is-firing .tva-gate__aperture{animation:none;}
  body.tva-transit main,body.tva-transit footer,body.tva-transit .bar{transition:none;}
}

/* ================= TVA ACCESS GATE ================= */
body.tva-locked{overflow:hidden;}
.tva-gate{
  position:fixed; inset:0; z-index:500;
  display:grid; place-items:center; padding:24px;
  background:
    radial-gradient(circle at 50% 45%, rgba(232,163,61,.12), transparent 25%),
    linear-gradient(180deg, rgba(14,11,8,.97), rgba(7,6,5,.99));
  color:var(--cream);
  transition:opacity .8s ease, visibility .8s ease, filter .8s ease;
}
.tva-gate::before{
  content:""; position:absolute; inset:22px; pointer-events:none;
  border:1px solid rgba(232,163,61,.18);
  background-image:
    linear-gradient(rgba(232,163,61,.035) 1px,transparent 1px),
    linear-gradient(90deg,rgba(232,163,61,.035) 1px,transparent 1px);
  background-size:42px 42px;
  mask-image:linear-gradient(to bottom,transparent,#000 15%,#000 85%,transparent);
}
.tva-gate.is-opening{opacity:0; visibility:hidden; filter:blur(8px); pointer-events:none;}
.tva-gate__frame{
  width:min(720px,100%); position:relative; z-index:1;
  border:1px solid rgba(232,163,61,.34);
  background:rgba(22,16,9,.82);
  box-shadow:0 30px 100px rgba(0,0,0,.55), inset 0 0 60px rgba(232,163,61,.035);
  padding:38px 34px 34px;
}
.tva-gate__frame::before,
.tva-gate__frame::after{
  content:""; position:absolute; width:26px; height:26px; border-color:var(--amber); opacity:.7;
}
.tva-gate__frame::before{left:-1px;top:-1px;border-left:2px solid;border-top:2px solid;}
.tva-gate__frame::after{right:-1px;bottom:-1px;border-right:2px solid;border-bottom:2px solid;}
.tva-gate__eyebrow{
  display:flex; justify-content:space-between; gap:20px; align-items:center;
  font-size:9px; letter-spacing:.16em; text-transform:uppercase; color:var(--amber-deep);
  border-bottom:1px solid var(--line); padding-bottom:14px;
}
.tva-gate__live{color:var(--amber); display:inline-flex;align-items:center;gap:7px;}
.tva-gate__live i{width:6px;height:6px;border-radius:50%;background:var(--amber);box-shadow:0 0 12px rgba(232,163,61,.9);animation:pulse 1.3s infinite;}
.tva-gate__title{font-size:clamp(34px,7vw,64px);line-height:.98;margin:28px 0 14px;color:var(--cream);}
.tva-gate__copy{max-width:55ch;color:var(--paper-dim);font-size:12px;line-height:1.75;}
.tva-gate__status{display:flex;flex-wrap:wrap;gap:8px;margin:22px 0 28px;}
.tva-gate__chip{font-size:8px;letter-spacing:.1em;text-transform:uppercase;border:1px solid var(--line);padding:6px 8px;color:var(--paper-dim);}
.tva-gate__chip--hot{border-color:rgba(232,163,61,.5);color:var(--amber);}
.tva-switch-wrap{display:flex;align-items:center;justify-content:center;gap:24px;padding:18px 0 8px;}
.tva-switch-label{text-align:right;min-width:125px;}
.tva-switch-label strong{display:block;font-size:11px;letter-spacing:.1em;color:var(--cream);}
.tva-switch-label span{display:block;font-size:8px;letter-spacing:.08em;text-transform:uppercase;color:var(--amber-deep);margin-top:4px;}
/* TVA ignition console — physical, mechanical access control */
.tva-switch{
  position:relative; width:118px; height:190px; flex:0 0 auto; border:1px solid #705021; border-radius:9px; cursor:pointer;
  background:
    linear-gradient(90deg,rgba(255,255,255,.035),transparent 18%,transparent 82%,rgba(255,255,255,.025)),
    repeating-linear-gradient(0deg,#17110a 0 8px,#21170b 8px 9px), #120d08;
  box-shadow:inset 0 0 0 5px #0a0805,inset 0 0 25px rgba(0,0,0,.9),0 18px 45px rgba(0,0,0,.45);
  transition:transform .25s ease, box-shadow .3s ease, border-color .3s ease;
}
.tva-switch::after{content:"TEMPORAL IGNITION // 01";position:absolute;left:10px;right:10px;top:9px;font:6px var(--font-mono);letter-spacing:.13em;color:#6e5735;text-align:center;}
.tva-switch:hover{border-color:var(--amber);box-shadow:inset 0 0 0 5px #0a0805,inset 0 0 25px rgba(0,0,0,.9),0 0 30px rgba(232,163,61,.12),0 18px 45px rgba(0,0,0,.45);}
.tva-switch:active{transform:translateY(2px);}
.tva-switch::before{content:"";position:absolute;left:50%;top:48px;bottom:26px;width:7px;transform:translateX(-50%);background:linear-gradient(90deg,#241a10,#4b3820,#1b130b);border:1px solid #59401f;box-shadow:0 0 0 2px #090705, inset 0 0 7px #000;}
.tva-switch__plate{position:absolute;left:50%;top:77px;width:78px;height:78px;transform:translateX(-50%);border:2px solid #5f431f;border-radius:50%;background:radial-gradient(circle,#1e150b 0 45%,#0b0906 46% 58%,#302114 59% 62%,#0b0906 63%);box-shadow:inset 0 0 20px #000,0 0 0 3px #080604,0 0 0 4px #3a2815;}
.tva-switch__plate::before{content:"ARM";position:absolute;inset:7px;border:1px dashed #60451f;border-radius:50%;display:grid;place-items:center;font:7px var(--font-mono);letter-spacing:.18em;color:#8b6a39;}
.tva-switch__plate::after{content:"12  3  6  9";position:absolute;left:50%;top:-17px;width:100px;transform:translateX(-50%);font:6px var(--font-mono);letter-spacing:.45em;color:#60451f;white-space:nowrap;text-align:center;}
.tva-switch__lever{position:absolute;left:50%;top:91px;width:18px;height:70px;transform:translate(-50%,-8%) rotate(24deg);transform-origin:50% 86%;border-radius:7px;background:linear-gradient(90deg,#382613,#e8a33d 44%,#6d4a20 55%,#24180c);box-shadow:inset 2px 0 2px rgba(255,255,255,.18),0 0 12px rgba(232,163,61,.15);transition:transform .55s cubic-bezier(.2,.8,.2,1),box-shadow .3s ease;}
.tva-switch__knob{position:absolute;left:50%;top:-8px;width:30px;height:30px;transform:translateX(-50%);border-radius:50%;background:radial-gradient(circle at 35% 30%,#ffd37a,#d88b28 55%,#633f18);border:2px solid #765323;box-shadow:0 0 0 3px #130e08,0 0 18px rgba(232,163,61,.35);}
.tva-switch__lever::after{content:"PULL";position:absolute;top:34px;left:28px;transform:rotate(90deg);font:6px var(--font-mono);letter-spacing:.16em;color:#806039;white-space:nowrap;}
.tva-switch.is-on{border-color:var(--amber);box-shadow:inset 0 0 0 5px #0a0805,inset 0 0 30px rgba(232,163,61,.08),0 0 35px rgba(232,163,61,.2),0 18px 45px rgba(0,0,0,.45);}
.tva-switch.is-on .tva-switch__lever{transform:translate(-50%,-8%) rotate(-27deg);box-shadow:0 0 28px rgba(232,163,61,.75);}
.tva-switch.is-on .tva-switch__plate::before{content:"FIRE";color:var(--amber);text-shadow:0 0 9px var(--amber);}
.tva-switch__caption{position:absolute;left:8px;right:8px;bottom:8px;font-size:6px;letter-spacing:.13em;color:#a37a3d;text-transform:uppercase;border-top:1px solid #3c2b18;padding-top:7px;}
.tva-switch__guard{position:absolute;left:50%;top:64px;width:91px;height:106px;transform:translateX(-50%);border:1px solid rgba(232,163,61,.15);border-radius:45px 45px 12px 12px;pointer-events:none;}
.tva-switch__bolt{position:absolute;width:5px;height:5px;border-radius:50%;background:#6e4d25;box-shadow:inset 1px 1px 2px #000;}
.tva-switch__bolt--a{left:8px;top:8px}.tva-switch__bolt--b{right:8px;top:8px}.tva-switch__bolt--c{left:8px;bottom:8px}.tva-switch__bolt--d{right:8px;bottom:8px}
.tva-switch__guardline{position:absolute;left:14px;right:14px;top:55px;border-top:1px solid rgba(176,67,42,.45);}
.tva-switch__guardline::after{content:"WARNING // TEMPORAL ENERGY";position:absolute;left:50%;top:4px;transform:translateX(-50%);font:5px var(--font-mono);letter-spacing:.11em;color:#74432f;white-space:nowrap;}
@keyframes ignitionBlink{0%,100%{opacity:.35}50%{opacity:1}}
.tva-switch:not(.is-on) .tva-switch__plate{animation:ignitionBlink 1.8s ease-in-out infinite;}
.tva-switch:focus-visible{outline:2px solid var(--amber);outline-offset:5px;}

/* Easy one-click TVA authorization console */
.tva-access-wrap{display:flex;flex-direction:column;align-items:center;justify-content:center;margin:18px auto 4px;}
.tva-access-label{text-align:center;margin-bottom:10px;text-transform:uppercase;}
.tva-access-label__eyebrow{display:block;font:7px var(--font-mono);letter-spacing:.2em;color:var(--amber-deep);margin-bottom:5px;}
.tva-access-label strong{display:block;font:600 12px var(--font-mono);letter-spacing:.13em;color:var(--cream);}
.tva-access-label span:last-child{display:block;font:7px var(--font-mono);letter-spacing:.12em;color:var(--amber);margin-top:5px;}
.tva-access-console{position:relative;width:190px;height:190px;border:1px solid rgba(232,163,61,.52);border-radius:50%;padding:0;background:radial-gradient(circle at 50% 45%,#3a2915 0,#1b130a 30%,#0b0906 58%,#050403 100%);box-shadow:0 0 0 6px rgba(7,5,3,.95),0 0 0 7px rgba(232,163,61,.13),inset 0 0 34px #000,0 0 40px rgba(232,163,61,.14);cursor:pointer;color:var(--cream);transition:transform .2s ease,border-color .25s ease,box-shadow .25s ease;overflow:hidden;}
.tva-access-console::before{content:"";position:absolute;inset:13px;border:1px dashed rgba(232,163,61,.28);border-radius:50%;}
.tva-access-console::after{content:"AUTHORIZED ACCESS";position:absolute;left:0;right:0;bottom:18px;font:6px var(--font-mono);letter-spacing:.18em;color:#806039;}
.tva-access-console:hover{transform:scale(1.025);border-color:var(--amber);box-shadow:0 0 0 6px rgba(7,5,3,.95),0 0 0 7px rgba(232,163,61,.3),inset 0 0 34px #000,0 0 60px rgba(232,163,61,.25);}
.tva-access-console:active{transform:scale(.985);}
.tva-access-console:focus-visible{outline:2px solid var(--amber);outline-offset:7px;}
.tva-access-console__halo{position:absolute;inset:27px;border-radius:50%;border:1px solid rgba(232,163,61,.16);box-shadow:0 0 28px rgba(232,163,61,.08);animation:accessHalo 2.2s ease-in-out infinite;}
.tva-access-console__ring{position:absolute;border-radius:50%;pointer-events:none;}
.tva-access-console__ring--outer{inset:4px;border:1px solid rgba(232,163,61,.18);border-left-color:var(--amber);border-bottom-color:rgba(176,67,42,.5);animation:accessSpin 9s linear infinite;}
.tva-access-console__ring--inner{inset:22px;border:1px solid rgba(232,163,61,.18);border-right-color:var(--amber);border-top-color:rgba(60,110,100,.45);animation:accessSpinReverse 6s linear infinite;}
.tva-access-console__ticks{position:absolute;inset:8px;border-radius:50%;background:repeating-conic-gradient(from 0deg,rgba(232,163,61,.45) 0deg 1deg,transparent 1deg 15deg);mask:radial-gradient(circle,transparent 0 74%,#000 75% 77%,transparent 78%);}
.tva-access-console__core{position:absolute;left:50%;top:50%;width:92px;height:92px;transform:translate(-50%,-50%);border:1px solid rgba(232,163,61,.42);border-radius:50%;display:flex;flex-direction:column;align-items:center;justify-content:center;background:radial-gradient(circle,#2b1d0d,#0d0a06 72%);box-shadow:inset 0 0 20px #000,0 0 18px rgba(232,163,61,.08);}
.tva-access-console__symbol{font:600 17px var(--font-mono);letter-spacing:.28em;text-indent:.28em;color:var(--cream);text-shadow:0 0 15px rgba(232,163,61,.45);}
.tva-access-console__action{font:600 7px var(--font-mono);letter-spacing:.17em;color:var(--amber);margin-top:8px;}
.tva-access-console__sub{font:6px var(--font-mono);letter-spacing:.1em;color:#806039;margin-top:4px;}
.tva-access-console__sweep{position:absolute;left:50%;top:50%;width:1px;height:82px;transform-origin:50% 100%;background:linear-gradient(transparent,var(--amber));box-shadow:0 0 8px rgba(232,163,61,.7);animation:accessNeedle 2.8s linear infinite;opacity:.7;}
.tva-access-meta{display:flex;align-items:center;justify-content:center;gap:9px;margin-top:12px;font:6px var(--font-mono);letter-spacing:.12em;color:rgba(233,221,192,.38);}
.tva-access-meta i{width:3px;height:3px;border-radius:50%;background:var(--amber);box-shadow:0 0 7px var(--amber);}
.tva-access-console.is-on{border-color:var(--amber);box-shadow:0 0 0 6px rgba(7,5,3,.95),0 0 0 7px rgba(232,163,61,.55),inset 0 0 34px #000,0 0 90px rgba(232,163,61,.4);}
.tva-access-console.is-on .tva-access-console__core{box-shadow:inset 0 0 20px #000,0 0 35px rgba(232,163,61,.45);}
@keyframes accessSpin{to{transform:rotate(360deg)}}
@keyframes accessSpinReverse{to{transform:rotate(-360deg)}}
@keyframes accessNeedle{to{transform:rotate(360deg)}}
@keyframes accessHalo{0%,100%{opacity:.45;transform:scale(.97)}50%{opacity:1;transform:scale(1.03)}}

.tva-gate__instruction{text-align:center;font-size:9px;letter-spacing:.13em;text-transform:uppercase;color:var(--paper-dim);margin-top:12px;}
.tva-gate__seal{position:absolute;right:28px;top:26px;width:72px;height:72px;border:1px solid rgba(176,67,42,.55);border-radius:50%;display:grid;place-items:center;color:var(--rust);font-size:7px;letter-spacing:.1em;text-align:center;transform:rotate(12deg);opacity:.7;}
.tva-gate__seal::before{content:"";position:absolute;inset:7px;border:1px dashed currentColor;border-radius:50%;}
.tva-gate__boot{height:3px;background:#2a2012;margin-top:26px;overflow:hidden;opacity:.65;}
.tva-gate__boot i{display:block;width:18%;height:100%;background:linear-gradient(90deg,var(--rust),var(--amber),var(--teal));animation:gateBoot 2.8s ease-in-out infinite;}
@keyframes gateBoot{0%{transform:translateX(-120%)}55%{transform:translateX(240%)}100%{transform:translateX(520%)}}
.tva-gate__warning{margin-top:12px;text-align:center;font-size:8px;color:var(--rust);letter-spacing:.1em;text-transform:uppercase;}
body.tva-unlocked .bar, body.tva-unlocked main, body.tva-unlocked footer{animation:tvaReveal .9s ease both;}
@keyframes tvaReveal{from{opacity:.15;filter:blur(5px);transform:scale(1.008)}to{opacity:1;filter:none;transform:none}}
@media (max-width:720px){
  .tva-gate{padding:14px;}
  .tva-gate__frame{padding:28px 20px 24px;}
  .tva-gate__seal{display:none;}
  .tva-switch-wrap{gap:16px;}
  .tva-switch-label{min-width:92px;}
  .tva-switch{width:94px;height:164px;}
  .tva-switch__plate{width:58px;height:58px;}
  .tva-switch__lever{height:62px;}
  .tva-access-console{width:154px;height:154px;}
  .tva-access-console__core{width:78px;height:78px;}
  .tva-access-console__symbol{font-size:14px;}
  .tva-access-meta{gap:6px;font-size:5px;}
}
@media (prefers-reduced-motion:reduce){
  .tva-gate,.tva-gate.is-opening{transition:none;}
  .tva-gate__boot i,.tva-gate__live i{animation:none;}
  .tva-access-console__ring--outer,.tva-access-console__ring--inner,.tva-access-console__sweep,.tva-access-console__halo{animation:none;}
}

/* ================= TVA CONTROL ROOM ================= */
.tva-control{
  position:relative; padding:100px 32px 110px; overflow:hidden;
  background:
    radial-gradient(circle at 20% 20%, rgba(232,163,61,.10), transparent 34%),
    radial-gradient(circle at 85% 75%, rgba(60,110,100,.08), transparent 30%),
    linear-gradient(180deg, rgba(232,163,61,.025), transparent 45%),
    var(--bg);
  border-top:1px solid var(--line);
  border-bottom:1px solid var(--line);
}
.tva-control::before{
  content:""; position:absolute; inset:20px; pointer-events:none;
  border:1px solid rgba(232,163,61,.05);
  background-image:linear-gradient(rgba(232,163,61,.025) 1px,transparent 1px),
    linear-gradient(90deg,rgba(232,163,61,.025) 1px,transparent 1px);
  background-size:34px 34px;
  mask-image:linear-gradient(to bottom,transparent,#000 14%,#000 86%,transparent);
}
.tva-control__inner{max-width:1180px; margin:0 auto; position:relative; z-index:1;}
.tva-control__head{
  display:flex; align-items:flex-end; justify-content:space-between; gap:30px; margin-bottom:46px;
}
.tva-control__head h2{font-size:clamp(30px,4vw,48px); line-height:1.05; color:var(--cream);}
.tva-control__head p{max-width:430px; color:var(--paper-dim); font-size:12px; line-height:1.7;}
.tva-control__grid{
  display:grid; grid-template-columns:minmax(330px,.95fr) minmax(0,1.05fr); gap:18px;
}
.tva-panel{
  position:relative; background:rgba(22,16,9,.82); border:1px solid var(--line);
  box-shadow:0 20px 60px rgba(0,0,0,.18); overflow:hidden;
}
.tva-panel__top{
  display:flex; align-items:center; justify-content:space-between; gap:12px;
  padding:12px 16px; border-bottom:1px solid var(--line);
  font-size:9px; letter-spacing:.12em; text-transform:uppercase; color:var(--amber-deep);
}
.tva-live-dot{display:inline-flex; align-items:center; gap:7px; color:var(--amber);}
.tva-live-dot i{width:6px;height:6px;border-radius:50%;background:var(--amber);box-shadow:0 0 12px rgba(232,163,61,.8);animation:pulse 1.4s infinite;}
.tva-clock-panel{min-height:590px;}
.tva-clock-wrap{display:grid; place-items:center; padding:34px 24px 20px;}
.tva-clock{
  --clock-size:min(420px,70vw);
  width:var(--clock-size); height:var(--clock-size); max-width:420px; max-height:420px;
  position:relative; border-radius:50%;
  background:
    radial-gradient(circle at center, #1c150c 0 42%, transparent 42.4%),
    conic-gradient(from 0deg, rgba(232,163,61,.06), rgba(232,163,61,.22), rgba(60,110,100,.12), rgba(232,163,61,.06));
  border:1px solid rgba(232,163,61,.6);
  box-shadow:0 0 0 8px rgba(232,163,61,.025),0 0 0 16px rgba(232,163,61,.035),inset 0 0 50px rgba(232,163,61,.08),0 0 55px rgba(232,163,61,.08);
}
.tva-clock::before{
  content:""; position:absolute; inset:12px; border-radius:50%;
  border:1px dashed rgba(232,163,61,.28);
}
.tva-clock::after{
  content:""; position:absolute; inset:27px; border-radius:50%;
  border:1px solid rgba(233,221,192,.10);
}
.tva-clock__ticks{position:absolute; inset:0; border-radius:50%; background:repeating-conic-gradient(from 0deg,rgba(244,236,215,.8) 0deg .8deg,transparent .8deg 6deg); mask:radial-gradient(circle,transparent 0 43%,#000 43.5% 48%,transparent 48.5%);}
.tva-clock__ticks--major{position:absolute; inset:0; border-radius:50%; background:repeating-conic-gradient(from 0deg,rgba(232,163,61,.9) 0deg 1.6deg,transparent 1.6deg 30deg); mask:radial-gradient(circle,transparent 0 43%,#000 43.5% 50%,transparent 50.5%);}
.tva-clock__hand{
  position:absolute; left:50%; bottom:50%; width:2px; height:34%; transform-origin:50% 100%;
  border-radius:4px 4px 1px 1px; background:var(--cream); transform:translateX(-50%) rotate(0deg);
  box-shadow:0 0 8px rgba(244,236,215,.35); z-index:4;
}
.tva-clock__hand--hour{height:25%; width:5px; background:var(--amber);}
.tva-clock__hand--second{height:39%; width:1px; background:var(--rust);}
.tva-clock__hub{
  position:absolute; left:50%; top:50%; width:13px; height:13px; transform:translate(-50%,-50%);
  border-radius:50%; background:var(--amber); border:3px solid var(--bg); box-shadow:0 0 18px rgba(232,163,61,.7); z-index:6;
}
.tva-clock__brand{
  position:absolute; left:50%; top:26%; transform:translateX(-50%);
  font-size:10px; letter-spacing:.18em; color:var(--amber); text-transform:uppercase; white-space:nowrap;
}
.tva-clock__case{
  position:absolute; left:50%; bottom:24%; transform:translateX(-50%);
  font-size:8px; letter-spacing:.14em; color:var(--paper-dim); white-space:nowrap;
}
.tva-clock__digital{
  text-align:center; font-family:var(--font-mono); letter-spacing:.16em; color:var(--amber);
  font-size:22px; margin-top:8px; font-variant-numeric:tabular-nums;
}
.tva-clock__date{text-align:center;font-size:9px;letter-spacing:.12em;text-transform:uppercase;color:var(--paper-dim);margin-top:3px;}
.tva-clock__readouts{
  display:grid; grid-template-columns:repeat(3,1fr); border-top:1px solid var(--line); margin-top:24px;
}
.tva-readout{padding:14px 12px;border-right:1px solid var(--line);text-align:center;}
.tva-readout:last-child{border-right:0;}
.tva-readout span{display:block;font-size:8px;letter-spacing:.12em;text-transform:uppercase;color:var(--amber-deep);}
.tva-readout strong{display:block;font-size:12px;color:var(--cream);margin-top:3px;}
.tva-console{display:grid; grid-template-columns:1fr 1fr; gap:18px; background:transparent; border:0; overflow:visible; box-shadow:none;}
.tva-console__panel{background:rgba(22,16,9,.82);border:1px solid var(--line);min-height:286px;}
.tva-console__panel--wide{grid-column:1/-1;min-height:245px;}
.tva-metrics{display:grid;grid-template-columns:1fr 1fr;gap:10px;padding:16px;}
.tva-metric{padding:14px;border:1px solid var(--line);background:rgba(14,11,8,.72);}
.tva-metric__label{font-size:8px;letter-spacing:.12em;text-transform:uppercase;color:var(--amber-deep);}
.tva-metric__value{font-family:var(--font-display);font-size:26px;color:var(--cream);margin-top:4px;}
.tva-meter{height:5px;background:#261d11;margin-top:8px;overflow:hidden;}
.tva-meter i{display:block;height:100%;width:82%;background:linear-gradient(90deg,var(--rust),var(--amber),var(--teal));transition:width .45s ease;}
.tva-controls{display:flex;flex-wrap:wrap;gap:9px;padding:0 16px 16px;}
.tva-btn{
  font-family:var(--font-mono);font-size:10px;letter-spacing:.08em;text-transform:uppercase;
  border:1px solid var(--line);background:transparent;color:var(--cream);padding:10px 12px;cursor:pointer;
  transition:transform .15s ease,border-color .2s ease,background .2s ease,color .2s ease;
}
.tva-btn:hover,.tva-btn.is-active{border-color:var(--amber);color:var(--amber);background:rgba(232,163,61,.06);transform:translateY(-1px);}
.tva-log{height:148px;overflow:auto;padding:14px 16px;font-size:10px;line-height:1.7;color:var(--paper-dim);scrollbar-width:thin;}
.tva-log p{padding:3px 0;border-bottom:1px dashed rgba(233,221,192,.06);}
.tva-log p::before{content:"[";color:var(--amber-deep);}
.tva-log p::after{content:"]";color:var(--amber-deep);}
.tva-dossier{display:grid;grid-template-columns:150px 1fr;gap:18px;padding:16px;}
.tva-art{
  width:150px;height:150px;object-fit:cover;border:1px solid rgba(232,163,61,.35);
  filter:saturate(.85) contrast(1.05);background:#161009;cursor:pointer;
  transition:transform .35s ease,filter .35s ease,box-shadow .35s ease;
}
.tva-art:hover{transform:rotate(-2deg) scale(1.03);filter:saturate(1.05);box-shadow:0 0 28px rgba(232,163,61,.14);}
.tva-dossier h3{font-size:20px;color:var(--cream);margin-bottom:7px;}
.tva-dossier p{font-size:11px;color:var(--paper-dim);line-height:1.7;}
.tva-dossier__code{font-size:9px;letter-spacing:.13em;color:var(--amber-deep);margin-bottom:8px;}
.tva-agent{display:flex;gap:8px;margin-top:12px;}
.tva-agent input{min-width:0;flex:1;background:var(--bg);border:1px solid var(--line);color:var(--cream);padding:9px 10px;font:10px var(--font-mono);}
.tva-agent button{white-space:nowrap;}
.tva-chip-row{display:flex;flex-wrap:wrap;gap:7px;padding:0 16px 16px;}
.tva-chip{font-size:8px;letter-spacing:.08em;text-transform:uppercase;border:1px solid var(--line);padding:5px 7px;color:var(--paper-dim);}
.tva-chip.is-hot{color:var(--amber);border-color:rgba(232,163,61,.55);}
.tva-pulse{animation:tvaPulse .55s ease;}
@keyframes tvaPulse{0%{box-shadow:0 0 0 0 rgba(232,163,61,.4)}100%{box-shadow:0 0 0 22px rgba(232,163,61,0)}}
.tva-toast{
  position:fixed;right:22px;bottom:22px;z-index:180;max-width:330px;padding:12px 15px;
  background:#171008;border:1px solid var(--amber-deep);color:var(--cream);font-size:10px;
  letter-spacing:.04em;box-shadow:0 14px 40px rgba(0,0,0,.35);transform:translateY(18px);opacity:0;pointer-events:none;
  transition:.25s ease;
}
.tva-toast.is-visible{transform:translateY(0);opacity:1;}
.file.is-selected{background:rgba(232,163,61,.08);box-shadow:inset 0 0 0 1px rgba(232,163,61,.5);}
.file.is-selected .file__stamp{opacity:1;transform:translateX(0);color:var(--amber);border-color:var(--amber);}
.tl__node{cursor:pointer;}
.tl__node.is-selected .tl__card{transform:translateY(-2px);color:var(--amber);}
@media (max-width:900px){
  .tva-control__head{align-items:flex-start;flex-direction:column;}
  .tva-control__grid{grid-template-columns:1fr;}
}
@media (max-width:720px){
  .tva-control{padding-left:18px;padding-right:18px;}
  .tva-console{grid-template-columns:1fr;}
  .tva-console__panel--wide{grid-column:auto;}
  .tva-dossier{grid-template-columns:100px 1fr;}
  .tva-art{width:100px;height:100px;}
  .tva-clock-panel{min-height:0;}
  .tva-clock__readouts{grid-template-columns:1fr;}
  .tva-readout{border-right:0;border-bottom:1px solid var(--line);}
  .tva-readout:last-child{border-bottom:0;}
}
@media (prefers-reduced-motion: reduce){
  .tva-live-dot i{animation:none;}
  .tva-art{transition:none;}
}

/* scrollbar */
html.has-cursor ::-webkit-scrollbar{width:10px;}
html.has-cursor ::-webkit-scrollbar-track{background:var(--bg);}
html.has-cursor ::-webkit-scrollbar-thumb{background:var(--amber-deep); border-radius:5px; border:2px solid var(--bg);}
"""

JS = r"""
(function(){
  // mobile nav
  var burger=document.getElementById('burger'), nav=document.getElementById('mobilenav');
  if(burger){
    burger.addEventListener('click', function(){
      var open=nav.classList.toggle('is-open');
      burger.setAttribute('aria-expanded', open?'true':'false');
    });
    nav.querySelectorAll('a').forEach(function(a){
      a.addEventListener('click', function(){ nav.classList.remove('is-open'); burger.setAttribute('aria-expanded','false'); });
    });
  }

  // countdown to event start (first date in DATES range, assume local time 08:00)
  var target = new Date("2026-11-14T08:00:00");
  var d=document.getElementById('cd-d'), h=document.getElementById('cd-h'),
      m=document.getElementById('cd-m'), s=document.getElementById('cd-s');
  function pad(n){ return String(n).padStart(2,'0'); }
  function tick(){
    var diff = target - new Date();
    if(diff < 0) diff = 0;
    var days = Math.floor(diff/86400000);
    var hrs = Math.floor((diff%86400000)/3600000);
    var mins = Math.floor((diff%3600000)/60000);
    var secs = Math.floor((diff%60000)/1000);
    if(d) d.textContent = pad(days);
    if(h) h.textContent = pad(hrs);
    if(m) m.textContent = pad(mins);
    if(s) s.textContent = pad(secs);
  }
  tick();
  setInterval(tick, 1000);

  // scroll reveal
  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;


  // ---- cinematic camera: subtle light/parallax only; no layout changes ----
  (function(){
    if(reduceMotion) return;
    var root = document.documentElement;
    var light = document.getElementById('cinemaLight');
    var hero = document.querySelector('.hero');
    var branches = document.getElementById('branchSvg');
    var ticking = false;
    var targetX = 50, targetY = 28;
    var currentX = 50, currentY = 28;

    function updateCamera(){
      ticking = false;
      currentX += (targetX - currentX) * 0.08;
      currentY += (targetY - currentY) * 0.08;
      root.style.setProperty('--cinema-x', currentX + '%');
      root.style.setProperty('--cinema-y', currentY + '%');
      if(Math.abs(targetX-currentX) > .05 || Math.abs(targetY-currentY) > .05){
        ticking = true;
        requestAnimationFrame(updateCamera);
      }
    }

    window.addEventListener('pointermove', function(e){
      if(e.pointerType === 'touch') return;
      targetX = (e.clientX / Math.max(window.innerWidth, 1)) * 100;
      targetY = (e.clientY / Math.max(window.innerHeight, 1)) * 100;
      if(!ticking){ ticking = true; requestAnimationFrame(updateCamera); }
      if(branches){
        var bx = (e.clientX / Math.max(window.innerWidth,1) - .5) * -10;
        var by = (e.clientY / Math.max(window.innerHeight,1) - .5) * -7;
        branches.style.setProperty('--branch-drift-x', bx.toFixed(2) + 'px');
        branches.style.setProperty('--branch-drift-y', by.toFixed(2) + 'px');
      }
    }, {passive:true});

    window.addEventListener('scroll', function(){
      if(!hero) return;
      var rect = hero.getBoundingClientRect();
      var progress = Math.max(0, Math.min(1, -rect.top / Math.max(rect.height,1)));
      var drift = Math.min(22, progress * 22);
      var fade = Math.max(.78, 1 - progress * .34);
      hero.style.setProperty('--hero-drift', drift.toFixed(2) + 'px');
      hero.style.setProperty('--hero-focus', fade.toFixed(3));
    }, {passive:true});

    if(hero){
      hero.querySelector('.hero__inner').style.transform = 'translate3d(0,var(--hero-drift,0px),0)';
      hero.querySelector('.hero__inner').style.opacity = 'var(--hero-focus,1)';
    }

    // Trigger a brief cinematic exposure change as major sections enter view.
    if('IntersectionObserver' in window){
      var cinematicSections = document.querySelectorAll('.tva-control, .briefing, .files, .tl, .recruit');
      var observer = new IntersectionObserver(function(entries){
        entries.forEach(function(entry){
          if(entry.isIntersecting){
            entry.target.classList.add('cinema-focus');
            observer.unobserve(entry.target);
          }
        });
      }, {threshold:.16});
      cinematicSections.forEach(function(section){ observer.observe(section); });
    }
  })();
  var revealTargets = document.querySelectorAll('.file, .tl__node, .stat, .faq__item, .briefing__doc, .briefing__stamp');
  revealTargets.forEach(function(el){ el.classList.add('reveal'); });
  if('IntersectionObserver' in window && !reduceMotion){
    var io = new IntersectionObserver(function(entries){
      entries.forEach(function(entry){
        if(entry.isIntersecting){
          entry.target.classList.add('is-visible');
          io.unobserve(entry.target);
        }
      });
    }, {threshold:0.12, rootMargin:'0px 0px -40px 0px'});
    revealTargets.forEach(function(el){ io.observe(el); });
  } else {
    revealTargets.forEach(function(el){ el.classList.add('is-visible'); });
  }

  // faq accordion
  document.querySelectorAll('.faq__q').forEach(function(btn){
    btn.addEventListener('click', function(){
      var expanded = btn.getAttribute('aria-expanded') === 'true';
      document.querySelectorAll('.faq__q').forEach(function(other){
        other.setAttribute('aria-expanded','false');
        other.nextElementSibling.style.maxHeight = null;
      });
      if(!expanded){
        btn.setAttribute('aria-expanded','true');
        var panel = btn.nextElementSibling;
        panel.style.maxHeight = panel.scrollHeight + 'px';
      }
    });
  });

  // registration form (front-end only demo)
  var form = document.getElementById('regForm');
  var note = document.getElementById('regNote');
  if(form){
    form.addEventListener('submit', function(e){
      e.preventDefault();
      if(!form.checkValidity()){ form.reportValidity(); return; }
      form.classList.add('is-sent');
      note.textContent = 'Filed. Check your inbox for a confirmation from the organising committee.';
    });
  }

  // hero branching timeline SVG — one orchestrated load animation
  (function(){
    var svg = document.getElementById('branchSvg');
    if(!svg) return;
    var ns = 'http://www.w3.org/2000/svg';
    var W = 1200, H = 800, cx = W/2, cy = H*0.42;
    var color = '#e8a33d';

    function path(d, opacity, width, delay, dur){
      var p = document.createElementNS(ns,'path');
      p.setAttribute('d', d);
      p.setAttribute('fill','none');
      p.setAttribute('stroke', color);
      p.setAttribute('stroke-width', width);
      p.setAttribute('stroke-linecap','round');
      p.setAttribute('opacity', opacity);
      svg.appendChild(p);
      var len;
      try { len = p.getTotalLength(); } catch(e){ len = 800; }
      p.style.strokeDasharray = len;
      p.style.strokeDashoffset = len;
      if(!reduceMotion){
        p.style.transition = 'stroke-dashoffset '+dur+'ms cubic-bezier(.4,.6,.2,1) '+delay+'ms';
        requestAnimationFrame(function(){
          requestAnimationFrame(function(){ p.style.strokeDashoffset = 0; });
        });
      } else {
        p.style.strokeDashoffset = 0;
      }
      return p;
    }

    // central trunk
    path('M '+cx+' '+(H+40)+' C '+cx+' '+(cy+140)+', '+cx+' '+(cy+60)+', '+cx+' '+cy, 0.9, 2, 0, 1200);

    // branches fanning from the node, varying reach + curve
    var branchCount = 9;
    for(var i=0;i<branchCount;i++){
      var t = i/(branchCount-1);
      var angle = (t-0.5) * Math.PI * 0.95;
      var reach = 260 + Math.random()*260;
      var ex = cx + Math.sin(angle)*reach;
      var ey = cy - Math.cos(angle)*reach*0.62 - 60;
      var mx = cx + Math.sin(angle)*reach*0.45;
      var my = cy - 80;
      var d = 'M '+cx+' '+cy+' Q '+mx+' '+my+', '+ex+' '+ey;
      path(d, 0.16 + Math.random()*0.22, 1, 300 + i*90, 1400);

      // small twig off some branches
      if(i % 2 === 0){
        var tx = ex + (Math.random()-0.5)*90;
        var ty = ey - 40 - Math.random()*40;
        path('M '+ex+' '+ey+' Q '+(ex+ (tx-ex)*0.5)+' '+(ey-20)+', '+tx+' '+ty, 0.12, 1, 900+i*90, 900);
      }
    }

    // node glow
    var glow = document.createElementNS(ns,'circle');
    glow.setAttribute('cx', cx); glow.setAttribute('cy', cy); glow.setAttribute('r', 5);
    glow.setAttribute('fill', color);
    glow.style.opacity = 0.9;
    glow.style.filter = 'drop-shadow(0 0 10px '+color+')';
    svg.appendChild(glow);
  })();

  // ---- custom cursor + ember trail (fine pointer, no reduced motion) ----
  var canFancyCursor = window.matchMedia('(hover:hover) and (pointer:fine)').matches && !reduceMotion;
  if(canFancyCursor){
    document.documentElement.classList.add('has-cursor');
    var cursorEl = document.createElement('div');
    cursorEl.className = 'cursor';
    document.body.appendChild(cursorEl);

    var canvas = document.createElement('canvas');
    canvas.className = 'emberCanvas';
    document.body.appendChild(canvas);
    var ctx = canvas.getContext('2d');
    function resizeCanvas(){ canvas.width = window.innerWidth; canvas.height = window.innerHeight; }
    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);

    var embers = [];
    var mouseX = -100, mouseY = -100, lastX = -100, lastY = -100;

    document.addEventListener('mousemove', function(e){
      mouseX = e.clientX; mouseY = e.clientY;
      cursorEl.style.left = mouseX + 'px';
      cursorEl.style.top = mouseY + 'px';

      var dist = Math.hypot(mouseX-lastX, mouseY-lastY);
      if(dist > 4 && embers.length < 140){
        embers.push({
          x: mouseX, y: mouseY,
          vx: (Math.random()-0.5)*0.4,
          vy: -0.3 - Math.random()*0.5,
          life: 1,
          size: 1.4 + Math.random()*1.8
        });
        lastX = mouseX; lastY = mouseY;
      }

      var target = e.target;
      var interactive = target.closest('a, button, .file, input, select, .faq__q');
      cursorEl.classList.toggle('is-hover', !!interactive);
    });

    function renderEmbers(){
      ctx.clearRect(0,0,canvas.width,canvas.height);
      for(var i=embers.length-1;i>=0;i--){
        var p = embers[i];
        p.x += p.vx; p.y += p.vy; p.life -= 0.018;
        if(p.life <= 0){ embers.splice(i,1); continue; }
        ctx.globalAlpha = Math.max(p.life, 0) * 0.8;
        ctx.fillStyle = '#e8a33d';
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.size * p.life, 0, Math.PI*2);
        ctx.fill();
      }
      ctx.globalAlpha = 1;
      requestAnimationFrame(renderEmbers);
    }
    renderEmbers();
  }

  // ---- card tilt (case files) ----
  if(!reduceMotion){
    document.querySelectorAll('.file').forEach(function(card){
      card.addEventListener('mousemove', function(e){
        var r = card.getBoundingClientRect();
        var px = (e.clientX - r.left) / r.width - 0.5;
        var py = (e.clientY - r.top) / r.height - 0.5;
        card.style.setProperty('--ry', (px * 7) + 'deg');
        card.style.setProperty('--rx', (py * -7) + 'deg');
      });
      card.addEventListener('mouseleave', function(){
        card.style.setProperty('--rx', '0deg');
        card.style.setProperty('--ry', '0deg');
      });
    });
  }

  // ---- magnetic buttons ----
  if(!reduceMotion){
    document.querySelectorAll('.btn--primary, .bar__cta').forEach(function(btn){
      btn.addEventListener('mousemove', function(e){
        var r = btn.getBoundingClientRect();
        var mx = (e.clientX - r.left - r.width/2) * 0.28;
        var my = (e.clientY - r.top - r.height/2) * 0.35;
        btn.style.setProperty('--mx', mx + 'px');
        btn.style.setProperty('--my', my + 'px');
      });
      btn.addEventListener('mouseleave', function(){
        btn.style.setProperty('--mx', '0px');
        btn.style.setProperty('--my', '0px');
      });
    });
  }

  // ---- hero glitch word, continuous unstable signal ----
  // Keep the exact existing glitch animation; only change how often it is retriggered.
  var glitchWord = document.querySelector('.glitch');
  if(glitchWord && !reduceMotion){
    function glitchHero(){
      glitchWord.classList.remove('is-glitching');
      void glitchWord.offsetWidth;
      glitchWord.classList.add('is-glitching');
      setTimeout(function(){ glitchWord.classList.remove('is-glitching'); }, 260);
      setTimeout(glitchHero, 420 + Math.random()*1100);
    }
    glitchHero();
  }

  // ---- redacted text: tap-to-toggle for touch devices ----
  document.querySelectorAll('.redact').forEach(function(r){
    r.setAttribute('tabindex','0');
    r.addEventListener('click', function(){ r.classList.toggle('is-open'); });
  });





  // ---- Loki Variant Archive ----
  (function(){
    var archive=document.getElementById('lokiArchive');
    var ytFrame=document.getElementById('lokiDoomsdayPlayer');
    if(ytFrame){
      try{
        var ytSep=ytFrame.src.indexOf('?')>-1?'&':'?';
        ytFrame.src += ytSep+'origin='+encodeURIComponent(window.location.origin);
      }catch(e){}
    }
    var closeBtn=document.getElementById('lokiArchiveClose');
    var core=document.getElementById('lokiGodCore');
    var info=document.getElementById('lokiVariantInfo');
    var status=document.getElementById('lokiAudioStatus');
    var railA=document.getElementById('lokiVariantRail'), railB=document.getElementById('lokiVariantRailRight');
    if(!archive||!core) return;
    var variants=[
      ['L-000','Loki Laufeyson','Sacred Timeline / Fallen Variant','The MCU Loki who faces Thanos aboard the Statesman in Avengers: Infinity War. This branch ends with Loki killed by Thanos before the Loki series begins.','fallen','{{LOKI_LAUFEYSON_IMAGE_DATA}}'],
      ['L-014','Classic Loki','Richard E. Grant / Elder Variant','An older Loki who survived his destined death through illusion and lived in isolation before choosing a final glorious purpose.','classic','{{CLASSIC_LOKI_IMAGE_DATA}}'],
      ['L-019','Kid Loki','Young Variant','A child variant whose branch diverged after killing Thor. Small body, significant temporal threat.','kid'],
      ['L-027','President Loki','Political Variant','A self-declared leader surrounded by rival Lokis. Authority claim: disputed. Confidence level: excessive.','president'],
      ['L-031','Boastful Loki','Weaponized Variant','A Loki whose archive signature is accompanied by unusually large claims and an even larger hammer.','boastful'],
      ['L-041','Sylvie','Variant / Enchantress Track','A Loki variant who rejected the TVA designation and pursued the truth behind the organization.','sylvie','{{SYLVIE_IMAGE_DATA}}'],
            ['L-052','Frost Giant Loki','Jotun Variant','A branch in which Loki retains his biological Frost Giant appearance rather than presenting as an Asgardian prince.','jotun','{{FROST_GIANT_LOKI_IMAGE_DATA}}'],
            ['L-073','Tour de France Loki','Sporting Variant','A brief but highly memorable temporal anomaly associated with a bicycle, competition and an unfortunate race-day branch.','tour','{{TOUR_DE_FRANCE_LOKI_IMAGE_DATA}}'],
      ['L-101','Theater / Illusion Loki','Performance Variant','A Loki branch whose survival strategy centers on deception, spectacle and impossible escapes.','theater']
    ];
    // Build a literal, readable genealogy: ten visible variant nodes branch from the single GOS root.
    var treeMap=document.getElementById('lokiTreeMap');
    var treeLines=treeMap ? treeMap.querySelector('.loki-tree-map__lines') : null;
    function makeTreeNode(v,i){{
      var n=document.createElement('button'); n.type='button'; n.className='loki-tree-node loki-tree-node--'+i;
      var portrait=v[5] ? '<span class="loki-tree-node__portrait"><img src="'+v[5]+'" alt="'+v[1]+' variant portrait" draggable="false"></span>' : '<span class="loki-tree-node__portrait portrait--'+v[4]+'"></span>';
      n.innerHTML=portrait+'<span><span class="loki-tree-node__id">'+v[0]+'</span><span class="loki-tree-node__name">'+v[1]+'</span><span class="loki-tree-node__tag">'+v[2]+'</span></span>';
      n.addEventListener('click',function(){{
        document.querySelectorAll('.loki-tree-node,.loki-variant').forEach(function(x){{{{x.classList.remove('is-selected')}}}});
        n.classList.add('is-selected');
        info.innerHTML='<b>'+v[1].toUpperCase()+'</b> // '+v[2].toUpperCase()+'<br>'+v[3];
      }});
      treeMap.appendChild(n);
    }}
    if(treeMap && treeLines){{
      var pts=[[65,40],[55,150],[65,265],[55,380],[100,465],[735,40],[745,150],[735,265],[745,380],[700,465]];
      pts.forEach(function(pt,i){{
        var x=pt[0], y=pt[1], side=x<400?-1:1, rootX=400+side*52, rootY=260+(y-260)*.16;
        var c1x=rootX+side*80, c2x=x-side*80;
        var d='M '+rootX+' '+rootY+' C '+c1x+' '+rootY+' '+c2x+' '+y+' '+x+' '+y;
        var glow=document.createElementNS('http://www.w3.org/2000/svg','path'); glow.setAttribute('d',d); glow.setAttribute('class','glow'); treeLines.appendChild(glow);
        var path=document.createElementNS('http://www.w3.org/2000/svg','path'); path.setAttribute('d',d); treeLines.appendChild(path);
        var dot=document.createElementNS('http://www.w3.org/2000/svg','circle'); dot.setAttribute('cx',x); dot.setAttribute('cy',y); dot.setAttribute('r','4'); dot.setAttribute('fill','rgba(232,163,61,.9)'); treeLines.appendChild(dot);
      }});
      variants.forEach(function(v,i){{makeTreeNode(v,i);}});
    }}

    function makeCard(v){
      var b=document.createElement('button'); b.className='loki-variant'; b.type='button';
      var portrait=v[5] ? '<span class="loki-variant__portrait portrait--'+v[4]+'"><img src="'+v[5]+'" alt="'+v[1]+' variant portrait" draggable="false"><span></span></span>' : '<span class="loki-variant__portrait portrait--'+v[4]+'"><span></span></span>';
      b.innerHTML=portrait+'<span class="loki-variant__id">'+v[0]+'</span><span class="loki-variant__name">'+v[1]+'</span><span class="loki-variant__tag">'+v[2]+'<em>BRANCH OF L-∞</em></span>';
      b.addEventListener('click',function(){
        document.querySelectorAll('.loki-variant').forEach(function(x){x.classList.remove('is-selected')}); b.classList.add('is-selected');
        info.innerHTML='<b>'+v[1].toUpperCase()+'</b> // '+v[2].toUpperCase()+'<br>'+v[3];
      }); return b;
    }
    variants.forEach(function(v,i){(i<6?railA:railB).appendChild(makeCard(v));});

    // Every variant remains temporally unstable. The archive continuously
    // reintroduces short, irregular TVA-style interference instead of only
    // glitching once on first interaction.
    function triggerVariantGlitch(){
      var cards=Array.prototype.slice.call(document.querySelectorAll('.loki-variant'));
      if(!cards.length) return;
      var card=cards[Math.floor(Math.random()*cards.length)];
      card.classList.remove('is-glitching');
      void card.offsetWidth;
      card.classList.add('is-glitching');
      setTimeout(function(){card.classList.remove('is-glitching');},220+Math.random()*260);
    }
    setInterval(function(){
      if(archive.classList.contains('is-open')){
        triggerVariantGlitch();
        if(Math.random()>.55) setTimeout(triggerVariantGlitch,120+Math.random()*260);
      }
    },850);

    var audioCtx=null, activeNodes=[];
    function proceduralLokiCue(){
      try{
        var AC=window.AudioContext||window.webkitAudioContext; if(!AC) return false; audioCtx=audioCtx||new AC(); if(audioCtx.state==='suspended') audioCtx.resume();
        var n=audioCtx.currentTime, master=audioCtx.createGain(); master.gain.setValueAtTime(.0001,n); master.gain.exponentialRampToValueAtTime(.055,n+.25); master.gain.exponentialRampToValueAtTime(.0001,n+18); master.connect(audioCtx.destination);
        function t(f,s,d,g,type){var o=audioCtx.createOscillator(),x=audioCtx.createGain();o.type=type||'sine';o.frequency.setValueAtTime(f,n+s);x.gain.setValueAtTime(.0001,n+s);x.gain.exponentialRampToValueAtTime(g,n+s+.08);x.gain.exponentialRampToValueAtTime(.0001,n+s+d);o.connect(x);x.connect(master);o.start(n+s);o.stop(n+s+d+.03);activeNodes.push(o);}
        t(73.42,0,8,.06,'triangle'); t(110,1.1,7,.035,'sine'); t(146.83,2.2,6,.028,'sine'); t(220,4,5,.022,'sine'); t(293.66,6.5,4,.018,'sine'); t(369.99,9,3,.016,'sine');
        [0,1.1,2.2,3.3,4.4,5.5,6.6,7.7,8.8].forEach(function(s){t(98,s,.07,.018,'square');});
        status.classList.add('is-live'); status.querySelector('span').textContent='ORIGINAL TEMPORAL SCORE // LIVE'; return true;
      }catch(e){return false;}
    }
    function requestYouTubePlay(){
      // YouTube Error 153 blocks this video's embedded player in some environments.
      // Open the official source directly instead of using an iframe.
      var official='https://www.youtube.com/watch?v=183tEhupiSQ';
      try{
        var w=window.open(official,'_blank','noopener,noreferrer');
        if(!w){ window.location.href=official; }
      }catch(e){ window.location.href=official; }
      status.classList.add('is-live');
      status.querySelector('span').textContent='LOKI THEME // OFFICIAL CHANNEL OPEN';
    }
    function doomsdayCue(){
      requestYouTubePlay();
      try{
        var AC=window.AudioContext||window.webkitAudioContext;if(!AC)return true;audioCtx=audioCtx||new AC();if(audioCtx.state==='suspended')audioCtx.resume();
        var n=audioCtx.currentTime,m=audioCtx.createGain();m.gain.setValueAtTime(.0001,n);m.gain.exponentialRampToValueAtTime(.035,n+.08);m.gain.exponentialRampToValueAtTime(.0001,n+2.8);m.connect(audioCtx.destination);
        function t(f,s,d,g,type){var o=audioCtx.createOscillator(),x=audioCtx.createGain();o.type=type||'sawtooth';o.frequency.setValueAtTime(f,n+s);x.gain.setValueAtTime(.0001,n+s);x.gain.exponentialRampToValueAtTime(g,n+s+.03);x.gain.exponentialRampToValueAtTime(.0001,n+s+d);o.connect(x);x.connect(m);o.start(n+s);o.stop(n+s+d+.03);}
        [55,55,61.74,73.42].forEach(function(f,i){t(f,i*.32,1.6,.022,'sawtooth');});
      }catch(e){}
      info.innerHTML='<b>LOKI // TEMPORAL SCORE</b><br>The official Loki theme channel is open. If playback is blocked, use the Play control in the YouTube player.';
      status.classList.add('is-live'); status.querySelector('span').textContent='LOKI THEME // CHANNEL OPEN'; return true;
    }
    function openArchive(){
      archive.classList.add('is-open');archive.setAttribute('aria-hidden','false');document.body.classList.add('loki-archive-open');
      var float=document.getElementById('lokiFloat'); if(float) float.classList.add('is-hidden');
      proceduralLokiCue();
      setTimeout(function(){closeBtn.focus()},50);
    }
    function closeArchive(){archive.classList.remove('is-open');archive.setAttribute('aria-hidden','true');document.body.classList.remove('loki-archive-open');}
    window.__openLokiArchive=openArchive;
    var discovery=document.getElementById('lokiDiscovery'); if(discovery) discovery.addEventListener('click',openArchive);
    var floatButton=document.getElementById('lokiFloatButton'); if(floatButton) floatButton.addEventListener('click',openArchive);
    [document.querySelector('.tva-gate__seal'),document.querySelector('.bar__mark'),document.querySelector('.tva-prelude__brand')].forEach(function(el){if(el){el.classList.add('loki-trigger');el.addEventListener('click',openArchive);}});
    document.querySelectorAll('[data-easter]').forEach(function(el){var s=(el.getAttribute('data-easter')||'').toLowerCase();if(s.indexOf('loki')>-1||s.indexOf('sylvie')>-1||s.indexOf('mobius')>-1||s.indexOf('b-15')>-1){el.classList.add('loki-trigger');el.addEventListener('dblclick',openArchive);}});
    closeBtn.addEventListener('click',closeArchive);
    document.addEventListener('keydown',function(e){if(e.key==='Escape'&&archive.classList.contains('is-open'))closeArchive();});
    core.addEventListener('click',function(){doomsdayCue();core.classList.add('is-doomsday');setTimeout(function(){core.classList.remove('is-doomsday')},900);});
    core.addEventListener('keydown',function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();doomsdayCue();}});
  })();

  // ---- TVA temporal access gate ----
  (function(){
    var gate = document.getElementById('tvaGate');
    var accessSwitch = document.getElementById('tvaAccessSwitch');
    var switchStatus = document.getElementById('tvaSwitchStatus');
    var warning = document.getElementById('tvaGateWarning');
    if(!gate || !accessSwitch) return;

    document.body.classList.add('tva-locked');

    var prelude = document.getElementById('tvaPrelude');
    var soundStatus = document.getElementById('tvaSoundStatus');
    var audioCtx = null;
    var audioNodes = [];

    function startTemporalScore(){
      try{
        var AC = window.AudioContext || window.webkitAudioContext;
        if(!AC) return false;
        audioCtx = audioCtx || new AC();
        if(audioCtx.state === 'suspended') audioCtx.resume();
        var now = audioCtx.currentTime;
        var master = audioCtx.createGain();
        master.gain.setValueAtTime(0.0001, now);
        master.gain.exponentialRampToValueAtTime(.72, now + .18);
        master.gain.exponentialRampToValueAtTime(.0001, now + 6.6);
        master.connect(audioCtx.destination);

        function tone(freq, start, duration, gain, type, detune){
          var osc = audioCtx.createOscillator();
          var g = audioCtx.createGain();
          osc.type = type || 'sine';
          osc.detune.setValueAtTime(detune || 0, now + start);
          osc.frequency.setValueAtTime(freq, now + start);
          g.gain.setValueAtTime(0.0001, now + start);
          g.gain.exponentialRampToValueAtTime(gain, now + start + .07);
          g.gain.exponentialRampToValueAtTime(0.0001, now + start + duration);
          osc.connect(g); g.connect(master);
          osc.start(now + start); osc.stop(now + start + duration + .05);
          audioNodes.push(osc);
        }
        function noise(start, duration, gain){
          var buffer = audioCtx.createBuffer(1, audioCtx.sampleRate * duration, audioCtx.sampleRate);
          var data = buffer.getChannelData(0);
          for(var i=0;i<data.length;i++){ data[i]=(Math.random()*2-1) * Math.pow(1-i/data.length,.35); }
          var src = audioCtx.createBufferSource();
          var filter = audioCtx.createBiquadFilter();
          var g = audioCtx.createGain();
          filter.type='bandpass'; filter.frequency.value=1150; filter.Q.value=.7;
          g.gain.setValueAtTime(.0001, now + start);
          g.gain.exponentialRampToValueAtTime(gain, now + start + .03);
          g.gain.exponentialRampToValueAtTime(.0001, now + start + duration);
          src.buffer=buffer; src.connect(filter); filter.connect(g); g.connect(master);
          src.start(now+start); src.stop(now+start+duration+.02); audioNodes.push(src);
        }
        // Original procedural cue. It uses the documented high-level palette of the Loki/TVA sound world—
        // layered electronics, analog/mechanical pulses, dark energy and a theremin-like rising lead—
        // without copying the copyrighted recording or melody.
        tone(55,0,5.9,.085,'sawtooth',-4);
        tone(55.7,0,5.6,.055,'sawtooth',4);
        tone(82.4,.35,5.0,.034,'triangle');
        tone(110,.65,4.3,.018,'triangle',-7);
        [0,.48,.96,1.44,1.92,2.40,2.88,3.36,3.84,4.32,4.80].forEach(function(t){ tone(104.65,t,.045,.034,'square'); });
        [1.18,1.78,2.38,2.98,3.58].forEach(function(t){ tone(156.8,t,.08,.018,'square',-9); });
        tone(196,1.25,3.8,.015,'sine');
        tone(233.08,1.55,3.45,.017,'sine');
        tone(311.13,2.0,2.9,.019,'sine');
        tone(466.16,2.25,2.5,.014,'sine');
        tone(622.25,2.55,2.05,.010,'sine');
        tone(220,4.18,1.65,.022,'sine');
        tone(329.63,4.35,1.45,.018,'sine');
        tone(440,4.52,1.25,.014,'sine');
        noise(.10,.55,.018);
        noise(1.35,.32,.012);
        noise(2.75,.42,.016);
        noise(4.72,.72,.018);
        return true;
      }catch(e){ return false; }
    }

    function unlockTVA(){
      if(accessSwitch.classList.contains('is-on')) return;
      accessSwitch.classList.add('is-on');
      accessSwitch.setAttribute('aria-label','TVA temporal access initialized');
      if(switchStatus) switchStatus.textContent='AUTHORIZATION ACCEPTED · IGNITION FIRED';
      if(switchStatus) switchStatus.textContent='AUTHORIZATION ACCEPTED · IGNITION FIRED';
      if(soundStatus){
        var soundStarted = startTemporalScore();
        soundStatus.textContent = soundStarted ? 'AUDIO CHANNEL LIVE · TEMPORAL SIGNAL ACQUIRED' : 'AUDIO CHANNEL UNAVAILABLE · VISUAL SIGNAL ACQUIRED';
      }
      gate.classList.add('is-firing');
      var frame = gate.querySelector('.tva-gate__frame');
      if(frame) frame.classList.add('is-scanning');
      if(warning) warning.textContent='IGNITION FIRED · CHRONAL FIELD BUILDING';

      setTimeout(function(){ if(warning) warning.textContent='VARIANT SIGNATURE ACCEPTED · TIME DOOR ROTATING'; }, 520);
      setTimeout(function(){ if(warning) warning.textContent='NEXUS LOCK ACQUIRED · TEMPORAL APERTURE STABILIZING'; }, 860);
      setTimeout(function(){
        document.body.classList.remove('tva-locked');
        document.body.classList.add('tva-transit');
        document.body.classList.add('tva-unlocked');
        gate.classList.add('is-opening');
        if(typeof showToast === 'function') showToast('TVA ACCESS GRANTED · WELCOME, VARIANT');
      }, 980);
      setTimeout(function(){
        gate.remove();
        document.body.classList.remove('tva-transit');
        window.dispatchEvent(new Event('resize'));
        audioNodes.forEach(function(node){ try{ node.disconnect(); }catch(e){} });
      }, 2350);
    }

    accessSwitch.addEventListener('click', unlockTVA);
    accessSwitch.addEventListener('keydown', function(e){
      if(e.key === 'Enter' || e.key === ' '){
        e.preventDefault();
        unlockTVA();
      }
    });

    setTimeout(function(){
      gate.classList.add('is-breaking');
      setTimeout(function(){
        if(prelude) prelude.classList.add('is-done');
        gate.classList.add('is-ready');
        accessSwitch.focus();
      }, 820);
    }, 6200);
  })();

  // ---- TVA control room: live analog clock, scanner, dossier, and variant selector ----
  (function(){
    var clock = document.getElementById('tvaClock');
    var hour = document.getElementById('tvaHour');
    var minute = document.getElementById('tvaMinute');
    var second = document.getElementById('tvaSecond');
    var digital = document.getElementById('tvaDigital');
    var dateOut = document.getElementById('tvaDate');
    var temporalMeter = document.getElementById('temporalMeter');
    var temporalValue = document.getElementById('temporalValue');
    var branchValue = document.getElementById('branchValue');
    var scanLog = document.getElementById('tvaLog');
    var toast = document.getElementById('tvaToast');
    var art = document.getElementById('tvaArt');
    var agentId = document.getElementById('agentId');
    var selectedTrack = document.getElementById('selectedTrack');
    var scanBtn = document.getElementById('scanTimeline');
    var coordinateBtn = document.getElementById('newCoordinates');
    var copyBtn = document.getElementById('copyAgent');
    var clockMode = document.getElementById('clockMode');
    var clockModeLabel = document.getElementById('clockModeLabel');

    function pad2(n){ return String(n).padStart(2,'0'); }
    function showToast(message){
      if(!toast) return;
      toast.textContent = message;
      toast.classList.add('is-visible');
      clearTimeout(showToast.timer);
      showToast.timer = setTimeout(function(){ toast.classList.remove('is-visible'); }, 2600);
    }
    var useUTC = false;
    function nowTick(){
      var now = new Date();
      var ms = now.getMilliseconds();
      var sec = (useUTC ? now.getUTCSeconds() : now.getSeconds()) + ms/1000;
      var min = (useUTC ? now.getUTCMinutes() : now.getMinutes()) + sec/60;
      var rawHour = useUTC ? now.getUTCHours() : now.getHours();
      var hrs = (rawHour%12) + min/60;
      if(hour) hour.style.transform = 'translateX(-50%) rotate(' + (hrs*30) + 'deg)';
      if(minute) minute.style.transform = 'translateX(-50%) rotate(' + (min*6) + 'deg)';
      if(second) second.style.transform = 'translateX(-50%) rotate(' + (sec*6) + 'deg)';
      if(digital) digital.textContent = pad2(useUTC ? now.getUTCHours() : now.getHours()) + ':' + pad2(useUTC ? now.getUTCMinutes() : now.getMinutes()) + ':' + pad2(useUTC ? now.getUTCSeconds() : now.getSeconds());
      if(dateOut) dateOut.textContent = useUTC ? now.toLocaleDateString('en-GB',{timeZone:'UTC',weekday:'short',day:'2-digit',month:'short',year:'numeric'}) : now.toLocaleDateString(undefined,{weekday:'short',day:'2-digit',month:'short',year:'numeric'});
      requestAnimationFrame(nowTick);
    }
    nowTick();

    if(clock){
      for(var i=0;i<60;i++){
        var mark=document.createElement('span');
        mark.className='tva-clock__mark';
        mark.style.cssText='position:absolute;left:50%;top:50%;width:'+(i%5===0?'3px':'1px')+';height:'+(i%5===0?'12px':'6px')+';background:'+(i%5===0?'var(--amber)':'rgba(244,236,215,.45)')+';transform:translate(-50%,-50%) rotate('+(i*6)+'deg) translateY(-'+(i%5===0?'190px':'194px')+');transform-origin:center;opacity:'+(i%5===0?'1':'.8')+';z-index:2;pointer-events:none; border-radius:2px;';
        clock.appendChild(mark);
      }
    }

    var logs=[
      'TVA LINK ESTABLISHED — temporal channel stable',
      'ANALYSING BRANCH DENSITY — no hostile variance detected',
      'HUNTER B-15 / BENNETT UNIVERSITY — origin point confirmed',
      'CHRONAL FIELD — within acceptable student-chaos limits',
      'WATCHER NOTE — bring laptop, charger and an idea'
    ];
    function addLog(message){
      if(!scanLog) return;
      var p=document.createElement('p');
      var time=new Date().toLocaleTimeString([], {hour12:false});
      p.innerHTML='<strong>'+time+'</strong> '+message;
      scanLog.prepend(p);
      while(scanLog.children.length>7) scanLog.removeChild(scanLog.lastChild);
    }
    function randomCoordinates(){
      var letters='ABCDEFGHJKLMNPQRSTUVWXYZ';
      var sector=letters[Math.floor(Math.random()*letters.length)]+Math.floor(10+Math.random()*90);
      var branch=(Math.random()*999.999).toFixed(3);
      var stability=Math.floor(72+Math.random()*27);
      if(branchValue) branchValue.textContent=sector+' · '+branch;
      if(temporalValue) temporalValue.textContent=stability+'%';
      if(temporalMeter) temporalMeter.style.width=stability+'%';
      addLog('NEW VARIANT COORDINATES — '+sector+' / '+branch+' / integrity '+stability+'%');
      if(clock){ clock.classList.remove('tvaPulse'); void clock.offsetWidth; clock.classList.add('tvaPulse'); }
    }
    if(scanBtn){
      scanBtn.addEventListener('click',function(){
        scanBtn.classList.add('is-active');
        addLog(logs[Math.floor(Math.random()*logs.length)]);
        randomCoordinates();
        showToast('TEMPORAL SCAN COMPLETE · branch contained');
        setTimeout(function(){scanBtn.classList.remove('is-active');},500);
      });
    }
    if(coordinateBtn) coordinateBtn.addEventListener('click',randomCoordinates);

    if(copyBtn && agentId){
      copyBtn.addEventListener('click',function(){
        var value=agentId.value;
        if(navigator.clipboard && window.isSecureContext){
          navigator.clipboard.writeText(value).then(function(){ showToast('AGENT ID COPIED TO CLIPBOARD'); });
        }else{
          agentId.select();
          try{ document.execCommand('copy'); showToast('AGENT ID COPIED'); }catch(e){ showToast('AGENT ID: '+value); }
        }
      });
    }

    if(art){
      art.addEventListener('click',function(){
        art.classList.remove('tvaPulse'); void art.offsetWidth; art.classList.add('tvaPulse');
        showToast('TVA ARCHIVE IMAGE DECLASSIFIED');
      });
    }

    if(clockMode){
      clockMode.addEventListener('click',function(){
        useUTC = clockMode.dataset.mode !== 'utc';
        clockMode.dataset.mode = useUTC ? 'utc' : 'local';
        if(clockModeLabel) clockModeLabel.textContent = useUTC ? 'UTC TEMPORAL MODE' : 'LOCAL TEMPORAL MODE';
        showToast(useUTC ? 'CLOCK SHIFTED TO UTC' : 'CLOCK RETURNED TO LOCAL TIME');
      });
    }

    document.querySelectorAll('.file').forEach(function(card){
      card.addEventListener('click',function(){
        document.querySelectorAll('.file').forEach(function(other){ other.classList.remove('is-selected'); });
        card.classList.add('is-selected');
        var code=card.querySelector('.file__code');
        var name=card.querySelector('.file__name');
        if(selectedTrack) selectedTrack.textContent=(code?code.textContent:'TVA')+' · '+(name?name.textContent:'VARIANT');
        addLog('CASE FILE OPENED — '+(code?code.textContent:'')+' '+(name?name.textContent:''));
        showToast('CASE FILE LOCKED · '+(code?code.textContent:''));
      });
      card.addEventListener('keydown',function(e){
        if(e.key==='Enter' || e.key===' '){ e.preventDefault(); card.click(); }
      });
    });

    document.querySelectorAll('.tl__node').forEach(function(node){
      node.addEventListener('click',function(){
        document.querySelectorAll('.tl__node').forEach(function(n){ n.classList.remove('is-selected'); });
        node.classList.add('is-selected');
        var title=node.querySelector('.tl__title');
        if(title) showToast('CHECKPOINT PINNED · '+title.textContent);
      });
    });

    randomCoordinates();
  })();

  // ---- live "variants declared" ticker number ----
  var liveNum = document.getElementById('liveVariants');
  if(liveNum){
    var base = 236;
    function bump(){
      base += Math.floor(Math.random()*3);
      liveNum.textContent = base;
    }
    setInterval(bump, 4000 + Math.random()*3000);
  }
})();
"""

JS = JS.replace("{{SYLVIE_IMAGE_DATA}}", SYLVIE_IMAGE_DATA)
JS = JS.replace("{{LOKI_LAUFEYSON_IMAGE_DATA}}", LOKI_LAUFEYSON_IMAGE_DATA)
JS = JS.replace("{{CLASSIC_LOKI_IMAGE_DATA}}", CLASSIC_LOKI_IMAGE_DATA)
JS = JS.replace("{{FROST_GIANT_LOKI_IMAGE_DATA}}", FROST_GIANT_LOKI_IMAGE_DATA)
JS = JS.replace("{{TOUR_DE_FRANCE_LOKI_IMAGE_DATA}}", TOUR_DE_FRANCE_LOKI_IMAGE_DATA)

HTML = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(ev['name'])} — {esc(ev['organizer'])}</title>
<meta name="description" content="{esc(ev['tagline'])}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300;0,9..144,500;0,9..144,600;0,9..144,700;0,9..144,900;1,9..144,500&family=IBM+Plex+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="icon" href="data:,">
<style>
{CSS}

/* ================= LOKI ARCHIVE — STRUCTURAL CSS ================= */
.loki-archive{{
  position:fixed; inset:0; z-index:500; display:none; overflow:hidden;
  color:var(--paper); background:#070604; font-family:var(--font-mono);
}}
.loki-archive.is-open{{display:block; animation:lokiArchiveIn .45s ease both;}}
.loki-archive__bg{{position:absolute;inset:0;background:
  radial-gradient(circle at 50% 45%,rgba(232,163,61,.10),transparent 25%),
  radial-gradient(circle at 50% 110%,rgba(55,93,83,.14),transparent 48%),
  linear-gradient(180deg,#0c0906,#100b07 48%,#080705);}}
.loki-archive__grid{{position:absolute;inset:0;opacity:.32;background-image:
  linear-gradient(rgba(232,163,61,.07) 1px,transparent 1px),
  linear-gradient(90deg,rgba(232,163,61,.07) 1px,transparent 1px);
  background-size:42px 42px;transform:perspective(700px) rotateX(55deg) scale(1.6) translateY(18%);transform-origin:center bottom;}}
.loki-archive__scan{{position:absolute;inset:0;pointer-events:none;background:repeating-linear-gradient(180deg,transparent 0 5px,rgba(255,255,255,.018) 6px 7px);mix-blend-mode:screen;}}
.loki-archive__header{{position:relative;z-index:3;height:58px;display:flex;align-items:center;justify-content:space-between;gap:18px;padding:0 24px;border-bottom:1px solid rgba(232,163,61,.28);background:rgba(10,7,4,.94);font-size:10px;letter-spacing:.14em;text-transform:uppercase;}}
.loki-archive__header b{{color:var(--amber);}}
.loki-archive__close{{appearance:none;border:1px solid rgba(232,163,61,.45);background:#120d08;color:var(--paper);padding:9px 12px;font:inherit;font-size:8px;letter-spacing:.12em;cursor:pointer;}}
.loki-archive__close:hover{{border-color:var(--amber);color:var(--amber);}}
.loki-archive__stage{{position:relative;z-index:2;display:grid;grid-template-columns:minmax(180px,230px) minmax(520px,1fr) minmax(180px,230px);gap:14px;align-items:stretch;max-width:1500px;height:calc(100vh - 58px - 96px);margin:0 auto;padding:16px 20px 0;}}
.loki-branch-network{{position:absolute;inset:0;z-index:0;width:100%;height:100%;pointer-events:none;overflow:visible;}}
.loki-branch-network path{{fill:none;stroke:rgba(232,163,61,.18);stroke-width:1.2;stroke-dasharray:3 7;animation:lokiBranchFlow 8s linear infinite;}}
.loki-branch-network__glow path{{stroke:rgba(232,163,61,.28);stroke-width:3;filter:blur(4px);opacity:.35;}}
.loki-branch-network__core circle{{fill:rgba(232,163,61,.55);stroke:rgba(232,163,61,.25);}}
.loki-tree-caption{{position:absolute;top:6px;left:50%;transform:translateX(-50%);z-index:2;font:7px var(--font-mono);letter-spacing:.14em;color:#7e6a50;text-transform:uppercase;white-space:nowrap;}}
.loki-tree-caption b{{color:var(--amber);}}
.loki-archive__rail{{z-index:4;}} .loki-archive__center{{z-index:3;}}
.loki-variant__tag em{{display:block;margin-top:3px;color:rgba(232,163,61,.55);font-style:normal;font-size:6px;letter-spacing:.09em;}}
.loki-core__halo--inner{{inset:13%;border-color:rgba(78,138,111,.26);animation-duration:8s;animation-direction:reverse;}}
.loki-god-photo{{position:relative;width:min(330px,29vw);height:min(470px,58vh);border:1px solid rgba(232,163,61,.42);background:#080706;overflow:hidden;box-shadow:0 0 70px rgba(232,163,61,.11),0 25px 70px rgba(0,0,0,.72);z-index:2;transform:translateZ(0);}}
.loki-god-photo::before{{content:"";position:absolute;inset:0;z-index:3;pointer-events:none;background:linear-gradient(180deg,rgba(7,5,3,.05),transparent 45%,rgba(7,5,3,.34)),repeating-linear-gradient(180deg,transparent 0 4px,rgba(255,255,255,.018) 5px 6px);mix-blend-mode:screen;}}
.loki-god-photo::after{{content:"L-∞ // ROOT";position:absolute;left:10px;bottom:9px;z-index:4;padding:4px 6px;border:1px solid rgba(232,163,61,.38);background:rgba(7,5,3,.72);font:7px var(--font-mono);letter-spacing:.12em;color:var(--amber);}}
.loki-god-photo img{{display:block;width:100%;height:100%;object-fit:cover;object-position:center top;user-select:none;}}
.loki-core__clickhint{{position:absolute;bottom:-18px;left:50%;transform:translateX(-50%);z-index:5;font:6px var(--font-mono);letter-spacing:.12em;color:#80694c;text-transform:uppercase;white-space:nowrap;opacity:.82;}}
@keyframes lokiBranchFlow{{to{{stroke-dashoffset:-100;}}}}
@media(max-width:900px){{.loki-branch-network{{display:none;}}.loki-tree-caption{{position:relative;top:auto;left:auto;transform:none;grid-column:1/-1;text-align:center;margin-bottom:-2px;white-space:normal;}}.loki-god-photo{{width:min(320px,74vw);height:min(430px,62vh);}}.loki-core__clickhint{{bottom:-16px;}}}}

.loki-archive__rail{{display:flex;flex-direction:column;gap:8px;min-width:0;overflow:auto;padding:4px 4px 18px 0;scrollbar-width:thin;}}
.loki-variant{{display:grid;grid-template-columns:48px 54px 1fr;grid-template-rows:auto auto;gap:3px 9px;width:100%;padding:11px 12px;text-align:left;appearance:none;border:1px solid rgba(232,163,61,.16);border-left:2px solid rgba(232,163,61,.32);background:rgba(18,13,8,.78);color:var(--paper-dim);font:inherit;cursor:pointer;transition:.2s ease;}}
.loki-variant__portrait{{grid-row:1/3;width:48px;height:58px;border:1px solid rgba(232,163,61,.22);position:relative;overflow:hidden;background:radial-gradient(circle at 50% 28%,#7d5a3e 0 15%,#211711 16% 36%,#0e0a07 37% 100%);box-shadow:inset 0 0 18px rgba(232,163,61,.05);}}
.loki-variant__portrait::before{{content:"";position:absolute;left:14px;top:10px;width:20px;height:22px;border-radius:48% 48% 44% 44%;background:#b88968;box-shadow:0 0 0 4px rgba(232,163,61,.05);}}
.loki-variant__portrait::after{{content:"";position:absolute;left:7px;right:7px;bottom:3px;height:31px;clip-path:polygon(18% 0,82% 0,100% 100%,0 100%);background:linear-gradient(90deg,#15100c,#704322,#15100c);border-top:1px solid rgba(232,163,61,.2);}}
.loki-variant__portrait span{{position:absolute;z-index:3;left:8px;right:8px;top:5px;height:14px;border-top:2px solid #b58a42;border-radius:50%;}}
.loki-variant__portrait.portrait--fallen{{background:radial-gradient(circle at 50% 28%,#8d6b53 0 15%,#261a15 16% 36%,#080706 37% 100%);}}
.loki-variant__portrait.portrait--fallen::after{{background:linear-gradient(90deg,#111,#3d2a24,#111);}}
.loki-variant__portrait img{{position:absolute;z-index:1;inset:0;width:100%;height:100%;object-fit:cover;object-position:center 28%;display:block;filter:saturate(.9) contrast(1.06) brightness(.9);}}
.loki-variant:hover .loki-variant__portrait img,.loki-variant.is-selected .loki-variant__portrait img{{filter:saturate(1) contrast(1.1) brightness(.98);}}
.portrait--sylvie::before,.portrait--sylvie::after{{z-index:2;pointer-events:none;}}
.portrait--sylvie::before{{left:0;top:0;width:100%;height:100%;border-radius:0;background:linear-gradient(180deg,rgba(9,20,13,.04),rgba(7,5,3,.34));box-shadow:none;}}
.portrait--sylvie::after{{left:0;right:0;bottom:0;height:42%;clip-path:none;background:linear-gradient(180deg,transparent,rgba(8,7,4,.62));border-top:0;}}
.portrait--sylvie span{{left:5px;right:5px;top:5px;height:auto;bottom:5px;border:1px solid rgba(232,163,61,.34);border-radius:0;box-shadow:inset 0 0 14px rgba(232,163,61,.08);}}.portrait--sylvie img{{object-position:center 28%;filter:saturate(.95) contrast(1.08) brightness(.94);}}
.portrait--gator{{background:radial-gradient(ellipse at 50% 50%,#55783e 0 28%,#172013 29% 65%,#0b0906 66%);}}
.portrait--gator::before{{left:8px;top:22px;width:32px;height:15px;border-radius:50%;background:#678f48;box-shadow:inset 8px 0 0 #304622,inset -8px 0 0 #304622;}}
.portrait--kid::before{{height:18px;top:12px;}}
.portrait--jotun::before{{background:#6e91a2;box-shadow:0 0 12px rgba(96,157,186,.3);}}
.portrait--sylvie::after{{background:linear-gradient(180deg,transparent 48%,rgba(7,5,3,.34) 100%);height:42%;clip-path:none;border-top:0;}}
.portrait--classic::after{{background:linear-gradient(90deg,#283025,#6d7a66,#283025);}}
.portrait--president::after{{background:linear-gradient(90deg,#1c382e,#b18a42,#1c382e);}}
.portrait--boastful::after{{background:linear-gradient(90deg,#243229,#876c3d,#243229);}}
.portrait--tour::after{{background:linear-gradient(90deg,#17301d,#b48c39,#17301d);}}
.portrait--theater::after{{background:linear-gradient(90deg,#261b2b,#6f3d69,#261b2b);}}
.portrait--stories::after{{background:linear-gradient(90deg,#1a342c,#d3a14c,#1a342c);}}
.loki-audio.is-live a{{border-color:rgba(232,163,61,.78);box-shadow:0 0 18px rgba(232,163,61,.18);animation:channelPulse 1.4s ease-in-out infinite;}}
@keyframes channelPulse{{0%,100%{{box-shadow:0 0 8px rgba(232,163,61,.08);}}50%{{box-shadow:0 0 22px rgba(232,163,61,.28);}}}}
.loki-variant.is-glitching{{animation:lokiVariantGlitch .22s steps(2,end) both;filter:brightness(1.28) saturate(1.18);}}
.loki-variant.is-glitching::before{{content:"VARIANT DESYNC";position:absolute;right:7px;top:5px;z-index:7;color:#e8a33d;font-size:6px;letter-spacing:.1em;text-shadow:-2px 0 #65d7df,2px 0 #d65b5b;pointer-events:none;}}
.loki-variant.is-glitching .loki-variant__portrait img{{filter:saturate(1.5) contrast(1.3) brightness(1.15);transform:translateX(2px) skewX(-2deg);}}
@keyframes lokiVariantGlitch{{0%{{transform:translateX(0);clip-path:inset(0)}}20%{{transform:translateX(-3px);clip-path:inset(12% 0 58% 0)}}40%{{transform:translateX(4px);clip-path:inset(62% 0 8% 0)}}60%{{transform:translateX(-2px);clip-path:inset(30% 0 34% 0)}}80%{{transform:translateX(2px);clip-path:inset(5% 0 76% 0)}}100%{{transform:translateX(0);clip-path:inset(0)}}}}

.loki-variant:hover,.loki-variant.is-selected{{border-color:rgba(232,163,61,.62);background:rgba(232,163,61,.075);color:var(--cream);transform:translateX(2px);box-shadow:0 0 20px rgba(232,163,61,.06);}}
.loki-variant__id{{grid-row:1/3;color:var(--amber-deep);font-size:8px;letter-spacing:.06em;padding-top:2px;}}
.loki-variant__name{{font-family:var(--font-display);font-size:12px;line-height:1.05;color:var(--cream);}}
.loki-variant__tag{{font-size:7px;line-height:1.35;letter-spacing:.06em;text-transform:uppercase;color:#8e7657;}}
.loki-archive__center{{position:relative;min-width:0;display:flex;flex-direction:column;align-items:center;justify-content:flex-end;padding:18px 12px 22px;}}
.loki-detail{{align-self:stretch;margin-bottom:4px;padding:8px 10px;border-top:1px solid rgba(232,163,61,.18);border-bottom:1px solid rgba(232,163,61,.18);font-size:8px;line-height:1.7;letter-spacing:.08em;color:#a99478;text-align:center;text-transform:uppercase;}}
.loki-detail span{{color:var(--amber);}}
.loki-core{{position:relative;width:min(430px,38vw);aspect-ratio:1;min-width:280px;display:grid;place-items:center;cursor:pointer;outline:none;filter:drop-shadow(0 25px 50px rgba(0,0,0,.65));}}
.loki-core__halo{{position:absolute;inset:5%;border:1px solid rgba(232,163,61,.34);border-radius:50%;box-shadow:0 0 60px rgba(232,163,61,.08),inset 0 0 50px rgba(232,163,61,.04);animation:lokiHalo 12s linear infinite;}}
.loki-core__halo::before,.loki-core__halo::after{{content:"";position:absolute;border-radius:50%;inset:8%;border:1px dashed rgba(232,163,61,.22);}}
.loki-core__halo::after{{inset:18%;border-color:rgba(62,106,95,.25);animation:lokiHalo 8s linear infinite reverse;}}
.loki-god{{position:relative;width:48%;height:70%;margin-top:3%;display:block;filter:drop-shadow(0 0 20px rgba(232,163,61,.18));}}
.loki-god__head{{position:absolute;left:25%;top:22%;width:50%;height:26%;border-radius:46% 46% 42% 42%;background:radial-gradient(circle at 38% 32%,#c39a78 0 8%,#805f49 42%,#35261f 100%);border:1px solid rgba(232,163,61,.28);z-index:3;}}
.loki-god__head::before{{content:"";position:absolute;left:25%;top:52%;width:50%;height:2px;background:#d4b69a;box-shadow:-13px -8px 0 -1px #17100d,13px -8px 0 -1px #17100d;opacity:.75;}}
.loki-god__horn{{position:absolute;top:0;width:31%;height:31%;z-index:2;background:linear-gradient(145deg,#e8d5a9,#8e713e 58%,#332718);border:1px solid rgba(232,163,61,.45);}}
.loki-god__horn--l{{left:12%;clip-path:polygon(30% 100%,0 0,72% 42%,100% 100%);transform:rotate(-8deg);}}
.loki-god__horn--r{{right:12%;clip-path:polygon(28% 100%,0 42%,72% 0,100% 100%);transform:rotate(8deg);}}
.loki-god__cloak{{position:absolute;left:12%;top:40%;width:76%;height:48%;clip-path:polygon(20% 0,80% 0,100% 100%,0 100%);background:linear-gradient(90deg,#17120e,#5b321e 46%,#17120e);border:1px solid rgba(232,163,61,.24);}}
.loki-god__gold{{position:absolute;left:20%;top:40%;width:60%;height:50%;clip-path:polygon(0 0,35% 12%,50% 0,65% 12%,100% 0,78% 100%,22% 100%);background:linear-gradient(90deg,#5c431e,#d59b39 48%,#5c431e);opacity:.8;}}
.loki-god__hands{{position:absolute;left:15%;top:63%;width:70%;height:22%;z-index:4;border-bottom:3px solid #c8a27d;border-radius:50%;opacity:.72;}}
.loki-god__story-ring{{position:absolute;left:-15%;top:47%;width:130%;height:35%;border:1px solid rgba(232,163,61,.42);border-radius:50%;transform:rotate(-12deg);box-shadow:0 0 18px rgba(232,163,61,.12);}}
.loki-core__label{{position:absolute;bottom:2%;left:50%;transform:translateX(-50%);width:100%;text-align:center;font-size:8px;letter-spacing:.13em;color:#9f896b;text-transform:uppercase;white-space:nowrap;}}
.loki-core__label b{{display:block;font-family:var(--font-display);font-size:24px;line-height:1;color:var(--cream);letter-spacing:.08em;margin-bottom:5px;}}
.loki-core.is-doomsday{{animation:lokiDoom .9s ease;}}
.loki-core.is-doomsday .loki-core__halo{{border-color:rgba(176,67,42,.8);box-shadow:0 0 90px rgba(176,67,42,.22),inset 0 0 50px rgba(176,67,42,.08);}}
.loki-archive__info{{position:relative;z-index:3;max-width:900px;min-height:58px;margin:0 auto;padding:12px 24px;border:1px solid rgba(232,163,61,.2);border-bottom:0;background:rgba(12,9,6,.94);font-size:9px;line-height:1.65;letter-spacing:.04em;color:#b7a58d;text-align:center;}}
.loki-archive__info b{{color:var(--amber);font-size:10px;}}
.loki-audio{{position:absolute;right:24px;bottom:16px;z-index:4;display:flex;align-items:center;gap:8px;font-size:7px;letter-spacing:.1em;color:#78634a;text-transform:uppercase;}}
.loki-audio i{{width:6px;height:6px;border-radius:50%;border:1px solid #6f5a40;background:transparent;}}
.loki-audio a{{color:#8e7657;text-decoration:none;border-bottom:1px solid rgba(232,163,61,.2);padding-bottom:2px;}} .loki-audio a:hover{{color:var(--amber);}}
.loki-audio.is-live{{color:var(--amber);}}.loki-audio.is-live i{{background:var(--amber);box-shadow:0 0 12px rgba(232,163,61,.8);animation:pulse 1s infinite;}}
.loki-trigger{{cursor:pointer;}}
@keyframes lokiArchiveIn{{from{{opacity:0;filter:blur(8px)}}to{{opacity:1;filter:none}}}}
@keyframes lokiHalo{{to{{transform:rotate(360deg)}}}}
@keyframes lokiDoom{{0%,100%{{transform:scale(1)}}30%{{transform:scale(1.045);filter:drop-shadow(0 0 35px rgba(176,67,42,.5))}}60%{{transform:scale(.985)}}}}
body.loki-archive-open{{overflow:hidden;}}
@media(max-width:900px){{
  .loki-archive__stage{{grid-template-columns:1fr;height:calc(100vh - 58px - 150px);overflow:auto;padding:12px 16px 0;}}
  .loki-archive__center{{order:1;min-height:410px;}}.loki-archive__rail{{order:2;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));overflow:visible;}}.loki-core{{width:min(360px,72vw);}}.loki-archive__info{{margin:0 16px;}}.loki-audio{{display:none;}}
}}
@media(max-width:560px){{
  .loki-archive__header{{height:auto;min-height:58px;padding:10px 12px;font-size:8px;}}.loki-archive__close{{padding:8px;font-size:7px;}}.loki-archive__stage{{height:calc(100vh - 80px - 125px);}}.loki-archive__rail{{grid-template-columns:1fr;}}.loki-core{{min-width:230px;width:78vw;}}.loki-core__label b{{font-size:19px;}}.loki-archive__info{{font-size:8px;}}.loki-detail{{font-size:7px;}}
}}
@media(prefers-reduced-motion:reduce){{.loki-archive.is-open{{animation:none}}.loki-core__halo{{animation:none}}.loki-core__halo::after{{animation:none}}}}

/* ---- discoverable Loki archive trigger ---- */
.loki-discovery{{position:relative;margin:28px auto 0;max-width:620px;display:flex;justify-content:center;z-index:5;}}
.loki-discovery__button{{position:relative;display:flex;align-items:center;gap:14px;width:min(100%,620px);padding:13px 16px 13px 12px;border:1px solid rgba(232,163,61,.48);background:linear-gradient(90deg,rgba(18,13,8,.94),rgba(46,28,13,.9),rgba(18,13,8,.94));color:var(--cream);font:inherit;text-align:left;cursor:pointer;overflow:hidden;box-shadow:0 0 28px rgba(232,163,61,.07),inset 0 0 18px rgba(232,163,61,.025);transition:.22s ease;animation:lokiDiscoveryPulse 3.8s ease-in-out infinite;}}
.loki-discovery__button::before{{content:"";position:absolute;top:0;bottom:0;left:-28%;width:22%;background:linear-gradient(90deg,transparent,rgba(255,218,145,.2),transparent);transform:skewX(-18deg);animation:lokiSweep 4.8s ease-in-out infinite;}}
.loki-discovery__button:hover,.loki-discovery__button:focus-visible{{border-color:var(--amber);transform:translateY(-2px);box-shadow:0 0 34px rgba(232,163,61,.15),inset 0 0 22px rgba(232,163,61,.05);outline:none;}}
.loki-discovery__seal{{width:38px;height:38px;flex:0 0 38px;border:1px solid rgba(232,163,61,.72);border-radius:50%;display:grid;place-items:center;font-size:8px;letter-spacing:.08em;color:var(--amber);position:relative;}}
.loki-discovery__seal::before{{content:"";position:absolute;inset:5px;border:1px dashed rgba(232,163,61,.38);border-radius:50%;animation:lokiHalo 7s linear infinite;}}
.loki-discovery__copy{{min-width:0;display:flex;flex-direction:column;gap:3px;}}
.loki-discovery__eyebrow{{font-size:7px;letter-spacing:.16em;color:#c79b58;text-transform:uppercase;text-shadow:0 0 8px rgba(232,163,61,.18);animation:lokiClassifiedText 3.2s ease-in-out infinite;}}
.loki-discovery__title{{font-family:var(--font-display);font-size:15px;letter-spacing:.06em;color:var(--cream);text-transform:uppercase;}}
.loki-discovery__sub{{font-size:7px;letter-spacing:.08em;color:#746047;text-transform:uppercase;}}
.loki-discovery__arrow{{margin-left:auto;color:var(--amber);font-size:18px;transition:transform .2s ease;}}
.loki-discovery__button:hover .loki-discovery__arrow,.loki-discovery__button:focus-visible .loki-discovery__arrow{{transform:translateX(4px);}}
.loki-discovery__stamp{{position:absolute;right:12px;top:7px;font-size:6px;letter-spacing:.13em;color:rgba(255,190,92,.98);border:1px solid rgba(232,163,61,.62);padding:3px 5px;transform:rotate(-3deg);text-transform:uppercase;text-shadow:0 0 9px rgba(232,163,61,.45);box-shadow:0 0 14px rgba(232,163,61,.08),inset 0 0 8px rgba(232,163,61,.05);animation:lokiStampGlow 2.1s ease-in-out infinite;}}
.loki-float{{position:fixed;right:20px;bottom:20px;z-index:145;}}
.loki-float.is-hidden{{display:none;}}
.loki-float__button{{position:relative;display:flex;align-items:center;gap:9px;padding:9px 12px;border:1px solid rgba(232,163,61,.58);background:linear-gradient(100deg,rgba(10,8,6,.96),rgba(55,34,12,.94),rgba(10,8,6,.96));color:var(--cream);font:7px var(--font-mono);letter-spacing:.1em;text-transform:uppercase;cursor:pointer;overflow:hidden;box-shadow:0 8px 30px rgba(0,0,0,.45),0 0 22px rgba(232,163,61,.09),inset 0 0 16px rgba(232,163,61,.04);animation:lokiFloatPulse 2.8s ease-in-out infinite;}}
.loki-float__button::after{{content:"";position:absolute;top:-20%;bottom:-20%;left:-45%;width:26%;background:linear-gradient(90deg,transparent,rgba(255,229,167,.65),rgba(255,255,255,.92),rgba(255,229,167,.55),transparent);transform:skewX(-20deg);filter:blur(.4px);opacity:.8;animation:lokiClassifiedShine 3.2s ease-in-out infinite;pointer-events:none;}}
.loki-float__button i{{width:7px;height:7px;border-radius:50%;background:var(--amber);box-shadow:0 0 12px rgba(232,163,61,.85),0 0 24px rgba(255,220,140,.35);animation:pulse 1.1s infinite;position:relative;z-index:1;}}
.loki-float__button:hover,.loki-float__button:focus-visible{{border-color:#ffd98a;transform:translateY(-2px);outline:none;box-shadow:0 8px 34px rgba(0,0,0,.5),0 0 34px rgba(232,163,61,.2),inset 0 0 20px rgba(255,218,145,.07);}}
.loki-float__hint{{position:absolute;right:0;bottom:calc(100% + 8px);width:210px;padding:8px 10px;border:1px solid rgba(232,163,61,.2);background:rgba(9,7,5,.96);font-size:6px;line-height:1.5;letter-spacing:.1em;color:#8f7859;text-align:right;text-transform:uppercase;opacity:0;transform:translateY(4px);pointer-events:none;transition:.2s ease;}}
.loki-float:hover .loki-float__hint,.loki-float:focus-within .loki-float__hint{{opacity:1;transform:translateY(0);}}
@keyframes lokiDiscoveryPulse{{0%,100%{{box-shadow:0 0 28px rgba(232,163,61,.05),inset 0 0 18px rgba(232,163,61,.025)}}50%{{box-shadow:0 0 34px rgba(232,163,61,.13),inset 0 0 22px rgba(232,163,61,.05)}}}}
@keyframes lokiSweep{{0%,55%{{left:-28%}}75%,100%{{left:120%}}}}
@keyframes lokiClassifiedShine{{0%,52%{{left:-45%;opacity:0}}62%{{opacity:.95}}78%,100%{{left:135%;opacity:0}}}}
@keyframes lokiClassifiedText{{0%,70%,100%{{text-shadow:0 0 7px rgba(232,163,61,.12)}}82%{{text-shadow:0 0 13px rgba(255,218,145,.72)}}}}
@keyframes lokiStampGlow{{0%,100%{{opacity:.72;box-shadow:0 0 10px rgba(232,163,61,.05),inset 0 0 6px rgba(232,163,61,.03)}}50%{{opacity:1;box-shadow:0 0 20px rgba(232,163,61,.2),inset 0 0 10px rgba(255,218,145,.08)}}}}
@keyframes lokiFloatPulse{{0%,100%{{box-shadow:0 8px 30px rgba(0,0,0,.45),0 0 14px rgba(232,163,61,.04)}}50%{{box-shadow:0 8px 30px rgba(0,0,0,.45),0 0 26px rgba(232,163,61,.12)}}}}
@media(max-width:560px){{.loki-discovery{{margin-top:20px}}.loki-discovery__button{{padding-right:12px}}.loki-discovery__stamp{{display:none}}.loki-float{{right:10px;bottom:10px}}.loki-float__button{{padding:8px 9px;font-size:6px}}.loki-float__hint{{display:none}}}}
@media(prefers-reduced-motion:reduce){{.loki-discovery__button,.loki-float__button,.loki-discovery__eyebrow,.loki-discovery__stamp,.loki-float__button::after,.loki-discovery__seal::before,.loki-discovery__button::before{{animation:none}}}}


</style>
</head>
<body>



<!-- LOKI VARIANT ARCHIVE / HIDDEN TVA ACCESS -->
<div class="loki-archive" id="lokiArchive" aria-hidden="true" role="dialog" aria-modal="true" aria-label="TVA Loki Variant Archive">
  <div class="loki-archive__bg"></div><div class="loki-archive__grid"></div><div class="loki-archive__scan"></div>
  <header class="loki-archive__header"><span>TVA // CLASSIFIED VARIANT ARCHIVE // <b>LOKI LAUFEYSON</b> // LOKI SERIES FILE</span><button class="loki-archive__close" id="lokiArchiveClose">CLOSE FILE [ESC]</button></header>
  <div class="loki-archive__stage">
    <svg class="loki-branch-network" viewBox="0 0 1000 620" preserveAspectRatio="none" aria-hidden="true">
      <g class="loki-branch-network__glow">
        <path d="M500 575 C500 520 500 455 500 390 C500 350 500 320 500 285"/>
        <path d="M500 390 C425 360 340 245 62 92"/><path d="M500 380 C425 365 320 285 40 205"/><path d="M500 375 C420 365 300 345 34 320"/><path d="M500 405 C420 430 300 470 55 450"/><path d="M500 420 C430 465 350 525 85 565"/>
        <path d="M500 390 C575 360 660 245 938 92"/><path d="M500 380 C575 365 680 285 960 205"/><path d="M500 375 C580 365 700 345 966 320"/><path d="M500 405 C580 430 700 470 945 450"/><path d="M500 420 C570 465 650 525 915 565"/>
        <path d="M500 430 C455 455 430 500 380 545"/><path d="M500 430 C545 455 570 500 620 545"/>
      </g>
      <g class="loki-branch-network__core"><circle cx="500" cy="575" r="10"/><circle cx="500" cy="575" r="23"/></g>
    </svg>
    <div class="loki-tree-caption">THE BRANCHING TREE · HELD BY <b>L-∞</b> · GOD OF STORIES</div>
    <aside class="loki-archive__rail" id="lokiVariantRail"></aside>
    <section class="loki-archive__center">
      <div class="loki-detail">TEMPORAL ENTITY // NEXUS-CLASS // AUTHORITY: UNKNOWN<br>ROOT SIGNATURE: <span>L-∞ / GOD OF STORIES</span> · BRANCH COUNT: <span>10</span> · FILE STATUS: <span id="lokiFileStatus">ACTIVE</span></div>
      <div class="loki-tree-map" id="lokiTreeMap">
        <div class="loki-tree-map__title">EVERY VARIANT BRANCHES FROM THE GOD OF STORIES</div>
        <svg class="loki-tree-map__lines" viewBox="0 0 800 520" preserveAspectRatio="none" aria-hidden="true"></svg>
        <div class="loki-tree-map__root">
          <div class="loki-core" id="lokiGodCore" tabindex="0" role="button" aria-label="Main Loki — God of Stories. Click to open the official Loki theme.">
        <div class="loki-core__halo"></div>
        <div class="loki-core__halo loki-core__halo--inner"></div>
        <div class="loki-god-photo"><img src="{GOS_IMAGE_DATA}" alt="God of Stories Loki" draggable="false"></div>
        <div class="loki-core__label"><b>LOKI</b>GOD OF STORIES // ROOT VARIANT // L-∞</div>
        <div class="loki-core__clickhint">CLICK ROOT VARIANT · OPEN LOKI THEME CHANNEL</div>
          </div>
        </div>
      </div>
    </section>
    <aside class="loki-archive__rail" id="lokiVariantRailRight"></aside>
  </div>
  <div class="loki-archive__info" id="lokiVariantInfo"><b>SELECT A VARIANT</b> // TVA records will populate this terminal. <span class="loki-archive__hint">SYLVIE FILE CONTAINS USER-SUPPLIED ARCHIVE IMAGE</span></div>
  <div class="loki-audio" id="lokiAudioStatus"><i></i><span>ARCHIVE AUDIO // STANDBY</span><a href="https://www.youtube.com/watch?v=183tEhupiSQ" target="_blank" rel="noopener noreferrer">OPEN OFFICIAL LOKI THEME</a></div>
</div>

<div class="tva-gate" id="tvaGate" aria-modal="true" role="dialog" aria-labelledby="tvaGateTitle">
  <div class="tva-gate__prelude" id="tvaPrelude" aria-hidden="true">
    <div class="tva-prelude__fracture" aria-hidden="true"></div>
    <div class="tva-prelude__breaktext">TIME IS BREAKING<small>NEXUS EVENT DETECTED // BRANCH SEPARATION IN PROGRESS</small></div>
    <div class="tva-prelude__door" aria-hidden="true"><span></span><i></i><b>TIME DOOR // NODE 15</b></div>
    <div class="tva-prelude__noise" aria-hidden="true"></div>
    <div class="tva-prelude__scanline" aria-hidden="true"></div>
    <div class="tva-prelude__stamp tva-prelude__stamp--left">DIVISION // <b>ACCESS</b><br>NODE // 15<br>STATUS // <b>WATCHING</b></div>
    <div class="tva-prelude__stamp tva-prelude__stamp--right">TEMPORAL AUTHORITY<br>SECURITY CLASS // <b>RED</b><br>PRUNING // <b>STANDBY</b></div>
    <div class="tva-prelude__stamp tva-prelude__stamp--bottom">VARIANT DETECTOR<br>SIGNATURE // <b>UNRESOLVED</b><br>CASE // NEXUS-15</div>
    <div class="tva-prelude__stamp" style="left:8%;bottom:12%;transform:rotate(3deg)">ARCHIVE NOTE<br>LOKI // <b>BRANCHING EVENT</b><br>FILE // GLORIOUS-PURPOSE</div>
    <div class="tva-prelude__core">
      <div class="tva-prelude__ring"></div>
      <div class="tva-prelude__ring" style="inset:17%;border-color:rgba(232,163,61,.12);transform:rotate(18deg);"></div>
      <div class="tva-prelude__ring" style="inset:28%;border-style:dotted;border-color:rgba(176,67,42,.22);transform:rotate(-31deg);"></div>
      <div class="tva-prelude__dial"></div>
      <div class="tva-prelude__needle"></div>
      <div class="tva-prelude__field"></div>
      <div class="tva-prelude__copy">
        <div class="tva-prelude__brand">T V A</div>
        <div class="tva-prelude__sub">TEMPORAL VARIANCE AUTHORITY · NODE 15</div>
      </div>
      <div class="tva-prelude__micro"><i></i> CHRONAL VECTOR CALIBRATING <i></i></div>
    </div>
    <div class="tva-prelude__telemetry">CHRONAL FIELD <b>STABLE</b> · BRANCH INDEX <b>14-15.11.26</b> · ANALOG CHANNEL <b>01</b> · NEXUS <b>DETECTED</b> · VARIANT <b>SYLVIE-CLASS</b></div>
  </div>
  <div class="tva-gate__aperture" aria-hidden="true"></div>
  <div class="tva-gate__frame">
    <div class="tva-gate__noise" aria-hidden="true"></div>
    <div class="tva-gate__eyebrow">
      <span>TIME VARIANCE AUTHORITY · SECURE ACCESS</span>
      <span class="tva-gate__live"><i></i>CHANNEL LIVE</span>
    </div>
    <div class="tva-gate__seal" aria-hidden="true">TVA<br>AUTHORIZED<br>ACCESS</div>
    <h1 class="tva-gate__title" id="tvaGateTitle">Temporal access<br><em>required.</em></h1>
    <p class="tva-gate__copy">This branch is classified. Initialize the TVA temporal console to establish a secure connection before entering the NEXUS PROTOCOL timeline.</p>
    <div class="tva-gate__status" aria-label="TVA access status">
      <span class="tva-gate__chip tva-gate__chip--hot">CLEARANCE: PENDING</span>
      <span class="tva-gate__chip">BRANCH: UNPRUNED</span>
      <span class="tva-gate__chip">CASE: 2026-11-14</span>
      <span class="tva-gate__chip tva-easter-hint" tabindex="0" data-easter="HUNTER B-15 / HUNTER SIGNATURE">ORIGIN: HUNTER B-15</span>
      <span class="tva-gate__chip tva-easter-hint" tabindex="0" data-easter="NEXUS-CLASS VARIANT // LOKI ARCHIVE">NEXUS: 15</span>
      <span class="tva-gate__chip">PRUNE AUTH: STANDBY</span>
    </div>
    <div class="tva-gate__diagnostics" aria-label="Temporal diagnostics">
      <div class="tva-diagnostic"><div class="tva-diagnostic__top"><span>CHRONAL STABILITY</span><span>72%</span></div><div class="tva-diagnostic__value">FIELD COHERENCE</div><div class="tva-diagnostic__meter"><i></i></div></div>
      <div class="tva-diagnostic"><div class="tva-diagnostic__top"><span>BRANCH DRIFT</span><span>LOW</span></div><div class="tva-diagnostic__value">0.43 VARIANCE</div><div class="tva-diagnostic__meter"><i></i></div></div>
      <div class="tva-diagnostic"><div class="tva-diagnostic__top"><span>NEXUS SIGNAL</span><span>LOCKED</span></div><div class="tva-diagnostic__value">EVENT WINDOW FOUND</div><div class="tva-diagnostic__meter"><i></i></div></div>
      <div class="tva-diagnostic"><div class="tva-diagnostic__top"><span>TIME DOOR</span><span>ARMED</span></div><div class="tva-diagnostic__value">ANALOG CHANNEL 01</div><div class="tva-diagnostic__meter"><i></i></div></div>
    </div>
    <div class="tva-gate__casefile"><span>CASE FILE // <b>NEXUS PROTOCOL</b></span><span>ACCESS WINDOW // <b>14–15 NOV 2026</b></span></div>
    <div class="tva-access-wrap">
      <div class="tva-access-label">
        <span class="tva-access-label__eyebrow">TVA TEMPORAL CONSOLE</span>
        <strong>AUTHORIZATION NODE</strong>
        <span id="tvaSwitchStatus">AWAITING INPUT</span>
      </div>
      <button class="tva-access-console" id="tvaAccessSwitch" type="button" aria-label="Initialize TVA temporal access">
        <span class="tva-access-console__halo" aria-hidden="true"></span>
        <span class="tva-access-console__ring tva-access-console__ring--outer" aria-hidden="true"></span>
        <span class="tva-access-console__ring tva-access-console__ring--inner" aria-hidden="true"></span>
        <span class="tva-access-console__ticks" aria-hidden="true"></span>
        <span class="tva-access-console__core" aria-hidden="true">
          <span class="tva-access-console__symbol">TVA</span>
          <span class="tva-access-console__action">INITIALIZE</span>
          <span class="tva-access-console__sub">TEMPORAL ACCESS</span>
        </span>
        <span class="tva-access-console__sweep" aria-hidden="true"></span>
      </button>
      <div class="tva-access-meta">
        <span>NODE 15</span><i></i><span>CHRONAL CHANNEL 01</span><i></i><span>SECURE</span>
      </div>
    </div>
    <p class="tva-gate__instruction">Click the TVA authorization node to open the time door</p>
    <div class="tva-gate__sound"><i></i><span id="tvaSoundStatus">AUDIO CHANNEL ARMED · PRESS INITIALIZE TO HEAR TEMPORAL SIGNAL</span></div>
    <div class="tva-gate__boot" aria-hidden="true"><i></i></div>
    <div class="tva-gate__warning" id="tvaGateWarning">ACCESS LOCKED · TEMPORAL CHANNEL NOT INITIALIZED</div>
    <div class="tva-gate__serial">TVA-NODE15 // NEXUS-ACCESS // 00014-00015 // FOR ALL TIME, ALWAYS</div>
  </div>
</div>


<div class="grain" aria-hidden="true"></div>
<div class="scanline" aria-hidden="true"></div>
<div class="cinema-vignette" aria-hidden="true"></div>
<div class="cinema-light" id="cinemaLight" aria-hidden="true"></div>
<div class="tva-toast" id="tvaToast" role="status" aria-live="polite"></div>
<div class="loki-float" id="lokiFloat">
  <div class="loki-float__hint">A sealed variant record has been flagged. This file is not part of the public event briefing.</div>
  <button class="loki-float__button" id="lokiFloatButton" type="button" aria-label="Open Loki classified archive"><i></i> LOKI // CLASSIFIED FILE</button>
</div>
<div class="tva-easter-console" id="tvaEasterConsole" aria-live="polite"><div class="tva-easter-console__inner"><div class="tva-easter-console__head"><span>TVA ARCHIVE // EASTER FILE</span><span id="tvaEasterClose">ESC</span></div><div class="tva-easter-console__body" id="tvaEasterBody">Awaiting a variant to trigger a classified archive record.</div><span class="tva-easter-console__sig">TEMPORAL ARCHIVE // EYES ONLY</span></div></div>

<header class="bar">
  <div class="bar__seal">
    <svg viewBox="0 0 40 40" class="seal__ring" aria-hidden="true">
      <circle cx="20" cy="20" r="17" fill="none" stroke="currentColor" stroke-width="1.4"/>
      <circle cx="20" cy="20" r="12.5" fill="none" stroke="currentColor" stroke-width="0.8"/>
    </svg>
    <span class="bar__mark">GFG · BU</span>
  </div>
  <nav class="bar__nav">
    <a href="#briefing">Briefing</a>
    <a href="#files">Case Files</a>
    <a href="#timeline">Timeline</a>
    <a href="#control">TVA Control</a>
    <a href="#recruit">Recruit</a>
  </nav>
  <a href="#recruit" class="bar__cta">Apply for variant status</a>
  <button class="bar__burger" id="burger" aria-label="Open menu" aria-expanded="false">
    <span></span><span></span><span></span>
  </button>
</header>

<div class="mobilenav" id="mobilenav">
  <a href="#briefing">Briefing</a>
  <a href="#loki-briefing">TVA Files</a>
  <a href="#files">Case Files</a>
  <a href="#timeline">Timeline</a>
  <a href="#recruit">Recruit</a>
</div>

<main>

  <section class="hero" id="top">
    <svg class="hero__branches" id="branchSvg" viewBox="0 0 1200 800" preserveAspectRatio="xMidYMid slice" aria-hidden="true"></svg>

    <div class="hero__inner">
      <p class="hero__case">{esc(ev['case_no'])}</p>
      <h1 class="hero__title">
        <span class="line">Your reality</span>
        <span class="line">just became a</span>
        <span class="line hero__variant glitch" data-text="variant.">variant.<span class="glitch__ghost glitch__ghost--cyan" aria-hidden="true">variant.</span><span class="glitch__ghost glitch__ghost--red" aria-hidden="true">variant.</span></span>
      </h1>
      <p class="hero__tagline">{esc(ev['tagline'])}</p>

      <div class="hero__meta">
        <div class="hero__metaitem"><span>Dates</span><strong>{esc(ev['dates'])}</strong></div>
        <div class="hero__metaitem"><span>Location</span><strong>{esc(ev['venue'])}</strong></div>
        <div class="hero__metaitem"><span>Format</span><strong>{esc(ev['format'])}</strong></div>
      </div>

      <div class="hero__actions">
        <a href="#recruit" class="btn btn--primary">Report for duty</a>
        <a href="#briefing" class="btn btn--ghost">Read the briefing</a>
      </div>

      <div class="loki-discovery">
        <button class="loki-discovery__button" id="lokiDiscovery" type="button" aria-label="Open classified Loki variant archive">
          <span class="loki-discovery__seal">TVA</span>
          <span class="loki-discovery__copy">
            <span class="loki-discovery__eyebrow">CLASSIFIED DISCOVERY // FILE L-∞</span>
            <span class="loki-discovery__title">A Loki variant was detected on this branch.</span>
            <span class="loki-discovery__sub">Open the sealed TVA archive before leaving this timeline.</span>
          </span>
          <span class="loki-discovery__arrow" aria-hidden="true">→</span>
          <span class="loki-discovery__stamp">EYES ONLY</span>
        </button>
      </div>

      <div class="countdown" id="countdown" aria-label="Time remaining until the timeline reconverges">
        <div class="countdown__label">Time variance countdown</div>
        <div class="countdown__row">
          <div class="countdown__unit"><span id="cd-d">00</span><small>days</small></div>
          <div class="countdown__unit"><span id="cd-h">00</span><small>hrs</small></div>
          <div class="countdown__unit"><span id="cd-m">00</span><small>min</small></div>
          <div class="countdown__unit"><span id="cd-s">00</span><small>sec</small></div>
        </div>
      </div>
    </div>

    <div class="hero__scroll" aria-hidden="true"><span></span> keep scrolling the timeline</div>
  </section>

  <div class="ticker" role="status" aria-label="Live containment status">
    <div class="ticker__track" aria-hidden="true">
      <span>TIMELINE STATUS: BRANCHED</span>
      <span>{esc(ev['case_no'])}</span>
      <span class="ticker__live">VARIANTS DECLARED: <span id="liveVariants">236</span></span>
      <span>CONTAINMENT: PENDING TEAM ARRIVAL</span><span>ARCHIVE TRACE: MISS MINUTES // 1 UNAUTHORIZED SMILE</span>
      <span>LOCATION: {esc(ev['venue'])}</span>
      <span>TIMELINE STATUS: BRANCHED</span>
      <span>{esc(ev['case_no'])}</span>
      <span class="ticker__live">VARIANTS DECLARED: <span aria-hidden="true">236</span></span>
      <span>CONTAINMENT: PENDING TEAM ARRIVAL</span>
      <span>LOCATION: {esc(ev['venue'])}</span>
    </div>
  </div>


  <section class="tva-control" id="control">
    <div class="tva-control__inner">
      <div class="tva-control__head">
        <div>
          <span class="tag">TVA control room</span>
          <h2>Monitor the branch.<br>Keep the timeline weird.</h2>
        </div>
        <p>Interactive TVA instruments for the field team: a live temporal clock, branch scanner, agent dossier and selectable case files.</p>
      </div>

      <div class="tva-control__grid">
        <div class="tva-panel tva-clock-panel">
          <div class="tva-panel__top">
            <span>CHRONAL INSTRUMENT · TVA-Ω</span>
            <span class="tva-live-dot"><i></i>LIVE</span>
          </div>
          <div class="tva-clock-wrap">
            <div class="tva-clock" id="tvaClock" aria-label="Live TVA temporal clock">
              <div class="tva-clock__ticks"></div>
              <div class="tva-clock__ticks--major"></div>
              <div class="tva-clock__brand">TIME VARIANCE AUTHORITY</div>
              <div class="tva-clock__case">{esc(ev['case_no'])}</div>
              <div class="tva-clock__hand tva-clock__hand--hour" id="tvaHour"></div>
              <div class="tva-clock__hand tva-clock__hand--minute" id="tvaMinute"></div>
              <div class="tva-clock__hand tva-clock__hand--second" id="tvaSecond"></div>
              <div class="tva-clock__hub"></div>
            </div>
            <div class="tva-clock__digital" id="tvaDigital">00:00:00</div>
            <div class="tva-clock__date" id="tvaDate">TEMPORAL DATE</div>
            <div class="tva-clock__readouts">
              <div class="tva-readout"><span>Mode</span><strong id="clockModeLabel">LOCAL TEMPORAL MODE</strong></div>
              <div class="tva-readout"><span>Origin</span><strong>BENNETT · HUNTER B-15</strong></div>
              <div class="tva-readout"><span>Status</span><strong>UNPRUNED</strong></div>
            </div>
          </div>
          <div class="tva-controls">
            <button class="tva-btn" id="clockMode" data-mode="local" type="button">Shift clock mode</button>
          </div>
        </div>

        <div class="tva-console">
          <div class="tva-console__panel">
            <div class="tva-panel__top"><span>Temporal integrity</span><span id="temporalValue">82%</span></div>
            <div class="tva-metrics">
              <div class="tva-metric">
                <div class="tva-metric__label">Branch stability</div>
                <div class="tva-metric__value" id="branchValue">B-15 · 000.000</div>
                <div class="tva-meter"><i id="temporalMeter"></i></div>
              </div>
              <div class="tva-metric">
                <div class="tva-metric__label">Selected case</div>
                <div class="tva-metric__value" id="selectedTrack">NONE · SELECT A FILE</div>
              </div>
            </div>
            <div class="tva-controls">
              <button class="tva-btn" id="scanTimeline" type="button">Scan timeline</button>
              <button class="tva-btn" id="newCoordinates" type="button">Find branch</button>
            </div>
            <div class="tva-chip-row">
              <span class="tva-chip is-hot">PRUNE PROTOCOL ARMED</span>
              <span class="tva-chip">CHRONAL SHIELD: ON</span>
              <span class="tva-chip">ANOMALY: STUDENT-CLASS</span>
            </div>
          </div>

          <div class="tva-console__panel">
            <div class="tva-panel__top"><span>Field agent dossier</span><span>ACCESS: OPEN</span></div>
            <div class="tva-dossier">
              <img class="tva-art" id="tvaArt" src="{CLOCK_ART_DATA}" alt="TVA-inspired orange clock character illustration">
              <div>
                <div class="tva-dossier__code">ARCHIVE ARTIFACT · CLOCK-01</div>
                <h3>The Temporal Clock</h3>
                <p>Archive visual recovered from the anomaly. Click the artifact to pulse the containment field.</p>
                <div class="tva-agent">
                  <input id="agentId" value="TVA-BU-2026-Ω7K4" aria-label="Agent ID" readonly>
                  <button class="tva-btn" id="copyAgent" type="button">Copy ID</button>
                </div>
              </div>
            </div>
          </div>

          <div class="tva-console__panel tva-console__panel--wide">
            <div class="tva-panel__top"><span>Chronal terminal</span><span>LIVE FEED</span></div>
            <div class="tva-log" id="tvaLog" aria-live="polite">
              <p><strong>TVA</strong> Booting temporal console…</p>
              <p><strong>TVA</strong> Waiting for agent input…</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <section class="loki-bridge" id="loki-briefing">
    <div class="loki-bridge__head">
      <span class="tag">TVA ARCHIVE // LOKI DOSSIER</span>
      <h2>The TVA remembers every branch.</h2>
      <p>This archive is built around Marvel Studios’ <em>Loki</em>: the TVA, its variants, its bureaucracy, and the question at the heart of the series — what happens when a timeline stops following the path it was assigned?</p>
    </div>
    <div class="loki-bridge__grid">
      <article class="loki-bridge__card">
        <span class="loki-bridge__code">FILE 01 // TVA</span>
        <h3>Time Variance Authority</h3>
        <p>The TVA exists outside ordinary time and space and monitors what it considers dangerous deviations. In the series, Loki arrives there after becoming a temporal variant, putting him inside a bureaucracy built around timelines, paperwork and controlled intervention.</p>
        <div class="loki-bridge__fact">KEY TERMS · TVA · SACRED TIMELINE · NEXUS EVENT · VARIANT</div>
      </article>
      <article class="loki-bridge__card">
        <span class="loki-bridge__code">FILE 02 // PERSONNEL</span>
        <h3>Mobius · B-15 · Miss Minutes</h3>
        <p>Agent Mobius investigates dangerous Variants; Hunter B-15 is one of the TVA’s field hunters; and Miss Minutes serves as the organization’s animated clock-like interface and guide. Their names appear throughout this site as classified terminals and Easter eggs.</p>
        <div class="loki-bridge__fact">FIELD AGENT · HUNTER · TVA INTERFACE</div>
      </article>
      <article class="loki-bridge__card">
        <span class="loki-bridge__code">FILE 03 // VARIANTS</span>
        <h3>Loki · Sylvie · The Branches</h3>
        <p>The archive treats Loki as the root signature and branches outward into Classic Loki, Kid Loki, President Loki, Boastful Loki, Frost Giant Loki, Tour de France Loki, Sylvie and other variant files. Sylvie is explicitly identified by Marvel as another version of Loki.</p>
        <div class="loki-bridge__fact">ROOT SIGNATURE · L-∞ · VARIANT TREE · SYLVIE</div>
      </article>
      <article class="loki-bridge__card">
        <span class="loki-bridge__code">FILE 04 // TVA SYSTEMS</span>
        <h3>TemPads · Time Doors · Archives</h3>
        <p>The TVA’s technology is part of the visual language here: TemPads, Time Doors, temporal monitoring, case files and the archive terminal. The interface deliberately turns the website into an in-universe TVA console.</p>
        <div class="loki-bridge__fact">TEMPORAL ACCESS · CHRONOMONITORING · CASE FILES</div>
      </article>
      <article class="loki-bridge__card">
        <span class="loki-bridge__code">FILE 05 // THE STORY</span>
        <h3>From Sacred Timeline to Free Branches</h3>
        <p>The series moves from the TVA’s belief in a controlled Sacred Timeline toward a much larger multiversal conflict. Season 2 returns Loki to the TVA as he deals with time slipping and the organization’s changing future.</p>
        <div class="loki-bridge__fact">SEASON 1 · SEASON 2 · MULTIVERSE · GLORIOUS PURPOSE</div>
      </article>
      <article class="loki-bridge__card loki-bridge__card--mission">
        <span class="loki-bridge__code">SIDE FILE // NEXUS PROTOCOL</span>
        <h3>Why this timeline is here</h3>
        <p>NEXUS PROTOCOL is the real-world event occupying this TVA branch: a 24-hour on-campus hackathon at Bennett University on 14–15 November 2026. It is the mission payload inside the Loki/TVA experience — not the archive’s subject.</p>
        <div class="loki-bridge__fact">14–15 NOV 2026 · BENNETT UNIVERSITY · 24 HOURS</div>
      </article>
    </div>
  </section>

  <section class="briefing" id="briefing">
    <div class="briefing__grid">
      <div class="briefing__doc">
        <span class="tag tva-easter-hint" tabindex="0" data-easter="MOBIUS M. MOBIUS // ANALYST ARCHIVE">Classified briefing</span>
        <h2>The timeline branched.<br>We need it debugged.</h2>
        <p>Somewhere between a stray semicolon and an unhandled exception, the Sacred Timeline forked. The Time Variance Authority has traced the anomaly to a single point of origin: <span class="redact" tabindex="0">Bennett University, {esc(ev['dates'])}<span class="redact__bar" aria-hidden="true"></span><span class="redact__tag">DECLASSIFIED</span></span>.</p>
        <p>{esc(ev['organizer'])} is opening a containment site — <span class="redact" tabindex="0">{esc(ev['format'])}<span class="redact__bar" aria-hidden="true"></span><span class="redact__tag">DECLASSIFIED</span></span> — for anyone willing to step off their assigned path and build something that shouldn't exist yet. Every team that registers is issued variant status for the duration of the event: full access to mentors, hardware support and a live judging floor.</p>
        <p>You don't need to be a returning agent. You need an idea, a team, and a willingness to get <span class="redact" tabindex="0">pruned<span class="redact__bar" aria-hidden="true"></span><span class="redact__tag">DECLASSIFIED</span></span> and try again. Hover or tap a blacked-out line to declassify it.</p>
      </div>
      <div class="briefing__stamp" aria-hidden="true">
        <svg viewBox="0 0 220 220">
          <circle cx="110" cy="110" r="100" fill="none" stroke="currentColor" stroke-width="3"/>
          <circle cx="110" cy="110" r="86" fill="none" stroke="currentColor" stroke-width="1"/>
          <text x="110" y="102" text-anchor="middle" class="stamptext">VARIANT</text>
          <text x="110" y="128" text-anchor="middle" class="stamptext">AUTHORIZED</text>
        </svg>
      </div>
    </div>

    <div class="stats">
      {render_stats(DATA['stats'])}
    </div>
  </section>

  <section class="files" id="files">
    <div class="section__head">
      <span class="tag">Open case files</span>
      <h2>Declare your track.<br>Eight files are open for review.</h2>
    </div>
    <div class="files__grid">
      {render_tracks(DATA['tracks'])}
    </div>
  </section>

  <section class="tl" id="timeline">
    <div class="section__head section__head--center">
      <span class="tag tva-easter-hint" tabindex="0" data-easter="SACRED TIMELINE // TVA ARCHIVE REFERENCE">The sacred timeline</span>
      <h2>Every branch, in order</h2>
    </div>
    <div class="tl__spine">
      {render_timeline(DATA['timeline'])}
    </div>
  </section>

  <section class="recruit" id="recruit">
    <div class="recruit__grid">
      <div class="recruit__copy">
        <span class="tag tag--light">Recruitment open</span>
        <h2>File your registration<br>before the branch is pruned.</h2>
        <p>Entry is free. Teams of 2–4, solo variants welcome. Confirmation and further instructions are sent to the email you file below.</p>

        <div class="faq" id="faq">
          {render_faq(DATA['faq'])}
        </div>
      </div>

      <form class="recruit__form" id="regForm" novalidate>
        <div class="recruit__formhead">
          <span class="form__casecode">FORM TVA-002</span>
          <h3>Variant registration</h3>
        </div>

        <label class="field">
          <span>Full name</span>
          <input type="text" name="name" required placeholder="As it should appear on your badge">
        </label>

        <label class="field">
          <span>Email</span>
          <input type="email" name="email" required placeholder="you@example.com">
        </label>

        <label class="field">
          <span>Phone</span>
          <input type="tel" name="phone" required placeholder="10-digit mobile number">
        </label>

        <label class="field">
          <span>College / Institution</span>
          <input type="text" name="college" required placeholder="Bennett University, or elsewhere">
        </label>

        <div class="field field--row">
          <label class="field">
            <span>Team size</span>
            <select name="teamsize" required>
              <option value="">Select</option>
              <option>Solo (1)</option>
              <option>2</option>
              <option>3</option>
              <option>4</option>
            </select>
          </label>
          <label class="field">
            <span>Track</span>
            <select name="track" required>
              <option value="">Select a case file</option>
              <option>V-01 · AI / ML Variants</option>
              <option>V-02 · Web3 & Ledger Anomalies</option>
              <option>V-03 · Open Source Nexus</option>
              <option>V-04 · Cybersecurity Containment</option>
              <option>V-05 · Recruit Track</option>
            </select>
          </label>
        </div>

        <button type="submit" class="btn btn--primary btn--block">
          <span class="btn__label">Submit for review</span>
          <span class="btn__stamped">Filed ✓</span>
        </button>
        <p class="recruit__note" id="regNote">This form is a preview of the flow — no data leaves your browser. The live event will link to the official registration form.</p>
      </form>
    </div>
  </section>

</main>

<footer class="foot">
  <div class="foot__top">
    <div class="foot__brand">
      <span class="bar__mark">GFG · BU</span>
      <p>{esc(ev['organizer'])}</p>
    </div>
    <div class="foot__links">
      <a href="#briefing">Briefing</a>
      <a href="#files">Case Files</a>
      <a href="#timeline">Timeline</a>
      <a href="#control">TVA Control</a>
      <a href="#recruit">Recruit</a>
    </div>
  </div>
  <div class="foot__bottom">
    <span>{esc(ev['case_no'])}</span>
    <span>For the Timeline. · <span class="tva-easter-hint" tabindex="0" data-easter="ALWAYS // ARCHIVE PHRASE FLAGGED">ARCHIVE</span></span>
  </div>
</footer>

<script>
{JS}
</script>
</body>
</html>
"""
output = HTML

(HERE / "index.html").write_text(output, encoding="utf-8")
print("Built index.html —", len(output), "bytes")
