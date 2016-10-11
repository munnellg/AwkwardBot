#!/usr/bin/env python3
import re
import os
import random
from collections import defaultdict

# A speech bot built on the trigram language model.
class AwkwardBot:
	# The location of our training data
	datadir = os.path.join(os.path.dirname(__file__), 'data')

	# The trigram model
	model = defaultdict(                       # Word 1
				lambda : defaultdict(          # Word 2
					lambda : defaultdict(int)  # P(Word 3 | Word 1, Word 2)
				)
			)

	start_flag = "START" # Marker for the start of a sentence
	stop_flag  = "STOP"  # Marker for the end of a sentence

	# Ridiculous upper bound on sentence length, but it's a good idea to
	# have a point at which we should stop
	max_sent_len = 1000

	# Initialize a new model object
	def __init__(self):
		# Check if the model has already been trained. If not, train it now.
		if len(AwkwardBot.model) == 0:
			# Get a list of all the input files in our datadir
			files = [os.path.join(AwkwardBot.datadir, f) for f in os.listdir(AwkwardBot.datadir) if os.path.isfile(os.path.join(AwkwardBot.datadir, f))]

			# Load input files line by line. Assume each line is a sentence
			sentences = []
			for doc in files:
				# Open file
				speech = open(doc, 'r')
				# Get sentences/lines. Remove leading and trailing spaces
				sentences += [sentence.strip() for sentence in speech]
				# Close file
				speech.close()

			words = [ [word for word in self.tokenize_sentence(sentence)] for sentence in sentences ]
			self.build_model(words)

	# Model works on probabilities. Normalise reduces them to values between
	# zero and one. This allows us to use them to compute probabilities
	def normalise(self):
		# Iterate over word pairs and compute probability of third word
		# being used to complete the statement
		for word1 in AwkwardBot.model:
			for word2 in AwkwardBot.model[word1]:
				words = AwkwardBot.model[word1][word2]

				# Each cycle our count starts at zero
				total = 0

				# Compute total frequency of all outcomes
				for count in words:
					total += words[count]

				# Normalise
				for count in words:
					words[count] = words[count]/total

	# Build the trigram model using tokenized sentences passed as input
	def build_model(self, sents):
		# Start reading the sentences and learning from them
		for sent in sents:
			# Pad the beginning of every sentence with start flags so the bot
			# knows it's the beginning of the sentence. Same at the end of the
			# sentence with stop flags
			old1, old2 = AwkwardBot.start_flag, AwkwardBot.start_flag
			for word in sent + [AwkwardBot.stop_flag, AwkwardBot.stop_flag]:
				# Look at words in threes and count how often we see
				# particular triplets
				AwkwardBot.model[old2][old1][word] += 1

				# Remember what we've seen
				old2 = old1
				old1 = word

		# Normalize our computed counts so that they represent probabilities
		# rather than raw counts
		self.normalise()

	# Generates a random new sentence based on what the bot has learned from
	# the text that it read
	def say_something(self):
		# First two words in our triple
		word1, word2 = AwkwardBot.start_flag, AwkwardBot.start_flag
		# Third word whose value depends on that of the previous two
		word3 = ""

		# Will contain the words which make up our sentence
		sentence = []

		# Loop for no more than our ridiculous upper bound. Just a good idea
		# to know that we'll eventually stop
		for counter in range(AwkwardBot.max_sent_len):
			# Given word1 and word2, pick a suitable value for word3
			word3 = self.get_word(word1, word2)

			# Check if we're done building the sentence
			if word3 == AwkwardBot.stop_flag:
				break

			# If not, expand our sentence and prepare to choose another word
			sentence.append(word3)
			word1 = word2
			word2 = word3

		# Build a sentence from the words we found and return it
		return " ".join(sentence)

	# Find a suitable word which might follow word1 and word2 in a sentence
	def get_word(self, word1, word2):
		# Counter which we'll need for counting probabilities
		total = 0

		# Get a random value which we'll use to choose a word
		r = random.random()

		# Search for a word which might complete the triple word1, word2 word3
		for key in AwkwardBot.model[word1][word2]:
			# Keep counting probabilities until we get a number that's bigger
			# than the random value
			total += AwkwardBot.model[word1][word2][key]

			# When we've counted enough to exceed our random probability
			# it means that we've found a suitable word
			if total > r:
				# We've found our word! Return it!
				return key

	# Split a sentence up into words, punctuation, etc.
	def tokenize_sentence(self, sentence):
		# This isn't a great way to find words in sentences, but it'll do
		regex = r"[\w\'-]+|[\.\?!]+"
		return re.findall(regex, sentence)

# If this script is run by itself, say something and then quit
if __name__=="__main__":
	tb = AwkwardBot()
	print(tb.say_something())
