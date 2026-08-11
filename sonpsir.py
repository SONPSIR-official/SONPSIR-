#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os
from core.lexer import Лексер, нормализовать
from core.parser import Парсер
from core.codegen import Генератор
from core.errors import ОшибкаСонпсир

ПРЕЛЮДИЯ = '''import random, sys, math, time
аргументы = sys.argv[1:]
перенос = chr(10)
def спросить(подсказка=""):
    return input(подсказка)
def спросить_число(подсказка=""):
    return int(input(подсказка))
def остаток_от_деления(a, b):
    return a % b
def разделить_текст(текст, разделитель=None):
    return текст.split(разделитель)
def записать_в_файл(путь, текст):
    with open(путь, "w", encoding="utf-8") as _ф:
        _ф.write(str(текст))
def дописать_в_файл(путь, текст):
    with open(путь, "a", encoding="utf-8") as _ф:
        _ф.write(str(текст))
def прочитать_файл(путь):
    with open(путь, encoding="utf-8") as _ф:
        return _ф.read()
def ключи(словарь):
    return list(словарь.keys())
def значение(словарь, ключ, по_умолчанию=None):
    return словарь.get(ключ, по_умолчанию)
def забрать_страницу(адрес):
    import urllib.request
    req = urllib.request.Request(адрес, headers={"User-Agent": "SONPSIR/1.0"})
    with urllib.request.urlopen(req, timeout=15) as o:
        return o.read().decode("utf-8", errors="replace")
def отправить_запрос(адрес, данные=None):
    import urllib.request, urllib.parse
    data = None
    if данные is not None:
        data = urllib.parse.urlencode(данные).encode() if isinstance(данные, dict) else str(данные).encode()
    req = urllib.request.Request(адрес, data=data, headers={"User-Agent": "SONPSIR/1.0"})
    with urllib.request.urlopen(req, timeout=15) as o:
        return o.read().decode("utf-8", errors="replace")
def найти_в_html(html, тег):
    from html.parser import HTMLParser
    class P(HTMLParser):
        def __init__(self):
            super().__init__(); self.res = []; self.depth = 0; self.buf = None
        def handle_starttag(self, t, a):
            if t == тег:
                self.depth += 1
                if self.buf is None: self.buf = ""
        def handle_endtag(self, t):
            if t == тег:
                self.depth -= 1
                if self.depth == 0 and self.buf is not None:
                    self.res.append(self.buf); self.buf = None
        def handle_data(self, d):
            if self.buf is not None: self.buf += d
    p = P(); p.feed(html); return p.res
def атрибуты_тегов(html, тег, атрибут):
    from html.parser import HTMLParser
    res = []
    class P(HTMLParser):
        def handle_starttag(self, t, attrs):
            if t == тег:
                for k, v in attrs:
                    if k == атрибут: res.append(v)
    P().feed(html); return res
def разобрать_json(текст):
    import json
    return json.loads(текст)
def в_json(объект):
    import json
    return json.dumps(объект, ensure_ascii=False)
def открыть_базу(путь):
    import sqlite3
    return sqlite3.connect(путь)
def база_выполнить(соединение, sql, данные=None):
    cur = соединение.execute(sql, данные or ())
    соединение.commit(); return cur.rowcount
def база_выбрать(соединение, sql, данные=None):
    import sqlite3
    соединение.row_factory = sqlite3.Row
    return [dict(r) for r in соединение.execute(sql, данные or ()).fetchall()]
def закрыть_базу(соединение):
    соединение.close()
def веб_сервер(порт, обработчик):
    from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
    class H(BaseHTTPRequestHandler):
        def do_GET(self):
            ответ = str(обработчик(self.path))
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(ответ.encode("utf-8"))
        def log_message(self, *a): pass
    сервер = ThreadingHTTPServer(("0.0.0.0", порт), H)
    сервер.handle_error = lambda *a, **k: print("SONPSIR: запрос с ошибкой пропущен (проверь обработчик)")
    сервер.serve_forever()
def телеграм_обновления(токен, смещение=0):
    import urllib.request, json
    адрес = f"https://api.telegram.org/bot{токен}/getUpdates?offset={смещение}&timeout=5"
    with urllib.request.urlopen(адрес, timeout=10) as o:
        return json.loads(o.read().decode()).get("result", [])
def телеграм_ответить(токен, чат, текст):
    import urllib.request, json
    адрес = f"https://api.telegram.org/bot{токен}/sendMessage"
    данные = json.dumps({"chat_id": чат, "text": str(текст)}).encode()
    req = urllib.request.Request(адрес, data=данные, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=10) as o:
        return json.loads(o.read().decode())
_визуал = {"компоненты": [], "заголовок": "SONPSIR", "тема": "неон", "шрифт": "системный", "размер": "средняя", "форма": "скруглённая", "свой_css": []}
_ТЕМЫ = {"неон": ("#00dbde","#fc00ff"), "закат": ("#ff512f","#dd2476"), "океан": ("#1a2980","#26d0ce"), "лес": ("#11998e","#38ef7d"), "огонь": ("#f12711","#f5af19"), "фиолет": ("#8e2de2","#4a00e0"), "золото": ("#f7971e","#ffd200"), "лайм": ("#a8ff78","#78ffd6"), "розовый": ("#ee9ca7","#ff9a9e"), "сталь": ("#485563","#29323c"), "мята": ("#00b09b","#96c93d"), "индиго": ("#396afc","#2948ff"), "кибер": ("#00f2fe","#4facfe"), "песок": ("#c79081","#dfa579"), "ночь": ("#232526","#414345"), "кровь": ("#870000","#190a05")}
_РАЗМЕРЫ = {"крошечная": ("5px 10px",".7rem"), "маленькая": ("8px 14px",".85rem"), "средняя": ("12px 26px","1rem"), "большая": ("16px 36px","1.25rem"), "огромная": ("22px 48px","1.6rem")}
_ФОРМЫ = {"пилюля": "999px", "скруглённая": "14px", "квадрат": "4px", "круг": "50%", "лист": "0 70% 0 70%", "волна": "60% 40% 55% 45% / 50% 60% 40% 50%"}
_ШРИФТЫ = {"системный": ("system-ui, sans-serif",""), "округлый": ("'Nunito', sans-serif","Nunito"), "строгий": ("'Montserrat', sans-serif","Montserrat"), "рукописный": ("'Caveat', cursive","Caveat"), "моно": ("'JetBrains Mono', monospace","JetBrains+Mono"), "элегантный": ("'Playfair Display', serif","Playfair+Display"), "комикс": ("'Comic Neue', cursive","Comic+Neue"), "футура": ("'Orbitron', sans-serif","Orbitron"), "детский": ("'Neucha', cursive","Neucha"), "антиква": ("'PT Serif', serif","PT+Serif")}
def визуал_заголовок(т): _визуал["заголовок"] = str(т)
def визуал_тема(т): _визуал["тема"] = т
def визуал_шрифт(ш): _визуал["шрифт"] = ш
def визуал_размер(р): _визуал["размер"] = р
def визуал_форма(ф): _визуал["форма"] = ф
def визуал_очистить(): _визуал["компоненты"] = []
def визуал_текст(т): _визуал["компоненты"].append(("текст", str(т)))
def визуал_кнопка(подпись, имя, тема=None, размер=None, форма=None):
    _визуал["компоненты"].append(("кнопка", str(подпись), str(имя), тема or _визуал["тема"], размер or _визуал["размер"], форма or _визуал["форма"]))
def визуал_поле(имя, подсказка="", размер=None):
    _визуал["компоненты"].append(("поле", str(имя), str(подсказка), размер or _визуал["размер"]))
def визуал_шаблоны():
    return f"Шаблонов кнопок: {len(_ТЕМЫ) * len(_РАЗМЕРЫ) * len(_ФОРМЫ)} (тем {len(_ТЕМЫ)} x размеров {len(_РАЗМЕРЫ)} x форм {len(_ФОРМЫ)}). Шрифтов: {len(_ШРИФТЫ)}"
_ВИЗУАЛ_ICON = '<svg xmlns="http://www.w3.org/2000/svg" width="192" height="192"><defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#00dbde"/><stop offset="1" stop-color="#fc00ff"/></linearGradient></defs><rect width="192" height="192" rx="40" fill="url(#g)"/><text x="96" y="128" font-size="95" text-anchor="middle" fill="#fff" font-family="sans-serif" font-weight="bold">S</text></svg>'
def _визуал_manifest():
    import json
    return json.dumps({"name": _визуал["заголовок"], "short_name": _визуал["заголовок"], "start_url": "/", "display": "standalone", "background_color": "#0f0c29", "theme_color": "#302b63", "icons": [{"src": "/icon.svg", "sizes": "192x192", "type": "image/svg+xml"}]}, ensure_ascii=False)
def _визуал_css():
    c1, c2 = _ТЕМЫ.get(_визуал["тема"], _ТЕМЫ["неон"])
    fam, _ = _ШРИФТЫ.get(_визуал["шрифт"], _ШРИФТЫ["системный"])
    css = f"*{{box-sizing:border-box;margin:0;padding:0}}body{{font-family:{fam};min-height:100vh;background:linear-gradient(135deg,#0f0c29,#302b63,#24243e);color:#eee;display:flex;align-items:center;justify-content:center;padding:20px}}.card{{background:rgba(255,255,255,.08);backdrop-filter:blur(12px);border:1px solid rgba(255,255,255,.15);border-radius:24px;padding:40px;max-width:520px;width:100%;box-shadow:0 20px 60px rgba(0,0,0,.4);text-align:center}}h1{{font-size:2rem;margin-bottom:20px;background:linear-gradient(90deg,{c1},{c2});-webkit-background-clip:text;-webkit-text-fill-color:transparent}}.t{{margin:12px 0;font-size:1.05rem;opacity:.9}}"
    for имя, (a, b) in _ТЕМЫ.items():
        css += f".btn-{имя}{{background:linear-gradient(90deg,{a},{b});box-shadow:0 6px 20px {b}55}}"
    for имя, (pad, fs) in _РАЗМЕРЫ.items():
        css += f".size-{имя}{{padding:{pad};font-size:{fs}}}.inp-{имя}{{font-size:{fs}}}"
    for имя, r in _ФОРМЫ.items():
        css += f".shape-{имя}{{border-radius:{r}}}"
    css += ".btn{display:inline-block;margin:8px 6px;border:none;color:#fff;font-weight:600;cursor:pointer;text-decoration:none}.btn:active{transform:scale(.95)}.f{margin:14px 0}.f input{padding:12px 16px;border-radius:12px;border:1px solid rgba(255,255,255,.2);background:rgba(255,255,255,.08);color:#eee;margin-right:8px}"
    css += "".join(_визуал.get("свой_css", []))
    return css
def _визуал_font_link():
    _, g = _ШРИФТЫ.get(_визуал["шрифт"], ("", ""))
    return f'<link href="https://fonts.googleapis.com/css2?family={g}&display=swap" rel="stylesheet">' if g else ""
def _визуал_html():
    тело = ""
    for к in _визуал["компоненты"]:
        if к[0] == "текст":
            тело += f'<p class="t">{к[1]}</p>'
        elif к[0] == "кнопка":
            тело += f'<a class="btn btn-{к[3]} size-{к[4]} shape-{к[5]}" href="/событие?имя={к[2]}">{к[1]}</a>'
        elif к[0] == "поле":
            тело += f'<form class="f" action="/событие"><input class="inp-{к[3]}" name="{к[1]}" placeholder="{к[2]}"><button class="btn btn-{_визуал["тема"]} size-{_визуал["размер"]} shape-{_визуал["форма"]}">➔</button></form>'
        elif к[0] == "блок":
            тело += к[1]
    холст_html = ""
    if "холст" in _визуал:
        import json as _json
        х = _визуал["холст"]; данные = _json.dumps(х["пиксели"], ensure_ascii=False)
        kist = _json.dumps(_визуал.get("кисть", "#00dbde"))
        js = ("const KIST=" + kist + ";const px=" + данные + ";const c=document.getElementById('c');const g=c.getContext('2d');"
              "function draw(P){g.fillStyle='#111';g.fillRect(0,0,c.width,c.height);for(const k in P){const p=k.split(',');g.fillStyle=P[k];g.fillRect(p[0]*4,p[1]*4,4,4);}}draw(px);"
              "c.style.touchAction='none';"
              "c.addEventListener('pointerdown',e=>{const r=c.getBoundingClientRect();const x=Math.floor((e.clientX-r.left)/4),y=Math.floor((e.clientY-r.top)/4);fetch('/пиксель?x='+x+'&y='+y+'&ц='+encodeURIComponent(KIST));g.fillStyle=KIST;g.fillRect(x*4,y*4,4,4);});")

        холст_html = '<canvas id="c" width="' + str(х["ш"]*4) + '" height="' + str(х["в"]*4) + '" style="image-rendering:pixelated;max-width:100%"></canvas><script>' + js + '</script>'
    return f'<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><link rel="manifest" href="/manifest.webmanifest"><meta name="theme-color" content="#302b63">{_визуал_font_link()}<title>{_визуал["заголовок"]}</title><style>{_визуал_css()}</style></head><body><div class="card"><h1>{_визуал["заголовок"]}</h1>{тело}{холст_html}</div></body></html>'
def визуал_css(css): _визуал.setdefault("свой_css", []).append(css)
def визуал_блок(html): _визуал["компоненты"].append(("блок", html))
def визуал_витрина():
    g5 = 'display:grid;grid-template-columns:repeat(5,1fr);gap:6px;justify-items:center;margin:10px 0'
    h = '<p class="t">Шрифтов: '+str(len(_ШРИФТЫ))+' | Тем: '+str(len(_ТЕМЫ))+' | Размеров: '+str(len(_РАЗМЕРЫ))+' | Форм: '+str(len(_ФОРМЫ))+' | Комбинаций: '+str(len(_ТЕМЫ)*len(_РАЗМЕРЫ)*len(_ФОРМЫ))+'</p>'
    h += '<p class="t">— ШРИФТЫ —</p><div style="'+g5+'">'
    for имя,(fam,g) in _ШРИФТЫ.items():
        h += '<span style="font-family:'+fam+';background:rgba(255,255,255,.12);padding:6px 2px;border-radius:8px;font-size:.85rem">'+имя+'</span>'
    h += '</div><p class="t">— ТЕМЫ —</p><div style="'+g5+'">'
    for имя,(a,b) in _ТЕМЫ.items():
        h += '<span style="background:linear-gradient(90deg,'+a+','+b+');padding:8px 2px;border-radius:10px;font-size:.75rem;width:100%;text-align:center">'+имя+'</span>'
    h += '</div><p class="t">— РАЗМЕРЫ —</p><div style="display:flex;flex-wrap:wrap;gap:6px;justify-content:center">'
    for имя,(pad,fs) in _РАЗМЕРЫ.items():
        h += '<span class="btn btn-неон size-'+имя+' shape-пилюля" style="pointer-events:none">'+имя+'</span>'
    h += '</div><p class="t">— ФОРМЫ —</p><div style="'+g5+'">'
    for имя,r in _ФОРМЫ.items():
        h += '<span style="background:linear-gradient(90deg,#00dbde,#fc00ff);border-radius:'+r+';padding:10px 2px;font-size:.7rem;width:100%;text-align:center">'+имя+'</span>'
    h += '</div>'
    _визуал["компоненты"].append(("блок", h))
def визуал_показать(порт, на_событие=None):
    from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
    from urllib.parse import urlparse, parse_qs

def случайное_целое(от, до):
    return random.randint(от, до)

def выбрать(список):
    if not список: return None
    return random.choice(список)

def диапазон(от, до):
    return list(range(от, до))

def соединить(список, разделитель=" "):
    return разделитель.join(str(x) for x in список)

def создать_объект(**kwargs):
    return kwargs


import math
import statistics

# --- МАТЕМАТИКА ---
def среднее(список):
    if not список: return 0
    return sum(список) / len(список)

def медиана(список):
    if not список: return 0
    sorted_list = sorted(список)
    n = len(sorted_list)
    mid = n // 2
    if n % 2 == 0:
        return (sorted_list[mid - 1] + sorted_list[mid]) / 2
    else:
        return sorted_list[mid]

def дисперсия(список):
    if len(список) < 2: return 0
    return statistics.variance(список)

def факториал(н):
    if н < 0: return 0
    res = 1
    for i in range(1, н + 1): res *= i
    return res

def степень(основание, показатель):
    return основание ** показатель

def корень(число):
    return math.sqrt(число)

def логарифм(число, основание=math.e):
    return math.log(число, основание)

# --- УНИВЕРСАЛЬНАЯ ГЕНЕРАЦИЯ ---
def сгенерировать_числа(количество, от, до):
    return [random.randint(от, до) for _ in range(количество)]

def сгенерировать_дроби(количество, от, до):
    return [round(random.uniform(от, до), 2) for _ in range(количество)]

def сгенерировать_строки(количество, длина=5):
    import string
    chars = string.ascii_letters + string.digits
    return [''.join(random.choice(chars) for _ in range(длина)) for _ in range(количество)]

def сгенерировать_координаты(количество, x_max=100, y_max=100):
    return [(random.randint(0, x_max), random.randint(0, y_max)) for _ in range(количество)]

def перемешать(список):
    random.shuffle(список)
    return список

def уникальный_выбор(список, количество):
    if количество > len(список): return список
    return random.sample(список, количество)

    class H(BaseHTTPRequestHandler):
        def do_GET(self):
            u = urlparse(self.path)
            if u.path == "/manifest.webmanifest":
                код = _визуал_manifest().encode(); self.send_response(200); self.send_header("Content-Type", "application/manifest+json"); self.end_headers(); self.wfile.write(код); return
            if u.path == "/icon.svg":
                код = _ВИЗУАЛ_ICON.encode(); self.send_response(200); self.send_header("Content-Type", "image/svg+xml"); self.end_headers(); self.wfile.write(код); return
            if u.path == "/событие" and на_событие:
                пар = parse_qs(u.query); имя = пар.get("имя", [""])[0]
                данные = {k: v[0] for k, v in пар.items() if k != "имя"}
                на_событие(имя, данные)
            код = _визуал_html().encode()
            self.send_response(200); self.send_header("Content-Type", "text/html; charset=utf-8"); self.end_headers()
            self.wfile.write(код)
        def log_message(self, *a): pass
    print(f"ВИЗУАЛ запущен: http://localhost:{порт}")
    сервер = ThreadingHTTPServer(("0.0.0.0", порт), H)
    сервер.handle_error = lambda *a, **k: print("SONPSIR: запрос с ошибкой пропущен (проверь обработчик)")
    сервер.serve_forever()

def система(команда):
    import subprocess
    r = subprocess.run(команда, shell=False, capture_output=True, text=True)
    return r.stdout + r.stderr
def файл_существует(путь):
    import os
    return os.path.exists(путь)
def список_файлов(папка="."):
    import os
    return os.listdir(папка)
def отсортировать(список):
    return sorted(список)
def перевернуть(список):
    return список[::-1]
def перемешать(список):
    import random
    x = list(список); random.shuffle(x); return x
def случайный_элемент(список):
    import random
    return random.choice(список)
def сейчас_время():
    import datetime
    return datetime.datetime.now().strftime("%H:%M:%S")
def сегодня_дата():
    import datetime
    return datetime.datetime.now().strftime("%d.%m.%Y")
def поток(функция):
    import threading
    t = threading.Thread(target=функция); t.start(); return t
def каждые(секунды, функция):
    import threading, time
    def цикл():
        while True:
            функция(); time.sleep(секунды)
    t = threading.Thread(target=цикл, daemon=True); t.start(); return t
def забрать_json(адрес):
    import urllib.request, json
    req = urllib.request.Request(адрес, headers={"User-Agent": "SONPSIR/1.0"})
    with urllib.request.urlopen(req, timeout=15) as o:
        return json.loads(o.read().decode())
def извлечь_ссылки(текст):
    import re
    return re.findall(r"https?://[^\\s<>]+", текст)
def извлечь_emails(текст):
    import re
    return re.findall(r"[\\w.+-]+@[\\w-]+\\.[\\w.]+", текст)
def инфо_ип(ip):
    return забрать_json(f"http://ip-api.com/json/{ip}")
def координаты(адрес):
    import urllib.parse
    return забрать_json("https://nominatim.openstreetmap.org/search?format=json&q=" + urllib.parse.quote(адрес))
def погода(город):
    import urllib.request, urllib.parse
    req = urllib.request.Request("https://wttr.in/" + urllib.parse.quote(город) + "?format=3", headers={"User-Agent": "SONPSIR"})
    with urllib.request.urlopen(req, timeout=15) as o:
        return o.read().decode()
def импорт_модуль(имя):
    return __import__(имя)
def питон_eval(выражение):
    return eval(выражение)
def бот_запусти(токен, обработчик):
    import urllib.request, json, time
    смещение = 0
    print("Бот запущен. Ctrl+C — стоп.")
    while True:
        try:
            адрес = f"https://api.telegram.org/bot{токен}/getUpdates?offset={смещение}&timeout=10"
            with urllib.request.urlopen(адрес, timeout=15) as o:
                обновления = json.loads(o.read().decode()).get("result", [])
            for апд in обновления:
                смещение = апд["update_id"] + 1
                сообщение = апд.get("message") or {}
                текст = сообщение.get("text", "")
                чат = (сообщение.get("chat") or {}).get("id")
                if чат:
                    ответ = обработчик(текст)
                    if ответ is not None:
                        телеграм_ответить(токен, чат, ответ)
        except KeyboardInterrupt:
            break
        except Exception:
            time.sleep(2)
def визуал_холст(ширина, высота):
    _визуал["холст"] = {"ш": ширина, "в": высота, "пиксели": {}}
def визуал_пиксель(x, y, цвет):
    if "холст" in _визуал:
        _визуал["холст"]["пиксели"][f"{x},{y}"] = цвет
def чат_запусти(порт, название="SONPSIR Чат", файл="чат.db"):
    from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
    from urllib.parse import urlparse, parse_qs

def случайное_целое(от, до):
    return random.randint(от, до)

def выбрать(список):
    if not список: return None
    return random.choice(список)

def диапазон(от, до):
    return list(range(от, до))

def соединить(список, разделитель=" "):
    return разделитель.join(str(x) for x in список)

def создать_объект(**kwargs):
    return kwargs


import math
import statistics

# --- МАТЕМАТИКА ---
def среднее(список):
    if not список: return 0
    return sum(список) / len(список)

def медиана(список):
    if not список: return 0
    sorted_list = sorted(список)
    n = len(sorted_list)
    mid = n // 2
    if n % 2 == 0:
        return (sorted_list[mid - 1] + sorted_list[mid]) / 2
    else:
        return sorted_list[mid]

def дисперсия(список):
    if len(список) < 2: return 0
    return statistics.variance(список)

def факториал(н):
    if н < 0: return 0
    res = 1
    for i in range(1, н + 1): res *= i
    return res

def степень(основание, показатель):
    return основание ** показатель

def корень(число):
    return math.sqrt(число)

def логарифм(число, основание=math.e):
    return math.log(число, основание)

# --- УНИВЕРСАЛЬНАЯ ГЕНЕРАЦИЯ ---
def сгенерировать_числа(количество, от, до):
    return [random.randint(от, до) for _ in range(количество)]

def сгенерировать_дроби(количество, от, до):
    return [round(random.uniform(от, до), 2) for _ in range(количество)]

def сгенерировать_строки(количество, длина=5):
    import string
    chars = string.ascii_letters + string.digits
    return [''.join(random.choice(chars) for _ in range(длина)) for _ in range(количество)]

def сгенерировать_координаты(количество, x_max=100, y_max=100):
    return [(random.randint(0, x_max), random.randint(0, y_max)) for _ in range(количество)]

def перемешать(список):
    random.shuffle(список)
    return список

def уникальный_выбор(список, количество):
    if количество > len(список): return список
    return random.sample(список, количество)

    import html as _html
    import sqlite3, datetime
    from html import escape as _html_escape
    бд = sqlite3.connect(файл, check_same_thread=False)
    бд.execute("CREATE TABLE IF NOT EXISTS msg (имя TEXT, текст TEXT, время TEXT)")
    бд.commit()
    def страница():
        строки = бд.execute("SELECT имя, текст, время FROM msg ORDER BY rowid DESC LIMIT 40").fetchall()[::-1]
        лента = "".join('<p class="t"><b>%s</b> <small>%s</small>: %s</p>' % (_html.escape(и), _html.escape(в), _html.escape(т)) for и, т, в in строки)
        return ('<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="refresh" content="3"><title>'+_html.escape(название)+'</title><style>'+_визуал_css()+'</style></head><body><div class="card"><h1>'+_html.escape(название)+'</h1>'+лента+'<form class="f" action="/отправить"><input name="имя" placeholder="Имя"><input name="сообщение" placeholder="Сообщение"><button class="btn btn-неон size-средняя shape-пилюля">➔</button></form></div></body></html>')
    class H(BaseHTTPRequestHandler):
        def do_GET(self):
            u = urlparse(self.path)
            if u.path == "/отправить":
                пар = parse_qs(u.query)
                имя = пар.get("имя", ["гость"])[0]; текст = пар.get("сообщение", [""])[0]
                if текст:
                    бд.execute("INSERT INTO msg VALUES (?,?,?)", (имя, текст, datetime.datetime.now().strftime("%H:%M")))
                    бд.commit()
            self.send_response(200); self.send_header("Content-Type", "text/html; charset=utf-8"); self.end_headers()
            self.wfile.write(страница().encode())
        def log_message(self, *a): pass
    print("МЕССЕНДЖЕР запущен (история в %s): http://localhost:%s" % (файл, порт))
    сервер = ThreadingHTTPServer(("0.0.0.0", порт), H)
    сервер.handle_error = lambda *a, **k: print("SONPSIR: запрос с ошибкой пропущен (проверь обработчик)")
    сервер.serve_forever()
def отобразить(список, ф): return [ф(x) for x in список]
def отфильтровать(список, ф): return [x for x in список if ф(x)]
def свернуть(список, ф, старт):
    acc = старт
    for x in список: acc = ф(acc, x)
    return acc
def сортировать_по(список, ф): return sorted(список, key=ф)
def шаблон(текст, *арг): return текст.format(*арг)
def соединить(список, разделитель=" "): return разделитель.join(str(x) for x in список)
def заменить(текст, а, б): return текст.replace(а, б)
def процесс(функция, *арг):
    import multiprocessing
    p = multiprocessing.Process(target=функция, args=арг); p.start(); return p
def мессенджер_сервер(порт, файл="мессенджер.db"):
    from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
    from urllib.parse import urlparse, parse_qs

def случайное_целое(от, до):
    return random.randint(от, до)

def выбрать(список):
    if not список: return None
    return random.choice(список)

def диапазон(от, до):
    return list(range(от, до))

def соединить(список, разделитель=" "):
    return разделитель.join(str(x) for x in список)

def создать_объект(**kwargs):
    return kwargs


import math
import statistics

# --- МАТЕМАТИКА ---
def среднее(список):
    if not список: return 0
    return sum(список) / len(список)

def медиана(список):
    if not список: return 0
    sorted_list = sorted(список)
    n = len(sorted_list)
    mid = n // 2
    if n % 2 == 0:
        return (sorted_list[mid - 1] + sorted_list[mid]) / 2
    else:
        return sorted_list[mid]

def дисперсия(список):
    if len(список) < 2: return 0
    return statistics.variance(список)

def факториал(н):
    if н < 0: return 0
    res = 1
    for i in range(1, н + 1): res *= i
    return res

def степень(основание, показатель):
    return основание ** показатель

def корень(число):
    return math.sqrt(число)

def логарифм(число, основание=math.e):
    return math.log(число, основание)

# --- УНИВЕРСАЛЬНАЯ ГЕНЕРАЦИЯ ---
def сгенерировать_числа(количество, от, до):
    return [random.randint(от, до) for _ in range(количество)]

def сгенерировать_дроби(количество, от, до):
    return [round(random.uniform(от, до), 2) for _ in range(количество)]

def сгенерировать_строки(количество, длина=5):
    import string
    chars = string.ascii_letters + string.digits
    return [''.join(random.choice(chars) for _ in range(длина)) for _ in range(количество)]

def сгенерировать_координаты(количество, x_max=100, y_max=100):
    return [(random.randint(0, x_max), random.randint(0, y_max)) for _ in range(количество)]

def перемешать(список):
    random.shuffle(список)
    return список

def уникальный_выбор(список, количество):
    if количество > len(список): return список
    return random.sample(список, количество)

    import sqlite3, json, datetime
    бд = sqlite3.connect(файл, check_same_thread=False)
    бд.execute("CREATE TABLE IF NOT EXISTS msg (комната TEXT, имя TEXT, текст TEXT, время TEXT)")
    бд.commit()
    СТРАНИЦА = """<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Мессенджер SONPSIR</title>
<style>*{box-sizing:border-box;margin:0}body{font-family:system-ui;background:linear-gradient(135deg,#0f0c29,#302b63);color:#eee;min-height:100vh;display:flex;justify-content:center;padding:16px}.w{width:100%;max-width:520px;background:rgba(255,255,255,.08);border-radius:20px;padding:20px;backdrop-filter:blur(10px)}h1{font-size:1.4rem;margin-bottom:12px;background:linear-gradient(90deg,#00dbde,#fc00ff);-webkit-background-clip:text;-webkit-text-fill-color:transparent}input{width:100%;margin:5px 0;padding:11px;border-radius:12px;border:1px solid rgba(255,255,255,.2);background:rgba(255,255,255,.08);color:#eee}#feed{height:50vh;overflow-y:auto;margin:10px 0;padding:10px;background:rgba(0,0,0,.25);border-radius:12px}#feed p{margin:6px 0}button{width:100%;padding:12px;border:none;border-radius:12px;background:linear-gradient(90deg,#00dbde,#fc00ff);color:#fff;font-size:1rem;font-weight:600}</style></head>
<body><div class="w"><h1>Мессенджер SONPSIR</h1>
<input id="room" value="общая" placeholder="комната"><input id="name" placeholder="твоё имя">
<div id="feed"></div><form id="f"><input id="msg" placeholder="сообщение"><button>Отправить</button></form></div>
<script>function esc(s){return s.replace(/[<>&]/g,c=>({'<':'&lt;','>':'&gt;','&':'&amp;'}[c]))}
async function tick(){const room=encodeURIComponent(document.getElementById('room').value||'общая');
try{const r=await fetch('/лента?комната='+room);const d=await r.json();
document.getElementById('feed').innerHTML=d.map(m=>'<p><b>'+esc(m.имя)+'</b> <small>'+m.время+'</small>: '+esc(m.текст)+'</p>').join('');}catch(e){}}
setInterval(tick,2000);tick();
document.getElementById('f').onsubmit=async e=>{e.preventDefault();
const room=encodeURIComponent(document.getElementById('room').value||'общая');
const name=encodeURIComponent(document.getElementById('name').value||'гость');
const msg=encodeURIComponent(document.getElementById('msg').value);
if(msg){await fetch('/отправить?комната='+room+'&имя='+name+'&текст='+msg);document.getElementById('msg').value='';tick();}};</script></body></html>"""
    class H(BaseHTTPRequestHandler):
        def do_GET(self):
            u = urlparse(self.path); пар = parse_qs(u.query)
            if u.path == "/лента":
                ком = пар.get("комната", ["общая"])[0]
                строки = бд.execute("SELECT имя,текст,время FROM msg WHERE комната=? ORDER BY rowid DESC LIMIT 50", (ком,)).fetchall()[::-1]
                тело = json.dumps([{"имя":и,"текст":т,"время":в} for и,т,в in строки], ensure_ascii=False).encode()
                self.send_response(200); self.send_header("Content-Type","application/json"); self.end_headers(); self.wfile.write(тело); return
            if u.path == "/отправить":
                ком=пар.get("комната",["общая"])[0]; имя=пар.get("имя",["гость"])[0]; текст=пар.get("текст",[""])[0]
                if текст:
                    бд.execute("INSERT INTO msg VALUES (?,?,?,?)",(ком,имя,текст,datetime.datetime.now().strftime("%d.%m %H:%M"))); бд.commit()
                self.send_response(200); self.send_header("Content-Type","text/plain"); self.end_headers(); self.wfile.write(b"ok"); return
            код = СТРАНИЦА.encode()
            self.send_response(200); self.send_header("Content-Type","text/html; charset=utf-8"); self.end_headers()
            self.wfile.write(код)
        def log_message(self,*a): pass
    сервер = ThreadingHTTPServer(("0.0.0.0", порт), H)
    сервер.handle_error = lambda *a,**k: None
    print("МЕССЕНДЖЕР-СЕРВЕР:", порт, "(веб: http://localhost:%s, клиенты — по сети)" % порт)
    сервер.serve_forever()
def мессенджер_клиент(хост, порт, имя, комната="общая"):
    import time, threading
    база = f"http://{хост}:{порт}"
    видно = set()
    def лента():
        while True:
            try:
                данные = забрать_json(f"{база}/лента?комната={комната}")
                for м in данные:
                    ключ = (м["время"], м["имя"], м["текст"])
                    if ключ not in видно:
                        видно.add(ключ); print(f'[{м["время"]}] {м["имя"]}: {м["текст"]}')
            except Exception: pass
            time.sleep(2)
    threading.Thread(target=лента, daemon=True).start()
    print(f"Ты в комнате '{комната}' как '{имя}'. Пиши, Ctrl+C — выход.")
    while True:
        try: текст = input("> ")
        except (EOFError, KeyboardInterrupt): break
        if текст:
            try: отправить_запрос(f"{база}/отправить?комната={комната}&имя={имя}&текст={текст}")
            except Exception: print("сервер недоступен")
def зашифровать(текст, ключ="сонпсир"):
    import base64, hashlib
    k = hashlib.sha256(ключ.encode()).digest()
    b = str(текст).encode()
    return base64.b64encode(bytes(c ^ k[i % len(k)] for i, c in enumerate(b))).decode()
def расшифровать(токен, ключ="сонпсир"):
    import base64, hashlib
    k = hashlib.sha256(ключ.encode()).digest()
    x = base64.b64decode(токен)
    return bytes(c ^ k[i % len(k)] for i, c in enumerate(x)).decode()
def визуал_кисть(цвет):
    _визуал["кисть"] = цвет


import base64 as _b64
import html as _html_mod
from http.server import HTTPServer as _HTTPServer, BaseHTTPRequestHandler as _BaseHandler

_виз = {"заголовок": "SONPSIR", "тема": "светлая", "шрифт": "sans-serif", "размер": 16, "форма": "8", "компоненты": [], "кисть": "чёрный"}

def _виз_мим(путь):
    типы = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".gif": "image/gif", ".mp4": "video/mp4", ".webm": "video/webm"}
    for кон, тип in типы.items():
        if путь.endswith(кон):
            return тип
    return "application/octet-stream"

def _виз_данные(путь):
    with open(путь, "rb") as ф:
        return "data:" + _виз_мим(путь) + ";base64," + _b64.b64encode(ф.read()).decode()

def визуал_заголовок(т): _виз["заголовок"] = str(т)
def визуал_текст(т): _виз["компоненты"].append(("текст", _html_mod.escape(str(т)), _виз.get("цвет"), _виз.get("размер_текста")))
def визуал_цвет(ц):
    _таб = {"красный":"red","зелёный":"green","синий":"blue","белый":"white","чёрный":"black","жёлтый":"yellow","оранжевый":"orange","фиолетовый":"purple","голубой":"skyblue","серый":"gray","розовый":"pink"}
    _виз["цвет"] = _таб.get(str(ц), str(ц))
def визуал_масштаб(н): _виз["размер_текста"] = int(н)
def визуал_кнопка(т, действие=""): _виз["компоненты"].append(("кнопка", _html_mod.escape(str(т)), str(действие)))
def визуал_тема(т): _виз["тема"] = str(т)
def визуал_шрифт(т): _виз["шрифт"] = str(т)
def визуал_размер(н): _виз["размер"] = int(н)
def визуал_форма(т): _виз["форма"] = str(т)
def визуал_фото(путь): _виз["компоненты"].append(("фото", _виз_данные(путь)))
def визуал_видео(путь): _виз["компоненты"].append(("видео", _виз_данные(путь)))
def визуал_html(код): _виз["компоненты"].append(("html", str(код)))
def визуал_скрипт(код): _виз["компоненты"].append(("скрипт", str(код)))
def визуал_холст(ш, в): _виз["компоненты"].append(("холст", int(ш), int(в), []))
def визуал_кисть(цвет): _виз["кисть"] = str(цвет)
def визуал_пиксель(х, у):
    for к in _виз["компоненты"]:
        if к[0] == "холст":
            к[3].append((х, у, _виз["кисть"]))
def визуал_страница():
    темы = {"тёмная": ("#121212", "#eeeeee"), "светлая": ("#fafafa", "#111111")}
    фон, текст = темы.get(_виз["тема"], ("#fafafa", "#111111"))
    части = ["<body style='background:%s;color:%s;font-family:%s;font-size:%spx'>" % (фон, текст, _виз["шрифт"], _виз["размер"])]
    части.append("<h1>%s</h1>" % _html_mod.escape(str(_виз["заголовок"])))
    for к in _виз["компоненты"]:
        if к[0] == "текст":
            стиль = ""
            if len(к) > 2 and к[2]: стиль += "color:%s;" % к[2]
            if len(к) > 3 and к[3]: стиль += "font-size:%spx;" % к[3]
            части.append("<p style='%s'>%s</p>" % (стиль, к[1]))
        elif к[0] == "кнопка":
            части.append("<button onclick='%s'>%s</button>" % (к[2], к[1]))
        elif к[0] == "фото":
            части.append("<img src='%s' style='max-width:100%%;border-radius:%spx'>" % (к[1], _виз["форма"]))
        elif к[0] == "видео":
            части.append("<video src='%s' controls style='max-width:100%%;border-radius:%spx'></video>" % (к[1], _виз["форма"]))
        elif к[0] == "html":
            части.append(к[1])
        elif к[0] == "скрипт":
            части.append("<script>%s</script>" % к[1])
        elif к[0] == "холст":
            svg = ["<svg width='%s' height='%s'>" % (к[1], к[2])]
            for (х, у, ц) in к[3]:
                svg.append("<rect x='%s' y='%s' width='2' height='2' fill='%s'/>" % (х, у, ц))
            svg.append("</svg>")
            части.append("".join(svg))
    части.append("</body>")
    return "".join(части)
def визуал_показать(порт=8080):
    страница = визуал_страница()
    class _H(_BaseHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(страница.encode())
        def log_message(self, *а):
            pass
    сервер = _HTTPServer(("0.0.0.0", порт), _H)
    print("Страница открыта: http://localhost:%d" % порт)
    сервер.serve_forever()

def визуал_html_рус(текст):
    import re as _re
    out = []
    for стр in текст.strip().split(chr(10)):
        стр = стр.strip()
        if not стр: continue
        for тег, рус in [("h1","заголовок1"),("h2","заголовок2"),("h3","заголовок3"),("h4","заголовок4")]:
            if стр.startswith(рус + " "):
                out.append("<%s>%s</%s>" % (тег, стр[len(рус)+1:], тег))
                break
        else:
            m = _re.match(r"абзац\s+(.+)", стр)
            if m: out.append("<p>%s</p>" % m.group(1)); continue
            m = _re.match(r"кнопка\s+id='([^']+)'\s+(.+)", стр)
            if m: out.append("<button id='%s' style='padding:12px;margin:4px'>%s</button>" % (m.group(1), m.group(2))); continue
            m = _re.match(r"ввод\s+id='([^']+)'\s*(.*)", стр)
            if m: out.append("<input id='%s' style='padding:8px;margin:4px'>" % m.group(1)); continue
            m = _re.match(r"холст\s+id='([^']+)'\s+ширина=(\d+)\s+высота=(\d+)", стр)
            if m: out.append("<canvas id='%s' width='%s' height='%s'></canvas>" % (m.group(1), m.group(2), m.group(3))); continue
            m = _re.match(r"картинка\s+src='([^']+)'\s*(.*)", стр)
            if m: out.append("<img src='%s' style='max-width:100%%'>"); continue
            m = _re.match(r"ссылка\s+url='([^']+)'\s+(.+)", стр)
            if m: out.append("<a href='%s'>%s</a>" % (m.group(1), m.group(2))); continue
            m = _re.match(r"блок\s+id='([^']+)'", стр)
            if m: out.append("<div id='%s'></div>" % m.group(1)); continue
            m = _re.match(r"разделитель", стр)
            if m: out.append("<hr>"); continue
            out.append(стр)
    _виз["компоненты"].append(("html", chr(10).join(out)))

def визуал_скрипт_рус(код):
    from core.lexer import Лексер, нормализовать
    from core.parser import Парсер
    from core.codegen import JSГенератор
    дерево = Парсер(Лексер(нормализовать(код)).разобрать()).разобрать()
    js = JSГенератор().сгенерировать(дерево)
    пом = chr(10).join([
        "function элемент(id){return document.getElementById(id);}",
        "function текст(id,t){document.getElementById(id).innerText=t;}",
        "function длина(x){return x.length;}",
        "function на_клик(id,f){document.getElementById(id).onclick=f;}",
        "function случайное_целое(a,b){return Math.floor(Math.random()*(b-a+1))+a;}",
        "function фигура(в,р){return {в:в,р:р};}",
        "function куб_вершины(){return [[-1,-1,-1],[1,-1,-1],[1,1,-1],[-1,1,-1],[-1,-1,1],[1,-1,1],[1,1,1],[-1,1,1]];}",
        "function куб_рёбра(){return [[0,1],[1,2],[2,3],[3,0],[4,5],[5,6],[6,7],[7,4],[0,4],[1,5],[2,6],[3,7]];}",
        "function пирамида_вершины(){return [[-1,-1,-1],[1,-1,-1],[1,-1,1],[-1,-1,1],[0,1,0]];}",
        "function пирамида_рёбра(){return [[0,1],[1,2],[2,3],[3,0],[0,4],[1,4],[2,4],[3,4]];}",
        "function сфера_вершины(ш,в){var V=[];for(var i=0;i<=ш;i++){var th=Math.PI*i/ш;for(var j=0;j<=в;j++){var ph=2*Math.PI*j/в;V.push([Math.sin(th)*Math.cos(ph),Math.cos(th),Math.sin(th)*Math.sin(ph)]);}}return V;}",
        "function сфера_рёбра(ш,в){var E=[];for(var i=0;i<=ш;i++){for(var j=0;j<в;j++){E.push([i*(в+1)+j,i*(в+1)+j+1]);if(i<ш)E.push([i*(в+1)+j,(i+1)*(в+1)+j]);}}return E;}",
        "function сдвинуть(в,x,y,z){var н=[];for(var i=0;i<в.length;i++)н.push([в[i][0]+x,в[i][1]+y,в[i][2]+z]);return н;}",
        "function масштабировать(в,к){var н=[];for(var i=0;i<в.length;i++)н.push([в[i][0]*к,в[i][1]*к,в[i][2]*к]);return н;}",
        "function нарисовать_фигуры(кт,фигуры,а,б,цвет){for(var f=0;f<фигуры.length;f++){var в=фигуры[f].в;var р=фигуры[f].р;var точки=[];for(var i=0;i<в.length;i++){var x=в[i][0],y=в[i][1],z=в[i][2];var x1=x*Math.cos(а)-z*Math.sin(а);var z1=x*Math.sin(а)+z*Math.cos(а);var y1=y*Math.cos(б)-z1*Math.sin(б);var z2=y*Math.sin(б)+z1*Math.cos(б);var s=3/(3+z2);точки.push([200+x1*s*90,200+y1*s*90]);}for(var e=0;e<р.length;e++){линия(кт,точки[р[e][0]][0],точки[р[e][0]][1],точки[р[e][1]][0],точки[р[e][1]][1],цвет,2);}}}",
        "function холст(id){return document.getElementById(id).getContext('2d');}",
        "function фон(кт,ц,ш,в){кт.fillStyle=ц;кт.fillRect(0,0,ш,в);}",
        "function линия(кт,x1,y1,x2,y2,ц,т){кт.strokeStyle=ц;кт.lineWidth=т;кт.beginPath();кт.moveTo(x1,y1);кт.lineTo(x2,y2);кт.stroke();}",
        "function синус(x){return Math.sin(x);}",
        "function косинус(x){return Math.cos(x);}",
        "function добавить(с,э){с.push(э);}",
        "function кадр(ф){requestAnimationFrame(ф);}",
    ]) + chr(10)
    _виз["компоненты"].append(("скрипт", пом + js))

def цвет(текст, ц="зелёный"):
    коды = {"красный":"31","зелёный":"32","жёлтый":"33","синий":"34","фиолетовый":"35","голубой":"36","белый":"37"}
    return f"\033[{коды.get(ц,'37')}m{текст}\033[0m"
'''


