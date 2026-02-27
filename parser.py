class Game:
	def __init__(self, game_id):
		self.game_id = game_id
		self.total_kills = 0
		self.players = set()
		self.kills = {}

	def add_kill(self, killer, vitima):
		
		if killer != '<world>':
			self.players.add(killer)
		if vitima != '<world>':
			self.players.add(vitima)

		self.total_kills += 1

		if killer == '<world>':
			self.kills[vitima] = self.kills.get(vitima, 0) - 1
		else:
			self.kills[killer] = self.kills.get(killer, 0) + 1

	def get_players(self):
		return sorted(self.players) #retorna lista de players ordenada

	#gera um dicionário com as informações do jogo
	def gerar_dict(self):
		return {
			f'game_{self.game_id}': {
				'total_kills': self.total_kills,
				'players': self.get_players(),
				'kills': {p: self.kills.get(p, 0) for p in self.get_players()}
			}
		}

class QuakeLogParser:	
	def __init__(self, log_path): 
		self.log_path = log_path
		self.games = []

	def parse(self):
		current_game = None
		game_count = 0
		with open(self.log_path, 'r', encoding='utf-8') as file:
			for line in file:
				line = line.strip()
				# Detecta início de um novo jogo
				if 'InitGame:' in line:
					if current_game is not None:
						self.games.append(current_game)
					game_count += 1
					current_game = Game(game_count)
				# Detecta informações de jogador
				elif 'ClientUserinfoChanged:' in line and current_game is not None:
					player_name = self._extract_player_name(line)
					if player_name:
						current_game.players.add(player_name)
				# Detecta linhas de kill
				elif 'Kill:' in line and current_game is not None:
					self._extract_kill_info(line, current_game)
		if current_game is not None:
			self.games.append(current_game)

	def _extract_player_name(self, line):	
		try:
			info = line.split('ClientUserinfoChanged:')[1].strip()
			# Procura pelo padrão "n\<name>\t"
			if 'n\\' in info:
				# Extrai a parte após "n\"
				name_part = info.split('n\\')[1]
				# Pega tudo até o próximo backslash
				player_name = name_part.split('\\')[0]
				return player_name if player_name else None	
		except (IndexError, ValueError):
			# Ignora linhas malformadas
			pass
		return None

	def _extract_kill_info(self, line, game):
		try:
			# Remove a parte inicial "Kill: <id1> <id2> <mod>: "
			# Exemplo: "Kill: 1022 2 22: <world> killed Isgalamido by MOD_TRIGGER_HURT"
			kill_data = line.split('Kill:')[1].strip()

			# Separa a parte do descritor e a parte do texto
			# Formato: "<id1> <id2> <mod>: <killer> killed <victim> by <weapon>"
			parts = kill_data.split(': ', 1)
			if len(parts) < 2:
				return	
			kill_text = parts[1]
			
			# Extrai killer e victim
			# Formato esperado: "<killer> killed <victim> by <weapon>"
			if ' killed ' not in kill_text:
				return
			killer_part, victim_part = kill_text.split(' killed ', 1)
			killer = killer_part.strip()
			
			# Extrai a vítima (remove " by <weapon>")
			victim = victim_part.split(' by ')[0].strip()
			
			# Adiciona o kill ao jogo
			game.add_kill(killer, victim)
		
		except (IndexError, ValueError):
			# Ignora linhas malformadas
			pass
