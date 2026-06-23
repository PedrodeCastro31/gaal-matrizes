from pydantic import BaseModel

class Matriz(BaseModel):
    matriz: list[list[int]]
    ordem: int

    def __init__(self, matriz: list[list[int]], ordem: int):
        self.matriz = matriz
        self.ordem = ordem

    def __str__(self):
        return str(self.matriz)


#Template aleatório, vou mudar tudo