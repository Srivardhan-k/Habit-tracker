import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
load_dotenv('.env.local')

# --- Constants & Config ---
PAGE_TITLE = "Orbit - AI Habit Tracker"
PAGE_ICON = "🪐"

# Models
MODEL_FAST_RESPONSE = 'gemini-2.0-flash-lite-preview-02-05' # Updated to latest known or fallback to flash
MODEL_COMPLEX_TASK = 'gemini-2.0-flash' # Using Flash for chat as well for speed/cost in demo
MODEL_IMAGE_GEN = 'gemini-2.0-flash' # Placeholder, usually needs specialized model or Imagen
# Note: google-generativeai SDK might differ in model names compared to JS SDK. 
# We'll use standard Gemeni models available via the API.
# For Image generation, the Python SDK supports it via specialized calls or models. 
# We will use 'gemini-pro-vision' or similar for analysis, but for generation we might need to check capabilities.
# The JS app used 'gemini-3-pro-image-preview'. We'll try to stick to available models or mock if unavailable.
# Actually, for the purpose of this port, we will use 'gemini-2.0-flash' for text and check if it supports image gen (Imagen).
# If not, we might have to mock image generation or use a specific model if key allows.

APP_NAME = "Orbit"

# --- Types & State Management ---
if 'habits' not in st.session_state:
    st.session_state.habits = []

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = [
        {"role": "model", "text": "Hi! I'm Orbit, your personal productivity coach. How can I help you build better habits today?"}
    ]

if 'is_premium' not in st.session_state:
    st.session_state.is_premium = False

# --- Helper Functions ---
def init_gemini():
    api_key = os.getenv("API_KEY")
    if not api_key:
        st.error("API Key not found. Please set API_KEY in .env or .env.local")
        return None
    genai.configure(api_key=api_key)
    return True

def add_habit(title, goal=None):
    new_id = str(datetime.now().timestamp())
    new_habit = {
        'id': new_id,
        'title': title,
        'frequency': 'DAILY',
        'streak': 0,
        'completed_dates': [], # List of YYYY-MM-DD
        'created_at': datetime.now().isoformat(),
        'streak_goal': int(goal) if goal else None
    }
    st.session_state.habits.append(new_habit)

def toggle_habit(habit_id):
    today = datetime.now().strftime('%Y-%m-%d')
    for habit in st.session_state.habits:
        if habit['id'] == habit_id:
            if today in habit['completed_dates']:
                habit['completed_dates'].remove(today)
                # Recalculate streak (simple logic)
                habit['streak'] = max(0, habit['streak'] - 1) 
            else:
                habit['completed_dates'].append(today)
                habit['streak'] += 1
            break

def delete_habit(habit_id):
    st.session_state.habits = [h for h in st.session_state.habits if h['id'] != habit_id]

# --- UI Components ---

def render_sidebar():
    with st.sidebar:
        st.title(f"{PAGE_ICON} {APP_NAME}")
        
        # Navigation done via Tabs in Main, but we can put global actions here
        st.divider()
        
        if not st.session_state.is_premium:
            st.info("💎 Free Plan")
            if st.button("Upgrade to Pro", type="primary"):
                st.session_state.is_premium = True
                st.balloons()
                st.success("Upgraded to Pro!")
                st.rerun()
        else:
            st.success("💎 Premium Member")
            st.caption("Access to Gemini 1.5 Pro & 4K Vision Board")

        st.divider()
        st.caption("Powered by Google Gemini")

def render_habits_tab():
    st.header("Your Habits")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.caption("Track your daily progress")
    with col2:
        with st.popover("➕ New Habit"):
            new_habit_title = st.text_input("Habit Title", placeholder="e.g. Read 10 pages")
            new_habit_goal = st.number_input("Target Streak (Days)", min_value=1, value=30)
            
            # AI Suggestion
            if st.button("✨ AI Suggestion"):
                api_ready = init_gemini()
                if api_ready:
                    try:
                        model = genai.GenerativeModel('gemini-1.5-flash')
                        response = model.generate_content("Suggest 3 simple, actionable habits. Return only a list separated by commas.")
                        st.info(f"Suggestions: {response.text}")
                    except Exception as e:
                        st.error(f"AI Error: {e}")

            if st.button("Create Habit", type="primary", disabled=not new_habit_title):
                add_habit(new_habit_title, new_habit_goal)
                st.toast(f"Habit '{new_habit_title}' created!")
                st.rerun()

    if not st.session_state.habits:
        st.info("No habits yet. Start small!")
    else:
        today = datetime.now().strftime('%Y-%m-%d')
        for habit in st.session_state.habits:
            is_done = today in habit['completed_dates']
            
            # Custom Card Style using columns
            c1, c2, c3 = st.columns([0.1, 0.7, 0.2])
            
            with c1:
                # Checkbox trick: use button as toggle or actual checkbox
                # Streamlit checkbox state needs key/callback
                if st.checkbox("Done", value=is_done, key=f"check_{habit['id']}", label_visibility="collapsed"):
                    if not is_done: # Only toggle if changing to True (and vice versa logic needing state check)
                         # This is tricky in immediate mode. Better to check if changed.
                         # Actually `toggle_habit` handles logic. 
                         # We rely on on_change or just checking value after render?
                         pass
            
            # Since checkbox triggers rerun, we can check logic before/after or use on_change
            # Let's use a callback wrapper or just simple logic:
            # If UI state != data state, update data
            should_be_done = st.session_state[f"check_{habit['id']}"]
            if should_be_done != is_done:
                toggle_habit(habit['id'])
                st.rerun()

            with c2:
                title_style = "text-decoration: line-through; color: gray;" if is_done else "font-weight: bold;"
                st.markdown(f"<span style='{title_style}'>{habit['title']}</span>", unsafe_allow_html=True)
                st.caption(f"🔥 {habit['streak']} day streak | 🎯 Goal: {habit.get('streak_goal', '∞')}")
                
            with c3:
                if st.button("🗑️", key=f"del_{habit['id']}"):
                    delete_habit(habit['id'])
                    st.rerun()
            
            st.divider()

