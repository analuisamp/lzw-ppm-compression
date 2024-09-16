# compressor.py

import sys
from time import time
from lzw_compress import compressor  # Função para compressão LZW
from lzw_decompress import decompress  # Função para descompressão LZW
from bitarray import bitarray  # Biblioteca usada para manipulação de bits

# Verifica se o número de argumentos passados é correto
if len(sys.argv) != 4:
    print("Uso: python compressor.py [input_file] [max_dict_size] [estrategia: E ou R]")
    sys.exit(1)

# Receber variáveis da execução a partir dos argumentos passados via linha de comando
input_file = sys.argv[1]  # Arquivo de entrada a ser comprimido
tam_max = int(sys.argv[2])  # Tamanho máximo do dicionário utilizado no LZW
estrategia = sys.argv[3]  # Estratégia para lidar com o dicionário cheio: E (expansão) ou R (reset)

# Abrir o arquivo de entrada no modo binário ('rb' = read binary)
with open(input_file, 'rb') as file:
    data = file.read()  # Lê o conteúdo do arquivo e armazena em 'data'

# Compressão
inicio = time()  # Marca o tempo inicial da compressão
compressed_data, comprimento_medio = compressor(data, tam_max, estrategia)  # Executa a compressão
fim = time()  # Marca o tempo final da compressão

# Calcula o tamanho do arquivo comprimido em bytes
tam_compressed = len(compressed_data)  # Tamanho do dado comprimido
bytes_tam_compressed = tam_compressed.to_bytes(5, 'big')  # Converte o tamanho para 5 bytes no formato big-endian

# Gerar o nome do arquivo de saída, com a extensão '.lzw.bin'
split = input_file.split('.')  # Separa o nome do arquivo por '.' para lidar com a extensão
# Se houver exatamente uma extensão, substitui, senão apenas adiciona
output_file = split[0] + 'lzw.bin' if len(split) == 2 else input_file + 'lzw.bin'

# Escrever o arquivo comprimido
with open(output_file, 'wb') as file:  # Abre o arquivo de saída no modo binário de escrita ('wb' = write binary)
    file.write(bytes_tam_compressed)  # Escreve o tamanho do arquivo comprimido como cabeçalho
    compressed_data.tofile(file)  # Escreve o conteúdo comprimido no arquivo

# Exibe informações de desempenho da compressão
print(f'Demorou {fim - inicio} segundos para comprimir')  # Tempo total da compressão
print(f'O comprimento médio dos valores foi {comprimento_medio[-1]}')  # Comprimento médio dos símbolos comprimidos
print("Compressão concluída!")  # Confirmação de que a compressão terminou

# Descompressão
inicio = time()  # Marca o tempo inicial da descompressão
uncompressed_data = decompress(compressed_data, tam_max, tam_compressed)  # Executa a descompressão
fim = time()  # Marca o tempo final da descompressão

# Gerar o nome do arquivo de saída descomprimido
output_file = split[0] + 'uncompressed.bin' if len(split) == 2 else input_file + 'uncompressed.bin'

# Escrever o arquivo descomprimido
with open(output_file, 'wb') as file:  # Abre o arquivo de saída no modo binário de escrita
    for string in uncompressed_data:  # Itera sobre os dados descomprimidos
        file.write(string)  # Escreve cada string descomprimida no arquivo

# Exibe informações de desempenho da descompressão
print(f'Demorou {fim - inicio} segundos para descomprimir')  # Tempo total da descompressão
print("Descompressão concluída!")  # Confirmação de que a descompressão terminou


def compress_with_stats_lzw(data, max_dict_size):
    compressed_data = []  # Dados comprimidos
    lengths = []  # Lista para salvar os comprimentos médios até o n-ésimo byte
    last_m_lengths = []  # Lista para salvar os comprimentos dos últimos m bytes
    total_length = 0  # Comprimento total comprimido até o n-ésimo byte
    m = 100  # Valor de m

    # Simulação da compressão LZW
    for i, byte in enumerate(data):
        # Supondo que o processo de compressão adiciona um novo símbolo comprimido
        compressed_data.append(byte)  # Placeholder para o símbolo comprimido
        
        total_length += len(compressed_data)  # Atualiza o comprimento total
        avg_length = total_length / (i + 1)  # Comprimento médio até o n-ésimo byte
        lengths.append(avg_length)  # Salva o comprimento médio
        
        # Calcula o comprimento médio dos últimos m bytes
        if i + 1 >= m:
            avg_length_last_m = total_length / m
        else:
            avg_length_last_m = total_length / (i + 1)
        
        last_m_lengths.append(avg_length_last_m)

    return compressed_data, lengths, last_m_lengths

import matplotlib.pyplot as plt

def plot_avg_length(lengths, title="Curva de I(n) x n"):
    """
    Gera o gráfico do comprimento médio I(n) x n.
    
    :param lengths: Lista com os comprimentos médios até o n-ésimo byte.
    :param title: Título do gráfico.
    """
    plt.plot(range(len(lengths)), lengths)
    plt.title(title)
    plt.xlabel("Número de bytes (n)")
    plt.ylabel("Comprimento médio I(n)")
    plt.grid(True)
    plt.show()

def plot_avg_last_m_length(last_m_lengths, title="Curva de I(𝑚) x n"):
    """
    Gera o gráfico do comprimento médio I(𝑚) x n.
    
    :param last_m_lengths: Lista com os comprimentos médios dos últimos m bytes até o n-ésimo byte.
    :param title: Título do gráfico.
    """
    plt.plot(range(len(last_m_lengths)), last_m_lengths)
    plt.title(title)
    plt.xlabel("Número de bytes (n)")
    plt.ylabel("Comprimento médio dos últimos m bytes")
    plt.grid(True)
    plt.show()

# Compressão com LZW
compressed_data, lengths, last_m_lengths = compress_with_stats_lzw(data, max_dict_size=2**21)

# Gerar gráfico I(n) x n
plot_avg_length(lengths, title="Curva de I(n) x n - LZW")

# Gerar gráfico I(𝑚) x n
plot_avg_last_m_length(last_m_lengths, title="Curva de I(m) x n - LZW")


