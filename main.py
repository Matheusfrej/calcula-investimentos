import json

# Classe que representa cada nó (objeto de investimento) na árvore
class Node:
    def __init__(self, nome, recomendado=0, investido=0):
        self.nome = nome
        self.orig_recomendado = recomendado  # Valor recomendado original (fixo)
        self.recomendado = recomendado       # Valor recomendado atual (ajustável)
        self.investido = investido
        self.children = []
        self.parent = None

    def add_child(self, child):
        child.parent = self
        self.children.append(child)

    def update_upwards(self):
        """Atualiza recursivamente o valor investido e redistribui os orçamentos dos nós pais."""
        if self.parent:
            self.parent.investido = sum(child.investido for child in self.parent.children)
            self.parent.update_children_recommended()
            self.parent.update_upwards()

    def update_children_recommended(self):
        """Redistribui o orçamento recomendado entre os filhos (apenas os que ainda não foram investidos),
        de forma que a soma dos recomendados seja igual ao orçamento disponível neste nó.
        Propaga essa atualização recursivamente para os descendentes."""
        if not self.children:
            return
        restante = self.recomendado - sum(child.investido for child in self.children)
        total_orig = sum(child.orig_recomendado for child in self.children if child.investido == 0)
        for child in self.children:
            if child.investido == 0:
                child.recomendado = (child.orig_recomendado / total_orig * max(restante, 0)) if total_orig > 0 else 0
            child.update_children_recommended()

    def display(self, indent=0):
        espaco = " " * indent
        print(f"{espaco}{self.nome}: Investido R$ {self.investido:.2f} (Recomendado: R$ {self.recomendado:.2f})")
        for child in self.children:
            child.display(indent + 2)


def build_tree_from_config(name, conf, total_value):
    """
    Constrói recursivamente um nó a partir da configuração.
    Distribui o orçamento (total_value) entre os filhos usando os pesos definidos.
    """
    node = Node(name, recomendado=total_value)
    if "children" in conf:
        children_config = conf["children"]
        total_weight = sum(child_conf.get("weight", 0) for child_conf in children_config.values())
        for child_name, child_conf in children_config.items():
            weight = child_conf.get("weight", 0)
            child_node = build_tree_from_config(child_name, child_conf, node.recomendado * (weight / total_weight))
            node.add_child(child_node)
    return node


def build_full_tree(total, config):
    """
    Constrói a árvore completa a partir do dicionário de configuração.
    Para os nós diretos (filhos do "Investimento Total"), o usuário informa o peso para "Renda Variável"
    e o peso para "Renda Fixa" é automaticamente calculado como (1 - peso de Renda Variável).
    """
    root = Node("Investimento Total", recomendado=total)
    weights = {}
    items = config.items()
    items_length = len(items)
    current_item = 1
    total_weight = 0
    for key, conf in items:
        if current_item == items_length and items_length > 1:
            weights[key] = 1 - total_weight
        else:
            peso = float(input(f"Digite a porcentagem (peso) para {key} (padrão: {conf['weight']}): ") or conf["weight"])
            weights[key] = peso
            total_weight += peso
            current_item += 1
    total_weight = sum(weights.values())
    for key, conf in items:
        prop = weights[key] / total_weight
        child_node = build_tree_from_config(key, conf, total * prop)
        root.add_child(child_node)
    return root


def coletar_folhas(node):
    folhas = []
    def _coletar(n):
        if not n.children:
            folhas.append(n)
        else:
            for child in n.children:
                _coletar(child)
    _coletar(node)
    return folhas


def calcular_investimento(I, config):
    # Constrói a árvore de investimentos a partir da configuração e dos pesos informados
    root = build_full_tree(I, config)
    
    print("\nDistribuição Inicial:")
    root.display()
    
    folhas = coletar_folhas(root)
    for folha in folhas:
        valor = float(input(f"\nQuanto você realmente investiu em {folha.nome} (Recomendado: R$ {folha.recomendado:.2f})? ") or 0)
        folha.investido = valor
        folha.update_upwards()  # Propaga a atualização para os nós pais e ajusta os orçamentos dos irmãos
        print("\nDistribuição Atualizada:")
        root.display()
    
    print(f"\nDistribuição finalizada. Investimento Total Investido: R$ {root.investido:.2f}")


if __name__ == "__main__":
    I = float(input("Digite o valor do investimento: R$ "))
    
    # Carrega a configuração de investimentos a partir de um arquivo JSON
    with open("investment_config.json", "r", encoding="utf-8") as f:
        investment_config = json.load(f)
    
    calcular_investimento(I, investment_config)
