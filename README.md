# 📦 SmartStock

## Sistema Inteligente de Gestão de Almoxarifado

O **SmartStock** é um projeto autoral de um sistema de gestão inteligente de almoxarifado, concebido para integrar **controle operacional de estoque, inventário físico, rastreabilidade de materiais e análise de dados para apoio à decisão**.

O projeto nasceu a partir da observação de desafios comuns em operações reais de almoxarifado, como divergências de inventário, dificuldade de rastrear materiais, excesso de estoque, compras tardias e capital imobilizado.

> 🚧 **Este repositório apresenta o MVP (Minimum Viable Product) do SmartStock.**
>
> A versão atualmente implementada concentra-se na camada analítica do sistema, demonstrando como os dados de estoque podem ser transformados em indicadores e recomendações gerenciais.
>
> A visão completa do SmartStock é significativamente maior e prevê módulos operacionais de inventário por QR Code, movimentação de materiais, controle de materiais em campo, devoluções, conciliação de inventário e inteligência de reposição.

---

# 🚀 MVP Atual

A primeira versão funcional do SmartStock foi desenvolvida para validar uma das principais propostas do projeto:

**transformar dados operacionais de estoque em informações úteis para tomada de decisão.**

O MVP utiliza uma base fictícia de materiais e aplica regras de negócio para analisar:

- valor financeiro do estoque;
- necessidade de reposição;
- cobertura de estoque;
- consumo médio;
- lead time;
- Curva ABC;
- concentração de capital por categoria;
- possível excesso de estoque;
- capital potencialmente imobilizado.

---

## 📊 Demonstração do MVP

### Visão Geral

![Visão geral do SmartStock](assets/smartstock-cabecalho.png)

O painel apresenta uma visão executiva da situação do estoque, incluindo:

- valor total armazenado;
- quantidade de materiais cadastrados;
- materiais que necessitam de reposição;
- itens com baixa cobertura.

---

### 💰 Valor do Estoque por Categoria

![Valor do estoque por categoria](assets/smartstock-valor-categoria.png)

A análise permite identificar em quais categorias está concentrado o capital investido em estoque, auxiliando na identificação de grupos com maior impacto financeiro.

---

### 📊 Curva ABC

![Curva ABC do estoque](assets/smartstock-curva-abc.png)

Os materiais são classificados de acordo com sua participação no valor total do estoque:

- **Classe A:** itens que concentram aproximadamente 80% do valor;
- **Classe B:** faixa seguinte até aproximadamente 95%;
- **Classe C:** parcela restante.

A classificação ajuda a direcionar maior atenção aos materiais com maior impacto financeiro.

---

### 🛒 Central de Recomendações

![Central de recomendações](assets/smartstock-recomendacoes.png)

O SmartStock não se limita à apresentação de gráficos.

O MVP aplica regras de negócio para identificar materiais que podem necessitar de reposição.

O ponto de reposição considera:

- consumo médio;
- lead time;
- estoque de segurança.

A regra utilizada nesta versão é:

```text
Ponto de Reposição =
(Consumo Médio Diário × Lead Time)
+ Estoque de Segurança
```

Quando o estoque atual atinge ou fica abaixo do ponto de reposição, o material é sinalizado para análise de compra.

---

### 💤 Análise de Excesso de Estoque

![Análise de excesso de estoque](assets/smartstock-excesso.png)

O sistema também identifica materiais cuja cobertura está muito acima da necessidade estimada.

No MVP, materiais com cobertura superior a **180 dias** são sinalizados para análise gerencial.

Essa análise pode auxiliar na identificação de:

- excesso de estoque;
- baixa movimentação;
- compras acima da necessidade;
- capital imobilizado.

---

# 🔭 Visão Completa do SmartStock

O dashboard representa apenas a **primeira etapa funcional** do projeto.

A visão completa do SmartStock é a construção de uma plataforma capaz de acompanhar o ciclo do material desde sua entrada no almoxarifado até seu consumo, devolução ou ajuste de inventário.

A arquitetura planejada é dividida em módulos.

---

## 📱 1. Inventário Físico por QR Code

Uma das principais funcionalidades projetadas para o SmartStock é o **inventário por QR Code**.

