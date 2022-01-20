from tweepy import Cursor
from twitter_client import get_twitter_client
import pandas as pd

def usage():
    print("Usage:")
    print("python {} <username>".format(sys.argv[0]))

# Twitter API only provides your last 2k favorites or so. Save them to a csv in order to archive as much as you can.

if __name__ == '__main__':
    client = get_twitter_client()

    df_favs = pd.DataFrame(columns=['id','user','created_at','text','favorite_count','retweet_count','source'])

    for pg in range(1271): # When appending, this value might be smaller depending on the amout of tweets 
        print (pg)
        result_set = client.get_favorites(id='your_username',page=pg)
        for status in result_set:
            tweet = {'id': status.id,
                     'user': status.user.screen_name,
                     'created_at': status.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                     'text': status.text.replace('\n',''),
                     'favorite_count': status.favorite_count,
                     'retweet_count': status.retweet_count,
                     'source': status.source}
            print(tweet['created_at'])
            df_favs = df_favs.append(tweet,ignore_index=True)

    # On first execution, comment line 31 and leave 30
    # After you already have a csv, and only appends to it, comment line 30 and leave 31
    df_favs.to_csv('my-twitter-favs.csv', index=False)
    df_favs.to_csv('my-twitter-favs.csv', mode='a', header=False, index=False)

    df_clean = pd.read_csv(r'my-twitter-favs.csv',skipinitialspace=True)
    df_clean=df_clean.drop_duplicates(subset=['id'], keep='last')
    df_clean=df_clean.sort_values(by=['created_at'], ascending=False)
    df_clean.to_csv(r'my-twitter-favs.csv',index=False)
