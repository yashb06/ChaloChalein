import streamlit as st
import sys
sys.path.append("c:/Users/DARSHAN/OneDrive - somaiya.edu/Desktop/ChaloChalein")

from components.authentication import show_auth_page
from components.homepage import show_homepage
from components.chatbot import show_chatbot
from components.map_view import show_map
from firebase_admin import auth
import firebase_admin
from firebase_admin import credentials
import requests
from components.trips import show_trips

st.set_page_config(
    page_title="AI Travel Planner",
    page_icon="✈️",
    layout="wide"
)

st.markdown("""
    <style>
    .sidebar .sidebar-content {
        background-color: #004f32;
    }
    
    .sidebar-text {
        color: white !important;
        font-size: 1.2rem !important;
        padding: 0.5rem 0;
        margin: 0.5rem 0;
    }
    
    .sidebar-button {
        background-color: transparent;
        color: white;
        border: 1px solid white;
        border-radius: 20px;
        padding: 0.5rem 1rem;
        margin: 0.5rem 0;
        width: 100%;
        transition: all 0.3s;
    }
    
    .sidebar-button:hover {
        background-color: white;
        color: #004f32;
    }
    
    .user-info {
        background-color: rgba(255, 255, 255, 0.1);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    
    .separator {
        height: 1px;
        background-color: rgba(255, 255, 255, 0.2);
        margin: 1rem 0;
    }
    
    .logo-text {
        font-size: 1.5rem;
        font-weight: bold;
        color: white;
        text-align: center;
        padding: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)
if 'firebase_initialized' not in st.session_state:
    try:
        cred = credentials.Certificate("streamlit/chalochalein-1ba3c-firebase-adminsdk-fbsvc-0c3d443ca8.json")
        default_app = firebase_admin.initialize_app(cred)
        st.session_state.firebase_initialized = True
    except ValueError as e:
        st.session_state.firebase_initialized = True
        pass

def main():
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'page' not in st.session_state:
        st.session_state.page = 'home'
    with st.sidebar:
        st.markdown('<div class="logo-text">✈️ AI Travel Planner</div>', unsafe_allow_html=True)
        st.markdown('<div class="separator"></div>', unsafe_allow_html=True)

        if st.session_state.user:
            st.markdown(
                f'''
                <div class="user-info">
                    <div style="color: white;">
                        <i class="fas fa-user"></i> Welcome,
                        <br/>
                        {st.session_state.user['email']}
                    </div>
                </div>
                ''',
                unsafe_allow_html=True
            )

            col1, col2 = st.columns(2)
            with col1:
                if st.button("🏠 Home", key="home_btn", help="Go to homepage", use_container_width=True):
                    st.session_state.page = 'home'
                    st.rerun()
            with col2:
                if st.button("✈️ Plan Trip", key="plan_btn", help="Start planning your trip", use_container_width=True):
                    st.session_state.page = 'chatbot'
                    st.rerun()

            if st.button("🗺️ My Trips", key="trips_btn", help="View your saved trips", use_container_width=True):
                st.session_state.page = 'trips'
                st.rerun()
                
            st.markdown('<div class="separator"></div>', unsafe_allow_html=True)

            if st.button("🚪 Logout", key="logout_btn", help="Sign out from your account", use_container_width=True):
                st.session_state.user = None
                st.session_state.page = 'home'
                st.rerun()

    if st.session_state.page == 'home':
        show_homepage() 
    elif st.session_state.page == 'auth':
        show_auth_page()
    elif st.session_state.page == 'chatbot' and st.session_state.user:
        show_chatbot()
    elif st.session_state.page == 'trips' and st.session_state.user:
        show_trips()
    else:
        st.warning("Please login to access this feature")
        show_auth_page()

if __name__ == "__main__":
    main()
