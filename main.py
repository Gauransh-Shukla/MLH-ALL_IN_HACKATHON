import base64
import streamlit as st
from database import create_db, insert_into_db, insert_goal, get_goals
from utils import get_daily_affirmation, sentiment_analysis
import pandas as pd
import sqlite3
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from textblob import TextBlob
import random

# Theme customization MUST be the first streamlit command.
st.set_page_config(
    page_title="CBT Assistant App",
    layout="centered",
    initial_sidebar_state="expanded",
    page_icon=None,
)

# Custom CSS for styling
st.markdown("""
    <style>
        body {
            color: #4A4A4A;
            background-color: #E5E5E5;
        }
        .reportview-container .main .block-container {
            background-color: #ffffff;
            padding: 10px 30px;
            border-radius: 10px;
            box-shadow: 0 3px 6px rgba(0, 0, 0, 0.1);
            transition: box-shadow .2s ease-in-out, transform .2s ease-in-out;
        }
        .stButton>button {
            display: block;
            margin: 20px auto;
            background-color: #0E5F76;
            color: #E5E5E5;
        }
    </style>
    """, unsafe_allow_html=True)

# Main App
def main():

    

    menu_options = ['Home', 'Thought Record', 'Visualize Data', 'Feedback', 'About CBT', 'Resources', 'Goal Setting']
    choice = st.sidebar.radio("Navigate to:", menu_options)


    if choice == 'Home':
        st.header('Welcome to the CBT App!')
        
        st.write('This app assists you with Cognitive Behavioral Therapy (CBT) exercises and helps track your emotions and thoughts over time.')
        st.subheader("Today's Affirmation:")
        st.markdown(f'*{get_daily_affirmation()}*')
        st.image("https://static.wixstatic.com/media/0a03f9_f75a5674fab84d6790b67d00de7eceb1~mv2.png/v1/fill/w_767,h_512,al_c,q_90,usm_0.66_1.00_0.01,enc_auto/0a03f9_f75a5674fab84d6790b67d00de7eceb1~mv2.png", use_column_width=True, caption="CBT Assistant")

    elif choice == 'Thought Record':
        st.header('Thought Record')
        situation = st.text_input('Describe the situation:')
        feeling = st.text_input('Describe your feeling:')
        thought = st.text_input('What was the automatic thought?')
        evidence_for = st.text_area('Evidence supporting the thought:')
        evidence_against = st.text_area('Evidence against the thought:')
        alternative_thought = st.text_input('Alternative balanced thought:')
       
        if st.button('Submit Thought Record'):
            insert_into_db(situation, feeling, thought, evidence_for, evidence_against, alternative_thought)
            st.success('Thought record saved!')
            
            sentiment = sentiment_analysis(thought)
            st.write(f'Sentiment of your thought: **{sentiment}**')

    elif choice == 'Visualize Data':
        st.header('Data Visualization')
        conn = sqlite3.connect('cbt_app.db')
        df = pd.read_sql_query("SELECT * from thought_record", conn)
        st.set_option('deprecation.showPyplotGlobalUse', False)
        # Bar Plot of Feelings
        feelings_count = df['feeling'].value_counts()
        fig_feelings = px.bar(feelings_count, x=feelings_count.index, y=feelings_count.values, title='Frequency of Feelings')
        st.plotly_chart(fig_feelings)
        
        # Word Cloud of Situations
        situations_text = ' '.join(df['situation'])
        wordcloud = WordCloud(background_color='white', max_words=100, contour_width=3, contour_color='steelblue')
        wordcloud.generate(situations_text)

        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        st.pyplot()

    elif choice == 'Feedback':
        st.image("https://unbridlingyourbrilliance.com/wp-content/uploads/2019/07/feedback-1.jpg", use_column_width=True, caption="")
        st.header('Feedback')
        
        feedback = st.text_area('Provide your feedback:')
        if st.button('Submit Feedback'):
            st.success('Thanks for your feedback!')

    elif choice == 'About CBT':
        st.header('About CBT')
        
        st.write("""
        Cognitive Behavioral Therapy (CBT) is a psycho-social intervention that aims to improve mental health. 
        It focuses on challenging and changing unhelpful cognitive distortions and behaviors, improving emotional regulation, 
        and the development of personal coping strategies that target solving current problems.
        """)
        st.image("https://media.post.rvohealth.io/wp-content/uploads/sites/4/2022/05/264290-basic-principles-of-cognitive-behavioral-therapy_1296x1181-938x1024.jpg", use_column_width=True, caption="")

    elif choice == 'Goal Setting':
        st.header('Goal Setting')
        st.subheader('Set your mental well-being goals')
        goal = st.text_input('Your Goal:')
        if st.button('Set Goal'):
            insert_goal(goal)
            st.success(f'Goal "{goal}" set successfully!')
        #st.image("https://direct-therapy.org.uk/wp-content/uploads/2020/12/What-are-the-three-primary-goals-in-cognitive-therapy.png", use_column_width=True, caption="")
        st.subheader('Your Goals')
        goals = get_goals()
        for goal in goals:
            st.write("- " + goal)

    elif choice == 'Resources':
        st.header('Resources')
        st.image("https://www.mentalwellnesscentre.com/wp-content/uploads/2023/09/Cognitive-Behavioural-Therapy-India.jpg", caption="")
        st.write('Here are some resources about CBT...')
        st.markdown("[CBT Techniques and Benefits](https://www.verywellmind.com/what-is-cognitive-behavior-therapy-2795747)")
        st.markdown("[Understanding Mental Well-being](https://www.mentalhealth.gov/basics/what-is-mental-health)")
        st.markdown("[Techniques to Stay Calm](https://www.healthline.com/health/how-to-calm-down)")

    # Adding an option to export data
    if st.sidebar.button('Export Thought Records'):
        conn = sqlite3.connect('cbt_app.db')
        df = pd.read_sql_query("SELECT * from thought_record", conn)
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="thought_records.csv">Download Thought Records CSV File</a>'
        st.sidebar.markdown(href, unsafe_allow_html=True)

if __name__ == "__main__":
    create_db()
    main()