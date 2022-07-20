"""
Tweets were scraped using the following command:

    snscrape --jsonl --since 2021-12-01 twitter-search "paxlovid rebound day" > sns_search.jsonl

Using snscrape https://github.com/JustAnotherArchivist/snscrape.
"""

import json
import os
import time
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

PROMPT = """\
Paxlovid rebound, sometimes informally called 'rebound' or 'rebound COVID', is when the drug Paxlovid is taken to treat COVID-19 and then symptoms or a positive test returns after treatment is complete.  Is the following Tweet about the author themselves experiencing Paxlovid rebound? Answer as "Yes" or "No":

[[{tweet}]]
"""

JSONL_FILE = 'sns_search.jsonl'
OUTPUT_FILE = 'probably_rebounds.jsonl'


def write_tweet_data(tweets_data):
    # Just writing every time in case OI API error/etc
    with open(OUTPUT_FILE, 'w') as f:
        for tweet_data in tweets_data:
            f.write(json.dumps(tweet_data) + '\n')


def probably_a_rebound(tweet):
    response = openai.Completion.create(
      model="text-davinci-002",
      prompt=PROMPT.format(tweet=tweet),
      temperature=0.7,
      max_tokens=256,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0
    )
    
    answer = response.choices[0].text.strip().lower()
    return answer == 'yes'

    
def main():
    tweets_of_rebounds = []
    # Load from output file because API borked
    with open(OUTPUT_FILE) as f:
        for line in f:
            tweets_of_rebounds.append(json.loads(line))

    with open(JSONL_FILE) as f:
        for (lineno, line) in enumerate(f):
            if lineno <= 50:
                continue # apready processed

            tweet_data = json.loads(line) 
            tweet = tweet_data['renderedContent']

            time.sleep(1.1)  # OpenAI API has a 60 req/min limit
            if probably_a_rebound(tweet):
                tweets_of_rebounds.append(tweet_data)
                print('{} rebound: {}'.format(lineno, str(tweet_data)))
            else:
                print('{} not rebound: {}'.format(lineno, str(tweet_data)))
    
            write_tweet_data(tweets_of_rebounds)


if __name__ == '__main__':
    main()
