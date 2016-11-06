"""
Keeps scores for a game of Sushi Go. Run a game by calling the function
and passing in the number of players, followed by each of the players'
names. Type in your scores carefully, as you won't be able to revise them
afterwards. (now you can! -Eric)

By Tammy Chen and Samantha Wong and Eric Pai.
"""

DEFAULT_PROMPT = "--> "
NUM_ROUNDS = 3

from collections import defaultdict
from colorama import Fore, Back, Style

def style(style_str):
	print(style_str, end="")

def log(level, msg):
	assert level in "i d e".split()
	if level == "i":
		style(Style.DIM)
	elif level == "d":
		style(Fore.BLUE)
	elif level == "e":
		style(Fore.RED)
	print(msg)
	style(Style.RESET_ALL)

class Player:
	def __init__(self, name, number):
		self.scores = []
		self.name = name
		self.number = number
	def __repr__(self):
		return 'Player({0}, {1})'.format(self.name, self.number)

def log_title(msg):
	title_width = len(msg) + 4
	log("d", "{0}\n# {1} #\n{0}".format("#" * title_width, msg))

def get_players():
	log_title("Setup")
	i = 1
	player_names = []
	while True:
		name = get_input("Enter a name for player {0}, or type `done` to end"
			.format(i))
		if name == 'done':
			if len(player_names) < 2:
				log("e", "Need at least 2 players to play a game!")
				continue
			player_names = allow_edits(player_names, name="player")
			return player_names
		player_names.append(name)
		i += 1

def do_round(round_num, player_names):
	log_title("Round {0}".format(round_num))
	scores = []
	for player in players:
		score = get_input_type("Score for {0}:".format(player.name), "int")
		scores.append(score)
	scores = allow_edits(scores, name_list=player_names)
	return scores

def main():
	players = get_players()
	print(do_round(1, players))

def go(players):
	players = get_players()
	round = 1
	def play_round():
		nonlocal round
		# nonlocal scores
		print("Beginning of round", round)
		for name in scores.keys():
			score = get_input_type("Give a score for {0}:"\
				.format(name), "int")
			scores[name] = scores[name] + int(score)
		print("End of round", str(round))
		round += 1
		if round > 3:
			for name in scores.keys():
				dessert_score = get_input_type("Input dessert score for {0}:"\
					.format(name), "int")
				scores[name] = scores[name] + int(dessert_score)
			highest_score = 0
			winner = ''
			tie = False
			for name in scores.keys():
				if scores[name] > highest_score:
					highest_score = scores[name]
					winner = name
			for name in scores.keys():
				if scores[name] == highest_score and name != winner:
					print("There is a tie score of {0} between {1} and {2}!"\
						.format(highest_score, winner, name))
					tie = True
			if not tie:
				print("The winner is {0} with a score of {1}!"\
					.format(winner, highest_score))
			for name in scores.keys():
				print("{0}:{1}".format(name, scores[name]))
			return "Game finished!"
		else:
			return play_round()

	return play_round()

def allow_edits(items, name="item", name_list=None, deletable=False, nums_only=False):
	edit_name = "edit"
	delete_name = "del"
	possible_cmds = ["yes"] + \
		["{}{}".format(edit_name, i) for i,_ in enumerate(items, start=1)]
	if deletable:
		possible_cmds +=  + \
		["{}{}".format(delete_name, i) for i,_ in enumerate(items, start=1)]
	while True:
		log("i", "are these {0}s correct?".format(name))
		for i, item in enumerate(items, start=1):
			if name_list:
				print("  ({0})  {2}".format(name_list[i-1], item))
			else:
				print("  ({0} {1})  {2}".format(name, i, item))
		prompt = "type `yes` if correct,\n  or `{0}1` to edit item 1, etc."
		if deletable:
			prompt += "\n  or `{1}1` to delete item 1, etc."
		cmd = assert_input(prompt.format(edit_name, delete_name), possible_cmds)
		if cmd == 'yes':
			return items
		elif cmd.startswith(delete_name):
			delete_num = int(cmd[len(delete_name):]) - 1
			items = items[:delete_num] + items[delete_num + 1:]
			possible_cmds = ["yes"] + \
		["{}{}".format(edit_name, i) for i,_ in enumerate(items, start=1)] + \
		["{}{}".format(delete_name, i) for i,_ in enumerate(items, start=1)]
		elif cmd.startswith(edit_name):
			edit_num = int(cmd[len(edit_name):])
			input_type = "int" if nums_only else "str"
			value = get_input_type("enter a new value for {0} {1}"\
				.format(name, edit_num), value_type=input_type)
			items[edit_num - 1] = value

def assert_input(prompt, possible_values):
	input_prompt = "{0}\npossible values: {1}".format(prompt, possible_values)
	value = get_input(input_prompt)
	while value not in possible_values:
		log("e", "{0}^ invalid input".format(" " * len(DEFAULT_PROMPT)))
		value = get_input(input_prompt)
	return value

def get_input(prompt, input_prompt=DEFAULT_PROMPT, print_after=False):
	log("i", prompt)
	value = input(input_prompt)
	if print_after:
		print()
	return value

def get_input_type(prompt, value_type="str"):
	""" Gets input, and ensures it's of type `value_type`.
		Currently only supports str and int

	>>> score = get_input("Give a score", int)
	Give a score: asdf
	Give a score (must be int): 5
	>>> score
	5
	"""
	assert value_type in ["str", "int"], "{} type not supported".format(value_type)
	value = get_input(prompt)
	if value_type == "str":
		return value
	while True:
		try:
			return int(value)
		except:
			log("e", "{0}^ invalid input".format(" " * len(DEFAULT_PROMPT)))
			value = get_input(prompt)

# if __name__ == '__main__':
# 	go()