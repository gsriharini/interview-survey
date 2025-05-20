import json
from datetime import datetime
from pathlib import Path
import pandas as pd
from typing import Dict, Any

class DatabaseManager:
    def __init__(self):
        self.responses_dir = Path("data/responses")
        self.responses_dir.mkdir(parents=True, exist_ok=True)
        
    def save_response(self, response_data: Dict[str, Any]) -> str:
        """
        Save survey response to JSON file
        
        Args:
            response_data: Dictionary containing survey response
            
        Returns:
            str: Filename of saved response
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"response_{timestamp}.json"
        
        with open(self.responses_dir / filename, "w") as f:
            json.dump(response_data, f, default=str)
            
        return filename
    
    def get_all_responses(self) -> pd.DataFrame:
        """
        Read all responses into a pandas DataFrame
        
        Returns:
            pd.DataFrame: DataFrame containing all survey responses
        """
        responses = []
        for file in self.responses_dir.glob("*.json"):
            with open(file, "r") as f:
                responses.append(json.load(f))
        
        return pd.DataFrame(responses)
    
    def get_responses_by_type(self, survey_type: str) -> pd.DataFrame:
        """
        Get responses filtered by survey type
        
        Args:
            survey_type: Either "Job Candidate" or "Company Representative"
            
        Returns:
            pd.DataFrame: Filtered responses
        """
        df = self.get_all_responses()
        return df[df['survey_type'] == survey_type]
    
    def export_to_csv(self, filename: str) -> None:
        """
        Export all responses to CSV file
        
        Args:
            filename: Name of the CSV file
        """
        df = self.get_all_responses()
        df.to_csv(filename, index=False)