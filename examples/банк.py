#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import random, sys, math, time
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
    from http.server import HTTPServer, BaseHTTPRequestHandler
    class H(BaseHTTPRequestHandler):
        def do_GET(self):
            ответ = str(обработчик(self.path))
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(ответ.encode("utf-8"))
        def log_message(self, *a): pass
    HTTPServer(("0.0.0.0", порт), H).serve_forever()
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
        js = "const px=" + данные + ';const c=document.getElementById("c");const g=c.getContext("2d");g.fillStyle="#111";g.fillRect(0,0,c.width,c.height);for(const k in px){const p=k.split(",");g.fillStyle=px[k];g.fillRect(p[0]*4,p[1]*4,4,4);}'
        холст_html = '<canvas id="c" width="' + str(х["ш"]*4) + '" height="' + str(х["в"]*4) + '" style="image-rendering:pixelated;max-width:100%"></canvas><script>' + js + '</script>'
    return f'<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><link rel="manifest" href="/manifest.webmanifest"><meta name="theme-color" content="#302b63">{_визуал_font_link()}<title>{_визуал["заголовок"]}</title><style>{_визуал_css()}</style></head><body><div class="card"><h1>{_визуал["заголовок"]}</h1>{тело}{холст_html}</div></body></html>'
def визуал_css(css): _визуал.setdefault("свой_css", []).append(css)
def визуал_блок(html): _визуал["компоненты"].append(("блок", html))
def визуал_показать(порт, на_событие=None):
    from http.server import HTTPServer, BaseHTTPRequestHandler
    from urllib.parse import urlparse, parse_qs
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
    HTTPServer(("0.0.0.0", порт), H).serve_forever()

def система(команда):
    import subprocess
    r = subprocess.run(команда, shell=True, capture_output=True, text=True)
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
    return re.findall(r"https?://[^\s<>]+", текст)
def извлечь_emails(текст):
    import re
    return re.findall(r"[\w.+-]+@[\w-]+\.[\w.]+", текст)
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
def чат_запусти(порт, название="SONPSIR Чат"):
    from http.server import HTTPServer, BaseHTTPRequestHandler
    from urllib.parse import urlparse, parse_qs
    import html as _html
    чат = {"сообщения": []}
    def страница():
        лента = "".join('<p class="t"><b>%s</b>: %s</p>' % (_html.escape(и), _html.escape(т)) for и, т in чат["сообщения"][-40:])
        return ('<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="refresh" content="3"><title>'+_html.escape(название)+'</title><style>'+_ВИЗУАЛ_CSS+'</style></head><body><div class="card"><h1>'+_html.escape(название)+'</h1>'+лента+'<form class="f" action="/отправить"><input name="имя" placeholder="Имя"><input name="сообщение" placeholder="Сообщение"><button class="btn">➔</button></form></div></body></html>')
    class H(BaseHTTPRequestHandler):
        def do_GET(self):
            u = urlparse(self.path)
            if u.path == "/отправить":
                пар = parse_qs(u.query)
                имя = пар.get("имя", ["гость"])[0]; текст = пар.get("сообщение", [""])[0]
                if текст: чат["сообщения"].append((имя, текст))
            self.send_response(200); self.send_header("Content-Type", "text/html; charset=utf-8"); self.end_headers()
            self.wfile.write(страница().encode())
        def log_message(self, *a): pass
    print("ЧАТ запущен: http://localhost:%s" % порт)
    HTTPServer(("0.0.0.0", порт), H).serve_forever()
def заархивировать(путь, архив="out.zip"):
    import zipfile, os
    with zipfile.ZipFile(архив, "w", zipfile.ZIP_DEFLATED) as z:
        if os.path.isdir(путь):
            for r,_,fs in os.walk(путь):
                for f in fs: z.write(os.path.join(r,f), os.path.relpath(os.path.join(r,f), путь))
        else: z.write(путь, os.path.basename(путь))
    return архив
def разархивировать(архив, куда="."):
    import zipfile
    with zipfile.ZipFile(архив) as z: z.extractall(куда)
    return куда
def закодировать(текст):
    import base64
    return base64.b64encode(str(текст).encode()).decode()
def раскодировать(текст):
    import base64
    return base64.b64decode(текст).decode()
def хеш(текст, алгоритм="sha256"):
    import hashlib
    return hashlib.new(алгоритм, str(текст).encode()).hexdigest()
def копировать_файл(от, куда):
    import shutil; shutil.copy(от, куда); return куда
def удалить_файл(путь):
    import os; os.remove(путь)
def переименовать(от, куда):
    import os; os.rename(от, куда)
def создать_папку(имя):
    import os; os.makedirs(имя, exist_ok=True); return имя
def цвет(текст, ц="зелёный"):
    коды = {"красный":"31","зелёный":"32","жёлтый":"33","синий":"34","фиолетовый":"35","голубой":"36","белый":"37"}
    return f"[{коды.get(ц,'37')}m{текст}[0m"

class Счёт:
    def __init__(self, владелец, баланс):
        self.владелец = владелец
        self.баланс = баланс
    def пополнить(self, сумма):
        self.баланс = (self.баланс + сумма)
        print('Пополнено на', сумма)
    def снять(self, сумма):
        if (сумма > self.баланс):
            print('Не хватает денег!')
        else:
            self.баланс = (self.баланс - сумма)
            print('Снято', сумма)
    def отчёт(self):
        print('владелец:', self.владелец, 'баланс:', self.баланс)
мой = Счёт('Артур', 100)
мой.пополнить(50)
мой.снять(200)
мой.снять(30)
мой.отчёт()
текст = 'Привет, Мир'
print(текст.upper())
print(текст.lower())
список = [1, 2, 3]
if (2 in список):
    print('двойка есть')
число = int('42')
print((число + 1))