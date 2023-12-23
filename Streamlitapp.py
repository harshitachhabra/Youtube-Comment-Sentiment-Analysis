import streamlit as st
from googleapiclient.discovery import build
#from google_auth_oauthlib.flow import InstalledAppFlow
from textblob import TextBlob

# Set up YouTube API
API_KEY = 'AIzaSyAQAwg9uaqDqpGrNh-cuChYygevgjvDXgU'
youtube = build('youtube', 'v3', developerKey=API_KEY)

# Function to analyze sentiment
def analyze_sentiment(text):
    blob = TextBlob(text)
    # Classify as positive, negative, or neutral
    if blob.sentiment.polarity > 0:
        return 'positive'
    elif blob.sentiment.polarity < 0:
        return 'negative'
    else:
        return 'neutral'

# Streamlit app
st.title("YouTube Video Sentiment Analysis")

# Get video URL from the user
video_url = st.text_input("Enter YouTube Video URL:")

# Process video URL
if video_url:
    try:
        # Extract video ID from URL
        video_id = video_url.split("v=")[1]
        video_id = video_id.split('&')[0]
        st.write("video id: ",video_id)

        # Get video details
        video_response = youtube.videos().list(part='snippet', id=video_id).execute()

        # Check if the response contains items
        if 'items' in video_response and video_response['items']:
            video_title = video_response['items'][0]['snippet']['title']
            st.write(f"Video Title: {video_title}")

            # Get video comments
            comments_response = youtube.commentThreads().list(part='snippet', videoId=video_id, textFormat='plainText').execute()
            comments = [item['snippet']['topLevelComment']['snippet']['textDisplay'] for item in comments_response['items']]

            # Analyze sentiment of comments
            sentiments = [analyze_sentiment(comment) for comment in comments]
            positive_percentage = sum(1 for sentiment in sentiments if sentiment == 'positive') / len(sentiments) * 100
            negative_percentage = sum(1 for sentiment in sentiments if sentiment == 'negative') / len(sentiments) * 100
            neutral_percentage = sum(1 for sentiment in sentiments if sentiment == 'neutral') / len(sentiments) * 100
            # Display results
            st.subheader("Sentiment Analysis Results:")
            st.success(f"Positive Sentiment: {positive_percentage:.2f}%")
            st.error(f"Negative Sentiment: {negative_percentage:.2f}%")
            st.info(f"Neutral Sentiment: {neutral_percentage:.2f}%")

            # Display comments
            st.subheader("Sample Comments:")
            for i, comment in enumerate(comments[:5]):
                    st.write(f"{i + 1}. {comment}")
        else:
            st.write("Error: Unable to retrieve video details. Please check the video URL.")
    except Exception as e:
        st.write(f"An error occurred: {e}")
    #st.write("Video API Response:", video_response)
