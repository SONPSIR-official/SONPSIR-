class Генератор:
    def __init__(self):
        self.отступ = 0
        self.строки = []
        self.source_map = {}
    def _добавить(self, текст):
        self.строки.append("    " * self.отступ + текст)
    def сгенерировать(self, узел):
        if узел.тип == "Программа":
            for з in узел.заявления:
                self.заявление(з)
        else:
            self.заявление(узел)
        return "\n".join(self.строки)
    def заявление(self, з):
        метод = getattr(self, "з_" + з.тип, None)
        if метод is None:
            raise Exception("нет генератора для заявления %s" % з.тип)
        метод(з)
    def з_Пусть(self, у):
        self._добавить("%s = %s" % (у.имя, self.выражение(у.значение)))
    def з_Присваивание(self, у):
        self._добавить("%s = %s" % (self.выражение(у.цель), self.выражение(у.значение)))
    def з_Если(self, у):
        первый = True
        for усл, тело in у.ветви:
            ключ = "if" if первый else "elif"
            self._добавить("%s %s:" % (ключ, self.выражение(усл)))
            self.отступ += 1
            if тело:
                for з in тело:
                    self.заявление(з)
            else:
                self._добавить("pass")
            self.отступ -= 1
            первый = False
        if у.иначе_тело:
            self._добавить("else:")
            self.отступ += 1
            for з in у.иначе_тело:
                self.заявление(з)
            self.отступ -= 1
    def з_Пока(self, у):
        self._добавить("while %s:" % self.выражение(у.условие))
        self.отступ += 1
        if у.тело:
            for з in у.тело:
                self.заявление(з)
        else:
            self._добавить("pass")
        self.отступ -= 1
    def з_Повторять(self, у):
        self._добавить("for _ in range(%s):" % self.выражение(у.раз))
        self.отступ += 1
        if у.тело:
            for з in у.тело:
                self.заявление(з)
        else:
            self._добавить("pass")
        self.отступ -= 1
    def з_Для(self, у):
        self._добавить("for %s in %s:" % (у.имя, self.выражение(у.список)))
        self.отступ += 1
        if у.тело:
            for з in у.тело:
                self.заявление(з)
        else:
            self._добавить("pass")
        self.отступ -= 1
    def з_Функция(self, у):
        self._добавить("def %s(%s):" % (у.имя, ", ".join(у.аргументы)))
        self.отступ += 1
        if у.тело:
            for з in у.тело:
                self.заявление(з)
        else:
            self._добавить("pass")
        self.отступ -= 1
    def з_Вернуть(self, у):
        if у.значение is not None:
            self._добавить("return %s" % self.выражение(у.значение))
        else:
            self._добавить("return")
    def з_Выход(self, у):
        self._добавить("raise SystemExit")
    def з_Прервать(self, у):
        self._добавить("break")
    def з_Пропустить(self, у):
        self._добавить("continue")
    def з_Глобально(self, у):
        self._добавить("global %s" % ", ".join(у.имена))
    def з_Подключить(self, у):
        pass
    def з_Попробовать(self, у):
        self._добавить("try:")
        self.отступ += 1
        if у.тело:
            for з in у.тело:
                self.заявление(з)
        else:
            self._добавить("pass")
        self.отступ -= 1
        if у.перехват:
            имя = у.ошибка if у.ошибка else "_ошибка"
            self._добавить("except Exception as %s:" % имя)
            self.отступ += 1
            for з in у.перехват:
                self.заявление(з)
            self.отступ -= 1
    def з_ВыражениеЗаявление(self, у):
        self._добавить(self.выражение(у.выражение))
    def выражение(self, у):
        метод = getattr(self, "в_" + у.тип, None)
        if метод is None:
            raise Exception("нет генератора для выражения %s" % у.тип)
        return метод(у)
    def в_Число(self, у):
        return repr(у.значение)
    def в_Строка(self, у):
        return repr(у.значение)
    def в_ЛогикаЗначение(self, у):
        return "True" if у.значение else "False"
    def в_Ничто(self, у):
        return "None"
    def в_Переменная(self, у):
        return у.имя
    def в_Вызов(self, у):
        return "%s(%s)" % (у.имя, ", ".join(self.выражение(a) for a in у.аргументы))
    def в_Атрибут(self, у):
        return "%s.%s" % (self.выражение(у.объект), у.имя)
    def в_ВызовМетода(self, у):
        return "%s.%s(%s)" % (self.выражение(у.объект), у.имя, ", ".join(self.выражение(a) for a in у.аргументы))
    def в_Индекс(self, у):
        return "%s[%s]" % (self.выражение(у.объект), self.выражение(у.индекс))
    def в_Список(self, у):
        return "[%s]" % ", ".join(self.выражение(e) for e in у.элементы)
    def в_Арифметика(self, у):
        return "(%s %s %s)" % (self.выражение(у.левый), у.оп, self.выражение(у.правый))
    def в_Сравнение(self, у):
        return "(%s %s %s)" % (self.выражение(у.левый), у.оп, self.выражение(у.правый))
    def в_Логика(self, у):
        return "(%s %s %s)" % (self.выражение(у.левый), у.оп, self.выражение(у.правый))
    def в_Не(self, у):
        return "(not %s)" % self.выражение(у.операнд)
    def в_Унарный(self, у):
        return "(-%s)" % self.выражение(у.операнд)
