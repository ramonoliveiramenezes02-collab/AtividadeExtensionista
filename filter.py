import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns


df = pd.read_csv('servidoresABR2026.csv', sep=';')
df.columns = df.columns.str.replace('"', '').str.strip()
df['CARGO'] = df['CARGO'].str.replace('"', '').str.strip()

condicoes = [
    # 1. SAÚDE 
    df['CARGO'].str.contains('MÉDIC|MEDIC|ENFERM|SAÚDE|SAUDE|SEMUS|ACS|ENDEMIAS|ANESTESIOLOGISTA|BUCO|DENTISTA|ODONT|FARMAC|BIOQUIM|BIÓLOGO|BIOLOGO|LABORATORIO|PATOLOGIA|FONOAUDIÓLOGO|FONOAUDIOLOGO|FISIOTERAPEUTA|TERAPEUTA|NUTRICIONISTA|AMBULANCIA|ANIMAIS|HMI|HMII|HOSPITALAR|SAMU|PARTEIRA|PSICÓLOGO|PSICOLOGO|VIG SANITARIA|INSPETOR SANITARIO|ORTOPEDICA|RADIOLOGISTA|RADIOLOGIA', case=False, na=False),
    
    # 2. EDUCAÇÃO (Professores, diretores de escola, pedagogos, merendeiras, etc.)
    df['CARGO'].str.contains('PROF|MAGISTÉRIO|MAGISTERIO|SEMED|PEDAGOG|ESCOLA|CRECHE|MERENDA|CME|AUX.*SERV.*MANUT.*ALIM|TECN.*DA.*EDUCAÇÃO', case=False, na=False),
    
    # 3. SEGURANÇA E DEFESA (Guarda municipal, salva-vidas, vigilância comunitária)
    df['CARGO'].str.contains('GUARDA|VIGIL|DEFESA CIVIL|GUARD-VIDA|VIDEOMONITORAMENTO|SEG INTERNO', case=False, na=False),
    
    # 4. INFRAESTRUTURA, TRÂNSITO E SERVIÇOS URBANOS (Gari, motoristas, engenharia, zeladoria)
    df['CARGO'].str.contains('GARI|ZELADOR|VIGIA|PORTEIRO|MOTORISTA|SETRAN|TRANSITO|TRÂNSITO|TRANSP|INFRA-ESTRUT|PEDREIRO|PINTOR|SERRALHEIRO|ELETRICISTA|ELETROTÉCNICA|ENGENH|ARQUITETO|URBANISTA|EDIFICAÇÕES|EDIFICACOES|LIMPEZA PUBLICA|ABATEDOURO|MATADOURO|MAGAREFE|FUNERÁRIO|FUNERARIO|VAQUEIRO|POCOS|AGUA|SANEAMENTO', case=False, na=False),
    
    # 5. ASSISTÊNCIA SOCIAL E CIDADANIA (CRAS, CREAS, Procon, Conselhos)
    df['CARGO'].str.contains('SOCIAL|CADÚNICO|CADUNICO|SEDES|PROCON|CONSELHEIRO TUTELAR|SUAS|MULHER VIT', case=False, na=False),
    
    # 6. FISCALIZAÇÃO, JURÍDICO E ARRECADACAO (Foco nas receitas e leis municipais)
    df['CARGO'].str.contains('FISCAL|RECEITA|TRIBUT|ARRECAD|PROCURADOR|ADV|ADVOGADO|AUDITOR|PGM|CONTABIL|CONTADOR|LICITA|PREGOEIRO|CPL|REGISTRO DE PRECO', case=False, na=False),
    
    # 7. ALTA GESTÃO E POLÍTICA (Prefeito, Secretários municipais e gabinetes)
    df['CARGO'].str.contains('PREFEITO|SECRETARIO|SECRETÁRIO|GABINETE|SUPERINTEND|CERIMONIAL|ASSUNTO.*POLÍTICO|OUVIDOR', case=False, na=False),
    
    # 8. ADMINISTRAÇÃO GERAL E APOIO (A máquina administrativa de escritório)
    df['CARGO'].str.contains('ADM|ADMINISTRATIVO|RECURSOS HUMANOS|FINANCAS|FINANÇAS|TESOURO|CONTROLE INTERNO|DIVISÃO|DIVISAO|NUCLEO|NÚCLEO|SETOR|DEPARTAMENTO|DEPTO|CH DE DIV|LOGÍSTICA|LOGISTICA|COMPRA|ALMOX|CONTRATO|ATENDIMENTO|PROTOCOLO|ENCARREGADO|TELEFONISTA|DIGITADOR|PROGRAMADOR|INFORMATICA|INFORMÁTICA|COMPUTADOR|TECNOLOGIA|COMUNICAÇÃO|COMUNICACAO|ESTRATEGIC|PROJETOS|EVENTOS|LAZER|CULTURA|ESPORTE|INSTRUTOR|INTERPRETE|LIBRAS|BRAILE|COZINHA|COZINHEIR|COSTUREIR|BALANCEIRO|BRACAL|BRAÇAL|SERVICOS GERAIS', case=False, na=False)
]
areas = [
    'SAÚDE', 
    'EDUCAÇÃO', 
    'SEGURANÇA', 
    'INFRAESTRUTURA E URBANO', 
    'ASSISTÊNCIA SOCIAL', 
    'FISCALIZAÇÃO E JURÍDICO', 
    'ALTA GESTÃO E POLÍTICA',
    'ADMINISTRAÇÃO E APOIO'
]