def раскрыть_подключения(дерево, папка, включено):
    новые = []
    базы = [папка, os.path.join(os.path.expanduser("~"), "SONPSIR", "libs"), os.path.join(os.path.expanduser("~"), "SONPSIR", "stdlib")]
    for з in дерево.заявления:
        if з.тип == "Подключить":
            путь = з.путь if з.путь.endswith(".sps") else з.путь + ".sps"
            полный = None
            for б in базы:
                cand = os.path.join(б, путь)
                if os.path.exists(cand): полный = cand; break
            if полный is None:
                raise ОшибкаСонпсир(f"подключаемый файл не найден: {з.путь}")
            if полный in включено: continue
            включено.add(полный)
            with open(полный, encoding="utf-8") as ф: под_код = ф.read()
            под_дерево = Парсер(Лексер(нормализовать(под_код)).разобрать()).разобрать()
            под_дерево = раскрыть_подключения(под_дерево, os.path.dirname(полный), включено)
            новые.extend(под_дерево.заявления)
        else:
            новые.append(з)
    дерево.заявления = новые
    return дерево


def поднять_функции(дерево):
    функции = [z for z in дерево.заявления if z.тип in ("Функция", "Класс")]
    остальные = [z for z in дерево.заявления if z.тип not in ("Функция", "Класс")]
    дерево.заявления = функции + остальные
    return дерево