Cada material poderá possuir um QR Code associado a um identificador único.

Durante o inventário, o operador poderá escanear o código para recuperar automaticamente os dados do material:

```text
QR CODE → MAT-0047

Material: Cabo Flexível 2,5 mm
Localização esperada: Prateleira B-04

Estoque oficial: 120
Quantidade contada: 116

Divergência: -4
```

O operador informa apenas a quantidade encontrada fisicamente, reduzindo a necessidade de digitação e facilitando o processo de contagem.

Caso o QR Code esteja danificado, a arquitetura prevê busca manual pelo código ou descrição do material.

---

## 🔄 2. Base Transitória de Inventário

Uma decisão importante do projeto é que **uma contagem física não deve alterar automaticamente o estoque oficial**.

As contagens serão registradas inicialmente em uma base transitória:

```text
ESTOQUE OFICIAL
120 unidades
      ↓
INVENTÁRIO POR QR CODE
116 unidades
      ↓
BASE TRANSITÓRIA
Divergência: -4
      ↓
ANÁLISE
      ↓
Aprovar | Recontar | Rejeitar
      ↓
AJUSTE DO ESTOQUE OFICIAL
```

Essa abordagem permite investigar divergências antes de alterar os registros oficiais.

O responsável poderá:

- aprovar o ajuste;
- solicitar nova contagem;
- rejeitar a divergência;
- registrar uma justificativa.

Somente após aprovação o sistema deverá gerar uma movimentação de ajuste no estoque oficial, preservando a rastreabilidade da operação.

---

## 🚚 3. Materiais em Campo

Outro módulo planejado trata dos materiais retirados do almoxarifado para execução de serviços.

O objetivo é evitar que todo material retirado seja automaticamente interpretado como consumo definitivo.

Exemplo:

```text
Material retirado para serviço
30 metros de cabo

          ↓

Material efetivamente utilizado
22 metros

          ↓

Material devolvido
8 metros
```

O SmartStock poderá registrar:

- material retirado;
- responsável pela retirada;
- ordem de serviço;
- quantidade enviada;
- quantidade consumida;
- quantidade devolvida;
- materiais pendentes de devolução.

Isso permitirá acompanhar materiais que fisicamente não estão mais no almoxarifado, mas ainda não foram efetivamente consumidos.

---

## 📦 4. Movimentações de Estoque

A evolução do projeto prevê o controle das principais operações:

```text
ENTRADA
   ↓
ESTOQUE
   ↓
SAÍDA
   ↓
CAMPO / CONSUMO
   ↓
DEVOLUÇÃO
```

Além de:

- transferências;
- ajustes;
- inventários;
- perdas;
- devoluções;
- histórico de movimentações.

---

## 🧠 5. Inteligência de Reposição

A camada analítica demonstrada no MVP deverá ser integrada aos módulos operacionais.

A proposta é que o SmartStock utilize o histórico real de movimentações para auxiliar na definição de:

- consumo médio;
- cobertura;
- estoque de segurança;
- ponto de reposição;
- momento recomendado para compra;
- quantidade sugerida;
- comportamento da demanda.

Em etapas futuras, poderão ser incorporados modelos estatísticos e técnicas de previsão de demanda.

---

## 🏭 6. Análise de Fornecedores

A arquitetura também prevê acompanhamento de fornecedores, incluindo indicadores como:

- lead time médio;
- atrasos;
- frequência de fornecimento;
- materiais fornecidos;
- histórico de entregas.

Essas informações poderão alimentar as recomendações de reposição.

---

# 🧩 Fluxo Conceitual do Sistema

A visão futura do SmartStock pode ser resumida da seguinte forma:

```text
                    SMARTSTOCK
                         │
        ┌────────────────┼────────────────┐
        │                │                │
   OPERAÇÕES         INVENTÁRIO       INTELIGÊNCIA
        │                │                │
    Entradas          QR Code          Curva ABC
    Saídas            Contagem         Cobertura
    Devoluções        Divergências     Reposição
    Materiais         Aprovação        Excesso
    em campo                           Indicadores
        │                │                │
        └────────────────┼────────────────┘
                         │
                  ESTOQUE OFICIAL
                         │
                         ▼
                 APOIO À DECISÃO
```

