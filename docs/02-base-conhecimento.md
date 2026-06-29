# Base de Conhecimento

## Dados Utilizados

Descreva se usou os arquivos da pasta `data`, por exemplo:

| Arquivo | Formato | Descrição |
|---------|---------|-----------|
| `transacoes.csv` | CSV | Histórico de transações do cliente para análise |
| `historico_atendimento.csv` | CSV | Histórico das solicitações do cliente |
| `perfil_investidor.json` | JSON | Personaliza a experiência do cliente |
| `produtos_financeiros.json` | JSON | Produtos e serviços disponíveis para investimento |


---

## Adaptações nos Dados

> Você modificou ou expandiu os dados mockados? Descreva aqui.

- Adicionei mais produtos e serviços financeiros para abranger mais perfis. 

---

## Estratégia de Integração

### Como os dados são carregados?
> Descreva como seu agente acessa a base de conhecimento.

``` python 
#código para abrir os arquivos csv e json

import pandas as pd

historico = pd.read_csv("./data/historico_atendimento.csv")
transacoes = pd.read_csv("./data/transacoes.csv")

perfil = pd.read_json("./data/perfil_investidor.json")
produtos_financeiros = pd.read_json("./data/produtos_financeiros.json")

``` 

### Como os dados são usados no prompt?
> Os dados vão no system prompt? São consultados dinamicamente?

Dados são consultados dinamicamente pelo nosso agente. 

```text

DADOS E PERFIL DO CLIENTE:
{perfil_investidor_json}

HISTÓRICO DE TRANSAÇÕES E ATENDIMENTO:
{historico_e_transacoes_texto}

PRODUTOS FINANCEIROS DISPONÍVEIS:
{produtos_financeiros_json}
```

---

## Exemplo de Contexto Montado

> Mostre um exemplo de como os dados são formatados para o agente.

```
Dados do Cliente:
- Nome: João Silva
- Perfil: Moderado
- Saldo disponível: R$ 5.000

Últimas transações:
- 01/11: Supermercado - R$ 450
- 03/11: Streaming - R$ 55

Produtos disponíveis para aplicar: 
- Nome: ETF Global Rebound
- Risco: alto
- Indicado para: Diversificação internacional em empresas de tecnologia
...
```