def транслировать(код, папка):
    код = нормализовать(код)
    дерево = Парсер(Лексер(код).разобрать()).разобрать()
    дерево = раскрыть_подключения(дерево, папка, set())
    дерево = поднять_функции(дерево)
    return Генератор().сгенерировать(дерево)


def формат_текста(код):
    out = []; отступ = 0
    for сырая in код.split("\n"):
        с = сырая.strip()
        if not с: out.append(""); continue
        низ = с.lower()
        if низ.startswith("конец"):
            отступ = max(0, отступ - 1); out.append("    " * отступ + с); continue
        if низ.startswith("иначе") or низ.startswith("перехватить") or низ.startswith("случай"):
            out.append("    " * max(0, отступ - 1) + с); continue
        out.append("    " * отступ + с)
        if any(низ.startswith(k) for k in ("если", "пока", "повторять", "функция", "попробовать", "класс", "сопоставить", "для каждого")):
            отступ += 1
    return "\n".join(out)


def линтер(дерево):
    from core.nodes import Узел
    проблемы = []
    определ = {"само"}; константы = set(); функции = set(); типы = {}

    def сбор(у):
        if у is None: return
        if isinstance(у, (list, tuple)):
            for x in у: сбор(x)
            return
        if not isinstance(у, Узел): return
        if у.тип in ("Пусть", "Присвоить", "Константа"): определ.add(у.имя)
        if у.тип == "Константа": константы.add(у.имя)
        if у.тип == "ЦиклДиапазон": определ.add(у.счетчик)
        if у.тип == "ЦиклКаждый": определ.add(у.имя)
        if у.тип == "Функция":
            функции.add(у.имя); определ.add(у.имя)
            for p in у.параметры: определ.add(p)
        if у.тип == "Класс": функции.add(у.имя); определ.add(у.имя)
        for v in vars(у).values():
            if isinstance(v, (Узел, list, tuple)): сбор(v)
    сбор(дерево)

    def тип(у):
        if not isinstance(у, Узел): return None
        t = у.тип
        if t == "Число": return "число"
        if t == "Строка": return "текст"
        if t == "Булево": return "логика"
        if t == "Список": return "список"
        if t == "Словарь": return "словарь"
        if t == "Ничто": return "ничто"
        if t == "Имя": return типы.get(у.имя)
        if t == "Сравнение" or t == "Логика" or t == "Не": return "логика"
        if t == "Арифметика": return тип(у.левый) or тип(у.правый)
        if t == "Вызов":
            return {"len": "число", "int": "число", "str": "текст", "float": "число",
                    "спросить": "текст", "спросить_число": "число",
                    "random.randint": "число", "abs": "число", "round": "число"}.get(у.имя)
        return None

    КОНЕЦ_БЛОКА = ("Вернуть", "Выход", "Прервать", "Пропустить")
    def блоки(у):
        if у.тип == "Программа": yield у.заявления
        elif у.тип == "Если":
            for _, т in у.ветки: yield т
            if у.иначе: yield у.иначе
        elif у.тип in ("Пока", "ЦиклРаз", "ЦиклДиапазон", "ЦиклКаждый", "Функция", "Метод"):
            yield у.тело
        elif у.тип == "Попытка":
            yield у.тело; yield у.обработчик
        elif у.тип == "Класс":
            for м in у.методы: yield м.тело

    def проверка(у, в_печати=False):
        if у is None: return
        if isinstance(у, (list, tuple)):
            for x in у: проверка(x)
            return
        if not isinstance(у, Узел): return
        if у.тип == "Имя" and not в_печати:
            if у.имя not in определ and у.имя not in функции:
                import difflib
                близ = difflib.get_close_matches(у.имя, list(определ) + list(функции), n=1, cutoff=0.6)
                сов = f" Возможно, вы имели в виду '{близ[0]}'?" if близ else ""
                проблемы.append(f"строка {getattr(у, 'строка', '?')}: переменная '{у.имя}' не определена.{сов}")
        if у.тип == "Арифметика" and у.оп == "+":
            л, п = тип(у.левый), тип(у.правый)
            if л and п and {л, п} == {"текст", "число"}:
                проблемы.append("предупреждение: складываешь текст и число — приведи тип (в число / в строку)")
        if у.тип in ("Пусть", "Присвоить", "Константа"):
            типы[у.имя] = тип(у.значение)
        for блок in list(блоки(у)):
            недостижимо = False
            for з in блок:
                if недостижимо:
                    проблемы.append(f"строка {getattr(з, 'строка', '?')}: недостижимый код")
                if з.тип in КОНЕЦ_БЛОКА: недостижимо = True
        if у.тип == "Печать":
            for a in у.аргументы: проверка(a, True)
            return
        for v in vars(у).values():
            if isinstance(v, (Узел, list, tuple)): проверка(v)
    проверка(дерево)

    присвоения = set(); использ = set()
    def обход2(у):
        if у is None: return
        if isinstance(у, (list, tuple)):
            for x in у: обход2(x)
            return
        if not isinstance(у, Узел): return
        if у.тип == "Присвоить": присвоения.add(у.имя)
        if у.тип == "ПрисвоитьЦель" and у.цель.тип == "Имя": присвоения.add(у.цель.имя)
        if у.тип == "Имя": использ.add(у.имя)
        for v in vars(у).values():
            if isinstance(v, (Узел, list, tuple)): обход2(v)
    обход2(дерево)
    for имя in sorted(константы & присвоения):
        проблемы.append(f"ошибка: константа '{имя}' переприсваивается")
    for имя in sorted(определ - использ - функции - {"само"}):
        проблемы.append(f"предупреждение: '{имя}' не используется")
    return проблемы


