def go(players):
	""" Keeps scores for a game of Sushi Go. Run a game by calling the function and passing in 
	the number of players, followed by each of the players' names. Type in your scores carefully,
	as you won't be able to revise them afterwards.

	By Tammy Chen and Samantha Wong.
	"""
	scores = {}
	while players > 0:
		name = input("Input the player's name: ")
		scores[name] = 0
		players -= 1
	round = 1
	def play_round():
		nonlocal round
		nonlocal scores
		print("Beginning of round", round)
		for name in scores.keys():
			score = input("Give a score for " + name + ": ")
			scores[name] = scores[name] + int(score)
		print("End of round", str(round))
		round += 1
		if round > 3:
			for name in scores.keys():
				dessert_score = input("Input dessert score for " + name + ": ")
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
					print("There is a tie score of " + str(highest_score) + " between " + winner + " and " + name + "!")
					tie = True
			if not tie:
				print("The winner is " + winner + " with a score of " + str(highest_score) + "!")
			for name in scores.keys():
				print(name, ":", scores[name])
			return "Game finished!"
		else:
			return play_round()

	return play_round()