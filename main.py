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

	tam = nsets * assoc	
	cache_val = [0] * tam
	cache_tag = [0] * tam
	tag = 0
	indice = 0
	acessos = 0
	miss_compulsorio = 0
	miss_capacidade = 0
	miss_conflito = 0
	hit = 0
	missRate = 0
	hitRate = 0
	miss2Rate = 0


#calcula o número de bits offset, indice e tag
	n_bits_offset = math.log2(bsize)
	n_bits_indice = math.log2(nsets)

	n_bits_tag = 32 - n_bits_offset - n_bits_indice

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

		missRate = (miss_conflito + miss_capacidade + miss_compulsorio)/acessos
		hitRate = hit / acessos
		print(acessos, hitRate, missRate, miss_compulsorio, miss_capacidade, miss_conflito)

if __name__ == '__main__':
	main() 