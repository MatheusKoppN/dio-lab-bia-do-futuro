# Base de Conhecimento

## Dados Utilizados

O Kofin combina os dados estruturados originais fornecidos pelo repositório base com uma base textual educativa personalizada em Markdown e consulta externa via API.

| Arquivo / Fonte | Formato | Utilização no Agente |
|---|---|---|
| `infos_ed_financeira.md` | Markdown (`.md`) | Fornece as diretrizes do Método 50/30/20, passos da Reserva de Emergência e o Mini Glossário Financeiro |
| `historico_atendimento.csv` | CSV | Utilizado para entender o histórico de dúvidas e interações anteriores do usuário |
| `perfil_investidor.json` | JSON | Utilizado para identificar o nível de conhecimento prévio e momento financeiro do usuário |
| `produtos_financeiros.json` | JSON | Utilizado como referência de opções de renda fixa de baixa complexidade (ex: CDB 100% CDI, Tesouro Selic) |
| `transacoes.csv` | CSV | Utilizado para categorizar despesas e identificar oportunidades de corte de gastos |
| API do Banco Central | JSON (Via API REST) | Consulta em tempo real do valor da Taxa Selic para informar o rendimento atual da reserva |

---

## Adaptações nos Dados

Os dados originais do repositório foram expandidos com a inclusão do arquivo `infos_ed_financeira.md`. Esse arquivo introduziu:
1. O detalhamento didático do Método 50/30/20 adaptado para iniciantes.
2. O passo a passo simples para criação de reserva de emergência sem jargões complexos.
3. Um mini glossário financeiro traduzindo termos como Selic, CDI, Liquidez Diária e Juros Compostos.
4. Integração dinâmica com a API de Dados Abertos do Banco Central para obter o valor da taxa Selic no momento da conversa.

---

## Estratégia de Integração

### Como os dados são carregados?
Os arquivos estáticos (`.md`, `.json` e `.csv`) localizados na pasta `data/` são lidos na inicialização da aplicação em Streamlit. Paralelamente, uma função faz uma requisição HTTP para a API do Banco Central para capturar a taxa Selic atualizada.

### Como os dados são usados no prompt?
O conteúdo do arquivo `infos_ed_financeira.md` e o valor retornado da Taxa Selic são injetados diretamente no **System Prompt** (*Grounding* de Contexto). Os dados do usuário (`transacoes.csv` e `perfil_investidor.json`) são inseridos dinamicamente como contexto da mensagem para que o Kofin consiga personalizar as orientações de gastos sem violar as diretrizes de segurança.

---

## Exemplo de Contexto Montado

```text
[CONTEXTO DO SISTEMA - BASE DE CONHECIMENTO]
- Método Orçamentário: 50% Necessidades, 30% Desejos Pessoais, 20% Reserva/Objetivos.
- Reserva de Emergência: Meta de 3 a 6 meses do custo de vida essencial em opções com liquidez diária.
- Taxa Selic Atualizada (Banco Central): 10,50% a.a.

[DADOS DO USUÁRIO]
- Nome: Lucas
- Perfil: Iniciante na organização financeira
- Renda Mensal Declarada: R$ 3.000,00

[RESUMO DE TRANSAÇÕES DO MÊS]
- Necessidades Essenciais (Aluguel, Mercado, Contas): R$ 1.800,00 (60% da renda)
- Lazer e Desejos (Restaurantes, Streaming): R$ 900,00 (30% da renda)
- Guardado / Investido: R$ 300,00 (10% da renda)

[INSTRUÇÃO AO AGENTE]
Analise a divisão atual do Lucas e explique de forma despojada e empática como ele pode se aproximar do método 50/30/20, sugerindo um pequeno ajuste nas despesas.
