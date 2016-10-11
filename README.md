#AwkwardBot

AwkwardBot is a socially awkward little bot that doesn't really know
how to communicate. Load the data directory with some sample files for
it to learn from and it will try to say things based on what you've
taught it.

Right now, AwkwardBot comes with an example file containing some
Donald Trump speeches, so it's not very friendly. I suggest you try to
teach it something else.

##How to Teach AwkwardBot
Create a text file (it doesn't matter what you call it) and put it in
the data directory. Your text file should contain some training text
which the bot will try to copy. The text should be segmented so that
each line contains a single sentence.

Once you've loaded the data directory, run the awkward.py script and
AwkwardBot will try to learn from the inputs, say something meaningful
and then quit.

## How It Works

AwkwardBot uses an extremely simple language model called a Trigram
Model. When you start the script it reads the contents of the data
directory and splits the text files it contains into individual
words. The bot then groups those words into sets of three. For
example, the sentence "How are you today" would produce the sets

+ (START, START, How)
+ (START, How, are)
+ (How, are, you)
+ (are, you today)
+ (you, today, STOP)

Using these little sets, Trigram tries to complete sentences by
looking at pairs of words which have already been generate and trying
to complete them by selecting a suitable third option.