def консоль():
    print("SONPSIR-консоль. Пиши выражения, 'выход' — выход.")
    среда = {}
    exec(ПРЕЛЮДИЯ, среда)
    буфер = ""
    while True:
        try:
            строка = input(">>> " if not буфер else "... ")
        except (EOFError, KeyboardInterrupt):
            break
        if строка.strip() in ("выход", "quit", "exit"): break
        буфер += строка + "\n"
        try:
            питон = транслировать(буфер, os.getcwd())
        except ОшибкаСонпсир as e:
            if "не закрыт" in str(e): continue
            print("Ошибка:", e); буфер = ""; continue
        буфер = ""
        try:
            exec(compile(питон, "<консоль>", "exec"), среда)
        except SystemExit: break
        except NameError as e: print("SONPSIR пока не знает слово:", e)
        except Exception as e: print("Ошибка:", e)


def тесты(папка):
    import glob
    прошло = упало = 0
    for ф in sorted(glob.glob(os.path.join(папка, "*.sps"))):
        if not os.path.basename(ф).startswith("тест"): continue
        код = open(ф, encoding="utf-8").read()
        try:
            exec(compile(ПРЕЛЮДИЯ + транслировать(код, папка), ф, "exec"), {})
            print(f"  ✔ {os.path.basename(ф)}"); прошло += 1
        except Exception as e:
            print(f"  ✘ {os.path.basename(ф)}: {e}"); упало += 1
    print(f"Итого: прошло {прошло}, упало {упало}")
    if упало: sys.exit(1)