---

# 🎯 Problema que o Projeto Busca Resolver

Operações de almoxarifado podem enfrentar problemas como:

- baixa confiabilidade das quantidades registradas;
- inventários demorados;
- divergências entre estoque físico e sistema;
- dificuldade de rastrear materiais retirados;
- materiais sem devolução;
- compras realizadas tarde demais;
- excesso de materiais;
- capital imobilizado;
- pouca visibilidade sobre consumo;
- ausência de indicadores para decisão.

O SmartStock busca integrar **operação + controle + análise de dados** em uma única solução.

---

# 🛠️ Tecnologias do MVP

- **Python** — desenvolvimento e regras de negócio;
- **Pandas** — tratamento e análise dos dados;
- **NumPy** — geração e manipulação dos dados;
- **Streamlit** — interface da aplicação;
- **Plotly** — visualizações interativas;
- **Git** — controle de versão;
- **GitHub** — versionamento e documentação.

### Tecnologias consideradas para evolução

A arquitetura futura poderá incorporar:

- FastAPI;
- PostgreSQL;
- SQLAlchemy;
- API REST;
- autenticação e controle de usuários;
- bibliotecas para geração e leitura de QR Code;
- modelos estatísticos e de previsão.

---

# 🗂️ Estrutura Atual

```text
smartstock/
│
├── assets/
│   ├── smartstock-cabecalho.png
│   ├── smartstock-valor-categoria.png
│   ├── smartstock-curva-abc.png
│   ├── smartstock-recomendacoes.png
│   ├── smartstock-excesso.png
│   └── smartstock-sobre-projeto.png
│
├── database/
│   ├── gerar_dados.py
│   └── materiais.csv
│
├── docs/
│   └── visao-do-projeto.md
│
├── frontend/
│   └── app.py
│
├── .gitignore
├── README.md
└── requirements.txt
```

---

# 🧪 Dados

Todos os dados utilizados no MVP são **fictícios e gerados programaticamente**.

A base simula um ambiente de almoxarifado contendo:

- materiais;
- categorias;
- estoque atual;
- custos;
- consumo médio;
- lead time.

Nenhuma informação confidencial ou dado pertencente a empresas reais é utilizado.

---

# 🗺️ Roadmap

### ✅ MVP — Análise de Estoque

- [x] geração de base fictícia;
- [x] dashboard executivo;
- [x] valor total de estoque;
- [x] análise por categoria;
- [x] cobertura de estoque;
- [x] ponto de reposição;
- [x] Central de Recomendações;
- [x] Curva ABC;
- [x] identificação de possível excesso de estoque.

### 🔜 Evolução Operacional

- [ ] cadastro estruturado de materiais e fornecedores;
- [ ] banco de dados relacional;
- [ ] entradas e saídas;
- [ ] histórico de movimentações;
- [ ] inventário por QR Code;
- [ ] base transitória de inventário;
- [ ] conciliação de divergências;
- [ ] aprovação de ajustes;
- [ ] materiais em campo;
- [ ] controle de devoluções.

### 🔮 Inteligência

- [ ] análise histórica de consumo;
- [ ] desempenho de fornecedores;
- [ ] previsão de demanda;
- [ ] recomendações avançadas de compra;
- [ ] alertas automáticos;
- [ ] API para integração com outros sistemas.

---

# 👩‍💻 Sobre o Projeto

![Sobre o SmartStock](assets/smartstock-sobre-projeto.png)

O SmartStock faz parte do meu portfólio profissional e foi concebido para integrar conhecimentos de:

- análise de sistemas;
- análise de dados;
- Python;
- indicadores de negócio;
- gestão de estoque;
- modelagem de regras de negócio;
- visualização de dados;
- banco de dados;
- versionamento de software.

A estratégia de desenvolvimento adotada foi iniciar por um **MVP funcional**, validando primeiro a camada analítica e as principais regras de negócio.

A partir dessa base, o projeto poderá evoluir incrementalmente para um sistema completo de **controle, rastreabilidade e inteligência aplicada à gestão de almoxarifado**.