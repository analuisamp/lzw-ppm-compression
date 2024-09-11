# compressor.py

import sys
from time import time
from lzw_compress import compressor
from lzw_decompress import decompress
from bitarray import bitarray

if len(sys.argv) != 4:
    print("Uso: python compressor.py [input_file] [max_dict_size] [estrategia: E ou R]")
    sys.exit(1)

# Receber variáveis da execução
input_file = sys.argv[1]
tam_max = int(sys.argv[2])
estrategia = sys.argv[3]

# Abrir o arquivo de entrada
with open(input_file, 'rb') as file:
    data = file.read()

# Compressão
inicio = time()
compressed_data, comprimento_medio = compressor(data, tam_max, estrategia)
fim = time()

# Calcular o tamanho do arquivo comprimido
tam_compressed = len(compressed_data)
bytes_tam_compressed = tam_compressed.to_bytes(5, 'big')

# Gerar o nome do arquivo de saída
split = input_file.split('.')
output_file = split[0] + 'lzw.bin' if len(split) == 2 else input_file + 'lzw.bin'

# Escrever o arquivo comprimido
with open(output_file, 'wb') as file:
    file.write(bytes_tam_compressed)
    compressed_data.tofile(file)

print(f'Demorou {fim - inicio} segundos para comprimir')
print(f'O comprimento médio dos valores foi {comprimento_medio[-1]}')
print("Compressão concluída!")

# Descompressão
inicio = time()
uncompressed_data = decompress(compressed_data, tam_max, tam_compressed)
fim = time()

# Gerar o nome do arquivo de saída descomprimido
output_file = split[0] + 'uncompressed.bin' if len(split) == 2 else input_file + 'uncompressed.bin'

# Escrever o arquivo descomprimido
with open(output_file, 'wb') as file:
    for string in uncompressed_data:
        file.write(string)

print(f'Demorou {fim - inicio} segundos para descomprimir')
print("Descompressão concluída!")