def новый(имя):
    os.makedirs(os.path.join(имя, "examples"), exist_ok=True)
    with open(os.path.join(имя, "главная.sps"), "w", encoding="utf-8") as ф:
        ф.write(f"# Проект {имя} на SONPSIR\nчто печатать(привет)\n")
    with open(os.path.join(имя, "тест_основной.sps"), "w", encoding="utf-8") as ф:
        ф.write("проверить 1 + 1 == 2\n")
    print(f"Проект '{имя}' создан: главная.sps, тест_основной.sps")


def собрать(путь, формат=None):
    папка = os.path.dirname(os.path.abspath(путь))
    код = open(путь, encoding="utf-8").read()
    питон = транслировать(код, папка)
    полный = "#!/usr/bin/env python3\n# -*- coding: utf-8 -*-\n" + ПРЕЛЮДИЯ + "\n" + питон
    base = путь[:-4] if путь.endswith(".sps") else путь
    if формат in (None, "bin"):
        with open(base, "w", encoding="utf-8") as ф: ф.write(полный.replace("#!/usr/bin/env python3", "#!/data/data/com.termux/files/usr/bin/env python3", 1))
        os.chmod(base, 0o755); print(f"Собрано: {base} (запуск ./{os.path.basename(base)})")
    elif формат == "pyz":
        import zipfile
        out = base + ".pyz"
        with zipfile.ZipFile(out, "w") as z: z.writestr("__main__.py", полный)
        os.chmod(out, 0o755); print(f"Собрано: {out} — один файл, работает на любой ОС с Python")
    elif формат == "exe":
        out = base + ".py"
        with open(out, "w", encoding="utf-8") as ф: ф.write(полный)
        bat = base + "_build_exe.bat"
        with open(bat, "w") as ф: ф.write("pip install pyinstaller\npyinstaller --onefile " + os.path.basename(out) + "\necho Готово: dist\\")
        print(f"Создано: {out} + {bat} — запусти bat на Windows, получишь .exe")
    elif формат == "apk":
        имя = os.path.basename(base); d = имя + "_android"
        os.makedirs(os.path.join(d, "app/src/main/java/sonpsir/app"), exist_ok=True)
        with open(os.path.join(d, "settings.gradle"), "w") as ф: ф.write("include ':app'")
        with open(os.path.join(d, "app/build.gradle"), "w") as ф: ф.write("plugins{id 'com.android.application'}\nandroid{compileSdk 34;defaultConfig{applicationId 'sonpsir.app';minSdk 21;targetSdk 34}}\ndependencies{}")
        with open(os.path.join(d, "app/src/main/AndroidManifest.xml"), "w") as ф: ф.write('<manifest xmlns:android="http://schemas.android.com/apk/res/android"><uses-permission android:name="android.permission.INTERNET"/><application android:label="'+имя+'"><activity android:name=".Main" android:exported="true"><intent-filter><action android:name="android.intent.action.MAIN"/><category android:name="android.intent.category.LAUNCHER"/></intent-filter></activity></application></manifest>')
        with open(os.path.join(d, "app/src/main/java/sonpsir/app/Main.java"), "w") as ф: ф.write('package sonpsir.app;\nimport android.app.Activity;import android.os.Bundle;import android.webkit.WebView;\npublic class Main extends Activity{protected void onCreate(Bundle s){super.onCreate(s);WebView w=new WebView(this);w.getSettings().setJavaScriptEnabled(true);w.loadUrl("http://10.0.2.2:8080");setContentView(w);}}')
        print(f"Создан Android-проект {d}/ — открой в Android Studio → Build APK. (Сервер SONPSIR запускается отдельно.)")

