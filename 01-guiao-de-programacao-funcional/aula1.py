#Exercicio 1.1
def comprimento(lista):
	if lista == []:
		return 0
	return 1 + comprimento(lista[1:])

#Exercicio 1.2
def soma(lista):
	if lista == []:
		return 0
	return int(lista[0]) + soma(lista[1:])

#Exercicio 1.3
def existe(lista, elem):
	if lista == []:
		return False
	return lista[0] == elem or existe(lista[1:],elem)

#Exercicio 1.4
def concat(l1, l2):
	if l1 == []:
		return l2
	if l2 == []:
		return l1

	l1.append(l2[0])
	return concat(l1, l2[1:])

#Exercicio 1.5
def inverte(lista):
	if lista == []:
		return []
	return inverte(lista[1:]) + [lista[0]]

#Exercicio 1.6
def capicua(lista):
	if lista == []:
		return True
	if lista[0] == lista[-1]:
		return capicua(lista[1:-1])

#Exercicio 1.7
def explode(lista):
	if lista == []:
		return []
	if not isinstance(lista[0],list):
		return lista
	return lista[0] + (explode(lista[1:]))

#Exercicio 1.8
def substitui(lista, original, novo):
	if lista == []:
		return []
	if lista[0] == original:
		lista[0] = novo
	return [lista[0]] + substitui(lista[1:],original,novo)

	

#Exercicio 1.9
def junta_ordenado(lista1, lista2):
	if lista1 == []:
		return lista2
	if lista2 == []:
		return lista1
	ordem = lambda x,y: [min(x,y),max(x,y)]
	return ordem(lista1[0], lista2[0]) + junta_ordenado(lista1[1:], lista2[1:])

#Exercicio 1.10 #rever mais depois
def subconjuntos(lista):
	if lista == []:
		return [[]]
	tmp = subconjuntos(lista[1:])
	return tmp + [[lista[0]] + conj for conj in tmp]

#Exercicio 2.1
def separar(lista):
	if lista == []:
		return [], []
	par01, par02 = lista[0]
	lista01, lista02 = separar(lista[1:])
	return [par01] + lista01, [par02] + lista02

#Exercicio 2.2
def remove_e_conta(lista, elem):
	if lista == []:
		return [], 0

	listaPrv, count = remove_e_conta(lista[1:],elem)
	if lista[0] == elem:
		return listaPrv, count + 1
	return [lista[0]] + listaPrv, count
		
#Exercicio 3.1
def cabeca(lista):
	if(lista == []):
		return None
	return lista[0]

#Exercicio 3.2
def cauda(lista):
	if(lista == []):
		return None
	return lista[-1]

#Exercicio 3.3
def juntar(l1, l2):
	if len(l1) != len(l2):
		return None
	if l1 == []:
		return []
	return [(l1[0], l2[0])] + juntar(l1[1:],l2[1:])
	

#Exercicio 3.4
def menor(lista):
	if lista == []:
		return None

	minimo = menor(lista[1:])
	return lista[0] if (minimo is None) or (minimo is not None and lista[0] < minimo) else minimo

#Exercicio 3.6 #ve depois
def max_min(lista):
	if lista == []:
		return None, None
	return (max(lista),min(lista))
