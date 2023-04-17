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

	#gera cache
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
			#cálculo do endereço
			mod = indice % nsets

			#mapeamento direto
			if assoc == 1 :
				#miss compulsório
				if cache_val[mod] == 0:
					miss_compulsorio += 1
					cache_val[mod] = 1
					cache_tag[mod] = tag
				else:
					#hit
					if cache_tag[mod] == tag:
						hit += 1
					else:
						#miss conflito
						miss_conflito +=1
						cache_val[mod] = 1
						cache_tag[mod] = tag

			#mapeamento totalmente associativo
			elif nsets == 1:
				#variáveis auxiliares
				cont = 0
				disp = 0
				#procura o valor em todos os blocos
				for i in range(assoc):
					#verifica se há hit
					if cache_tag[i] == tag and cache_val[i] == 1:
						hit +=1
						cont = 1
						break
				#tratamento da falta
				if cont == 0:
					while disp == 0:
						#verifica se há espaço vazio na cache e miss compulsório
						for i in range(assoc):
							if cache_val[i] == 0:
								cache_val[i] = 1
								miss_compulsorio +=1
								cache_tag[i] = tag
								disp = 1
								break
						#miss de capacidade e substitui
						if disp!=1:
							miss_capacidade +=1
							endereco = subRandom(0, (assoc-1))
							cache_tag[endereco] = tag
							disp = 1

			#mapeamento conjunto associativo
			else: 
				#variável auxiliar
				cont=0
				#hit
				for i in range(assoc):
					if cache_tag[i][mod] == tag and cache_val[i][mod]== 1:
						hit +=1
						cont +=1
						break
				#tratamento da falta
				if cont==0:
					#checa por conjuntos vazios
					for i in range(assoc):
						if cache_val [i][mod]== 0 and cache_tag [i][mod]== 0:
							disp+=1
				if disp == assoc:
						for i in range(assoc):
							if cache_val [i][mod]== 0 and cache_tag [i][mod]== 0:
								cache_val[i][mod]= 1
								cache_tag[i][mod] = tag
								miss_compulsorio += 1
					#conflito ou capacidade?
				else:
					#conflito
					for i in range(assoc):
						if cache_val [i][mod]== 0:
							cache_val[i][mod]= 1
							cache_tag[i][mod] = tag
							miss_conflito += 1
							cont +=1
							break
					#capacidade
					if cont==0:
						endereco = subRandom(0, (assoc-1))
						cache_val[endereco][mod]= 1
						cache_tag[endereco][mod] = tag
						miss_capacidade += 1
						

		#cálculos
		misses = miss_conflito + miss_capacidade + miss_compulsorio
		missRate = (miss_conflito + miss_capacidade + miss_compulsorio)/acessos
		miss_compulsorio = miss_compulsorio / misses
		miss_capacidade = miss_capacidade/misses
		miss_conflito = miss_conflito/misses
		hitRate = hit / acessos

		#formato de saída
		if flagOut == 1:
			print(acessos,"{:.4f} {:.4f} {:.4f} {:.4f} {:.4f}". format(hitRate, missRate, miss_compulsorio, miss_capacidade, miss_conflito))
		elif flagOut == 0:
			print("Acessos:", acessos ,"Hit rate: {:.4f} Miss rate: {:.4f} Miss compulsório: {:.4f} Miss de capacidade: {:.4f} Miss de conflito: {:.4f}". format(hitRate, missRate, miss_compulsorio, miss_capacidade, miss_conflito))
		else:
			print("Erro de flag")


#função substituição random
def subRandom(valora, valorb):
	return random.randint(valora, valorb)

#função para criar cache
def criarCache (assoc,nsets, tam):
	if assoc !=1 and nsets !=1:
		cache = [[0] * nsets for i in range(assoc)]
	else:
		cache = [0] * tam
	return cache


if __name__ == '__main__':
	main()