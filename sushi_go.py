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

def log(color, msg):
	if color == "d":
		style(Style.DIM)
	elif color == "b":
		style(Fore.BLUE)
	elif color == "r":
		style(Fore.RED)
	elif color == 'g':
		style(Fore.GREEN)
	print(msg)
	style(Style.RESET_ALL)

def log_title(msg):
	title_width = len(msg) + 4
	log("b", "{0}\n# {1} #\n{0}".format("#" * title_width, msg))

def log_scoreboard(scores, players):
	lines = ["{0}'s score: {1}".format(name,score) for name,score in zip(players, scores)]
	line_width = len(max(lines, key=lambda line: len(line))) + 4
	max_score, min_score = max(scores), min(scores)
	log('_', '*' * line_width)
	for i, line in enumerate(lines):
		color = '_'
		if scores[i] == min_score:
			color = 'r'
		if scores[i] == max_score:
			color = 'g'
		log(color, '  {0}'.format(line))
	log('_', '*' * line_width)

def get_players():
	log_title("Setup")
	i = 1
	player_names = []
	while True:
		name = get_input("Enter a name for player {0}, or type `done` to end"
			.format(i))
		if name == 'done':
			if len(player_names) < 2:
				log("r", "Need at least 2 players to play a game!")
				continue
			player_names = allow_edits(player_names, name="player")
			return player_names
		player_names.append(name)
		i += 1

def do_round(round_num, players):
	log_title("Round {0}".format(round_num))
	scores = []
	for player in players:
		score = get_input_type("Score for {0}:".format(player), "int")
		scores.append(score)
	scores = allow_edits(scores, name_list=players, nums_only=True)
	return scores

def do_pudding(players):
	log_title("Pudding Counts")
	pudding_counts = []
	for player in players:
		count = get_input_type("Pudding count for {0}:".format(player), "int")
		pudding_counts.append(count)
	pudding_counts = allow_edits(pudding_counts, name_list=players, nums_only=True)
	if len(set(pudding_counts)) <= 1:
		return [0] * len(players)
	score_diffs = []
	min_, max_ = min(pudding_counts), max(pudding_counts)
	penalty = -6 / pudding_counts.count(min_)
	reward = 6 / pudding_counts.count(max_)
	for count in pudding_counts:
		if count == min_:
			score_diffs.append(penalty)
		elif count == max_:
			score_diffs.append(reward)
		else:
			score_diffs.append(0)
	return score_diffs

def do_finish(scores, players):
	log_title("Final Scores")
	log_scoreboard(scores, players)
	print() # empty line
	max_ = max(scores)
	winners = [name for score, name in zip(scores, players) if score == max_]
	style(Fore.MAGENTA)
	if len(winners) == 1:
		print("The winner is {0} with a score of {1}!".format(winners[0], max_))
	else:
		print("There is a tie score of {0} between these players:".format(max_))
		for winner in winners:
			print("  {0}".format(winner))
	style(Style.RESET_ALL)
	log_title("Game Finished")

def add_scores(scores1, scores2):
	return [i + j for i, j in zip(scores1, scores2)]

def main():
	players = get_players()
	scores = [0] * len(players)
	for round_num in range(1, NUM_ROUNDS + 1):
		scores = add_scores(scores, do_round(round_num, players))
		log_scoreboard(scores, players)
	scores = add_scores(scores, do_pudding(players))
	do_finish(scores, players)

def allow_edits(items, name="item", name_list=None, deletable=False, nums_only=False):
	edit_name = "edit"
	delete_name = "del"
	possible_cmds = ["yes"] + \
		["{}{}".format(edit_name, i) for i,_ in enumerate(items, start=1)]
	if deletable:
		possible_cmds +=  + \
		["{}{}".format(delete_name, i) for i,_ in enumerate(items, start=1)]
	while True:
		log("d", "are these {0}s correct?".format(name))
		for i, item in enumerate(items, start=1):
			if name_list:
				print("  ({0})  {1}".format(name_list[i-1], item))
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
		log("r", "{0}^ invalid input".format(" " * len(DEFAULT_PROMPT)))
		value = get_input(input_prompt)
	return value

def get_input(prompt, input_prompt=DEFAULT_PROMPT, print_after=False):
	log("d", prompt)
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
			log("r", "{0}^ invalid input".format(" " * len(DEFAULT_PROMPT)))
			value = get_input(prompt)

if __name__ == '__main__':
	main() # where all the magic happens xP

