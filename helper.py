from urlextract import URLExtract
extract=URLExtract()
from wordcloud import WordCloud
import pandas as pd
import emoji
from collections import Counter


def fetch_stats(selected_user,df):
    if selected_user != 'OverAll':
        df = df[df['user'] == selected_user]

    df['message'].to_csv('data.txt', index=False)
    num_message=df.shape[0]
    words=[]
    for message in df['message']:
        words.extend(message.split())

    words_size=len(words)

    links=[]
    for message in df['message']:
        links.extend(extract.find_urls(message))

    num_media=df[df['message'] == '<Media omitted>\n'].shape[0]
    return num_message, words_size, num_media, len(links)

def most_busy_user(df):
    x=df['user'].value_counts().head()
    new_df=round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'index':'user','user':'percent'})
    return x,new_df

def create_wordcloud(selected_user,df):
    f=open('stop_words.txt','r')
    stop_words=f.read()

    if selected_user != 'OverAll':
        df=df[df['user']==selected_user]

    temp=df[df['user']!='group_notification']
    temp=temp[temp['message']!='<Media omitted>\n']

    def remove_stop_words(message):
        y=[]
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    wc=WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    temp['message']=temp['message'].apply(remove_stop_words)
    df_wc=wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc

def most_common_words(selected_user,df):
    f=open('stop_words.txt','r')
    stop_words=f.read()

    if selected_user != 'OverAll':
        df=df[df['user']==selected_user]

    temp=df[df['user']!='group_notification']
    temp=temp[temp['message']!='<Media omitted>\n']

    words=[]
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_word=pd.DataFrame(Counter(words).most_common(20))

    return most_common_word

def emoji_help(selected_user,df):
    if selected_user != 'OverAll':
        df=df[df['user']==selected_user]


    words=[]
    for messages in df['message']:
        words.extend(messages.split())

    mystr=""
    for x in words:
        mystr=mystr + " "+ x
    mystr

    #now we have to put this string into the emoji function

    myemoji=emoji.emoji_list(mystr)

    #now we have to extract each emoji from this type of list

    pre_final_emoji_list=[]
    for i in range(len(myemoji)):
        pre_final_emoji_list.extend(myemoji[i]['emoji'])


    emojis_to_be_removed=[' ','🏻']

    final_emoji_list=[]
    for items in pre_final_emoji_list:
        if items not in emojis_to_be_removed:
            final_emoji_list.append(items)


    emoji_df=pd.DataFrame(Counter(final_emoji_list).most_common(10))
    return emoji_df.head(7).rename(columns={0:'emoji',1:'count'})

def monthly_timeline(selected_user,df):

    if selected_user != 'OverAll':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline

def week_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    if selected_user == 'Overall':
        return df['day_name'].value_counts()
    else:
        return df['day_name'].value_counts().reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], fill_value=0)

def activity_heatmap(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    if df.empty:
        print("No data available for the selected user.")
        return None  # or return an appropriate value

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return user_heatmap

def daily_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline