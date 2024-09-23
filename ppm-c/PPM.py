import time
from collections import defaultdict
import math

class PPMC:
    def __init__(self, max_order=3):
        self.max_order = max_order  # define o maior contexto
        self.contexts = defaultdict(lambda: defaultdict(int))  # armazena os contextos e suas frequências

    def update_context(self, context, symbol):
        """Atualiza a frequência do símbolo no contexto dado."""
        self.contexts[context][symbol] += 1

    def get_probability(self, context, symbol):
        """Obtém a probabilidade do símbolo no contexto dado."""
        if symbol in self.contexts[context]:
            total = sum(self.contexts[context].values())
            return self.contexts[context][symbol] / total
        return 0

    def compress(self, data):
        """Compressão usando PPM-C."""
        compressed_data = []
        for i in range(len(data)):
            # aara cada símbolo, tentamos prever seu contexto
            for order in range(self.max_order, 0, -1):
                context = tuple(data[max(0, i - order):i])
                if context in self.contexts and data[i] in self.contexts[context]:
                    # achamos o contexto
                    probability = self.get_probability(context, data[i])
                    compressed_data.append((context, data[i], probability))
                    break
            else:
                # contexto não encontrado, usamos um símbolo desconhecido
                compressed_data.append(((), data[i], 1.0 / 256))

            # atualizamos os contextos com o símbolo atual
            for order in range(1, self.max_order + 1):
                context = tuple(data[max(0, i - order):i])
                self.update_context(context, data[i])

        return compressed_data

    def decompress(self, compressed_data):
        """Descompressão usando PPM-C."""
        decompressed_data = []
        for context, symbol, _ in compressed_data:
            decompressed_data.append(symbol)
        return ''.join(decompressed_data)

def calculate_average_length(compressed_data):
    """Calcula o comprimento médio em bits dos valores comprimidos usando a entropia."""
    total_length = 0
    for context, symbol, probability in compressed_data:
        if probability > 0:
            total_length += -math.log2(probability)  # entropia: -log2(p)
        else:
            total_length += 8  # simbolizando um símbolo sem compressão (8 bits para cada caractere)
    return total_length / len(compressed_data)

# função para compressão e descompressão de um arquivo com diferentes valores de k
def compress_and_decompress_file(file_path, k_values):
    with open(file_path, 'r') as f:
        data = f.read()

    for k in k_values:
        print(f"\n--- Testando com k = {k} ---")
        compressor = PPMC(max_order=k)

        # compressão
        start_time = time.time()
        compressed_data = compressor.compress(data)
        compression_time = time.time() - start_time

        # descompressão
        start_time = time.time()
        decompressed_data = compressor.decompress(compressed_data)
        decompression_time = time.time() - start_time

        # verificar se a descompressão é igual ao arquivo original
        assert data == decompressed_data, "Erro: Os dados descomprimidos não são iguais ao original."

        # calcular o comprimento médio dos valores comprimidos
        average_length = calculate_average_length(compressed_data)

        # salvar o arquivo descomprimido
        output_file = f'descomprimido_k{k}.txt'
        with open(output_file, 'w') as out_f:
            out_f.write(decompressed_data)

        print(f"Tempo de compressão: {compression_time:.6f} segundos")
        print(f"Tempo de descompressão: {decompression_time:.6f} segundos")
        print(f"Comprimento médio dos valores comprimidos (em bits): {average_length:.2f}")
        print(f"Arquivo descomprimido gerado: {output_file}")

# exemplo de uso com arquivo de texto
file_path = 'dickens'  # caminho do arquivo
k_values = [0, 1, 4, 6, 8, 10]  # valores de k que serão testados
compress_and_decompress_file(file_path, k_values)
