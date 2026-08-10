#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SONPSIR v0.4 — русский язык программирования
import sys, re, os

ЗАМЕНЫ = [
    ("что печатать", "print"),
    ("спросить число", "спросить_число"),
    ("остаток от деления", "остаток_от_деления"),
    ("разделить текст", "разделить_текст"),
    ("перехватить ошибку", "except Exception"),
    ("дописать в файл", "дописать_в_файл"),
    ("записать в файл", "записать_в_файл"),
    ("прочитать файл", "прочитать_файл"),
    ("прервать цикл", "break"),
    ("пропустить круг", "continue"),
    ("попробовать", "try"),
    ("длина списка", "len"),
    ("длина текста", "len"),
    ("длина(", "len("),
    ("иначе если", "elif"),
    ("округлить", "round"),
    ("истина", "True"),
    ("ложь", "False"),
    ("функция", "def"),
    ("вернуть", "return"),
    ("пусть ", ""),
    ("если", "if"),
    ("иначе", "else"),
    ("пока", "while"),
    (" то", ":"),
]

ПРЕЛЮДИЯ = '''import random
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
def _выход():
    raise SystemExit
'''

def особые_выражения(с):
    return re.sub(r'случайное число от\s+(\w+)\s+до\s+(\w+)',
                  lambda m: f'random.randint({m.group(1)}, {m.group(2)})', с)

def логика(с):
    с = re.sub(r'\bне\s+равно\b', ' != ', с)
    с = re.sub(r'\bили\b', ' or ', с)
    с = re.sub(r'\bи\b', ' and ', с)
    с = re.sub(r'\bне\b', ' not ', с)
    return с

def обработать_текст(с, правила):
    части = re.split(r'("[^"]*"|\'[^\']*\')', с)
    for i in range(len(части)):
        if части[i][:1] in ('"', "'"):
            continue
        for рус, пит in правила:
            части[i] = части[i].replace(рус, пит)
        части[i] = логика(части[i])
        части[i] = особые_выражения(части[i])
    return "".join(части)

def точка(с):
    с = с.rstrip()
    return с if с.endswith(":") else с + ":"

def умная_печать(с, пер):
    m = re.match(r'^print\((.*)\)$', с)
    if not m:
        return с
    арг = m.group(1).strip()
    if not арг or арг[0] in "\"'":
        return с
    try:
        float(арг); return с
    except ValueError:
        pass
    if арг in пер:
        return с
    if any(c in арг for c in "+-*/()[]"):
        return с
    return f'print("{арг}")'

def это_конец(с): return с.startswith("конец")
def это_иначе(с):
    return (с == "иначе" or с.startswith("иначе если")
            or с.startswith("перехватить ошибку"))
def это_заголовок(с):
    return (с.startswith("если ") or с.startswith("пока ")
            or с.startswith("повторять ") or с.startswith("функция ")
            or с == "попробовать")

def повторять_в_for(с):
    m = re.match(r'повторять\s+(.+?)\s+раза?\s*$', с)
    if m: return f"for _ in range({m.group(1)}):"
    m = re.match(r'повторять\s+(\w+)\s+от\s+(.+?)\s+до\s+(.+?)\s*$', с)
    if m: return f"for {m.group(1)} in range({m.group(2)}, {m.group(3)} + 1):"
    return None

def добавить_в_список(с):
    m = re.match(r'добавить в\s+(\w+)\s*\((.*)\)\s*$', с)
    if m:
        return f"{m.group(1)}.append({m.group(2).strip()})"
    return None

def распознать_подключить(с):
    m = re.match(r'подключить\s+(\S+)\s*$', с)
    if m: return m.group(1)
    m = re.match(r'использовать\s+(\S+)\s*$', с)
    if m: return m.group(1)
    return None

