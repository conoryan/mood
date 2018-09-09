# mood
Generate a historical record of sentiment on a given query, based on news articles and tweets. For example, a user can query "trump" with two dates, and the output is an index score (range [-1,1]) representing the general sentiment of all news articles + tweets that make reference to "trump" between the two dates. Sentiment analysis is not the purpose of the project; the purpose is to aggregate and display (into a cohesive index) what sentiment is over all these different sources. Potential use: compare changes in this library's output with significant events to see the impact of those events on public opinion.

## next
immediately:
- Actually retrieve tweet data. It's hard to get the data I need; ideally, I'd have a database populated with a good number (100k?) of every day's most popular tweets (based on likes/retweets etc). I've tried a few libraries and none are great for this purpose, as generally you need a search query. `twitterscraper` library doesn't do enough because it won't retrieve the "popular" tweets (which are the ones I need), even when trying to use `result_type=popular` in the query. It also won't search "all tweets" (via a wildcard `*` search), which would be a great way for me to just get all popular tweets generally. I considered just taking the user's query and doing it real-time, but that won't work either because (1) it takes a while to get a large number of tweets to crunch, and (2) they have no guarantee of being popular even when I get them. 
- The official Twitter API (I guess via `tweepy`) does not work better as searching for the most popular of all tweets using a wildcard query also doesn't work; they want a solid query. It also lacks important features I need (like being able to just get the most popular of all tweets between two dates). With that API maybe I ideally would do: once per day, get the 100 most popular tweets, and then get the 100 most popular between each of those tweet IDs, and maybe subdivide further if I want more than 10000 tweets per day (which I do). One thing that may resolve all of this is to use the timeline query periodically and assume the algorithm is not biased. If there is a way to query the home timeline for popularity, it may be the best workaround.

waiting for:
- me to have time
- twitter to approve my developer project
- twitter search api to be useful for this project
- news scraping to be reliable for parsing dates
- to find good data on news site readership (for the algorithm calculation) in somenthing like millions per day or month

long term:
- a UI to display data in a graph over time (lol)

## links ive found useful
- https://github.com/taspinar/twitterscraper
- http://docs.tweepy.org/en/v3.6.0/index.html
- https://github.com/cjhutto/vaderSentiment
- https://sebastianraschka.com/Articles/2014_sqlite_in_python_tutorial.html#creating-a-new-sqlite-database
- https://media.readthedocs.org/pdf/newspaper/latest/newspaper.pdf
