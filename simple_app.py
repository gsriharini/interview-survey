import streamlit as st
from datetime import datetime

def initialize_session_state():
    if 'page' not in st.session_state:
        st.session_state.page = 'welcome'
    if 'all_responses' not in st.session_state:
        st.session_state.all_responses = []

def get_candidate_questions():
    return {
        'personal_info': [
            {'name': 'age_group', 'label': 'Age Group', 'type': 'select', 
             'options': ["20-25", "26-30", "31-35", "36+"]},
            {'name': 'experience', 'label': 'Experience Level', 'type': 'select',
             'options': ["Fresher", "1-3 years", "4-6 years", "7+ years"]},
            {'name': 'industry', 'label': 'Industry', 'type': 'select',
             'options': ["Technology", "Finance", "Healthcare", "Other"]}
        ],
        'assessment': [
            {'id': 'waiting_time', 'text': 'The waiting time at interview venues is too long'},
            {'id': 'travel_time', 'text': 'Travel to multiple interview locations is time-consuming'},
            {'id': 'scheduling', 'text': 'Interview scheduling conflicts with current work commitments'},
            {'id': 'tech_env', 'text': 'Technical assessment environments don\'t reflect real work scenarios'}
        ],
        'open_questions': [
            {'id': 'biggest_challenge', 'text': 'What is your biggest challenge in the current interview process?'},
            {'id': 'suggestions', 'text': 'What improvements would you suggest for the technical assessment process?'}
        ]
    }

def get_company_questions():
    return {
        'personal_info': [
            {'name': 'company_size', 'label': 'Company Size', 'type': 'select',
             'options': ["<100", "100-500", "501-1000", "1000+"]},
            {'name': 'industry', 'label': 'Industry', 'type': 'select',
             'options': ["Technology", "Finance", "Healthcare", "Other"]},
            {'name': 'role', 'label': 'Your Role in Hiring', 'type': 'text'}
        ],
        'assessment': [
            {'id': 'screening_time', 'text': 'Significant time spent on initial screening'},
            {'id': 'cost_per_hire', 'text': 'High cost per hire due to multiple rounds'},
            {'id': 'coordination', 'text': 'Difficulty in coordinating interviews'},
            {'id': 'plagiarism', 'text': 'Challenge in preventing plagiarism/cheating'}
        ],
        'open_questions': [
            {'id': 'biggest_challenge', 'text': 'What is your biggest challenge in the current recruitment process?'},
            {'id': 'automation_aspects', 'text': 'What aspects of candidate evaluation would you like to automate?'}
        ]
    }

def welcome_page():
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
    st.title("Interview Process Survey")
    
    # Get appropriate questions
    questions = get_candidate_questions() if st.session_state.survey_type == "Job Candidate" else get_company_questions()
    
    with st.form("survey_form"):
        responses = {}
        
        # Personal Information
        st.header("Personal Information")
        for field in questions['personal_info']:
            if field['type'] == 'select':
                responses[field['name']] = st.selectbox(
                    field['label'],
                    field['options']
                )
            else:
                responses[field['name']] = st.text_input(field['label'])
        
        # Experience Assessment
        st.header("Experience Assessment")
        for question in questions['assessment']:
            responses[question['id']] = st.slider(
                question['text'],
                1, 5,
                help="1: Strongly Disagree, 5: Strongly Agree"
            )
        
        # Open Questions
        st.header("Open Questions")
        for question in questions['open_questions']:
            responses[question['id']] = st.text_area(question['text'])
        
        submitted = st.form_submit_button("Submit Survey")
        
        if submitted:
            responses['timestamp'] = str(datetime.now())
            responses['survey_type'] = st.session_state.survey_type
            st.session_state.all_responses.append(responses)
            st.session_state.page = 'thank_you'
            st.rerun()

def thank_you_page():
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
    initialize_session_state()
    
    if st.session_state.page == 'welcome':
        welcome_page()
    elif st.session_state.page == 'survey':
        survey_page()
    elif st.session_state.page == 'thank_you':
        thank_you_page()

if __name__ == "__main__":
    main()
