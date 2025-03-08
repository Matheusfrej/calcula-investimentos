import json

COLORS = {
    "green": "\033[92m",
    "blue": "\033[94m",
    "yellow": "\033[93m",
    "cyan": "\033[96m",
    "magenta": "\033[95m",
    "red": "\033[91m",
    "reset": "\033[0m"
}

# Classe que representa cada nó (objeto de investimento) na árvore
class Node:
    def __init__(self, nome, recomendado=0, investido=0) -> None:
        self.nome = nome
        self.orig_recomendado = recomendado  # Valor recomendado original (fixo)
        self.recomendado = recomendado       # Valor recomendado atual (ajustável)
        self.investido = investido
        self.children = []
        self.parent = None

    def add_child(self, child) -> None:
        child.parent = self
        self.children.append(child)

    def update_upwards(self) -> None:
        """Atualiza recursivamente o valor investido e redistribui os orçamentos dos nós pais."""
        if self.parent:
            self.parent.investido = sum(child.investido for child in self.parent.children)
            self.parent.update_children_recommended()
            self.parent.update_upwards()

    def update_children_recommended(self) -> None:
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

    def display(self, indent=0) -> None:
        espaco = " " * indent
        print(f"{espaco}{COLORS['green']}{self.nome}{COLORS['reset']}: Investido {COLORS['blue']}R$ {self.investido:.2f}{COLORS['reset']} (Recomendado: {COLORS['yellow']}R$ {self.recomendado:.2f}{COLORS['reset']})")
        for child in self.children:
            child.display(indent + 2)


def build_tree_from_config(name, conf, total_value) -> Node:
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


def build_full_tree(total, config) -> Node:
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
            peso = float(input(f"Digite a porcentagem (peso) para {COLORS['cyan']}{key}{COLORS['reset']} (Pressione 'ENTER' para padrão: {conf['weight']}): ") or conf["weight"])
            weights[key] = peso
            total_weight += peso
            current_item += 1
    total_weight = sum(weights.values())
    for key, conf in items:
        prop = weights[key] / total_weight
        child_node = build_tree_from_config(key, conf, total * prop)
        root.add_child(child_node)
    return root


def coletar_folhas(node) -> list[Node]:
    folhas = []
    def _coletar(n) -> None:
        if not n.children:
            folhas.append(n)
        else:
            for child in n.children:
                _coletar(child)
    _coletar(node)
    return folhas


def calcular_investimento(I, config) -> None:
    # Constrói a árvore de investimentos a partir da configuração e dos pesos informados
    root = build_full_tree(I, config)
    
    print(f"\n{COLORS['magenta']}Distribuição Inicial:{COLORS['reset']}")
    root.display()
    
    folhas = coletar_folhas(root)
    index = 0
    acabou = False
    while not acabou:
        while index < len(folhas):
            folha = folhas[index]
            print(f"\n{COLORS['blue']}Digite \"VOLTAR\" para corrigir valor anterior{COLORS['reset']}") if (index > 0) else print()
            entrada = input(f"Quanto você realmente investiu em {COLORS['cyan']}{folha.nome}{COLORS['reset']} (Recomendado: {COLORS['yellow']}R$ {folha.recomendado:.2f}{COLORS['reset']})?: ")
            
            if entrada.upper() == "VOLTAR" and index > 0:
                print(f'\n{COLORS["magenta"]} Voltando... {COLORS["reset"]}')
                index -= 1
                continue
            try:
                valor = float(entrada)
                folha.investido = valor
                folha.update_upwards()
                print(f"\n{COLORS['magenta']}Distribuição Atualizada:{COLORS['reset']}")
                root.display()
                index += 1
            except ValueError:
                error_output = "\nEntrada inválida! Digite um valor numérico."
                if index == 1:
                    error_output = error_output.replace('.', ' ou \'VOLTAR\' para corrigir a entrada anterior.') 
                print(f"{COLORS['red']}{error_output}{COLORS['reset']}")
        last_chance = input(f"\n{COLORS['blue']}Digite \"VOLTAR\" para corrigir valor anterior{COLORS['reset']} ou pressione 'ENTER' para finalizar: ")
        if last_chance.upper() == 'VOLTAR':
            print(f'\n{COLORS["magenta"]} Voltando... {COLORS["reset"]}')
            index -= 1
        else:
            acabou = True
    
    print(f"\n{COLORS['green']}Distribuição finalizada.{COLORS['reset']}")
    print(f"Valor Planejado: {COLORS['blue']}R$ {root.recomendado:.2f}{COLORS['reset']}.")
    print(f"Valor Investido: {COLORS['blue']}R$ {root.investido:.2f}{COLORS['reset']}.")


if __name__ == "__main__":
    try:
        with open("investment_config.json", "r", encoding="utf-8") as f:
            investment_config = json.load(f)
    except FileNotFoundError:
        input(f"{COLORS['red']}Erro: O arquivo 'investment_config.json' não foi encontrado. Pressione 'ENTER' para fechar.{COLORS['reset']}")
        exit(1)
    
    while True:
        try:
            I = float(input("Digite o valor do investimento: R$ "))
            calcular_investimento(I, investment_config)
        except ValueError:
            print(f"{COLORS['red']}Valor inválido. Digite um número válido.{COLORS['reset']}")
            continue
        
        repeat = input("Pressione 'ENTER' para sair ou digite qualquer tecla para calcular novamente: ")
        if repeat == "":
            break
