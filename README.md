# Paxlovid rebound investigation - supporting code & data

This is an investigation of reports of Paxlovid rebound on Twitter.  See the details here:

  https://twitter.com/__philipn__/status/1547530190330269697

## Finding "no rebound" reports

First, we use a few simple Twitter search queries to find reported cases on Twitter where someone took Paxlovid and didn't rebound, detailed here:

  https://twitter.com/__philipn__/status/1547530190330269697

Then we see what day the individuals took Paxlovid relative to symptom onset, if they reported this information on Twitter.  This was recorded in this public Google Sheet:

https://docs.google.com/spreadsheets/d/1XZ2J6YGasKgeiL1Ep7iSNDn0m6h_jcfonuy0usKcSR4/edit#gid=1388488734

This first step - investigating "no rebound" - was fairly simple because of the limited number of reports on twitter.

## Finding rebound reports

This was more difficult.  The number of tweets returned by the "paxlovid rebound day" Twitter search was too numerous for manual investigation but didn't feel large enough for random sampling.  So I wrote some simple code to filter each tweet through the GPT-3 large language model with the aim of having GPT-3 tell me whether or not a given tweet was *about someone themselves reporting Paxlovid rebound* (versus just a tweet about paxlovid rebounds).

### GPT-3 parameters & usage

I used the default settings in the OpenAI Playground and the `text-davinci-002` model.  Classification didn't really work with the smaller language models available.

For prompt design, I picked a few semi-random example tweets from the snscrape JSON and got a feel for how different prompts performed. The prompt I settled on was:

  Paxlovid rebound, sometimes informally called 'rebound' or 'rebound COVID', is when the drug Paxlovid is taken to treat COVID-19 and then symptoms or a positive test returns after treatment is complete.  Is the following Tweet about the author themselves experiencing Paxlovid rebound? Answer as "Yes" or "No":
  
  [[{tweet}]]

I didn't expect the model to be able to perfectly classify the tweets, but it was good enough to narrow down the number that needed manual investigation.

# Notes on steps taken
 
 1. `snscrape` found 748 possible rebound tweets ("paxlovid rebound day").  This command was run on Jul 14 19:56, pacific time. See `twitter_rebound.py` for details.
 2. Narrowed this down to 274 probably rebounds using GPT-3 (`probably_rebounds.jsonl`), see `twitter_rebound.py` for details.
 3. Extract the relevant twitter URLs, examine in spreadsheet app:

      $ python jsonl_to_csv.py

 4. Look through each tweet, denote in spreadsheet if it is a true Paxlovid rebound.  If the tweet itself doesn't detail which day they started Paxlovid, try searching "from:@username paxlovid" or "from:@username covid" on Twitter to find supporting tweets.  If no information is available, leave the `day_of_symptoms_started_pax` field blank.

    If paxlovid was started before the start of symptoms, put down day 0. If started on first day of symptoms, day 1.

 5. Move all of the rows with a value for `day_of_symptoms_started_pax` into a new sheet (e.g. the known-days rebounds)
 6. Remove duplicates from sheet (unique twitter usernames)
 7. Save this as `rebound_info.xls`.
 8. Move into Google sheets for sharing:
