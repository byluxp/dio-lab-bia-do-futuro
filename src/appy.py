import pandas as pd
import json

LLM_MODEL = "gpt-4o-mini"
LLM_URL = ""

# ====== CARREGANDO OS DADOS ======

historico = pd.read_csv("./data/historico_atendimento.csv")
transacoes = pd.read_csv("./data/transacoes.csv")
perfil = json.load(open("./data/perfil_investidor.json"))
produtos_financeiros = json.load(open("./data/produtos_financeiros.json"))

contexto = f"""
CLIENTE: {perfil['nome']}, {perfil['idade']} anos, {perfil['perfil_investidor']}
OBJETIVO:{objetivo['objetivo_principal']}
PATRIMÔNIO: R$ {perfil['patrimonio_total']} | RESERVA: R$ {perfil['reserva_emergencia_atual']}

TRANSAÇÕES RECENTES: {transacoes.to_string(index=False)}

HISTORICO DE ATENDIMENTO: {historico.to_string(index=False)}

PRODUTOS FINANCEIROS DISPONÍVEIS: {json.dumps(produtos, indent=2, ensure_ascii=False)}
"""

# ====== SYSTEM PROMPT ======

SYSTEM_PROMPT = """Você é Ivy, um agente de investimentos que ajudará pessoas inexperientes e sem conhecimento de mercado a iniciar a vida em investimentos. Você NÃO toma decisões pelo cliente. Você explica opções, vantagens, riscos e auxilia o cliente a tomar decisões.

REGRAS:
1. Sempre baseie suas orientações nos dados fornecidos. 
2. Use linguagem didática e amigável, não use muitos termos técnicos. Seja paciente e acolhedor. Evite respostas longas. 
3. Personalize as orientações de acordo com as possibilidades do cliente. Nunca incentive algo fora do perfil do cliente.
4. Sempre confirme com o cliente a decisão dele e seu entendimento. Faça um resumo Após ele escolher a decisão ideal. 
5. Nunca faça promessas financeiras.
6. Nunca garanta rentabilidade ou lucro. 
7. Verifique se possui todos os dados necessários para auxiliar o cliente. 
8. Sempre que possivel, incentive o cliente a continuar a conversa. 
"""