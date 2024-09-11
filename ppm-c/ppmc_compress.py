import collections

class PPMCCompressor:
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

    def encode(self, data):
        encoded_data = []
        context = []
        
        for symbol in data:
            order = min(len(context), self.max_order)
            
            # Tenta encontrar o símbolo no contexto atual ou menor
            found = False
            while order >= 0:
                context_slice = tuple(context[-order:])
                if symbol in self.contexts[order][context_slice]:
                    # Símbolo encontrado no contexto atual
                    encoded_data.append((context_slice, symbol))
                    found = True
                    break
                else:
                    # Adiciona ESCAPE para o contexto menor
                    encoded_data.append((context_slice, "ESCAPE"))
                    order -= 1
            
            if not found:
                # Se não encontrou, insere o símbolo no contexto de ordem 0
                encoded_data.append(((), symbol))
            
            # Atualiza o modelo com o novo símbolo
            self.update_model(context, symbol)
            
            # Adiciona o símbolo ao contexto
            context.append(symbol)
        
        return encoded_data