#  "OUTROS"
df['AREA'] = np.select(condicoes, areas, default='OUTROS')

print(df[['CARGO', 'AREA']].drop_duplicates().head(20))

df['BRUTO_LIMPO'] = df['BRUTO'].astype(str)

df['BRUTO_LIMPO'] = df['BRUTO_LIMPO'].str.replace('.', '', regex=False).str.replace(',', '.', regex=False)

df['BRUTO_NUMERICO'] = pd.to_numeric(df['BRUTO_LIMPO'], errors='coerce')

# Agrupa por ÁREA
resumo_gastos = df.groupby('AREA')['BRUTO_NUMERICO'].sum().reset_index()

resumo_gastos.columns = ['Área', 'Gasto Total Acumulado (R$)']

# ORDER
resumo_gastos = resumo_gastos.sort_values(by='Gasto Total Acumulado (R$)', ascending=False)

# RESULTADO FORMATADO
print("\n--- RESUMO DE GASTOS POR ÁREA (IMPERATRIZ/MA) ---")
for index, linha in resumo_gastos.iterrows():
    valor_formatado = f"R$ {linha['Gasto Total Acumulado (R$)']:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    print(f"{linha['Área']}: {valor_formatado}")






sns.set_theme(style="whitegrid")
plt.figure(figsize=(13, 7))

# CRIA O GRAFICO
barplot = sns.barplot(
    data=resumo_gastos, 
    x=resumo_gastos['Gasto Total Acumulado (R$)'] / 1_000_000, 
    y='Área', 
    palette='viridis'
)

for i in range(len(resumo_gastos)):
    valor_milhoes = resumo_gastos['Gasto Total Acumulado (R$)'].iloc[i] / 1_000_000
    plt.text(
        x=valor_milhoes + 0.2, 
        y=i, 
        s=f"R$ {valor_milhoes:.2f}M", 
        va='center', 
        fontsize=10, 
        fontweight='bold',
        color='#333333'
    )

plt.title('Gasto Total com Pessoal por Área (04/26) - Imperatriz/MA\n(Valores brutos acumulados em Milhões de R$)', fontsize=14, fontweight='bold', pad=20)
plt.xlabel('Valores em Milhões (R$)', fontsize=12, labelpad=10)
plt.ylabel('Áreas Mapeadas', fontsize=12)

# LIM
max_valor = (resumo_gastos['Gasto Total Acumulado (R$)'].max() / 1_000_000)
plt.xlim(0, max_valor * 1.15)

plt.tight_layout()

nome_imagem = 'grafico_gastos_por_area_imperatriz.png'
plt.savefig(nome_imagem, dpi=300)
print(f"\nGráfico gerado com sucesso e salvo como '{nome_imagem}'!")

plt.show()