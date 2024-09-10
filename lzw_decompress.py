# lzw_decompress.py

def decompress(dados_comprimidos, tam_max, tam_arq_compress):
    first_element = True
    tam_max_dict = pow(2, tam_max) 
    dictionary_size = 256  # Tamanho inicial
    tam_bits = 8  # Número de bits necessários para o tamanho inicial
    dictionary = {i: bytes([i]) for i in range(dictionary_size)}  # Dicionário inicial

    result = []  # Lista para armazenar os bytes descomprimidos
    idx = 0  # Contador de bits já processados

    while idx < tam_arq_compress:
        code = dados_comprimidos[idx:idx + tam_bits].to01()
        idx += tam_bits
        code = int(code, 2)

        if first_element:
            saida = dictionary[code]
            result.append(saida)

            if len(dictionary) < tam_max_dict:
                dictionary[dictionary_size] = saida
                if len(dictionary) >= pow(2, tam_bits):
                    tam_bits += 1
            else:
                dictionary_size = 256
                tam_bits = 8
                dictionary = {i: bytes([i]) for i in range(dictionary_size)}
            
            first_element = False
            continue

        last_byte = dictionary[code][0:1]

        if dictionary_size < tam_max_dict:
            dictionary[dictionary_size] += last_byte
            dictionary_size += 1

        saida = dictionary[code]
        result.append(saida)

        if len(dictionary) < tam_max_dict:
            dictionary[dictionary_size] = saida
            if len(dictionary) >= pow(2, tam_bits):
                tam_bits += 1
        else:
            dictionary_size = 256
            tam_bits = 8
            dictionary = {i: bytes([i]) for i in range(dictionary_size)}

    return result