def пакет(арг):
    libs = os.path.join(os.path.expanduser("~"), "SONPSIR", "libs")
    os.makedirs(libs, exist_ok=True)
    if арг == "список":
        for f in sorted(os.listdir(libs)): print(" ", f)
        return
    url = арг if арг.startswith("http") else "https://raw.githubusercontent.com/" + арг
    имя = url.rstrip("/").split("/")[-1]
    import urllib.request
    urllib.request.urlretrieve(url, os.path.join(libs, имя))
    print(f"Пакет установлен: libs/{имя}")
def учебник():
    уроки = [
     ("1 Переменные", "пусть имя = \"мир\"\nчто печатать(имя)"),
     ("2 Условия", "если х > 5 то\n    что печатать(\"много\")\nиначе\n    что печатать(\"мало\")\nконец если"),
     ("3 Циклы", "повторять 3 раза\n    что печатать(\"ура\")\nконец цикла\nдля каждого х из [1,2,3]\n    что печатать(х)\nконец цикла"),
     ("4 Функции", "функция квадрат(н)\n    вернуть н * н\nконец функции"),
     ("5 Списки и словари", "пусть с = [1,2,3]\nдобавить в с(4)\nпусть д = {\"имя\": \"Артур\"}"),
     ("6 Ошибки", "попробовать\n    что печатать(10 / 0)\nперехватить ошибку\n    что печатать(\"упало\")\nконец попытки"),
     ("7 Веб и визуал", "визуал заголовок(\"Привет\")\nвизуал кнопка(\"Жми\", \"к\")\nвизуал показать(8080)"),
     ("8 Файлы и сеть", "записать в файл(\"а.txt\", \"текст\")\nпусть с = забрать страницу(\"http://example.com\")"),
    ]
    for наз, код in уроки:
        print("\n=== " + наз + " ==="); print(код)
    print("\nСкопируй урок в файл и запусти: sonpsir файл.sps")
