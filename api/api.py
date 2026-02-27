from fastapi import FastAPI, HTTPException
from parser import QuakeLogParser
import os

app = FastAPI(title="Quake Parser API")

# Caminho do arquivo de log (ajuste se necessário)
LOG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'games.log')

# Instancia e processa o parser ao iniciar a API
parser = QuakeLogParser(LOG_PATH)
parser.parse()

@app.get("/games/ranking")
def ranking():
    """Retorna o ranking geral de kills por jogador."""
    ranking_dict = {}
    
    # Acumula kills de todos os jogos
    for game in parser.games:
        # Inclui todos os players do jogo, mesmo os com 0 kills
        for player in game.players:
            ranking_dict[player] = ranking_dict.get(player, 0) + game.kills.get(player, 0)
    
    # Ordena por kills decrescentes
    ranking_ordenado = sorted(ranking_dict.items(), key=lambda x: x[1], reverse=True)
    
    # Retorna como lista de dicts com posição, player e kills
    return [
        {"posicao": pos, "player": player, "kills": kills}
        for pos, (player, kills) in enumerate(ranking_ordenado, 1)
    ]

@app.get("/games/{game_id}")
def get_game(game_id: int):
    if game_id < 1 or game_id > len(parser.games):
        raise HTTPException(status_code=404, detail="Jogo não encontrado")
    game = parser.games[game_id - 1]
    return game.gerar_dict()

@app.get("/games")
def list_games():
    return [game.gerar_dict() for game in parser.games]

@app.get("/")
def root():
    return {"msg": "API Quake Parser. Use /games ou /games/{id}"}
