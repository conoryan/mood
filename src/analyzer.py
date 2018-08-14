def analyze_sentence(sentence):
  print(sentence)
  print(sentence.noun_phrases)
  print(sentence.polarity)

def analyze(article):
  from textblob import TextBlob # this is a hack
  blob = TextBlob(article.text)
  for sentence in blob.sentences:
    analyze_sentence(sentence)

def run(settings_filename, queue):
  while True:
    item = queue.get()
    item.download()
    item.parse()

    analyze(item)