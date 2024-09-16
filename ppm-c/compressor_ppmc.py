import sys
from ppmc_compress import PPMCCompressor  # Importa a classe de compressão PPMC
from ppmc_decompress import PPMCDecompressor  # Importa a classe de descompressão PPMC

# Verifica se o número de argumentos está correto
if len(sys.argv) != 2:
    print("Usage: python compressor_ppmc.py [input_file]")  # Instrução de uso do programa
    sys.exit(1)  # Encerra o programa se o número de argumentos estiver incorreto

# Lê o nome do arquivo de entrada passado como argumento
input_file = sys.argv[1]
with open(input_file, 'rb') as file:  # Abre o arquivo no modo binário para leitura
    data = file.read()  # Lê todo o conteúdo do arquivo e armazena em 'data'

# Compressão usando o algoritmo PPMC (Prediction by Partial Matching)
compressor = PPMCCompressor(max_order=4)  # Cria uma instância do compressor PPMC com ordem máxima 4
encoded_data = compressor.encode(data)  # Executa a compressão dos dados lidos

# Grava o arquivo comprimido no disco com a extensão '.ppmc'
with open(input_file + '.ppmc', 'wb') as file:  # Abre o arquivo comprimido para escrita em binário
    file.write(bytes(str(encoded_data), 'utf-8'))  # Escreve os dados comprimidos convertidos em string e depois em bytes

# Descompressão usando o algoritmo PPMC
decompressor = PPMCDecompressor(max_order=4)  # Cria uma instância do descompressor PPMC com ordem máxima 4
# Usa 'eval' para converter a string de volta para o formato de dado original (provavelmente uma lista ou estrutura complexa)
decoded_data = decompressor.decode(eval(str(encoded_data)))  

# Grava o arquivo descomprimido no disco com o sufixo '_uncompressed.txt'
with open(input_file + '_uncompressed.txt', 'wb') as file:  # Abre o arquivo descomprimido para escrita em binário
    file.write(bytes(decoded_data))  # Escreve os dados descomprimidos no arquivo

def compress_with_stats_ppmc(data, max_order=4):
    compressed_data = []  # Dados comprimidos
    lengths = []  # Lista para salvar os comprimentos médios até o n-ésimo byte
    last_m_lengths = []  # Lista para salvar os comprimentos dos últimos m bytes
    total_length = 0  # Comprimento total comprimido até o n-ésimo byte
    m = 100  # Valor de m

    context = []  # Contexto PPM-C
    compressor = PPMCCompressor(max_order)  # Usando a classe de compressão PPM-C

    for i, symbol in enumerate(data):
        compressed_data.append(symbol)  # Placeholder para o símbolo comprimido
        total_length += len(compressed_data)  # Atualiza o comprimento total
        avg_length = total_length / (i + 1)  # Comprimento médio até o n-ésimo byte
        lengths.append(avg_length)
        
        # Calcula o comprimento médio dos últimos m bytes
        if i + 1 >= m:
            avg_length_last_m = total_length / m
        else:
            avg_length_last_m = total_length / (i + 1)
        
        last_m_lengths.append(avg_length_last_m)
        
        # Atualiza o contexto
        context.append(symbol)
        compressor.update_model(context, symbol)

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

def plot_avg_last_m_length(last_m_lengths, title="Curva de I(m) x n"):
    """
    Gera o gráfico do comprimento médio I(m) x n.
    
    :param last_m_lengths: Lista com os comprimentos médios dos últimos m bytes até o n-ésimo byte.
    :param title: Título do gráfico.
    """
    plt.plot(range(len(last_m_lengths)), last_m_lengths)
    plt.title(title)
    plt.xlabel("Número de bytes (n)")
    plt.ylabel("Comprimento médio dos últimos m bytes")
    plt.grid(True)
    plt.show()

    # Compressão com PPM-C
compressed_data, lengths, last_m_lengths = compress_with_stats_ppmc(data, max_order=4)

# Gerar gráfico I(n) x n
plot_avg_length(lengths, title="Curva de I(n) x n - PPM-C")

# Gerar gráfico I(m) x n
plot_avg_last_m_length(last_m_lengths, title="Curva de I(m) x n - PPM-C")

