# mood
Generate a historical record of sentiment on a given query, based on news articles and tweets. 

## next
immediately:
- Actually retrieve tweet data. It's hard to get the data I need; ideally, I'd have a database populated with a good number (100k?) of every day's most popular tweets (based on likes/retweets etc). I've tried a few libraries and none are great for this purpose, as generally you need a search query. `twitterscraper` library doesn't do enough because it won't retrieve the "popular" tweets (which are the ones I need), even when trying to use `result_type=popular` in the query. I considered just taking the user's query and doing it real-time, but that won't work either because (1) it takes a while to get a large number of tweets to crunch, and (2) they have no guarantee of being popular even when I get them. The official Twitter API via `tweepy` may work better but I haven't been approved for access yet, and it seems to lack important features I need (like being able to just get the most popular of all tweets between two dates). With that API, I may try to: once per day, get the 100 most popular tweets, and then get the 100 most popular between each of those tweet IDs, and maybe subdivide further if I want more than 10000 tweets per day (I do)

and also waiting for:
- me to have time
- twitter to approve me
- twitter search api to be useful for this project
- news scraping to be reliable for parsing dates
- to find data on news site readership... for the algorithm calculation

long term:
- a UI to display data in a graph over time (lol)

## links ive found useful
- https://github.com/taspinar/twitterscraper
- https://github.com/cjhutto/vaderSentiment
- https://sebastianraschka.com/Articles/2014_sqlite_in_python_tutorial.html#creating-a-new-sqlite-database
- https://media.readthedocs.org/pdf/newspaper/latest/newspaper.pdf