def render_analytics_tab():
    st.header("Analytics")
    if not st.session_state.habits:
        st.warning("Add habits to see analytics.")
        return

    # Basic dataframe
    data = []
    for h in st.session_state.habits:
        data.append({
            "Habit": h['title'],
            "Streak": h['streak'],
            "Completions": len(h['completed_dates'])
        })
    
    df = pd.DataFrame(data)
    
    st.subheader("Current Streaks")
    st.bar_chart(df.set_index("Habit")["Streak"])
    
    st.subheader("Total Completions")
    fig = px.pie(df, values='Completions', names='Habit', hole=0.4)
    st.plotly_chart(fig)

def render_coach_tab():
    st.header("AI Coach")
    
    if not st.session_state.is_premium and len(st.session_state.chat_history) > 4:
         st.warning("🔒 Free limit reached. Upgrade to Pro to chat more!")
         return

    # Display History
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.write(msg["text"])

    # Chat Input
    if prompt := st.chat_input("Ask Orbit..."):
        # Add User Message
        st.session_state.chat_history.append({"role": "user", "text": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        # Generate Response
        api_ready = init_gemini()
        if api_ready:
            try:
                # Convert history for Gemini
                history_for_api = [
                    {"role": "user" if m["role"] == "user" else "model", "parts": [m["text"]]}
                    for m in st.session_state.chat_history if m["role"] != "model" or m["text"] != "" # Skip initial or format check
                ]
                # Simplify: just send prompt with context for now or use ChatSession
                model = genai.GenerativeModel('gemini-1.5-pro') 
                # Note: History management in manual stream is tricky, let's just send prompt + simplified context
                
                chat = model.start_chat(history=[
                    {"role": m["role"], "parts": [m["text"]]} 
                    for m in st.session_state.chat_history[:-1] # Exclude last user msg which is new
                ])
                
                response = chat.send_message(prompt)
                
                # Add AI Message
                st.session_state.chat_history.append({"role": "model", "text": response.text})
                with st.chat_message("model"):
                    st.write(response.text)
                    
            except Exception as e:
                st.error(f"Error: {e}")

def render_vision_tab():
    st.header("Vision Board")
    
    if not st.session_state.is_premium:
         st.info("🔒 Vision Board generation is a Pro feature.")
         st.markdown("Unlock **4K Image Generation** with Gemini Pro Vision.")
         return

    prompt = st.text_area("Describe your ideal future...", placeholder="A peaceful minimalist office with plants and a view of the mountains...")
    
    if st.button("Generate Vision"):
        api_ready = init_gemini()
        if api_ready:
            try:
                st.info("Generating image (Mocking Gemini Image Gen)...")
                # Real Image Gen call would go here. 
                # genai.GenerativeModel('imagen-3.0-generate-001') # Example
                # For this demo, we'll just check if we can call text model to simulate 'creative' text 
                # or actually call image model if available.
                # Since image generation requires specific setup/whitelist, we will simulate or use placeholder.
                
                # Let's try to fetch a placeholder from unsplash based on keywords using a simple request or just text.
                st.image("https://images.unsplash.com/photo-1484480974693-6ca0a78fb36b?auto=format&fit=crop&q=80&w=2072", caption="Vision Board (Mock)")
                st.success("Vision generated! (Simulated for this demo)")
                
            except Exception as e:
                st.error(f"Error: {e}")

# --- Main App ---
def main():
    st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON, layout="centered")
    
    render_sidebar()
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["Habits", "Analytics", "AI Coach", "Vision Board"])
    
    with tab1:
        render_habits_tab()
    with tab2:
        render_analytics_tab()
    with tab3:
        render_coach_tab()
    with tab4:
        render_vision_tab()

if __name__ == "__main__":
    main()
