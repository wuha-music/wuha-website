"""Build the static WUHA site from the Design canvas files (.dc.html) into ./site"""
import os, re, shutil, sys, json
from PIL import Image

SRC = os.path.dirname(os.path.abspath(__file__))  # source/
P = os.path.join(SRC, 'design')
OUT = os.path.join(os.path.dirname(SRC), 'site')
IMG = os.path.join(OUT, 'assets', 'img')
FNT = os.path.join(OUT, 'assets', 'fonts')
D = os.path.join(SRC, 'img')

shutil.rmtree(OUT, ignore_errors=True)
os.makedirs(IMG); os.makedirs(FNT)

# ---- assets ---------------------------------------------------------------
BLOBS = {
 '4ec5f2b561783bc0f811b4adc8145815': (os.path.join(D, 'wuha-logo.png'), 'wuha-logo.png', None),
 '3bbda600832c743d6db2d0f28cbc2bb1': (os.path.join(D, 'Cover-Losing-My-Shape-768x768.png'), 'cover-losing-my-shape.webp', 768),
 'e0081c817ef9819429a465602300dbb7': (os.path.join(D, 'Nothing-is-forever-C-Cover-768x768.png'), 'cover-nothing-is-forever.webp', 768),
 '5aef3926b9204320f9ad44580d176857': (os.path.join(D, 'Cover-Rainbow-Eyes-Club-Mix-WUHA-768x768.png'), 'cover-rainbow-eyes-club-mix.webp', 768),
 'b19370bc642c32855243f364747955b1': (os.path.join(D, 'WUHA-CD-Cover-Rainbow-Eyes-1-768x768.png'), 'cover-rainbow-eyes.webp', 768),
 '3908e2f16c12f510fa6c7bb08b6b5da0': (os.path.join(D, 'WUHA_Caroline_Extended_Club_Mix_Cover_Front-768x768.jpg'), 'cover-caroline-club-mix.webp', 768),
 '5767883bccdb2a18fa12e16ad23938c1': (os.path.join(D, 'WUHA_Caroline_Mark_Voc_Cover_Front-768x768.jpg'), 'cover-caroline.webp', 768),
 'd348640da877f8e61d26a21b2298d9b1': (os.path.join(D, 'wuha-hero-source.webp'), 'wuha-hero.webp', 2000),
 '79725613c1c4b3c60368a767808dae1d': (os.path.join(D, 'wuha-about-retouched.jpg'), 'wuha-band.webp', 1400),
 '87d984b7eb8c952f8ce7997636c2be55': (os.path.join(D, 'crowd-blue-pink.jpg'), 'crowd.webp', 2000),
 'e7a16fc6c7974a1092b684b76b0a948d': (os.path.join(D, 'BSR.jpeg'), 'bsr.webp', 400),
 '6ec1535fc3532fbbf3da2803c9aed2cf': (os.path.join(D, 'WUHA-EM-Club-Mix-Airplay-Venezuela-768x1365.png'), 'airplay-venezuela.webp', 600),
 '98e2a8e2171e801d23b3cfa0bb4dff48': (os.path.join(D, 'WUHA-EM-Club-Mix-Airplay-Mexico-768x1365.png'), 'airplay-mexico.webp', 600),
 '5f759146b5ce452b14ee226a56e65a19': (os.path.join(D, 'WUHA-Airplay-Uganda-768x1365.png'), 'airplay-uganda.webp', 600),
 '86aa8119fe8f596a10afca94145fd33f': (os.path.join(D, 'CragsRadio-768x1365.png'), 'airplay-cragsradio.webp', 600),
 '8519fa030f3e792b13867da1ad310798': (os.path.join(D, 'Chic-Radio-Hits-768x1365.jpg'), 'airplay-chic-radio-hits.webp', 600),
 '6079cabe893ff48e9abd6b50ff0ddeb2': (os.path.join(D, 'SilverMusic-Radio-768x1365.png'), 'airplay-silvermusic.webp', 600),
 '792e4e3de1a59e43bd9c5ab7fe576132': (os.path.join(D, 'DHEC-768x1365.png'), 'airplay-dhec.webp', 600),
 '13d62547ccde6fe28d4065af18f9b77a': (os.path.join(D, 'Breaking_Sound-768x1365.png'), 'airplay-breaking-sound.webp', 600),
}
for bid, (src, name, maxw) in BLOBS.items():
    dst = os.path.join(IMG, name)
    if maxw is None:
        shutil.copy(src, dst); continue
    im = Image.open(src)
    im = im.convert('RGBA') if im.mode in ('RGBA', 'LA', 'P') else im.convert('RGB')
    im.thumbnail((maxw, maxw * 2))
    im.save(dst, 'WEBP', quality=80, method=6)