def собрать_переменные(строки):
    пер = set()
    for с in строки:
        с = с.strip()
        if с.startswith("пусть "):
            имя = с[6:].split("=")[0].strip()
            if имя: пер.add(имя)
        m = re.match(r'повторять\s+(\w+)\s+от', с)
        if m: пер.add(m.group(1))
        if с.startswith("функция "):
            m = re.match(r'функция\s+\w+\s*\(([^)]*)\)', с)
            if m:
                for p in m.group(1).split(','):
                    p = p.strip()
                    if p: пер.add(p)
    return пер

def вставить_pass(строки):
    рез, n = [], len(строки)
    for i, с in enumerate(строки):
        рез.append(с)
        if с.rstrip().endswith(":"):
            мой = len(с) - len(с.lstrip())
            j = i + 1
            while j < n and (not строки[j].strip() or строки[j].strip().startswith("#")):
                j += 1
            if j >= n or (len(строки[j]) - len(строки[j].lstrip())) <= мой:
                рез.append(" " * (мой + 4) + "pass")
    return рез

def перевести_тело(код, включено, папка):
    правила = sorted(ЗАМЕНЫ, key=lambda x: -len(x[0]))
    строки = код.split("\n")
    пер = собрать_переменные(строки)
    out, отступ = [], 0
    for сырая in строки:
        с = сырая.strip()
        if not с:
            continue
        if с.startswith("#"):
            out.append("    " * отступ + с)
            continue
        под = распознать_подключить(с)
        if под:
            имя = под if под.endswith(".sps") else под + ".sps"
            полный = os.path.join(папка, имя)
            if полный not in включено:
                включено.add(полный)
                if os.path.exists(полный):
                    with open(полный, encoding="utf-8") as ф:
                        под_код = ф.read()
                    под_папка = os.path.dirname(полный)
                    под_строки = перевести_тело(под_код, включено, под_папка)
                    сдвиг = "    " * отступ
                    out.extend(сдвиг + x for x in под_строки)
                else:
                    out.append("    " * отступ + f"# ОШИБКА: не найден файл {имя}")
            continue
        if это_конец(с):
            отступ = max(0, отступ - 1)
            continue
        if это_иначе(с):
            з = точка(обработать_текст(с, правила))
            out.append("    " * max(0, отступ - 1) + з)
            continue
        if с in ("выход", "выход()", "завершить программу"):
            out.append("    " * отступ + "_выход()")
            continue
        пов = повторять_в_for(с)
        доб = добавить_в_список(с)
        if доб:
            out.append("    " * отступ + доб)
            continue
        з = обработать_текст(с, правила)
        if пов:
            з = пов
        if с.startswith("пока "):
            з = re.sub(r'\s+делать\s*$', '', з)
        if это_заголовок(с) or пов:
            out.append("    " * отступ + точка(з))
            отступ += 1
        else:
            out.append("    " * отступ + умная_печать(з, пер))
    return out

def перевести(код, папка):
    тело = перевести_тело(код, set(), папка)
    return ПРЕЛЮДИЯ + "\n".join(вставить_pass(тело))

def отформатировать(код):
    строки = код.split("\n")
    out, отступ = [], 0
    for сырая in строки:
        с = сырая.strip()
        if not с:
            out.append("")
            continue
        под = распознать_подключить(с)
        if это_конец(с):
            отступ = max(0, отступ - 1)
            out.append("    " * отступ + с)
        elif это_иначе(с):
            out.append("    " * max(0, отступ - 1) + с)
        elif под:
            out.append("    " * отступ + с)
        elif это_заголовок(с) or повторять_в_for(с):
            out.append("    " * отступ + с)
            отступ += 1
        else:
            out.append("    " * отступ + с)
    return "\n".join(out)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Запуск: python sonpsir.py файл.sps [--отладка|--формат]"); sys.exit()
    путь = sys.argv[1]
    папка = os.path.dirname(os.path.abspath(путь))
    with open(путь, encoding="utf-8") as ф:
        код = ф.read()
    if "--формат" in sys.argv:
        print(отформатировать(код))
        sys.exit()
    питон = перевести(код, папка)
    if "--отладка" in sys.argv:
        print("=== так видит Python ===\n" + питон + "\n========================")
    exec(compile(питон, "<SONPSIR>", "exec"), {})

