import sys
from time import time
from compressor import compressor
from decompressor import decompress

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Chame: main.py [input_file] [max_dict_size] [method: E ou R]")
        print("Obs -> tam_max_dictionary = 2^max_dict_size")
        sys.exit(1)

    # Recebe essas 3 variáveis na chamada de execução
    input_file = sys.argv[1]
    tam_max = int(sys.argv[2])
    method = sys.argv[3]

    # Abre o arquivo de entrada
    with open(input_file, 'rb') as file:
        data = file.read()  # Lê todos os dados

    # Compressão
    inicio = time()
    compressed_data, comprimento_medio = compressor(data, tam_max, method)  # Chama a compressão
    fim = time()

    # Calcula o tamanho do arquivo comprimido e coloca nos 5 primeiros bytes do arquivo
    tam_compressed = len(compressed_data)
    bytes_tam_compressed = tam_compressed.to_bytes(5, 'big')

    # Gera o nome do arquivo de saída comprimido
    split = input_file.split('.')
    if len(split) == 2:
        output_file = split[0] + '_compressed.lzw'
    elif len(split) == 1:
        output_file = input_file + '_compressed.lzw'

    # Escreve no arquivo de saída os bytes do tamanho e os bits da compressão
    with open(output_file, 'wb') as file:
        file.write(bytes_tam_compressed)
        compressed_data.tofile(file)

    print(f'Demorou {fim - inicio} segundos para comprimir')
    print(f'O comprimento médio dos valores foi {comprimento_medio[-1]}')

    # Descompressão
    inicio = time()
    uncompressed_data = decompress(compressed_data, tam_max, tam_compressed)  # Chama a descompressão
    fim = time()

    # Gera o nome do arquivo de saída descomprimido
    split = input_file.split('.')
    if len(split) == 2:
        output_file = split[0] + '_uncompressed.bin'
    elif len(split) == 1:
        output_file = input_file + '_uncompressed.bin'

    # Escreve no arquivo de saída os bytes da descompressão
    with open(output_file, 'wb') as file:
        for string in uncompressed_data:
            file.write(string)

    print(f'Demorou {fim - inicio} segundos para descomprimir')
