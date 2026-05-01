import os
from datetime import datetime, timedelta

# Configurações de simulação para o Supermercado Preço Justo
pasta_destino = "recup_tributaria"
meses = 60
data_inicio = datetime(2021, 1, 1)

def gerar_arquivos():
    for i in range(meses):
        data_atual = data_inicio + timedelta(days=30*i)
        competencia = data_atual.strftime("%m%Y")
        nome_mes = data_atual.strftime("%m/%Y")
        
        # 1. Simulação SPED Fiscal (Foco: Exclusão ICMS - Tese do Século)
        conteudo_sped_fiscal = f"""|0000|015|0|01{competencia}|31{competencia}|SUPERMERCADO PRECO JUSTO|00000000000100||RS|0000000|00000||A|1|
|C100|0|1|FORN_GERAL|55|00|1|{1000+i}|01{competencia}|01{competencia}|200000,00|0||0|0|0|200000,00|0|0|0|36000,00|0|0|0|0|
|C190|010|5102|18,00|200000,00|36000,00|0,00|0,00|0,00|0,00|
|9999|4|"""

        # 2. Simulação SPED Contribuições (Foco: Crédito Insumos e Monofásicos)
        conteudo_sped_contrib = f"""|0000|005|0|01{competencia}|31{competencia}|SUPERMERCADO PRECO JUSTO|00000000000100|RS|0000000|00000|00|
|A100|0|1|MANUT_MAQ|01|00|1|{500+i}|01{competencia}|01{competencia}|5000,00|0|0|0|5000,00|0|0|0|0|0|0|0|
|M100|01|0|200000,00|1,65|3300,00|0|0|3300,00|0|0|0|3300,00|
|M500|01|0|200000,00|7,60|15200,00|0|0|15200,00|0|0|0|15200,00|
|9999|5|"""

        # 3. Simulação DCTF Web (Foco: Confronto de Pagamentos)
        conteudo_dctf = f"""DETALHAMENTO DEBITOS {nome_mes}:
PIS (0692): R$ 3.300,00 - PAGO
COFINS (2172): R$ 15.200,00 - PAGO
OBS: Receitas monofásicas (NCM 2203, 2202) não segregadas."""

        # Salvando os arquivos (Simulação de escrita no Drive)
        with open(f"{pasta_destino}/EFD_FISCAL_{competencia}.txt", "w") as f: f.write(conteudo_sped_fiscal)
        with open(f"{pasta_destino}/EFD_CONTRIB_{competencia}.txt", "w") as f: f.write(conteudo_sped_contrib)
        with open(f"{pasta_destino}/DCTF_{competencia}.txt", "w") as f: f.write(conteudo_dctf)

    print(f"Sucesso! 180 arquivos gerados na pasta {pasta_destino}.")

if __name__ == "__main__":
    if not os.path.exists(pasta_destino): os.makedirs(pasta_destino)
    gerar_arquivos()