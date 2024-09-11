import collections

class PPMCDecompressor:
    def __init__(self, max_order=4):
        self.max_order = max_order
        self.contexts = [collections.defaultdict(collections.Counter) for _ in range(max_order + 1)]
        # Inicializa o contexto de ordem 0 com todos os possíveis símbolos (alfabeto ASCII básico)
        for i in range(256):
            self.contexts[0][()].update({i: 1})  # Ordem 0 com todos os símbolos

    def update_model(self, context, symbol):
        """
        Atualiza o modelo adicionando a frequência do símbolo ao contexto dado.
        """
        for i in range(min(len(context) + 1, self.max_order + 1)):
            self.contexts[i][tuple(context[-i:])][symbol] += 1

    def decode(self, encoded_data):
        decoded_data = []
        context = []
        
        for context_slice, symbol in encoded_data:
            if symbol == "ESCAPE":
                continue  # Pula para o próximo contexto se for ESCAPE
            else:
                # Decodifica o símbolo no contexto atual
                decoded_data.append(symbol)
                self.update_model(context, symbol)
                context.append(symbol)
        
        return decoded_data
