import os
import json
import pandas as pd
from google import genai
from google.genai import types
from dotenv import load_dotenv

# 1. Carrega as variáveis de ambiente definidas no arquivo .env local
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Força o carregamento do arquivo .env localizando-o explicitamente nesta pasta
dotenv_path = os.path.join(BASE_DIR, ".env")
load_dotenv(dotenv_path=dotenv_path)

# Captura a chave do ambiente carregado
api_key = os.environ.get("GEMINI_API_KEY")

# ====== VALIDAÇÃO E CONFIGURAÇÃO DA API GEMINI ======
if not api_key:
    raise ValueError(
        f"Erro: A variável GEMINI_API_KEY não foi encontrada.\n"
        f"Verifique se o arquivo .env está criado em: {BASE_DIR}\n"
        f"E se dentro dele existe a linha: GEMINI_API_KEY=sua_chave"
    )

client = genai.Client(api_key=api_key)
LLM_MODEL = "gemini-2.5-flash"


# ====== CARREGANDO OS DADOS ======

historico = pd.read_csv("./data/historico_atendimento.csv")
transacoes = pd.read_csv("./data/transacoes.csv")
perfil = json.load(open("./data/perfil_investidor.json"))
produtos_financeiros = json.load(open("./data/produtos_financeiros.json"))

contexto = f"""
CLIENTE: {perfil['nome']}, {perfil['idade']} anos, {perfil['perfil_investidor']}
OBJETIVO:{perfil['objetivo_principal']}
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

# ====== FUNÇÃO PARA ENVIAR PERGUNTA À API ======
def gerar_resposta_agente(mensagem_usuario):
    try:
        # Enviando a requisição para a API do Gemini de forma segura
        resposta = client.models.generate_content(
            model=LLM_MODEL,
            contents=mensagem_usuario,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                temperature=0.7,
            ),
        )
        return resposta.text
    except Exception as e:
        return f"Erro ao conectar com a API do Gemini: {e}\nCertifique-se de que a variável GEMINI_API_KEY está configurada corretamente no arquivo .env."

# ====== EXECUÇÃO DE TESTE LOCAL ======
if __name__ == "__main__":
    print("-" * 50)
    print("Iniciando teste do agente local com a API do Gemini...")
    print("-" * 50)
    
    exemplo_pergunta = "Quais opções de investimento combinam mais com o meu perfil atual?"
    print(f"Usuário: {exemplo_pergunta}\n")
    
    print("Ivy processando resposta...")
    resposta_ivy = gerar_resposta_agente(exemplo_pergunta)
    
    print("\nIvy:")
    print(resposta_ivy)
    print("-" * 50)