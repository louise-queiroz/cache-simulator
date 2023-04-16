import sys, math, struct, random

def main():
	if (len(sys.argv) != 7):
		print("Numero de argumentos incorreto. Utilize:")
		print("python cache_simulator.py <nsets> <bsize> <assoc> <substituição> <flag_saida> arquivo_de_entrada")
		exit(1)
	
	nsets = int(sys.argv[1])
	bsize = int(sys.argv[2])
	assoc = int(sys.argv[3])
	subst = sys.argv[4]
	flagOut = int(sys.argv[5])
	arquivoEntrada = sys.argv[6]

	print("nsets =", nsets)
	print("bsize =", bsize)
	print("assoc =", assoc)
	print("subst =", subst)
	print("flagOut =", flagOut)
	print("arquivo =", arquivoEntrada)

	tam = nsets * assoc	
	tag = 0
	indice = 0
	acessos = 0
	miss_compulsorio = 0
	miss_capacidade = 0
	miss_conflito = 0
	hit = 0
	misses = 0
	missRate = 0
	hitRate = 0
	endereco = 0
	cont = 0
	disp = 0

#calcula o número de bits offset, indice e tag
	n_bits_offset = math.log2(bsize)
	n_bits_indice = math.log2(nsets)
	
	n_bits_tag = 32 - n_bits_offset - n_bits_indice

	cache_tag = criarCache(assoc,nsets,tam)
	cache_val = criarCache(assoc,nsets,tam)

#abrir arquivo
	with open('addresses/' + arquivoEntrada, 'rb') as arquivo:

		while True:
			# lê 4 bytes (32 bits) do arquivo
			valor = arquivo.read(4)
			# verifica se chegou ao fim do arquivo
			if not valor:
				break
			# converte os bytes em um inteiro de 32 bits 
			#for i in range(tam):
			addr= int(int.from_bytes(valor, byteorder='big', signed=False))
			acessos += 1
			#tag
			tag = addr >> int((n_bits_offset + n_bits_indice))
			#indice
			indice = addr >> int(n_bits_offset) & int((math.pow(2,n_bits_indice)-1))
			mod = indice % nsets

			#função mapeamento direto
			if assoc == 1 :
				if cache_val[mod] == 0:
					miss_compulsorio += 1
					cache_val[mod] = 1
					cache_tag[mod] = tag
				else:
					if cache_tag[mod] == tag:
						hit += 1
					else:
						miss_conflito +=1
						cache_val[mod] = 1
						cache_tag[mod] = tag
			#função totalmente associativa
			elif nsets == 1:
				cont = 0
				disp = 0
				#procura o valor em todos os blocos
				for i in range(assoc):
					if cache_tag[i] == tag and cache_val[i] == 1:
						hit +=1
						cont = 1
						break
				#tratamento da falta
				if cont == 0:
					while disp == 0:
						for i in range(assoc):
							if cache_val[i] == 0:
								cache_val[i] = 1
								miss_compulsorio +=1
								cache_tag[i] = tag
								disp = 1
								break
						disp = 2
					if disp == 2:
						miss_capacidade +=1
						endereco = subRandom(0, (assoc-1))
						cache_tag[endereco] = tag
			else: #futura assoc conjunto
				erro += 1
				print("erro")

		misses = miss_conflito + miss_capacidade + miss_compulsorio
		missRate = (miss_conflito + miss_capacidade + miss_compulsorio)/acessos
		miss_compulsorio = miss_compulsorio / misses
		miss_capacidade = miss_capacidade/misses
		miss_conflito = miss_conflito/misses
		hitRate = hit / acessos

		print(acessos,"{:.4f} {:.4f} {:.4f} {:.4f} {:.4f}". format(hitRate, missRate, miss_compulsorio, miss_capacidade, miss_conflito))
		print(cache_tag)

def subRandom(valora, valorb):
	return random.randint(valora, valorb)

def criarCache (assoc,nsets, tam):
	if assoc !=1 and nsets !=1:
		cache = [[0] * nsets for i in range(assoc)]
	else:
		cache = [0] * tam
	return cache

if __name__ == '__main__':
	main() 