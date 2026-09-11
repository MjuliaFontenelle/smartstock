import pandas as pd
import numpy as np
from pathlib import Path

# Para gerar sempre os mesmos dados fictícios
np.random.seed(42)

# Quantidade de materiais que existirão no nosso almoxarifado fictício
QUANTIDADE_MATERIAIS = 100

# Descobre automaticamente a pasta database
PASTA_DATABASE = Path(__file__).resolve().parent

# Categorias fictícias
categorias = [
    "Elétrica",
    "Hidráulica",
    "Ferramentas",
    "EPI",
    "Fixação",
    "Manutenção"
]

# Criação dos materiais
materiais = pd.DataFrame({
    "codigo": [f"MAT-{i:04d}" for i in range(1, QUANTIDADE_MATERIAIS + 1)],

    "descricao": [
        f"Material fictício {i}"
        for i in range(1, QUANTIDADE_MATERIAIS + 1)
    ],

    "categoria": np.random.choice(
        categorias,
        QUANTIDADE_MATERIAIS
    ),

    "estoque_atual": np.random.randint(
        0,
        500,
        QUANTIDADE_MATERIAIS
    ),

    "custo_unitario": np.round(
        np.random.uniform(5, 500, QUANTIDADE_MATERIAIS),
        2
    ),

    "consumo_medio_mensal": np.random.randint(
        5,
        150,
        QUANTIDADE_MATERIAIS
    ),

    "lead_time_dias": np.random.randint(
        5,
        31,
        QUANTIDADE_MATERIAIS
    )
})

# Valor financeiro atualmente armazenado de cada material
materiais["valor_estoque"] = (
    materiais["estoque_atual"] *
    materiais["custo_unitario"]
).round(2)

# Salva a base fictícia em CSV
arquivo_saida = PASTA_DATABASE / "materiais.csv"

materiais.to_csv(
    arquivo_saida,
    index=False,
    encoding="utf-8-sig"
)

print("Base SmartStock criada com sucesso!")
print(f"{len(materiais)} materiais gerados.")
print(f"Arquivo salvo em: {arquivo_saida}")
print()
print(materiais.head())