import math
#Exercicio 4.1
impar = lambda x : x % 2 == 1

#Exercicio 4.2
positivo = lambda x : x >= 0

#Exercicio 4.3
comparar_modulo = lambda x,y : abs(y) - abs(x) > 0

#Exercicio 4.4
cart2pol = lambda x,y: (math.sqrt(x*x+y*y), math.atan2(y,x))

#Exercicio 4.5
def ex5(f,g,h):
    return lambda x,y,z: h(f(x,y),g(y,z))

f = lambda x,y:x + y
g = lambda x,y:x * y
h = lambda x,y:x**y

funcao = ex5(f,g,h)

#Exercicio 4.6/Função filtro?
def quantificador_universal(lista, f):
    if len(lista) == 1:
        return f(lista[0])
    if lista == []:
        return False
    return (f(lista[0]) and quantificador_universal(lista[1:],f))

#Exercicio 4.9
#f tem que processar valor None, ve isto melhor
def ordem(lista, f):
    if len(lista) == 1:
        return lista[0]
    tmp = ordem(lista[1:],f)
    return lista[0] if f(lista[0], tmp) else tmp

#Exercicio 4.10
def filtrar_ordem(lista, f):
    menor = ordem(lista, f)
    resto = [x for x in lista if x != menor]
    return menor, resto

#Exercicio 5.2
def ordenar_seleccao(lista, ordem):
    if lista == []:
        return []
    elem, outrosElems = filtrar_ordem(lista, ordem)
    return [elem] + ordenar_seleccao(outrosElems, ordem)
