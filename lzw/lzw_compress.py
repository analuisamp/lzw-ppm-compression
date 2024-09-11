# lzw_compress.py

from bitarray import bitarray

def compressor(dados_entrada, tam_max, estrategia='R'):
    tam_max_dict = pow(2, tam_max)
    dictionary_size = 256  # Tamanho inicial
    tam_bits = 8  # Número de bits necessários para o tamanho inicial
    dictionary = {bytes([i]): i for i in range(dictionary_size)}  # Dicionário inicial

    result = bitarray()  # Armazenará os bits comprimidos
    comprimento_medio = []  # Lista para armazenar o comprimento médio
    comprimento_total = 0  # Comprimento total do arquivo
    
    current = b''  # Variável para guardar a string de bytes

    for byte in dados_entrada:
        new_string = current + bytes([byte])

        if new_string in dictionary:
            current = new_string
        else:
            result.extend(format(dictionary[current], 'b').zfill(tam_bits))
            comprimento_medio.append(len(result) / comprimento_total)

            # Verifica se o dicionário atingiu o tamanho máximo
            if len(dictionary) < tam_max_dict:
                dictionary[new_string] = dictionary_size
                dictionary_size += 1

                if len(dictionary) >= pow(2, tam_bits):
                    tam_bits += 1
            else:
                # Estratégia E: Não fazer nada, o dicionário para de crescer
                if estrategia == 'E':
                    pass
                # Estratégia R: Reiniciar o dicionário
                elif estrategia == 'R':
                    dictionary_size = 256
                    tam_bits = 8
                    dictionary = {bytes([i]): i for i in range(dictionary_size)}
            
            current = bytes([byte])
        
        comprimento_total += 1

    # Codificar o último elemento
    if current:
        result.extend(format(dictionary[current], 'b').zfill(tam_bits))
        comprimento_medio.append(len(result) / comprimento_total)

    return result, comprimento_medio
