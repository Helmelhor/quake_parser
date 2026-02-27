import streamlit as st
import requests
import pandas as pd
import plotly.express as px

class QuakeDashboard:
	
	def __init__(self):
		self.api_url_ranking = "https://quake-parser.onrender.com/ranking"
		self.api_url_games = "https://quake-parser.onrender.com/games"
		self.api_url_game = "https://quake-parser.onrender.com/games/{}"
		self.visualizacao = None
		self.df = None

	def configurar_sidebar(self):
		st.sidebar.title("Opções")
		self.visualizacao = st.sidebar.radio(
			"Selecione a visualização:",
			["Ranking", "Pesquisar Game", "Todos os Games"]
		)

	def carregar_ranking(self):
		resposta = requests.get(self.api_url_ranking)
		if resposta.status_code == 200:
			st.success("Dados carregados com sucesso!")
			ranking = resposta.json()
			self.df = pd.DataFrame(ranking)
			return True
		else:
			st.error("Erro ao obter dados da API")
			return False

	def criar_grafico_barra(self):
		return px.bar(
			self.df.sort_values("kills"),
			x="kills",
			y="player",
			orientation="h",
			title="Ranking de Kills por Jogador",
			labels={"kills": "Kills", "player": "Jogador"}
		)

	def criar_grafico_pizza(self):
		return px.pie(
			self.df,
			names="player",
			values="kills",
			title="Proporção de Kills por Jogador",
			hole=0.3
		)

	def exibir_ranking(self):
		grafico_barra = self.criar_grafico_barra()
		grafico_pizza = self.criar_grafico_pizza()
		st.plotly_chart(grafico_barra)
		st.plotly_chart(grafico_pizza)

	def exibir_pesquisar_game(self):
		st.subheader("Pesquisar Game por ID (1 - 21)")
		game_id = st.number_input("Digite o ID do jogo:", min_value=1, max_value=21, step=1, format="%d")
		if game_id:
			resposta_game = requests.get(self.api_url_game.format(int(game_id)))
			if resposta_game.status_code == 200:
				st.dataframe(resposta_game.json())
			else:
				st.error("Jogo não encontrado!")

	def exibir_todos_games(self):
		st.subheader("Todos os Games")
		resposta_games = requests.get(self.api_url_games)
		if resposta_games.status_code == 200:
			lista_games = resposta_games.json()
			for game in lista_games:
				st.dataframe(game)
		else:
			st.error("Erro ao obter lista de games da API")

	def executar(self):
		st.title("Dashboard de partidas do Quake 3")
		self.configurar_sidebar()

		with st.spinner("Carregando dados e gráficos..."):
			if self.carregar_ranking():
				if self.visualizacao == "Ranking":
					self.exibir_ranking()
				elif self.visualizacao == "Pesquisar Game":
					self.exibir_pesquisar_game()
				else:
					self.exibir_todos_games()


if __name__ == "__main__":
	dashboard = QuakeDashboard()
	dashboard.executar()
    
