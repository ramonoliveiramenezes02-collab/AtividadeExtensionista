
df['CARGO'] = df['CARGO'].str.replace('"', '').str.strip()

# Extrai os cargos únicos e ordena em ordem alfabética
cargos_unicos = sorted(df['CARGO'].dropna().unique())

# Salva essa lista em um arquivo de texto (.txt)
with open('cargos_unicos.txt', 'w', encoding='utf-8') as f:
    for cargo in cargos_unicos:
        f.write(f"{cargo}\n")

print(f"Sucesso! Foram encontrados {len(cargos_unicos)} cargos diferentes.")
