import tweepy
from textblob import TextBlob
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
import re
nltk.download('stopwords')
nltk.download('punket')

###consumer key
consumer_key=' '
###consumer secret key
consumer_secret=' '
### access token
access_token=' '
#### access token secret key
access_token_secret=' '


auth=tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_token_secret)

def search_tweet():          ####count the tweets & search
    ht=input("enter the specific hashtag :")
    api=tweepy.API(auth)
    tweets=api.search(q=ht,count = 200)
    total=0
    for data in tweets:
        print(data.text)
        a = TextBlob(data.text)
        print(a)
        print(a.sentiment)
        print("Created at:" +str(data.created_at))
        print("username:"+data.user.name)
        print("---------------")
        total = total +  data.user.followers_count
    print("Total no of person tweeted:" + str(total))

def extract_user():  ####for specific user
    query = input("Enter the username of the user:")
    api=tweepy.API(auth)
    Tweets=api.user_timeline(screen_name=query, count=200)  ###Search for tweets by the given screen name
    for i in Tweets:
        tb=TextBlob(i.text)
        print(tb)
        print(tb.sentiment)


def search_keyword():    ####specific keyword
    user=input("Enter the name of user")
    query=[]
    tweets=[]
    tweets2=[]
    shows= True
    qw = input("Enter  the keywords ro be searched for :")
    query.append(qw)
    ask = input("Do you want to add more keywords?(Y/N)")
    ask = ask.upper()
    if ask == "Y":
        pass
    elif ask == "N":
        shows = False
    else:
        print("invalid input  \n"
              "Taking default input as 'No' ")
        shows = False
    api=tweepy.API(auth)
    result = api.user_timeline(screen_name=user,
                               count=200)  ### searches for the 200 tweets by the perticular user as the limit in tweepy is 200 only
    for data in result:
        tweets.append(data)
    oldest = tweets[-1].id  ### stores the id of the last tweet retrieved
    oldest_at = tweets[-1].created_at  ### Stores the time and date of the last tweet retrieved
    qu = True
    while qu:  ###to retrieve more older tweets
        qu2 = input("Do you want  more  tweets older than " + str(oldest_at) + "(Y/N)  :")
        qu2 = qu2.upper()
        if qu2 == "Y":
            api=tweepy.API(auth)
            result2 = api.user_timeline(screen_name=user, count=200,
                                        max_id=oldest)  ###retrieve the tweet older then the given tweet id
            for data in result2:
                tweets.append(data)  ###  appended the new tweets retrived
            oldest = tweets[-1].id
            oldest_at = tweets[-1].created_at
        elif qu2 == "N":
            qu = False
        else:
            print("invalid input  \n"
                  "Taking default input as 'No' ")
            qu = False
    count = -1
    for tweet1 in tweets:
        count = count + 1  ###starts the list from beginning
        tweet = tweet1.text
        tweet = re.sub(r"http\S+", "", tweet)  ##### removes the URL from the text of tweet
        tweets[count].text = tweet
    for keyword in query:
        for data in tweets:
            tex = TextBlob(data.text)
            qw = tex.find(keyword)
            if qw != -1:
                tweets2.append(data)  ### Appends the modified tweets
            else:
                pass
    if len(tweets2) > 0:
        for data in tweets:
            b=TextBlob(data.text)
            print(b)
    else:
        print("No tweet found with the related keywords")

def extract_info():
    query=input("enter the specific hashtag ")
    api=tweepy.API(auth)
    tweets=api.search(q=query,count=200)
    location=[]
    for data in tweets:
        t=TextBlob(data.text)
        print("language of Tweet :" + t.detect_language() + "\t timezone :" + str(data.user.time_zone))  ###Extract language and timezone for the tweets
        loc = data.user.location  ###Extract location from user info
        location.append(loc)
    word_counts = Counter(location)
    print("location \t No of occurences ")
    common_loc = word_counts.most_common(5)  ###passes the 5 most common locaton to the common_loc list
    for data in common_loc:
        print(data)
    print("Blank space indicates no location defined by the user")

