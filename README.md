# Calcula Investimentos

Este programa ajuda a distribuir automaticamente um montante de investimento entre diferentes classes de ativos com base em um arquivo de configuração [JSON](https://pt.wikipedia.org/wiki/JSON). O usuário pode informar quanto realmente investiu em cada ativo, e o programa ajusta a distribuição dos valores recomendados para manter o total investido dentro do orçamento.

## Como Usar

### 1. Criar o Arquivo de Configuração (JSON)

Antes de executar o programa, você deve criar um arquivo JSON contendo a estrutura de investimentos.

Crie um arquivo chamado `investment_config.json` no mesmo diretório do programa e preencha com a estrutura desejada. O arquivo precisa ter esse nome. Abaixo está um exemplo de configuração genérica:

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

### 2. Executar o Programa `.exe`
Se você baixou a pasta do programa, o executável `.exe` já está pronto para uso. Para rodá-lo:

1. Abra a pasta onde baixou o programa.
2. Certifique-se de que o arquivo `investment_config.json` está na mesma pasta que o executável.
3. Dê um duplo clique no arquivo `CalculaInvestimentos.exe` para iniciar o programa.

> **Importante:** O programa será executado no terminal e pedirá que você insira os valores conforme necessário.

---

### 2. Executar com Python (Desenvolvedores ou Usuários Avançados)

Se você tem o Python instalado, pode rodar o programa diretamente. Certifique-se de que tem os arquivos `main.py` e `investment_config.json` na mesma pasta.

#### Comando para rodar o programa:
```sh
python main.py
```

O programa solicitará:
- O valor total do investimento.
- O peso inicial para os campos do JSON mais externos (ex: "Renda Variável" e "Renda Fixa").
- Os valores investidos para cada ativo.

---

### 3. Criar o Executável `.exe` (Para Desenvolvedores)
Caso queira gerar um novo executável para distribuição, siga os passos abaixo.

#### 3.1 Instalar o PyInstaller
Se ainda não tiver o PyInstaller instalado, execute:
```sh
pip install pyinstaller
```

#### 3.2 Gerar o Executável
Navegue até a pasta onde está o `main.py` e execute o seguinte comando:
```sh
pyinstaller --onefile --name=CalculaInvestimentos main.py
```

##### Parâmetros explicados:
- `--onefile`: Cria um único arquivo `.exe`.
- `--name=CalculaInvestimentos`: Define o nome do executável.

O executável gerado estará na pasta `dist/`, com o nome `CalculaInvestimentos.exe`. Coloque o executável no mesmo diretório de `investment_config.json` para garantir que ele funcione corretamente.

---

### 4. Personalização
- Para adicionar novos ativos, edite o arquivo `investment_config.json`.
- Altere os pesos para ajustar a distribuição recomendada.

---

Este programa facilita a gestão de investimentos, ajustando automaticamente os valores conforme os aportes realizados pelo usuário. Se tiver dúvidas, consulte o código ou entre em contato! 🚀

