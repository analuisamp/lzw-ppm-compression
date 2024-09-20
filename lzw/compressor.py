from bitarray import bitarray
import json

def compressor(dados_entrada, tam_max, method, save_dict=False):  # Adicionando o argumento save_dict
    tam_max_dict = pow(2, tam_max)
    dictionary_size = 256  # Tamanho inicial do dicionário
    tam_bits = 8  # Quantidade de bits necessária inicialmente
    dictionary = {bytes([i]): i for i in range(dictionary_size)}  # Dicionário inicial

    result = bitarray()  # Onde serão colocados os bits da compressão
    comprimento_medio = []  # Lista de comprimentos médios do arquivo
    comprimento_total = 0  # Comprimento atual do arquivo
    
    current = b''  # Variável para guardar a string de bytes sendo processada

    for byte in dados_entrada:
        new_string = current + bytes([byte])
        if new_string in dictionary:
            current = new_string
        else:
            result.extend(format(dictionary[current], 'b').zfill(tam_bits))
            comprimento_medio.append(len(result) / comprimento_total)

            if len(dictionary) < tam_max_dict:
                dictionary[new_string] = dictionary_size
                dictionary_size += 1

                if len(dictionary) >= pow(2, tam_bits):
                    tam_bits += 1
            else:
                if method == 'R':
                    dictionary_size = 256
                    tam_bits = 8
                    dictionary = {bytes([i]): i for i in range(dictionary_size)}

            current = bytes([byte])

        comprimento_total += 1

    if current:
        result.extend(format(dictionary[current], 'b').zfill(tam_bits))
        comprimento_medio.append(len(result) / comprimento_total)

    # Salva o dicionário em um arquivo se a opção save_dict for True
    if save_dict:
        with open("static_dictionary.json", "w") as dict_file:
            json_dict = {str(k): v for k, v in dictionary.items()}  # Convertendo as chaves para string
            json.dump(json_dict, dict_file)

    return result, comprimento_medio
