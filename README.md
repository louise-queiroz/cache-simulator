# cache-simulator

## Instalação 
É preciso ter a versão 3 do python em sua máquina, caso for linux pode se instalar com o seguinte comando via terminal:
```
sudo apt-get install python3.
```

Caso seja windows:

Acesse o site oficial do [Python] (https://www.python.org/downloads/windows/);
Faça o download e instalação.

## Compilação
Para compilar o main "cache_simulator.py" é necessário inserir via linha de comando:
```
python3 cache_simulator.py <nsets> <bsize> <assoc> <substituição> <flag_saida> arquivo_de_entrada
```

**cache_simulator.py**: nome do arquivo de execução; <br /> 
**nsets**: número de conjuntos na cache (número total de “linhas” ou “entradas” da cache); <br /> 
**bsize**: tamanho do bloco em bytes; <br /> 
**assoc**: grau de associatividade (número de vias ou blocos que cada conjunto possui); <br /> 
**substituição**:  política de substituição, R de random. <br /> 
**flag_saida**: flag que ativa o modo padrão de saída de dados; <br /> 
**arquivo_de_entrada**: arquivo com os endereços para acesso à cache.