def remove_stopwords():
    query = input("enter the specific hashtag ")
    api = tweepy.API(auth)
    tweets = api.search(q=query, count=200)
    stop_words=set(stopwords.words('english'))
    for data in tweets:
        data.text=data.text.lower()
        word_tokens=word_tokenize(data.text)
        filtered_sentence=[]
        for w in word_tokens:
            if w not in stop_words:
                filtered_sentence.append(w)
        msg=" ".join(map(str,filtered_sentence))
        data.text = msg
    data1=[]
    for dt in tweets:
        data2=dt.text.split(" ",30)
        data1.extend(data2)
    for data in tweets:
        tb=TextBlob(data.text)
        print(tb)
        print(tb.sentiment)
        print("Created at:"+str(data.created_at))
        print("username:"+data.user.name)
    word = Counter(data1)
    print("Printing the top 10 words appearing in the tweets:")
    top10 = word.most_common(10)
    for data in top10:
        print(data)




def send_message():
    user=input("enter the username of the person:")
    message=input("enter the message :")
    api=tweepy.API(auth)
    api.send_direct_message(screen_name=user,text=message)

def tweeting():
    text = input("What do you want to tweet")
    api=tweepy.API(auth)
    api.update_status(text)

def for_narendra_modi():
    print("Retreving tweets")
    api=tweepy.API(auth)
    Tweets = api.user_timeline(screen_name= "@narendramodi", count=200)  ###Search for tweets by the given screen name
    for data in Tweets:
        tweet = TextBlob(data.text)
        print(tweet)
        print(tweet.sentiment)  ### For analysis of sentiments
        print("Done at :" + str(data.created_at))  ### Print the time for the creation of tweet
        print("Username :" + data.user.name)  ### Print the user name of the twitter user
        print("---------------------------------------------")
    query = []  ### Stores the keywords to be searched for
    tweets = []  ### to store the tweets
    tweets2 = []  ### to store modified tweets
    shows = True
    while shows:  ### to store the no of keywords till we want
        qw = input("Enter  the keywords ro be searched for :")
        query.append(qw)
        ask = input("Do you want to add more keywords?(Y/N)")
        ask = ask.upper()
        if ask == "Y":
            pass
        elif ask == "N":
            shows = False
        else:
            print("invalid input  \n"
                  "Taking default input as 'No' ")
            shows = False

    for data in Tweets:
        tweets.append(data)
    oldest = tweets[-1].id  ### stores the id of the last tweet retrieved
    oldest_at = tweets[-1].created_at  ### Stores the time and date of the last tweet retrieved
    qu = True
    while qu:  ###to retrieve more older tweets
        qu2 = input("Do you want  more  tweets older than " + str(oldest_at) + "(Y/N)  :")
        qu2 = qu2.upper()
        if qu2 == "Y":
            result = api.user_timeline(screen_name="@narendramodi", count=200,
                                        max_id=oldest)  ###retrieve the tweet older then the given tweet id
            for data in result:
                tweets.append(data)  ###  appended the new tweets retrived
            oldest = tweets[-1].id
            oldest_at = tweets[-1].created_at
        elif qu2 == "N":
            qu = False
        else:
            print("invalid input  \n"
                  "Taking default input as 'No' ")
            qu = False
    count = -1
    for tweet1 in tweets:
        count = count + 1  ###starts the list from beginning
        tweet = tweet1.text
        tweet = re.sub(r"http\S+", "", tweet)  ##### removes the URL from the text of tweet
        tweets[count].text = tweet
    for keyword in query:
        for data in Tweets:
            tex = TextBlob(data.text)
            qw = tex.find(keyword)
            if qw != -1:
                tweets2.append(data)  ### Appends the modified tweets
            else:
                pass
    if len(tweets2) > 0:
        for data in tweets:
            tweet = TextBlob(data.text)
            print(tweet)
            print(tweet.sentiment)  ### For analysis of sentiments
            print("Done at :" + str(data.created_at))  ### Print the time for the creation of tweet
            print("Username :" + data.user.name)  ### Print the user name of the twitter user
            print("---------------------------------------------")
    else:
        print("No tweet found with the related keywords")

