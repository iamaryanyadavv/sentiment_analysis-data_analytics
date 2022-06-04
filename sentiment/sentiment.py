
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

import json
# nltk.download('vader_lexicon')
# sia = SentimentIntensityAnalyzer()
# print(sia.polarity_scores("My 3 year old got food poisoning while we were waiting for our covid test results. The room looked like a college dormitory. Beds were hard. Shower was basic. This is not a 5 star hotel\u2026 I will not be staying here again"))

f = open("./data/bangkok_hotels_final.json")
            
data = json.load(f)

arr = []
for i in data["hotels"]:
    arr.append({ 
        "name" : i["name"], 
        "rating" : i["overall_rating"], 
        "reviews" : i["reviews"]
        })
f.close()



def sentiment_analyser(arr):
    sia = SentimentIntensityAnalyzer()
    hotels = {}

    for i in arr:
        pos_count = 0
        neg_count = 0
        neu_count = 0
        count = 0
        total_score = 0
        for j in i["reviews"]:
            title_score = sia.polarity_scores(j["review_title"])["compound"]
            comment_score = sia.polarity_scores(j["review_comment"])["compound"]
            # print(title_score, comment_score)

            avg_score = (title_score * 0.6 + comment_score * 0.4) 

            if avg_score > 0:
                pos_count = pos_count + 1
            elif avg_score < 0:
                neg_count = neg_count + 1
            else:
                neu_count = neu_count + 1

            count = count + 1
            total_score = total_score + avg_score

        hotels[i["name"]] = {
            "positives" : pos_count / count,
            "negatives" : neg_count / count,
            "neutrals" : neu_count / count,
            "ratio" : pos_count / neg_count,
            "total_score" : total_score / count,
            "rating" : i["rating"]
            }

    # print(hotels)

    return hotels

        
    
    
sentiment_analyser(arr)