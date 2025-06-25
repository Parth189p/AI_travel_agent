# pylint: disable = invalid-name
import os
import uuid

import streamlit as st
from langchain_core.messages import HumanMessage

from agents.agent import Agent


def populate_envs(sender_email, receiver_email, subject):
    os.environ['FROM_EMAIL'] = sender_email
    os.environ['TO_EMAIL'] = receiver_email
    os.environ['EMAIL_SUBJECT'] = subject


def send_email(sender_email, receiver_email, subject, thread_id):
    try:
        populate_envs(sender_email, receiver_email, subject)
        config = {'configurable': {'thread_id': thread_id}}
        st.session_state.agent.graph.invoke(None, config=config)
        st.success('Email sent successfully!')
        # Clear session state
        for key in ['travel_info', 'thread_id']:
            st.session_state.pop(key, None)
    except Exception as e:
        st.error(f'Error sending email: {e}')


def initialize_agent():
    if 'agent' not in st.session_state:
        st.session_state.agent = Agent()


def render_custom_css():
    st.markdown(
        '''
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
        
        .stApp {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            font-family: 'Poppins', sans-serif;
        }
        
        .main-container {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            padding: 2rem;
            margin: 1rem;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(10px);
        }
        
        .main-title {
            font-size: 3em;
            color: #2c3e50;
            text-align: center;
            margin-bottom: 0.5em;
            font-weight: 700;
            font-family: 'Poppins', sans-serif;
        }
        
        .subtitle {
            font-size: 1.3em;
            color: #34495e;
            text-align: center;
            margin-bottom: 2em;
            font-weight: 400;
        }
        

        
        .travel-info-container {
            background: #f8f9fa;
            border-radius: 15px;
            padding: 2rem;
            margin: 1rem 0;
            border-left: 5px solid #3498db;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
        }
        
        .email-form-container {
            background: #f8f9fa;
            border-radius: 15px;
            padding: 2rem;
            margin: 1rem 0;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
        }
        
        .stButton > button {
            background: linear-gradient(45deg, #3498db, #2980b9);
            color: white;
            border: none;
            border-radius: 25px;
            padding: 0.75rem 2rem;
            font-size: 1.1em;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 5px 15px rgba(52, 152, 219, 0.4);
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(52, 152, 219, 0.6);
        }
        
        .stTextArea > div > div > textarea {
            border-radius: 15px;
            border: 2px solid #e0e0e0;
            font-size: 1.1em;
            transition: all 0.3s ease;
        }
        
        .stTextArea > div > div > textarea:focus {
            border-color: #3498db;
            box-shadow: 0 0 10px rgba(52, 152, 219, 0.3);
        }
        
        .stTextInput > div > div > input {
            border-radius: 10px;
            border: 2px solid #e0e0e0;
            transition: all 0.3s ease;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: #3498db;
            box-shadow: 0 0 10px rgba(52, 152, 219, 0.3);
        }
        
        .hero-section {
            text-align: center;
            padding: 2rem 0;
        }
        
        .stats-container {
            display: flex;
            justify-content: space-around;
            margin: 2rem 0;
        }
        
        .stat-item {
            text-align: center;
            padding: 1rem;
        }
        
        .stat-number {
            font-size: 2em;
            font-weight: 700;
            color: #3498db;
        }
        
        .stat-label {
            font-size: 0.9em;
            color: #2c3e50;
            font-weight: 400;
        }
        </style>
        ''', unsafe_allow_html=True)


def render_hero_section():
    st.markdown('''
        <div class="hero-section">
            <div class="main-title">✈️🌍 AI Travel Agent 🏨🗺️</div>
            <div class="subtitle">Your intelligent companion for seamless travel planning</div>
        </div>
    ''', unsafe_allow_html=True)


def render_query_section():
    st.markdown("### 🔍 Enter your travel query and get flight and hotel information:")
    
    # Create columns for better layout
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col2:
        user_input = st.text_area(
            'Travel Query',
            height=150,
            key='query',
            placeholder='Type your travel query here...',
        )
        
        search_button = st.button('Get Travel Information', type='primary', use_container_width=True)
    
    return user_input, search_button


def process_query(user_input):
    if user_input:
        try:
            with st.spinner('Searching for travel information...'):
                thread_id = str(uuid.uuid4())
                st.session_state.thread_id = thread_id

                messages = [HumanMessage(content=user_input)]
                config = {'configurable': {'thread_id': thread_id}}

                result = st.session_state.agent.graph.invoke({'messages': messages}, config=config)

                st.markdown('''
                    <div class="travel-info-container">
                        <h3 style="color: #2c3e50; margin-bottom: 1rem;">Travel Information</h3>
                    </div>
                ''', unsafe_allow_html=True)
                
                st.write(result['messages'][-1].content)
                st.session_state.travel_info = result['messages'][-1].content

        except Exception as e:
            st.error(f'Error: {e}')
    else:
        st.warning('Please enter a travel query to get started.')


def render_email_form():
    st.markdown('''
        <div class="email-form-container">
            <h3 style="color: #2c3e50; text-align: center; margin-bottom: 1rem;">Do you want to send this information via email?</h3>
        </div>
    ''', unsafe_allow_html=True)
    
    send_email_option = st.radio(
        '', 
        ('No', 'Yes'),
        horizontal=True
    )
    
    if send_email_option == 'Yes':
        with st.form(key='email_form'):
            col1, col2 = st.columns(2)
            
            with col1:
                receiver_email = st.text_input('Receiver Email', placeholder='recipient@example.com')
            
            with col2:
                subject = st.text_input('Email Subject', value='Travel Information')
            
            submit_button = st.form_submit_button(
                label='Send Email', 
                type='primary',
                use_container_width=True
            )

        if submit_button:
            sender_email = os.environ.get('SMTP_USERNAME', 'parth.cilans@gmail.com')
            if sender_email and receiver_email and subject:
                with st.spinner('Sending email...'):
                    send_email(sender_email, receiver_email, subject, st.session_state.thread_id)
            else:
                st.error('Please fill out all email fields.')


def render_footer():
    st.markdown('''
        <div style="text-align: center; padding: 2rem; color: #666; border-top: 1px solid #eee; margin-top: 3rem;">
            <p>🤖 Powered by Advanced AI Technology | Built for seamless travel experiences</p>
        </div>
    ''', unsafe_allow_html=True)


def main():
    # Configure page
    st.set_page_config(
        page_title="AI Travel Agent",
        page_icon="✈️",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    initialize_agent()
    render_custom_css()
    
    # Main container
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # Hero section
    render_hero_section()
    
    # Query section
    user_input, search_button = render_query_section()
    
    # Process query when button is clicked
    if search_button:
        process_query(user_input)
    
    # Show email form if travel info exists
    if 'travel_info' in st.session_state:
        render_email_form()
    
    # Footer
    render_footer()
    
    st.markdown('</div>', unsafe_allow_html=True)


if __name__ == '__main__':
    main()