def бенч(запросов=200, потоков=20):
    import time, threading, urllib.request
    from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
    class H(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200); self.send_header("Content-Type", "text/plain"); self.end_headers(); self.wfile.write(b"ok")
        def log_message(self, *a): pass
    сервер = ThreadingHTTPServer(("127.0.0.1", 9999), H); сервер.daemon_threads = True
    threading.Thread(target=сервер.serve_forever, daemon=True).start()
    сделано = 0; лок = threading.Lock()
    def работник(н):
        nonlocal сделано
        for _ in range(н):
            try:
                urllib.request.urlopen("http://127.0.0.1:9999/").read()
                with лок: сделано += 1
            except: pass
    t0 = time.time()
    ths = [threading.Thread(target=работник, args=(запросов // потоков,)) for _ in range(потоков)]
    for t in ths: t.start()
    for t in ths: t.join()
    dt = time.time() - t0
    сервер.shutdown()
    print(f"Запросов: {сделано} | потоков: {потоков} | время: {dt:.2f} c | скорость: {сделано/dt:.0f} запросов/сек")
def иде(порт=8090):
    from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
    import io, contextlib
    СТРАНИЦА = """<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>SONPSIR IDE</title>
<style>*{box-sizing:border-box}body{font-family:monospace;background:#111;color:#eee;margin:0;padding:10px}h1{font-size:1.1rem;color:#00dbde}textarea{width:100%;height:45vh;background:#1b1b25;color:#eee;border:1px solid #333;border-radius:8px;padding:10px;font-size:14px}button{margin:3px;padding:10px 14px;border:none;border-radius:8px;background:#302b63;color:#eee}#run{background:linear-gradient(90deg,#00dbde,#fc00ff);font-weight:700}pre{background:#000;border:1px solid #333;border-radius:8px;padding:10px;min-height:20vh;white-space:pre-wrap}</style></head>
<body><h1>SONPSIR IDE</h1>
<div id="bar"></div>
<textarea id="code" spellcheck="false">пусть х = 5
что печатать("х =", х)</textarea>
<br><button id="run" onclick="run()">ЗАПУСТИТЬ</button>
<pre id="out"></pre>
<script>
const sym=["(",")","[","]","{","}",'"',":","=","+","-","*","/",",","_"];
const bar=document.getElementById("bar");
sym.forEach(s=>{const b=document.createElement("button");b.textContent=s;b.onclick=()=>ins(s);bar.appendChild(b);});
function ins(s){const c=document.getElementById("code");c.value+=s;c.focus();}
async function run(){const code=document.getElementById("code").value;
const r=await fetch("/запустить",{method:"POST",body:code});
document.getElementById("out").textContent=await r.text();}
</script></body></html>"""
    class H(BaseHTTPRequestHandler):
        def do_GET(self):
            код = СТРАНИЦА.encode(); self.send_response(200); self.send_header("Content-Type", "text/html; charset=utf-8"); self.end_headers(); self.wfile.write(код)
        def do_POST(self):
            длина = int(self.headers.get("Content-Length", 0))
            код = self.rfile.read(длина).decode("utf-8")
            буфер = io.StringIO(); вывод = ""
            try:
                питон, карта = транслировать_с_картой(код, os.getcwd())
                with contextlib.redirect_stdout(буфер):
                    exec(compile(ПРЕЛЮДИЯ + "\n" + питон, "<иде>", "exec"), {})
                вывод = буфер.getvalue()
            except Exception as e:
                вывод = буфер.getvalue() + "ОШИБКА: " + str(e)
            тело = вывод.encode(); self.send_response(200); self.send_header("Content-Type", "text/plain; charset=utf-8"); self.end_headers(); self.wfile.write(тело)
        def log_message(self, *a): pass
    сервер = ThreadingHTTPServer(("0.0.0.0", порт), H); сервер.handle_error = lambda *a, **k: None
    print("IDE запущена: http://localhost:%s" % порт)
    сервер.serve_forever()
def справка():
    print("SONPSIR — русский язык программирования")
    print("  python sonpsir.py файл.sps            запустить")
    print("  python sonpsir.py файл.sps --отладка  показать Python")
    print("  python sonpsir.py консоль             интерактивная консоль")
    print("  python sonpsir.py формат файл.sps     причесать отступы")
    print("  python sonpsir.py проверь файл.sps    линтер")
    print("  python sonpsir.py тесты папка         прогнать тест_*.sps")
    print("  python sonpsir.py новый имя           создать проект")
    print("  python sonpsir.py собери файл.sps     собрать в исполняемый файл")
    print("  python sonpsir.py следи файл.sps        горячая перезагрузка")
    print("  python sonpsir.py пакет <url|user/repo/файл>  установить пакет")


def транслировать_с_картой(код, папка):
    код = нормализовать(код)
    дерево = Парсер(Лексер(код).разобрать()).разобрать()
    дерево = раскрыть_подключения(дерево, папка, set())
    дерево = поднять_функции(дерево)
    г = Генератор(); питон = г.сгенерировать(дерево)
    return питон, г.source_map
def следи(файл):
    print("команда следи отключена в этой версии")

def переведи(сообщение):
    таб = {
        "unterminated string": "незакрытая строка — проверь кавычки",
        "invalid syntax": "ошибка в построении команды — проверь синтаксис",
        "expected an indented block": "после этой строки нужен блок с отступом",
        "unexpected indent": "лишний отступ в начале строки",
        "division by zero": "деление на ноль",
        "is not defined": "не найдено — создай через пусть или проверь опечатку",
        "not callable": "это не команда — проверь имя",
        "No module named": "библиотека не установлена — поставь через pip",
    }
    for англ, рус in таб.items():
        if англ in сообщение:
            return рус
    return сообщение

def main():
    if len(sys.argv) > 1 and sys.argv[1].endswith('.cpp'):
        from cpp_mode import перевести_cpp
        exec(перевести_cpp(open(sys.argv[1], encoding='utf-8').read()))
        return

    if len(sys.argv) < 2:
        справка(); return
    команда = sys.argv[1]
    if команда == "консоль": консоль(); return
    if команда == "учебник": учебник(); return
    if команда == "бенч": бенч(); return
    if команда == "иде": иде(); return
    if команда == "новый" and len(sys.argv) > 2: новый(sys.argv[2]); return
    if команда == "собери" and len(sys.argv) > 2: собрать(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None); return
    if команда == "следи" and len(sys.argv) > 2: следи(sys.argv[2]); return
    if команда == "пакет": пакет(sys.argv[2] if len(sys.argv) > 2 else "список"); return
    if команда == "тесты": тесты(sys.argv[2] if len(sys.argv) > 2 else "."); return
    if команда == "формат" and len(sys.argv) > 2:
        print(формат_текста(open(sys.argv[2], encoding="utf-8").read())); return
    if команда == "проверь" and len(sys.argv) > 2:
        код = open(sys.argv[2], encoding="utf-8").read()
        дерево = Парсер(Лексер(нормализовать(код)).разобрать()).разобрать()
        проблемы = линтер(дерево)
        print("\n".join(проблемы) if проблемы else "Проблем не найдено"); return
    путь = команда
    папка = os.path.dirname(os.path.abspath(путь))
    with open(путь, encoding="utf-8") as ф:
        код = ф.read()
    try:
        try:
            питон, карта = транслировать_с_картой(код, папка)
        except SyntaxError as e:
            print("ОШИБКА в '%s': %s" % (os.path.basename(путь), переведи(str(e))))
            sys.exit(1)
    except ОшибкаСонпсир as e:
        print("ОШИБКА SONPSIR:", e); sys.exit(1)
    полный = ПРЕЛЮДИЯ + "\n" + питон
    if "--отладка" in sys.argv:
        print("=== так видит Python ==="); print(полный); print("========================")
    import hashlib, tempfile
    ключ = hashlib.md5(полный.encode()).hexdigest()
    кэш = os.path.join(tempfile.gettempdir(), "sonpsir_" + ключ + ".py")
    if not os.path.exists(кэш):
        with open(кэш, "w", encoding="utf-8") as ф: ф.write(полный)
    сдвиг = (ПРЕЛЮДИЯ + "\n").count("\n")
    карта_полная = {k + сдвиг: v for k, v in карта.items()}
    сдвиг = (ПРЕЛЮДИЯ + "\n").count("\n")
    карта_полная = {k + сдвиг: v for k, v in карта.items()}
    try:
        exec(compile(полный, путь, "exec"), {})
    except SystemExit:
        pass
    except Exception as e:
        import traceback
        tb = traceback.extract_tb(e.__traceback__)
        стр = карта_полная.get(tb[-1].lineno) if tb else None
        рус = {"ZeroDivisionError":"деление на ноль","TypeError":"несовместимые типы",
               "IndexError":"нет такого элемента","KeyError":"нет такого ключа",
               "NameError":"имя не найдено","ValueError":"плохое значение",
               "FileNotFoundError":"файл не найден"}.get(type(e).__name__, str(e))
        print(f"❌ОШИБКА в '{os.path.basename(путь)}'" + (f", строка {стр}" if стр else "") + f": {переведи(рус)}")
        подсказка = {
            "NameError": "ты взял имя, которого нет. Создай его через 'пусть' или проверь опечатку.",
            "ZeroDivisionError": "нельзя делить на ноль.",
            "TypeError": "смешаны разные типы (текст и число). Приведи: в число(...) или в строку(...).",
            "IndexError": "в списке нет такого номера элемента.",
            "KeyError": "в словаре нет такого ключа.",
            "FileNotFoundError": "файл не найден — проверь имя и путь.",
            "ValueError": "не получилось превратить текст в число.",
        }.get(type(e).__name__)
        if подсказка: print("SONPSIR подсказывает:", подсказка)
        sys.exit(1)


if __name__ == "__main__":
    main()
