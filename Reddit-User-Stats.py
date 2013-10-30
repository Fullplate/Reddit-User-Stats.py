# User Comment Statistics for Reddit
# Michael Harmer, October 2013
# Utilises the Reddit API, the requests Python module and Python 3

import requests, sys

class User:
	def __init__(self, name):
		self.name = name
		self.commentList = []

	def addComment(self, newComment):
		self.commentList.append(newComment)

	def display(self):
		for i in self.commentList:
			i.display()

	def stats(self):
		totComments, totChars, totUps, totDowns, highComment, lowComment = 0,0,0,0,1,1
		allSubs = {}
		for c in self.commentList:
			# general stats
			totComments += 1
			totChars += c.chars
			totUps += c.ups
			totDowns += c.downs
			# counts by subreddit
			if c.subreddit in allSubs:
				allSubs[c.subreddit] += 1
			else:
				allSubs[c.subreddit] = 1
			# most/least popular
			if c.ups - c.downs > highComment:
				highComment = c.ups - c.downs
			if c.ups - c.downs < lowComment:
				lowComment = c.ups - c.downs

		print("Username:", self.name)
		print("Displaying stats for up to 1000 most recent comments.")
		print("---")
		print("Total comments:", totComments)
		print("Avg length (characters):", int(totChars/totComments))
		print("Avg upvotes:", round(totUps/totComments, 2))
		print("Avg downvotes:", round(totDowns/totComments, 2))
		print("Highest voted:",highComment)
		print("Lowest voted:",lowComment)
		print("---")
		print("Top 5 Subreddits:")
		
		topSubs = list(sorted(allSubs, key=allSubs.get, reverse=True)[:5])
		for i in topSubs:
			print(i+" ("+str(allSubs[i])+")")

class Comment:
	def __init__(self, id, ups, downs, chars, subreddit):
		self.id = id
		self.ups = ups
		self.downs = downs
		self.chars = chars
		self.subreddit = subreddit

	def display(self):
		print("#",self.id)
		print("Subreddit:",self.subreddit)
		print("Total chars:",self.chars)
		print("Ups/Downs:",self.ups,self.downs)
		print()

def retrieveComments(username):
	""" retrieves comments and returns User object containing Comment objects """ 

	print("\nWorking", end="")

	url = 'http://www.reddit.com/user/'+username+'/comments/.json?limit=100'
	user = User(username)

	# perform initial api request and convert to JSON dictionary
	r = requests.get(url)
	commentSet = r.json()

	# while we have comments to process...
	while len(commentSet['data']['children']) > 0:
		print('.', end="")
		sys.stdout.flush()

		# process the current set of comments
		for c in commentSet['data']['children']:
			id = c['data']['id']
			ups = int(c['data']['ups'])
			downs = int(c['data']['downs'])
			chars = len(c['data']['body'])
			subreddit = c['data']['subreddit']
			user.addComment(Comment(id, ups, downs, chars, subreddit))

		# get the id of the last comment in the set
		lastId = commentSet['data']['children'][-1]['data']['id']

		# modify the url and retrieve the next set of comments
		url += "&after=t1_"+lastId
		r = requests.get(url)
		commentSet = r.json()

	print("\n")
	return user

def main():
	username = input("Enter username: ")
	retrieveComments(username).stats()

if __name__ == "__main__":
	main()