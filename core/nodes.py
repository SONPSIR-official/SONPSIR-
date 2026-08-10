# Узлы AST — дерева, которое строит парсер

class Узел:
    def __init__(self, тип, **поля):
        self.тип = тип
        for ключ, значение in поля.items():
            setattr(self, ключ, значение)

    def __repr__(self):
        return f"<Узел {self.тип}>"