def for_donald_trump():
    print("Retreving tweets")
    api =tweepy.API(auth)
    Tweets = api.user_timeline(screen_name="@realdonaldtrump", count=200)  ###Search for tweets by the given screen name
    for data in Tweets:
        tweet = TextBlob(data.text)
        print(tweet)
        print(tweet.sentiment)
        print("Done at :" + str(data.created_at))
        print("Username :" + data.user.name)
        print("---------------------------------------------")
    query = []  ### Stores the keywords to be searched for
    tweets = []  ### to store the tweets
    tweets2 = []  ### to store modified tweets
    shows = True
    while shows:  ### to store the no of keywords till we want
        qw = input("Enter  the keywords ro be searched for :")
        query.append(qw)
        ask = input("Do you want to add more keywords?(Y/N)")
        ask = ask.upper()
        if ask == "Y":
            pass
        elif ask == "N":
            shows = False
        else:
            print("invalid input  \n"
                  "Taking default input as 'No' ")
            shows = False

    for data in Tweets:
        tweets.append(data)
    oldest = tweets[-1].id  ### stores the id of the last tweet retrieved
    oldest_at = tweets[-1].created_at  ### Stores the time and date of the last tweet retrieved
    qu = True
    while qu:  ###to retrieve more older tweets
        qu2 = input("Do you want  more  tweets older than " + str(oldest_at) + "(Y/N)  :")
        qu2 = qu2.upper()
        if qu2 == "Y":
            result = api.user_timeline(screen_name="@realdonaldtrump", count=200,
                                        max_id=oldest)  ###retrieve the tweet older then the given tweet id
            for data in result:
                tweets.append(data)  ###  appended the new tweets retrived
            oldest = tweets[-1].id
            oldest_at = tweets[-1].created_at
        elif qu2 == "N":
            qu = False
        else:
            print("invalid input  \n"
                  "Taking default input as 'No' ")
            qu = False
    count = -1
    for tweet1 in tweets:
        count = count + 1  ###starts the list from beginning
        tweet = tweet1.text
        tweet = re.sub(r"http\S+", "", tweet)  ##### removes the URL from the text of tweet
        tweets[count].text = tweet
    for keyword in query:
        for data in Tweets:
            tex = TextBlob(data.text)
            qw = tex.find(keyword)
            if qw != -1:
                tweets2.append(data)
            else:
                pass
    if len(tweets2) > 0:
        for data in tweets:
            tweet = TextBlob(data.text)
            print(tweet)
            print(tweet.sentiment)
            print("Done at :" + str(data.created_at))
            print("Username :" + data.user.name)
            print("---------------------------------------------")
    else:
        print("No tweet found with the related keywords")





def menu():
    user_choice = int(input("Enter the choice.\n""1.Search the tweets and count the no of person tweeted\n"
                            "2.Extract for a particular user \n"
                            "3.Sending a message\n"
                            "4.Tweet\n"
                            "5.Search for a specific keyword\n"
                            "6.Extract info about the tweets\n"
                            "7.Remove stopwords from tweets\n"
                            "8.Extract Tweets for Narender Modi \n"
                            "9.Extract Tweets for Donald Trump\n"
                            "10.Exit\n"
                            ))
    if user_choice == 1:
        search_tweet()
        q = input("Want to do more search (Y/N)??")
        q = q.upper()
        if q == "Y":
            search_tweet()
        else:
            pass

    elif user_choice == 2:
        extract_user()

    elif user_choice == 3:
        send_message()

    elif user_choice == 4:
        tweeting()

    elif user_choice == 5:
        search_keyword()

    elif user_choice == 6:
        extract_info()

    elif user_choice == 7:
        remove_stopwords()

    elif user_choice == 8:
        for_narendra_modi()

    elif user_choice ==9:
        for_donald_trump()

    else:
        pass
menu()