# favicon from logo
lg = Image.open(os.path.join(D, 'wuha-logo.png'))
fav = Image.new('RGBA', (64, 64), (10, 10, 10, 255)); t = lg.copy(); t.thumbnail((56, 56)); fav.paste(t, ((64 - t.width) // 2, (64 - t.height) // 2), t)
fav.save(os.path.join(IMG, 'favicon.png'))

FS = os.path.join(SRC, 'fonts')
shutil.copy(os.path.join(FS, 'anton-latin-400-normal.woff2'), FNT)
for w in (400, 500, 600, 700):
    shutil.copy(os.path.join(FS, f'inter-latin-{w}-normal.woff2'), FNT)

# ---- data -----------------------------------------------------------------
def B(bid, depth):  # blob -> relative asset path
    return ('../' * depth) + 'assets/img/' + BLOBS[bid][1]

def L(sp, sc, ap, yt, am):
    return [dict(label='Spotify', url=sp), dict(label='SoundCloud', url=sc), dict(label='Apple Music', url=ap), dict(label='YouTube', url=yt), dict(label='Amazon Music', url=am)]

COV = {k: v for k, v in dict(losing='3bbda600832c743d6db2d0f28cbc2bb1', nothing='e0081c817ef9819429a465602300dbb7', rainbowClub='5aef3926b9204320f9ad44580d176857', rainbow='b19370bc642c32855243f364747955b1', carolineClub='3908e2f16c12f510fa6c7bb08b6b5da0', caroline='5767883bccdb2a18fa12e16ad23938c1').items()}
featured = L('https://open.spotify.com/track/16n7RpZmUyQnW5STC019jN', 'https://on.soundcloud.com/C70rlKUhHAFgGp354G', 'https://music.apple.com/at/song/losing-my-shape/6802519203', 'https://www.youtube.com/watch?v=MJXLZWHuYuo', 'https://amazon.de/music/player/albums/B0HFLL9X8Q')
for i, l in enumerate(featured):
    l.update(bg='#FF2E88' if i == 0 else 'transparent', fg='#0A0A0A' if i == 0 else '#F5F5F5', border='#FF2E88' if i == 0 else '#8A8A8A')
songs = [
 dict(cover=COV['nothing'], alt='Nothing Is Forever cover', date='2026-06-04', href='nothing-is-forever/', title='Nothing Is Forever', codes='ISRC QZWFX2661666\nISWC T-985.441.708-6', links=L('https://open.spotify.com/album/6PzTvdEGnA6TUWvCzrE0cA', 'https://on.soundcloud.com/k8gkXMQsF5Ucpz1Hmo', 'https://music.apple.com/at/album/nothing-is-forever-single/6767017107', 'https://youtu.be/6fRO12NRER8', 'https://amazon.de/music/player/albums/B0GZJ75PF7')),
 dict(cover=COV['rainbowClub'], alt='Rainbow Eyes EDM Club Mix cover', date='2025-11-27', href='rainbow-eyes-edm-club-mix/', title='Rainbow Eyes EDM Club Mix', codes='ISRC QT3FB2543559\nISWC T-335.815.048-4', links=L('https://open.spotify.com/album/5nGvGJoMtn1vQ4MERa67bE', 'https://soundcloud.com/wuha-music/rainbow-eyes-edm-club-mix', 'https://music.apple.com/at/song/rainbow-eyes-edm-club-mix/1845662251', 'https://youtu.be/OG51DSM73gk', 'https://amazon.com/music/player/tracks/B0FVJ1BJKH')),
 dict(cover=COV['rainbow'], alt='Rainbow Eyes cover', date='2025-05-29', href='rainbow-eyes/', title='Rainbow Eyes', codes='ISRC QZNWY2504889\nISWC T-332.322.688-2', links=L('https://open.spotify.com/track/0MfSlR26pT9XLhfOCopd6Q', 'https://soundcloud.com/wuha-music/rainbow-eyes', 'https://music.apple.com/at/song/rainbow-eyes/1813681695', 'https://www.youtube.com/watch?v=x_IUrgaaneo', 'https://amazon.com/music/player/tracks/B0F889RYQD')),
 dict(cover=COV['carolineClub'], alt='Caroline Extended Club Mix cover', date='2025-04-30', href='caroline-extended-club-mix/', title='Caroline Extended Club Mix', codes='ISRC QZMEM2546561\nISWC T-331.410.329-8', links=L('https://open.spotify.com/track/6RmhEHvWrRInEDPOYtmfQX', 'https://soundcloud.com/wuha-music/caroline-feat-mark', 'https://music.apple.com/at/song/caroline-extended-club-mix/1807645791', 'https://www.youtube.com/playlist?list=OLAK5uy_mH9DbpL8zCIJ83hdJ5w_mE5YlQbq0OaG4', 'https://amazon.com/music/player/tracks/B0F49L1S9N')),
 dict(cover=COV['caroline'], alt='Caroline feat. Marc Voc cover', date='2025-02-28', href='caroline/', title='Caroline (feat. Marc Voc)', codes='ISRC QZDA72504487\nISWC T-330.792.953-5', links=L('https://open.spotify.com/track/7rPiPqKrZdgBROQXhWjUPz', 'https://on.soundcloud.com/z90jXUje4AUjul09lh', 'https://music.apple.com/at/song/caroline-feat-mark-voc/1793828157', 'https://www.youtube.com/watch?v=S29j0sEb558', 'https://amazon.com/music/player/tracks/B0DVDXZ5S4')),
]
videos = [
 dict(kind='Music video', title='Caroline (feat. Marc Voc)', url='https://www.youtube.com/watch?v=S29j0sEb558', cover=COV['caroline']),
 dict(kind='Video', title='Nothing Is Forever', url='https://youtu.be/6fRO12NRER8', cover=COV['nothing']),
 dict(kind='Video', title='Rainbow Eyes', url='https://www.youtube.com/watch?v=x_IUrgaaneo', cover=COV['rainbow']),
 dict(kind='Video', title='Rainbow Eyes EDM Club Mix', url='https://youtu.be/OG51DSM73gk', cover=COV['rainbowClub']),
]
air = [('6ec1535fc3532fbbf3da2803c9aed2cf', 'Venezuela'), ('98e2a8e2171e801d23b3cfa0bb4dff48', 'Mexico'), ('5f759146b5ce452b14ee226a56e65a19', 'Uganda'), ('86aa8119fe8f596a10afca94145fd33f', 'CragsRadio'), ('8519fa030f3e792b13867da1ad310798', 'Chic Radio Hits'), ('6079cabe893ff48e9abd6b50ff0ddeb2', 'SilverMusic Radio'), ('792e4e3de1a59e43bd9c5ab7fe576132', 'DHEC'), ('13d62547ccde6fe28d4065af18f9b77a', 'Breaking Sound')]
airplays = [dict(img=b, name=n, alt='WUHA on air: ' + n) for b, n in air]
channels = [dict(label=a, url=b) for a, b in [('Spotify', 'https://open.spotify.com/artist/2Xa5A0dIwmZt8OBZrTv4qQ'), ('SoundCloud', 'https://soundcloud.com/wuha-music'), ('Instagram', 'https://www.instagram.com/wuha_music/'), ('Facebook', 'https://www.facebook.com/wuhamusic/'), ('YouTube', 'https://www.youtube.com/@wuha_music'), ('TikTok', 'https://www.tiktok.com/@wuha_music'), ('Amazon Music', 'https://music.amazon.de/artists/B0DT53D71V/wuha'), ('Apple Music', 'https://music.apple.com/at/artist/wuha/1790726364'), ('WhatsApp', 'https://whatsapp.com/channel/0029VbBXY1BC6Zvj8IFkdb3A')]]

# ---- template engine ------------------------------------------------------
def look(ctx, path):
    v = ctx
    for k in path.split('.'):
        v = v[k] if isinstance(v, dict) else getattr(v, k)
    return v

def esc(v):
    return str(v).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')

def find_block(s, tag, start):
    """return (open_start, open_end, close_start, close_end) of first <tag ...> from start, nesting aware"""
    o = s.find('<' + tag, start)
    if o < 0: return None
    oe = s.index('>', o) + 1
    depth, i = 1, oe
    while depth:
        n_open = s.find('<' + tag, i); n_close = s.find('</' + tag + '>', i)
        if n_open != -1 and n_open < n_close:
            depth += 1; i = s.index('>', n_open) + 1
        else:
            depth -= 1; i = n_close + len(tag) + 3
            if depth == 0: return o, oe, n_close, i

TOGGLE = {'sent', 'nlError', 'playerOn', 'playerOff', 'menuOpen'}

def render(s, ctx):
    out, i = [], 0
    while True:
        a = find_block(s, 'sc-for', i); b = find_block(s, 'sc-if', i)
        blk = min([x for x in (a, b) if x], key=lambda x: x[0], default=None)
        if not blk:
            out.append(holes(s[i:], ctx)); break
        o, oe, c, ce = blk
        out.append(holes(s[i:o], ctx))
        head, inner = s[o:oe], s[oe:c]
        if head.startswith('<sc-for'):
            lst = look(ctx, re.search(r'list="\{\{\s*([\w.]+)\s*\}\}"', head).group(1))
            name = re.search(r'as="(\w+)"', head).group(1)
            for it in lst:
                out.append(render(inner, dict(ctx, **{name: it})))
        else:
            key = re.search(r'value="\{\{\s*([\w.]+)\s*\}\}"', head).group(1)
            if key in TOGGLE:
                out.append(f'<div data-if="{key}"' + ('' if look(ctx, key) else ' hidden') + ' style="display: contents;">' + render(inner, ctx) + '</div>')
            elif look(ctx, key):
                out.append(render(inner, ctx))
        i = ce
    return ''.join(out)

def holes(s, ctx):
    s = re.sub(r'\s(onClick|onSubmit)="\{\{[^}]*\}\}"', '', s)
    return re.sub(r'\{\{\s*([\w.]+)\s*\}\}', lambda m: esc(look(ctx, m.group(1))), s)

FONTS = '''@font-face{font-family:Anton;src:url(DEPTHassets/fonts/anton-latin-400-normal.woff2) format("woff2");font-weight:400;font-display:swap}
@font-face{font-family:Inter;src:url(DEPTHassets/fonts/inter-latin-400-normal.woff2) format("woff2");font-weight:400;font-display:swap}
@font-face{font-family:Inter;src:url(DEPTHassets/fonts/inter-latin-500-normal.woff2) format("woff2");font-weight:500;font-display:swap}
@font-face{font-family:Inter;src:url(DEPTHassets/fonts/inter-latin-600-normal.woff2) format("woff2");font-weight:600;font-display:swap}
@font-face{font-family:Inter;src:url(DEPTHassets/fonts/inter-latin-700-normal.woff2) format("woff2");font-weight:700;font-display:swap}
html,body{margin:0;background:#0A0A0A;overflow-x:clip}*{box-sizing:border-box}[data-if][hidden]{display:none!important}img{max-width:100%}
'''

REVEAL_JS = r'''window.dataLayer=window.dataLayer||[];
function wuhaTrack(ev,p){var o={event:ev};for(var k in p)o[k]=p[k];window.dataLayer.push(o);}
document.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('a');if(!a)return;var h=a.getAttribute('href')||'',t=(a.textContent||'').trim();
 if(/open\.spotify\.com/.test(h))wuhaTrack('spotify_click',{link_text:t,page:location.pathname});
 if(/#newsletter$/.test(h))wuhaTrack('newsletter_button',{link_text:t,page:location.pathname});
 if(/(^|\/)listen\/$/.test(h)||(a.closest('.wuha-mbar')&&/listen/i.test(t)))wuhaTrack('listen_button',{link_text:t,page:location.pathname});
 if(a.closest('#downloads')||a.hasAttribute('data-download'))wuhaTrack('press_download',{file:a.getAttribute('data-download')||t});
});
(function(){
var reduce=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;
if(!reduce&&'IntersectionObserver' in window){
 var els=[].slice.call(document.querySelectorAll('section > div, section > h2, section > article, footer > div')).filter(function(el){return !el.closest('.wuha-hero')&&el.getBoundingClientRect().top>window.innerHeight;});
 els.forEach(function(el){el.classList.add('wuha-pre');});
 var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('wuha-in');e.target.classList.remove('wuha-pre');io.unobserve(e.target);}});},{threshold:0.12,rootMargin:'0px 0px -40px 0px'});
 els.forEach(function(el){io.observe(el);});
}
})();'''

MAIN_JS = '''(function(){
var nav=document.getElementById('wuha-nav2');
function onScroll(){var c=(window.scrollY||0)>140;nav.style.transform=c?'translateY(0)':'translateY(-100%)';nav.style.opacity=c?'1':'0';nav.style.visibility=c?'visible':'hidden';nav.style.transitionDelay=c?'0s':'0s,0s,450ms';nav.setAttribute('aria-hidden',c?'false':'true');[].forEach.call(nav.querySelectorAll('a'),function(a){a.tabIndex=c?0:-1;});}
window.addEventListener('scroll',onScroll,{passive:true});onScroll();
var reduce=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;
var sec=document.getElementById('numbers'),nums=[].slice.call(document.querySelectorAll('[data-count]'));
function show(p){nums.forEach(function(n){n.textContent=Math.round(+n.dataset.count*p).toLocaleString('en-US');});}
if(sec&&!reduce&&'IntersectionObserver' in window){var r=sec.getBoundingClientRect();if(!(r.top<window.innerHeight&&r.bottom>0)){show(0);var io=new IntersectionObserver(function(es){if(!es.some(function(e){return e.isIntersecting;}))return;io.disconnect();var t0=performance.now();function st(t){var p=Math.min(1,(t-t0)/1800);show(1-Math.pow(1-p,3));if(p<1)requestAnimationFrame(st);}requestAnimationFrame(st);},{threshold:0.35});io.observe(sec);}}
var menu=document.querySelector('[data-if="menuOpen"]'),burgers=[].slice.call(document.querySelectorAll('.wuha-burger'));
function setMenu(o){if(!menu)return;menu.hidden=!o;document.documentElement.style.overflow=o?'hidden':'';burgers.forEach(function(b){b.setAttribute('aria-expanded',o?'true':'false');});if(o){var c=menu.querySelector('button');if(c)c.focus();}}
burgers.forEach(function(b){b.addEventListener('click',function(){setMenu(true);});});
if(menu){menu.querySelector('button').addEventListener('click',function(){setMenu(false);});[].forEach.call(menu.querySelectorAll('a'),function(a){a.addEventListener('click',function(){setMenu(false);});});document.addEventListener('keydown',function(e){if(e.key==='Escape')setMenu(false);});}
var f=document.querySelector('#newsletter form');
if(f)f.addEventListener('submit',function(e){e.preventDefault();var ok=f.querySelector('[data-if="sent"]'),er=f.querySelector('[data-if="nlError"]'),bt=f.querySelector('button[type="submit"]');ok.hidden=true;er.hidden=true;bt.disabled=true;
 fetch('https://www.wuha.world/wp-admin/admin-ajax.php',{method:'POST',body:new URLSearchParams({action:'wuha_subscribe',email:f.email.value,lang:f.lang.value,website:f.website.value})})
 .then(function(r){return r.json().then(function(j){return {s:r.status,j:j};});})
 .then(function(x){if(x.j&&x.j.ok){ok.hidden=false;f.reset();wuhaTrack('newsletter_signup',{language:f.lang.value});}else{var m=er.querySelector('[data-msg]');if(x.s===429)m.textContent='Too many sign-ups from your connection. Please try again later.';else if(x.j&&x.j.error==='email')m.textContent='Please check your email address.';er.hidden=false;}})
 .catch(function(){er.hidden=false;}).then(function(){bt.disabled=false;});});
})();'''

SUB_JS = '''(function(){
var h=document.getElementById('wuha-hdr'),inner=h.firstElementChild,logo=h.querySelector('img');
function onScroll(){var s=(window.scrollY||0)>60;h.style.background=s?'rgba(10,10,10,0.72)':'rgba(10,10,10,1)';inner.style.padding=(s?'4px':'22px')+' 32px';logo.style.height=s?'20px':'34px';}
window.addEventListener('scroll',onScroll,{passive:true});onScroll();
var b=document.querySelector('[data-if="playerOff"] button');
if(b)b.addEventListener('click',function(){var on=document.querySelector('[data-if="playerOn"]');on.innerHTML='<iframe title="Spotify player" src="https://open.spotify.com/embed/'+document.body.dataset.embed+'?theme=0" width="100%" height="152" style="border:0;border-radius:12px;flex:1 1 100%" allow="encrypted-media" loading="lazy"></iframe>';on.hidden=false;document.querySelector('[data-if="playerOff"]').hidden=true;});
})();'''

SONGS = json.load(open(os.path.join(SRC, 'songs.json'), encoding='utf8'))
PAGES = [
 # source, out dir, depth, title, description
 ('Main.dc.html', '', 0, 'WUHA · International Synthpop Act from Vienna', 'WUHA is a synthpop band from Vienna, Austria. Music for the late-night drive and the dance floor. Feel the Groove.'),
 ('Press.dc.html', 'press', 1, 'Press kit · WUHA', 'WUHA press kit: bio, photos, logo, covers and facts for press, radio and playlist curators.'),
 ('Listen.dc.html', 'listen', 1, 'Listen · WUHA', 'Listen to WUHA on Spotify, Apple Music, YouTube, Amazon Music and SoundCloud.'),
]
for x in SONGS:
    PAGES.append(('Song.dc.html', x['slug'], 1, x['title'] + ' · WUHA', x['title'] + ' by WUHA, synthpop from Vienna. ' + x['tagline'] + ' Listen on Spotify, Apple Music and YouTube.', x))

def links(s, depth):
    up = '../' * depth
    s = s.replace('href="Main.dc.html#', f'href="{up or "./"}#').replace('href="Main.dc.html"', f'href="{up or "./"}"')
    for src, dst in [('Song.dc.html', 'losing-my-shape/'), ('Press.dc.html', 'press/'), ('Listen.dc.html', 'listen/')]:
        s = s.replace(f'href="{src}"', f'href="{up}{dst}"')
    s = re.sub(r'href="(https?://[^"]+)"', r'href="\1" target="_blank" rel="noopener"', s)
    return s

BUILD = os.environ.get('GITHUB_SHA', 'local')[:7]
for page in PAGES:
    src, odir, depth, title, desc = page[:5]
    song = page[5] if len(page) > 5 else None
    raw = open(os.path.join(P, src), encoding='utf8').read()
    helmet = re.search(r'<helmet>(.*?)</helmet>', raw, re.S).group(1)
    css = '\n'.join(re.findall(r'<style>(.*?)</style>', helmet, re.S))
    body = re.search(r'<x-dc>(.*?)</x-dc>', raw, re.S).group(1)
    body = re.sub(r'<helmet>.*?</helmet>', '', body, flags=re.S)
    ctx = dict(false=False, true=True, sent=False, nlError=False, menuOpen=False, menuExpanded='false', playerOn=False, playerOff=True,
               navHidden='true', navTransform='translateY(-100%)', navOpacity='0', navVisibility='hidden', navDelay='450ms', navTab='-1',
               navBg='rgba(10,10,10,1)', navPad='22px', logoH='34px',
               featured=dict(links=featured), songs=songs, videos=videos, airplays=airplays, channels=channels,
               num=dict(fans='1,961', playlists='70', followers='43,663', placements='85'))
    if song:
        ctx['song'] = dict(song, coverSrc='/_blob/' + song['cover'], hasIswc=bool(song['iswc']),
                           creditRows=[dict(k=k, v=v) for k, v in song['credits']],
                           blocks=[dict(t=x['t'], isHead=x['h'], isText=not x['h']) for x in song['story']])
        ctx['others'] = [dict(title=o['title'], short=o['short'], coverSrc='/_blob/' + o['cover'], href='../' + o['slug'] + '/') for o in SONGS if o['slug'] != song['slug']]
    for k, n in [('fans', 1961), ('playlists', 70), ('followers', 43663), ('placements', 85)]:
        body = body.replace('">{{num.%s}}</strong>' % k, '" data-count="%d">{{num.%s}}</strong>' % (n, k))
    html = render(body, ctx)
    html = re.sub(r'/_blob/([0-9a-f]{32})', lambda m: B(m.group(1), depth), html)
    # song cover/blob refs inside data were ids: map bare ids too
    html = re.sub(r'(src|href)="([0-9a-f]{32})"', lambda m: f'{m.group(1)}="{B(m.group(2), depth)}"', html)
    html = links(html, depth)
    html = html.replace("font-family: 'JetBrains Mono', monospace;", "font-family: ui-monospace, Menlo, Consolas, monospace;")
    js = REVEAL_JS
    if src == 'Main.dc.html':
        html = html.replace('<div aria-hidden="true" style="position: fixed; top: 0;', '<div id="wuha-nav2" aria-hidden="true" style="position: fixed; top: 0;', 1)
        js += MAIN_JS
    elif src in ('Song.dc.html', 'Press.dc.html'):
        html = html.replace('<header style="position: sticky;', '<header id="wuha-hdr" style="position: sticky;', 1)
        js += SUB_JS
    if src == 'Listen.dc.html':
        html = html.replace('width: 390px; height: 844px; box-sizing: border-box; overflow: hidden;', 'width: 100%; max-width: 440px; min-height: 100vh; margin: 0 auto; box-sizing: border-box;', 1)
    up = '../' * depth
    page = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{esc(desc)}">
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="#0A0A0A">
<meta name="build" content="{BUILD}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:image" content="{up}assets/img/wuha-hero.webp">
<link rel="icon" href="{up}assets/img/favicon.png">
<link rel="preload" href="{up}assets/fonts/anton-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<style>
{FONTS.replace('DEPTH', up)}{css}
</style>
</head>
<body{(' data-embed="' + song['embed'] + '"') if song else ''}>
{html.strip()}
<script>
{js}
</script>
</body>
</html>
'''
    d = os.path.join(OUT, odir); os.makedirs(d, exist_ok=True)
    open(os.path.join(d, 'index.html'), 'w', encoding='utf8').write(page)
    left = re.findall(r'\{\{[^}]*\}\}|<sc-|/_blob/', page)
    print(src, '->', os.path.join(odir, 'index.html'), 'leftovers:', left[:5])

open(os.path.join(OUT, 'robots.txt'), 'w').write('User-agent: *\nDisallow: /\n')
print('done')
