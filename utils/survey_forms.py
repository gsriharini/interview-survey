from dataclasses import dataclass
from typing import List, Optional, Dict, Any

@dataclass
class Field:
    name: str
    label: str
    type: str
    options: Optional[List[str]] = None
    required: bool = True

@dataclass
class Question:
    id: str
    text: str
    required: bool = True

@dataclass
class Category:
    name: str
    questions: List[Question]

class BaseSurvey:
    def __init__(self):
        self.personal_info_fields: List[Field] = []
        self.assessment_categories: List[Category] = []
        self.open_questions: List[Question] = []
        
    def validate_response(self, responses: Dict[str, Any]) -> List[str]:
        """
        Validate survey responses
        
        Args:
            responses: Dictionary of responses
            
        Returns:
            List[str]: List of validation error messages
        """
        errors = []
        
        # Validate personal info
        for field in self.personal_info_fields:
            if field.required and not responses.get(field.name):
                errors.append(f"{field.label} is required")
        
        # Validate assessment questions
        for category in self.assessment_categories:
            for question in category.questions:
                if question.required and not responses.get(question.id):
                    errors.append(f"Please answer: {question.text}")
        
        # Validate open questions
        for question in self.open_questions:
            if question.required and not responses.get(question.id):
                errors.append(f"Please answer: {question.text}")
        
        return errors

class CandidateSurvey(BaseSurvey):
    def __init__(self):
        super().__init__()
        
        # Personal Information
        self.personal_info_fields = [
            Field("age_group", "Age Group", "select", 
                  ["20-25", "26-30", "31-35", "36+"]),
            Field("experience", "Experience Level", "select",
                  ["Fresher", "1-3 years", "4-6 years", "7+ years"]),
            Field("industry", "Industry", "select",
                  ["Technology", "Finance", "Healthcare", "Other"]),
            Field("role", "Current/Target Role", "text")
        ]
        
        # Assessment Categories
        self.assessment_categories = [
            Category("Time and Logistics", [
                Question("waiting_time", "The waiting time at interview venues is too long"),
                Question("travel_time", "Travel to multiple interview locations is time-consuming"),
                Question("scheduling", "Interview scheduling conflicts with current work commitments"),
                Question("process_duration", "The entire interview process takes too many days/weeks")
            ]),
            Category("Technical Assessment", [
                Question("tech_env", "Technical assessment environments don't reflect real work scenarios"),
                Question("time_pressure", "Limited time in coding tests creates unnecessary pressure"),
                Question("platform_restrictions", "Online coding platforms are often restrictive"),
                Question("multiple_rounds", "Multiple rounds of technical assessment are repetitive")
            ]),
            Category("Communication", [
                Question("status_updates", "Lack of clear communication about interview status"),
                Question("recruiter_response", "Delayed responses from recruiters"),
                Question("process_clarity", "Unclear information about interview rounds"),
                Question("feedback", "Poor feedback about rejection reasons")
            ])
        ]
        
        # Open Questions
        self.open_questions = [
            Question("biggest_challenge", "What is your biggest challenge in the current interview process?"),
            Question("time_spent", "How much time on average do you spend preparing for and attending interviews?"),
            Question("suggestions", "What improvements would you suggest for the technical assessment process?"),
            Question("standardized_assessment", "Would you prefer a standardized technical assessment valid across multiple companies? Why?")
        ]

class CompanySurvey(BaseSurvey):
    def __init__(self):
        super().__init__()
        
        # Company Information
        self.personal_info_fields = [
            Field("company_size", "Company Size", "select",
                  ["<100", "100-500", "501-1000", "1000+"]),
            Field("industry", "Industry", "select",
                  ["Technology", "Finance", "Healthcare", "Other"]),
            Field("hiring_volume", "Average Annual Hires", "select",
                  ["<10", "10-50", "51-100", "100+"]),
            Field("role", "Your Role in Hiring", "text")
        ]
        
        # Assessment Categories
        self.assessment_categories = [
            Category("Resource Management", [
                Question("screening_time", "Significant time spent on initial screening"),
                Question("cost_per_hire", "High cost per hire due to multiple rounds"),
                Question("coordination", "Difficulty in coordinating interviews"),
                Question("evaluation_standards", "Challenge in maintaining consistent standards")
            ]),
            Category("Technical Assessment", [
                Question("test_creation", "Difficulty in creating standardized assessments"),
                Question("plagiarism", "Challenge in preventing plagiarism/cheating"),
                Question("evaluation_time", "Time consumed in evaluating assignments"),
                Question("skill_assessment", "Struggle with practical vs theoretical assessment")
            ]),
            Category("Process Efficiency", [
                Question("unsuitable_candidates", "Too much time spent on unsuitable candidates"),
                Question("dropout_rate", "High candidate drop-off during process"),
                Question("scheduling_issues", "Difficulty in scheduling multiple interviews"),
                Question("scaling_quality", "Challenge in maintaining quality while scaling")
            ])
        ]
        
        # Open Questions
        self.open_questions = [
            Question("biggest_challenge", "What is your biggest challenge in the current recruitment process?"),
            Question("time_per_hire", "How many hours on average does your team spend per hire?"),
            Question("automation_aspects", "What aspects of candidate evaluation would you like to automate?"),
            Question("ai_trust", "Would you trust an AI-based initial screening system? Why or why not?")
        ]