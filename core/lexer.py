import re
from .registry import КЛЮЧЕВЫЕ_СЛОВА, НОРМАЛИЗАЦИЯ_ДОП, ПИТОН_ИМЕНА_ДОП

class Токен:
    def __init__(self, тип, значение, строка=0, позиция=0):
        self.тип = тип
        self.значение = значение
        self.строка = строка
        self.позиция = позиция
    def __repr__(self):
        return "Токен(%s, %r)" % (self.тип, self.значение)

КЛЮЧ = "КЛЮЧ"
ИМЯ = "ИМЯ"
ЧИСЛО = "ЧИСЛО"
СТРОКА = "СТРОКА"
ОПЕРАТОР = "ОПЕРАТОР"
ЗНАК = "ЗНАК"
КОНЕЦ_ФАЙЛА = "КОНЕЦ_ФАЙЛА"

def нормализовать(код):
    сохранённые = []
    def сохранить(m):
        сохранённые.append(m.group(0))
        return "\x00%d\x00" % (len(сохранённые) - 1)
    код = re.sub(r'"(?:[^"\\]|\\.)*"', сохранить, код)
    for фраза, замена in sorted(НОРМАЛИЗАЦИЯ_ДОП.items(), key=lambda x: len(x[0]), reverse=True):
        шаблон = r'(?<![а-яёА-ЯЁa-zA-Z0-9_])' + re.escape(фраза) + r'(?![а-яёА-ЯЁa-zA-Z0-9_])'
        код = re.sub(шаблон, замена, код)
    код = re.sub(r'\x00(\d+)\x00', lambda m: сохранённые[int(m.group(1))], код)
    return код

class Лексер:
    def __init__(self, код):
        self.код = код
        self.поз = 0
        self.строка = 1
        self.начало_строки = 0
    def разобрать(self):
        токены = []
        while self.поз < len(self.код):
            c = self.код[self.поз]
            if c in ' \t\r':
                self.поз += 1
                continue
            if c == '\n':
                self.строка += 1
                self.поз += 1
                self.начало_строки = self.поз
                continue
            if c == '#':
                while self.поз < len(self.код) and self.код[self.поз] != '\n':
                    self.поз += 1
                continue
            старт = self.поз
            if c in ('"', "'"):
                кав = c
                self.поз += 1
                while self.поз < len(self.код) and self.код[self.поз] != кав:
                    if self.код[self.поз] == '\\':
                        self.поз += 1
                    if self.поз < len(self.код):
                        if self.код[self.поз] == '\n':
                            self.строка += 1
                        self.поз += 1
                if self.поз >= len(self.код):
                    raise SyntaxError("незакрытая строка (строка %d)" % self.строка)
                self.поз += 1
                токены.append(Токен(СТРОКА, self.код[старт:self.поз], self.строка, старт - self.начало_строки))
            elif c.isdigit():
                while self.поз < len(self.код) and (self.код[self.поз].isdigit() or self.код[self.поз] == '.'):
                    self.поз += 1
                токены.append(Токен(ЧИСЛО, self.код[старт:self.поз], self.строка, старт - self.начало_строки))
            elif c.isalpha() or c == '_':
                while self.поз < len(self.код) and (self.код[self.поз].isalnum() or self.код[self.поз] == '_'):
                    self.поз += 1
                текст = self.код[старт:self.поз]
                if текст in КЛЮЧЕВЫЕ_СЛОВА or текст in ПИТОН_ИМЕНА_ДОП:
                    токены.append(Токен(КЛЮЧ, текст, self.строка, старт - self.начало_строки))
                else:
                    токены.append(Токен(ИМЯ, текст, self.строка, старт - self.начало_строки))
            else:
                оп = c
                if self.поз + 1 < len(self.код) and self.код[self.поз:self.поз+2] in ('==','!=','<=','>=','**','//'):
                    оп = self.код[self.поз:self.поз+2]
                    self.поз += 1
                self.поз += 1
                if оп in '(),[]{}:':
                    токены.append(Токен(ЗНАК, оп, self.строка, старт - self.начало_строки))
                else:
                    токены.append(Токен(ОПЕРАТОР, оп, self.строка, старт - self.начало_строки))
        токены.append(Токен(КОНЕЦ_ФАЙЛА, "", self.строка, 0))
        return токены
