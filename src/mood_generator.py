from news_db_handler import NewsDBHandler 
from twitter_db_handler import TwitterDBHandler 

class MoodGenerator:
  def __init__(self, news_db, twitter_db, news_source_urls):
    self._news_db = news_db
    self._twitter_db = twitter_db

    self._news_source_urls = news_source_urls
    self._total_news_viewership = sum(news_source_urls.values())
    print(self._total_news_viewership)

  def _get_news_score(self, phrase, start_date, end_date):
    scores = self._news_db.get_data_for_phrase(phrase, start_date, end_date)
    print(scores)
    if (len(scores) == 0):
      return 0

    url_sum = {url: 0 for url in self._news_source_urls}
    url_count = {url: 0 for url in self._news_source_urls}
    for (score, url_root) in scores:
      url_sum[url_root] = url_sum[url_root] + score
      url_count[url_root] = url_count[url_root] + 1
    src_score = {url : url_sum[url] / float(url_count[url]) 
                  for url, count in url_count.items() if count > 0}
    print(src_score)   

    news_score = 0
    for url, score in src_score.items():
      news_score = news_score + score * self._news_source_urls[url]

    return news_score / float(self._total_news_viewership)

  def _get_twitter_score(self, phrase, start_date, end_date):
    data = self._twitter_db.get_data_for_phrase(phrase, start_date, end_date)
    if (len(data) == 0):
      return 0

    tot_likes = sum(n for (_, n, _) in data)
    tot_rts = sum(n for (_, _, n) in data)

    s = 0
    for (sentiment, likes, retweets) in data:
      weight = likes / tot_likes / 2.0 + retweets / tot_rts / 2.0
      s = s + (sentiment * weight)

    return s / float(len(data))

  def get_score(self, phrase, start_date, end_date):
    news_score = self._get_news_score(phrase, start_date, end_date)
    twitter_score = self._get_twitter_score(phrase, start_date, end_date)

    return (news_score + twitter_score) / 2.0