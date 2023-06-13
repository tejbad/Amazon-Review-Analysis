
from textblob import TextBlob
from nltk.corpus import stopwords

# def removeStopWords(text):
#     text=TextBlob(text)
#     tokens=set(text.words)
#     print("Tokens: ",tokens)
#     stop=set(stopwords.words("english"))
#     return tokens-stop


class Analysis():
    def __init__(self):        
        self.result = 0
        self.count = 0
        self.Eneg,self.neg,self.neu,self.pos,self.Epos = 0,0,0,0,0

    def process_rating(self,review):
        if review["rating"] == 1.0 and review["sentiment"] > -60:
            review["sentiment"] = review["sentiment"] - 30
        elif review["rating"] == 2.0 and review["sentiment"] > -40: 
            review["sentiment"] = review["sentiment"] - 15
        elif review["rating"] == 4.0 and review["sentiment"] < 40: 
            review["sentiment"] = review["sentiment"] + 15
        elif review["rating"] == 5.0 and review["sentiment"] < 60: 
            review["sentiment"] = review["sentiment"] + 30
        return review

    def distribute_data(self,review):
        if review["sentiment"] < -50:
            self.Eneg +=1
        elif -50 < review["sentiment"] < -10:
            self.neg +=1
        elif -10 < review["sentiment"] < 10:
            self.neu +=1
        elif 10 < review["sentiment"] < 50:
            self.pos +=1
        elif 50 < review["sentiment"] :
            self.Epos +=1

    def analysis(self,data):
        for review in data:
            self.count +=1
            # if count <=3:
                # review["body"] = removeStopWords(review["body"])
            # review["body"] = "Worst"
            blob = TextBlob(review["body"])
            # print(blob.sentiment)
            review["sentiment"] = round( blob.sentiment.polarity * 100 ,2)
            if review["rating"]:
                review = self.process_rating(review)
            self.result += review["sentiment"]
            
            self.distribute_data(review)

        result = self.result/len(data)
        result = float("{:.2f}".format(result))
        if result < 0 :
            sentiment = "Negative"
        elif result == 0 :
            sentiment = "Neutral"
        else:
            sentiment = "Positive"
        chart_data = {"Epos":self.Epos,"pos":self.pos,"neu":self.neu,"neg":self.neg,"Eneg":self.Eneg}
        return data,abs(result),sentiment,chart_data


