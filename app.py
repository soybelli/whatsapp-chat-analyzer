import streamlit as st
import preprocessor, helper, sentiment, sentiment_plot
import matplotlib.pyplot as plt
import seaborn as sns
import base64


# Set page configuration
st.set_page_config(
    page_title="WhatsApp Chat Analyzer",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Add a title and description
st.title("WhatsApp Chat Analyzer")
st.write("Analyze your WhatsApp chat data.")

# Add a file uploader in the sidebar
uploaded_file = st.sidebar.file_uploader("Upload Chat File", type=["txt"])


if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    # ... (Rest of your code)
    user_list=df['user'].unique().tolist()
    try:
        user_list.remove('group_notification')
    except:
        user_list=user_list
    user_list.sort()
    user_list.insert(0,"OverAll")
    selected_user=st.sidebar.selectbox("Show analysis wrt",user_list)

    df=sentiment.fetch_sentiment(df)  # add sentiment data


    if st.sidebar.button("Show Analysis"):
        num_message, words ,num_media ,num_links = helper.fetch_stats(selected_user,df)

        # Apply responsive layout
        col1, col2 = st.columns([2, 3])


        sentiment_value,dict1=sentiment.sentiment_value(df)
        timeline = helper.monthly_timeline(selected_user,df)
        w=sentiment_plot.sentiment_plot()
        with col1:
            # Display total messages and other statistics
            st.header("Statistics")
            st.metric("Total Messages", num_message)
            st.metric("Total Words", words)
            st.metric("Total Media Shared", num_media)
            st.metric("Total Links Shared", num_links)

            # Display monthly timeline
            st.header("Monthly Timeline")
            fig, ax = plt.subplots()
            ax.plot(timeline['time'], timeline['message'], color='green')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            # Display sentiment analysis
            st.header("Sentiment Analysis")
            st.write(f"The sentiment value is {sentiment_value}")
            st.bar_chart(dict1)
            st.bar_chart(w)

        # ... (Rest of your code)
        if selected_user != 'OverAll':
            col1,col2=st.columns(2)
            with col1:
                st.title("Daily Timeline")
                daily_timeline = helper.daily_timeline(selected_user, df)
                fig, ax = plt.subplots()
                ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.header("Most busy day")
                busy_day = helper.week_activity_map(selected_user,df)
                fig,ax = plt.subplots()
                ax.bar(busy_day.index,busy_day.values,color='purple')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            st.title("Weekly Activity Map")
            user_heatmap = helper.activity_heatmap(selected_user,df)
            fig,ax = plt.subplots()
            ax = sns.heatmap(user_heatmap)
            st.set_option('deprecation.showPyplotGlobalUse', False)
            st.pyplot(fig)

        #finding the busy user
        col1,col2=st.columns(2)
                
        x,new_df=helper.most_busy_user(df)
        emoji_df=helper.emoji_help(selected_user,df)

        with col1:
            st.title("Most Busy User")
            fig, ax1 = plt.subplots()
            ax1.bar(x.index, x.values)
            fig.autofmt_xdate()
            st.pyplot(fig)
            
        with col2:
            st.title("Most Used Emojis")
            st.dataframe(emoji_df)
                    
            
        #wordcloud
        st.title("WordCloud")
        df_wc=helper.create_wordcloud(selected_user,df)
        fig,ax=plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        #most common word
        most_common_word=helper.most_common_words(selected_user,df)
        st.title("Most Common Words")
        fig, ax1 = plt.subplots()
        ax1.barh(most_common_word[0], most_common_word[1])
        fig.autofmt_xdate()
        st.pyplot(fig)

# Display footer
st.markdown(
    """
    <div style="text-align: center;">
    <p>Created with ❤️ by Soumya Samanta</p>
    </div>
    """,
    unsafe_allow_html=True,
)

