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

def get_players():
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
			return [Player(name, i) for i, name in enumerate(player_names, start=1)]
		player_names.append(name)
		i += 1

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

def allow_edits(items, name="item"):
	edit_name = "edit"
	possible_cmds = ["yes"] + \
		["{}{}".format(edit_name, i) for i,_ in enumerate(items, start=1)]
	while True:
		log("i", "are these {0}s correct?".format(name))
		for i, item in enumerate(items, start=1):
			print("  ({0} {1})  {2}".format(name, i, item))
		cmd = assert_input("type `yes` if correct, or `{0}1` to edit item 1, etc."\
			.format(edit_name), possible_cmds)
		if cmd == 'yes':
			return items
		edit_num = int(cmd[len(edit_name):])
		value = get_input("enter a new value for {0} {1}".format(name, edit_num))
		items[edit_num - 1] = value

def assert_input(prompt, possible_values):
	input_prompt = "{0}\npossible values: {1}".format(prompt, possible_values)
	value = get_input(input_prompt)
	while value not in possible_values:
		log("e", "{0}^ invalid input\n".format(" " * len(DEFAULT_PROMPT)))
		value = get_input(input_prompt)
	return value

def style(style_str):
	print(style_str, end="")

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
			value = get_input("{0} (must be int): ".format(prompt))

# if __name__ == '__main__':
# 	go()