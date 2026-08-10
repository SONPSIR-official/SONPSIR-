import re

class Компилятор:
    def __init__(self, код):
        self.исходный_код = код
        self.python_код = []
        self.отступ = 0
        
    def транслировать(self):
        строки = self.исходный_код.split('\n')
        for строка in строки:
            очищенная = строка.strip()
            if not очищенная or очищенная.startswith('#'):
                continue
            
            # Обработка отступов (упрощенная)
            текущий_отступ = len(строка) - len(строка.lstrip())
            
            # Нормализация ключевых слов
            py_line = очищенная
            py_line = re.sub(r'^пусть\s+', '', py_line) # убираем "пусть"
            py_line = py_line.replace('что печатать', 'print')
            py_line = py_line.replace('выведи', 'print')
            py_line = py_line.replace('если ', 'if ')
            py_line = py_line.replace(' то', ':')
            py_line = py_line.replace('иначе:', 'else:')
            py_line = py_line.replace('иначе если ', 'elif ')
            py_line = py_line.replace('пока ', 'while ')
            py_line = py_line.replace(' делать', '')
            py_line = py_line.replace('повторять ', 'for _ in range(')
            py_line = py_line.replace(' раз)', '):')
            py_line = py_line.replace(' раза)', '):')
            py_line = py_line.replace('функция ', 'def ')
            py_line = py_line.replace(' вернуть ', ' return ')
            py_line = py_line.replace('истина', 'True')
            py_line = py_line.replace('ложь', 'False')
            
            # Добавляем отступ
            self.python_код.append('    ' * (текущий_отступ // 4) + py_line)
            
        return '\n'.join(self.python_код)
