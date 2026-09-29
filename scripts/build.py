from pathlib import Path
from PIL import Image, ImageOps
from html import escape

ROOT=Path(__file__).resolve().parent.parent
chapters=[('hanoi','Hanoi','A thousand little stories.','Coffee stools, passing faces, and life spilling onto the pavement.'),('ninh_binh','Ninh Binh','Take the slow way.','Between still water and limestone, the world learns to whisper.'),('sapa','Sapa','Somewhere above the everyday.','Mountain roads, shifting clouds, and the people who make a place.'),('da_nang','Da Nang','Room to breathe.','Salt in the air. Sand underfoot. A little space between everything.'),('hoi_an','Hoi An','Stay until the lights come on.','Yellow walls by day, lantern light by night. One more reason to linger.')]
assets=ROOT/'assets'; assets.mkdir(exist_ok=True)
def process(folder):
 results=[]
 for p in sorted((ROOT/folder).iterdir()):
  if p.suffix.lower() not in ['.jpg','.jpeg','.png']: continue
  stem=f'{folder}-{p.stem.lower()}'
  with Image.open(p) as original:
   im=ImageOps.exif_transpose(original).convert('RGB')
   w,h=im.size
   for size,label in [(900,'small'),(2000,'large')]:
    dest=assets/f'{stem}-{label}.webp'
    if not dest.exists():
     copy=im.copy();copy.thumbnail((size,size));copy.save(dest,'WEBP',quality=84,method=4)
   results.append((stem,w,h))
 return results
sections=[]; total=0
for n,(folder,name,title,desc) in enumerate(chapters,1):
 photos=process(folder); total+=len(photos); cards=[]
 for i,(stem,w,h) in enumerate(photos):
  cards.append(f'<button class="photo" data-full="assets/{stem}-large.webp" data-place="{name}" aria-label="View {name} photograph {i+1}" {"hidden" if i>=6 else ""}><img src="assets/{stem}-small.webp" width="{w}" height="{h}" alt="{name} — photograph {i+1} by Bedasree Samaddar" loading="lazy" decoding="async"><span>View photograph ↗</span></button>')
 slug=folder.replace('_','-')
 sections.append(f'<section class="chapter" id="{slug}" aria-labelledby="title-{slug}"><div class="chapter-top"><p class="eyebrow">Chapter {n:02d} / {len(photos)} photographs</p><h2 id="title-{slug}">{name}</h2><div class="chapter-copy"><h3>{title}</h3><p>{desc}</p></div></div><div class="gallery">{"".join(cards)}</div><button class="expand" aria-expanded="false">Explore all {len(photos)} photographs <span>＋</span></button></section>')
me=process('me')
portraits=''.join(f'<img src="assets/{stem}-small.webp" width="{w}" height="{h}" alt="A personal moment from Bedasree’s Vietnam journey" loading="lazy">' for stem,w,h in me)
nav=''.join(f'<a href="#{f.replace("_","-")}">{name}</a>' for f,name,*_ in chapters)
html=f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#f4f1e9"><title>Vietnam — Bedasree Samaddar</title><meta name="description" content="Vietnam through the lens of Bedasree Samaddar. A photographic journey through Hanoi, Ninh Binh, Sapa, Da Nang and Hoi An."><link rel="icon" href="favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="style.css"><script src="script.js" defer></script></head>
<body><a class="skip" href="#journey">Skip to photographs</a><header><a class="wordmark" href="#">Vietnam<span>BY BEDASREE SAMADDAR</span></a><a class="about-link" href="#about">Behind the lens ↗</a></header>
<main><section class="hero"><div class="hero-copy"><p class="eyebrow">A photographic travel diary</p><h1>Vietnam<span>In passing.<br>In pictures.</span></h1><p class="intro">A few places. A hundred little moments.<br>A country I’m still looking back at.</p><a class="journey-link" href="#journey">Come wander <span>↓</span></a><p class="hero-note">PHOTOGRAPHS & MEMORIES<br>BEDASREE SAMADDAR</p></div><figure class="cover"><img src="assets/hoi_an-dsc07920-large.webp" alt="Lantern reflections glowing on the water in Hoi An" width="6016" height="4016" fetchpriority="high"><figcaption><span>VIETNAM, THROUGH MY EYES</span><span>01 — 05</span></figcaption></figure></section>
<div class="journey-intro" id="journey"><p class="eyebrow">The places that stayed with me</p><p>Follow the light.<br><em>See where it takes you.</em></p><span>5 places / {total} photographs</span></div><nav class="places" aria-label="Locations">{nav}</nav>
{''.join(sections)}
<section class="about" id="about"><div class="portraits">{portraits}</div><div class="about-copy"><p class="eyebrow">One last stop / Behind the lens</p><h2>Hello, I’m<br><em>Bedasree.</em></h2><p>I’m Bedasree Samaddar. I collect moments that don’t fit in a suitcase: a passing smile, a mountain hush, a street after dark. Vietnam gave me plenty. These are the ones I brought home.</p><span class="signature">Bedasree Samaddar</span></div></section></main>
<footer><a class="wordmark" href="#">Vietnam</a><p>Photographs by Bedasree Samaddar.<br>A little of the journey, kept here.</p><a href="#">Back to the beginning ↑</a></footer>
<dialog id="viewer" aria-label="Photograph viewer"><div class="viewer-toolbar"><p id="photo-caption" aria-live="polite"></p><div class="viewer-actions"><button id="fullscreen" aria-label="Enter full screen" aria-pressed="false" hidden>Full screen ⛶</button><button id="close" aria-label="Close photograph">Close ×</button></div></div><button id="previous" class="arrow previous" aria-label="Previous photograph">←</button><img id="full-photo" alt=""><button id="next" class="arrow next" aria-label="Next photograph">→</button><p class="viewer-hint">← → to explore · Esc to close</p></dialog></body></html>'''
(ROOT/'index.html').write_text(html)
print(f'Built {total} travel photos and {len(me)} personal photos.')
