
import sys, math, struct
import numpy as np

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

	cache_val = [nsets * assoc]
	cache_tag = [nsets * assoc]
	tag = [nsets * assoc]
	cache_indice = [nsets * assoc]
	acessos = 0
	miss_compulsorio = 0
	miss_capacidade = 0
	miss_conflito = 0
	hit = 0
	tam = len(cache_val)

#cache vazia
	for i in range(tam):
		cache_val[i] = 0

#calcula o número de bits offset, indice e tag
	n_bits_offset = math.log2(bsize)
	n_bits_indice = math.log2(nsets)

	n_bits_tag = 32 - n_bits_offset - n_bits_indice

#abrir arquivo
	with open('addresses/' + arquivoEntrada, 'rb') as arquivo:
		#zerar tags e bits de validade
		tag = criarCacheTag(nsets, assoc)
		cache_val = criarCacheVal(nsets, assoc)
		while True:
			# lê 4 bytes (32 bits) do arquivo
			valor = arquivo.read(4)
			# verifica se chegou ao fim do arquivo
			if not valor:
				break
			# converte os bytes em um inteiro de 32 bits 
			addr= int(int.from_bytes(valor, byteorder='big', signed=False))
			acessos += 1
			#tag
			cache_tag[i] = addr >> int((n_bits_offset + n_bits_indice))
			#indice
			cache_indice[i] = addr >> int(n_bits_offset) & int((math.pow(2,n_bits_indice)-1))
			#print(addr)  # exibe o valor lido

			#função mapeamento direto
			if assoc == 1 :
				#add indice
				if cache_val[i] == 0:
					miss_compulsorio += 1
					cache_val[i] = 1
					cache_tag[i] = tag[i]
				else:
					if cache_tag[i] == tag[i]:
						hit += 1
					else:
						miss_conflito +=1
						cache_val[i] = 1
						cache_tag[i] = tag[i]
			#rever conceito de tot assoc ser nsets 1
			elif nsets == 1:
				#add indice
				if cache_val[i] == 0:
					miss_compulsorio += 1
					cache_val[i] = 1
					cache_tag[i] = tag[i]
				else:
					if cache_tag[i] == tag[i]:
						hit += 1
					else:
						#é capacidade ou conflito?
						miss_capacidade += 1
						cache_val[i] = 1
						cache_tag[i] = tag[i]
			else:
				#aplicar método de varias vias com matriz
				for i in assoc:
					if cache_val[i] == 0:
						miss_compulsorio += 1
						cache_val[i] = 1
						cache_tag[i] = tag[i]
					else:
						if cache_tag[i] == tag[i]:
							hit += 1
						else:
						#é capacidade ou conflito?
							miss_conflito+= 1
							cache_val[i] = 1
							cache_tag[i] = tag[i]


#função criar cache e zerar tags
def criarCacheTag(nsets, assoc):
	tam = [nsets * assoc]
	tag = [tam]
	for i in tam:
		tag[i] = 0
	return tag

#função zerar bits de validade
def criarCacheVal(nsets, assoc):
	tam = [nsets * assoc]
	val = [tam]
	for i in tam:
		val[i] = 0
	return val


#add indice para val e resolver assoc de vias