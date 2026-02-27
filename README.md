# Quake Parser

## Como usar

### 1. Usando online (Render)

1. **Acorde a API:**
   - Acesse: https://quake-parser.onrender.com/
   - Aguarde a mensagem de boas-vindas (isso "acorda" o servidor Render).
2. **Acesse o dashboard:**
   - Acesse: https://quake-parser-dashboard.onrender.com/
   - O dashboard irá consumir os dados da API automaticamente.

### 2. Executando localmente

1. Clone o repositório:
   ```bash
   git clone https://github.com/Helmelhor/quake_parser.git
   cd quake_parser
   ```
2. Crie um ambiente virtual:
   ```bash
   python -m venv env
   # No Windows:
   env\Scripts\activate
   # No Linux/Mac:
   source env/bin/activate
   ```
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
4. Execute o dashboard Streamlit:
   ```bash
   python -m streamlit run dash.py
   ```
   (Execute este comando na pasta raiz do projeto)

> **Importante:**
> Para o dashboard funcionar localmente, o servidor da API hospedado no Render deve estar "acordado" (acesse https://quake-parser.onrender.com/ antes de abrir o dashboard).

---

- Projeto desenvolvido para análise e visualização de logs de partidas do Quake 3 Arena.
- API construída com FastAPI, dashboard com Streamlit e gráficos interativos com Plotly.

