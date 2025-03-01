# Investimento Automático

Este programa ajuda a distribuir automaticamente um montante de investimento entre diferentes classes de ativos com base em um arquivo de configuração JSON. O usuário pode informar quanto realmente investiu em cada ativo, e o programa ajusta a distribuição dos valores recomendados para manter o total investido dentro do orçamento.

## Como Usar

### 1. Criar o Arquivo de Configuração (JSON)

Antes de executar o programa, você deve criar um arquivo JSON contendo a estrutura de investimentos.

Crie um arquivo chamado `investment_config.json` no mesmo diretório do programa e preencha com a estrutura desejada. Abaixo está um exemplo de configuração genérica:

```json
{
  "Renda Variável": {
    "weight": 0.4,
    "children": {
      "Ações": {
        "weight": 0.5,
        "children": {
          "EMPRESA1": {"weight": 1},
          "EMPRESA2": {"weight": 1}
        }
      },
      "FIIs": {
        "weight": 0.3,
        "children": {
          "FII1": {"weight": 1},
          "FII2": {"weight": 1}
        }
      },
      "ETFs": {
        "weight": 0.2,
        "children": {
          "ETF1": {"weight": 0.7},
          "ETF2": {"weight": 0.3}
        }
      }
    }
  },
  "Renda Fixa": {
    "weight": 0.6,
    "children": {
      "CDB": {"weight": 0.5},
      "LCI": {"weight": 0.5}
    }
  }
}
```

### 2. Executar o Programa

1. Certifique-se de que você tem o Python instalado (versão 3.6 ou superior).
2. No terminal, navegue até a pasta onde está o arquivo `investment_config.json` e o script Python.
3. Execute o script com o comando:
   
   ```sh
   python nome_do_script.py
   ```

4. O programa solicitará:
   - O valor total do investimento.
   - O peso inicial para os campos do JSON mais externos (ex: "Renda Variável" e "Renda Fixa").
   - Os valores investidos para cada ativo.

5. O programa exibirá a distribuição atualizada após cada entrada.

### 3. Exemplo de Uso

#### Entrada do Usuário:
```sh
Digite o valor do investimento: R$ 10000
Digite a porcentagem (peso) para Renda Variável (padrão: 0.4): 0.5
Quanto você realmente investiu em EMPRESA1 (Recomendado: R$ 1250.00)? 1300
Quanto você realmente investiu em EMPRESA2 (Recomendado: R$ 1200.00)? 1100
...
```

#### Saída do Programa:
```
Distribuição Atualizada:
Investimento Total: Investido R$ 2400.00 (Recomendado: R$ 10000.00)
  Renda Variável: Investido R$ 2400.00 (Recomendado: R$ 5000.00)
    Ações: Investido R$ 2400.00 (Recomendado: R$ 2500.00)
      EMPRESA1: Investido R$ 1300.00 (Recomendado: R$ 1250.00)
      EMPRESA2: Investido R$ 1100.00 (Recomendado: R$ 1200.00)
...
```

### 4. Personalização

- Para adicionar novos ativos, edite o arquivo `investment_config.json`.
- Altere os pesos para ajustar a distribuição recomendada.

---

Este programa facilita a gestão de investimentos, ajustando automaticamente os valores conforme os aportes realizados pelo usuário.

