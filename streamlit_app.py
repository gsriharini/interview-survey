import streamlit as st
import pandas as pd
from datetime import datetime
from utils.survey_forms import CandidateSurvey, CompanySurvey
from utils.database import DatabaseManager

def initialize_session_state():
    """Initialize session state variables"""
    if 'page' not in st.session_state:
        st.session_state.page = 'welcome'
    if 'responses' not in st.session_state:
        st.session_state.responses = {}

def welcome_page():
    """Display welcome page and survey type selection"""
    st.title("Interview Process Optimization Survey")
    st.write("""
    Help us improve the technical interview process by sharing your experiences.
    Your feedback will contribute to developing an AI-ML based solution for more
    efficient and fair technical assessments.
    """)
    
    survey_type = st.radio(
        "Select your role:",
        ("Job Candidate", "Company Representative")
    )
    
    if st.button("Start Survey"):
        st.session_state.survey_type = survey_type
        st.session_state.page = 'survey'
        st.rerun()

def survey_page():
    """Display the actual survey form"""
    st.title("Interview Process Survey")
    
    # Initialize appropriate survey form
    if st.session_state.survey_type == "Job Candidate":
        survey = CandidateSurvey()
    else:
        survey = CompanySurvey()
    
    # Create form
    with st.form("survey_form"):
        responses = {}
        
        # Personal Information
        st.header("Personal Information")
        for field in survey.personal_info_fields:
            if field.type == "select":
                responses[field.name] = st.selectbox(
                    field.label,
                    field.options
                )
            else:
                responses[field.name] = st.text_input(field.label)
        
        # Experience Assessment
        st.header("Experience Assessment")
        for category in survey.assessment_categories:
            st.subheader(category.name)
            for question in category.questions:
                responses[question.id] = st.slider(
                    question.text,
                    1, 5,
                    help="1: Strongly Disagree, 5: Strongly Agree"
                )
        
        # Open Questions
        st.header("Open Questions")
        for question in survey.open_questions:
            responses[question.id] = st.text_area(question.text)
        
        # Submit button
        submitted = st.form_submit_button("Submit Survey")
        
        if submitted:
            # Validate responses
            errors = survey.validate_response(responses)
            if errors:
                for error in errors:
                    st.error(error)
            else:
                # Save response
                responses['timestamp'] = datetime.now()
                responses['survey_type'] = st.session_state.survey_type
                db = DatabaseManager()
                db.save_response(responses)
                
                st.session_state.page = 'thank_you'
                st.rerun()

def thank_you_page():
    """Display thank you message after survey completion"""
    st.title("Thank You!")
    st.write("""
    Thank you for completing the survey! Your responses will help us improve
    the technical interview process through AI-ML based solutions.
    """)
    st.balloons()
    
    if st.button("Start New Survey"):
        st.session_state.page = 'welcome'
        st.rerun()

def main():
    """Main application"""
    initialize_session_state()
    
    if st.session_state.page == 'welcome':
        welcome_page()
    elif st.session_state.page == 'survey':
        survey_page()
    elif st.session_state.page == 'thank_you':
        thank_you_page()

if __name__ == "__main__":
    main()