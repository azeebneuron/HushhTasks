# processors/base_processor.py
from abc import ABC, abstractmethod
from typing import List, Optional
from models.pydantic_models import ProcessedData

class BaseProcessor(ABC):
    @abstractmethod
    async def process_text(self, text: str) -> ProcessedData:
        """
        Process a single text input
        
        Args:
            text (str): Input text to analyze
            
        Returns:
            ProcessedData: Structured analysis results
        """
        pass

    @abstractmethod
    async def batch_process(self, texts: List[str]) -> List[Optional[ProcessedData]]:
        """
        Process multiple texts
        
        Args:
            texts (List[str]): List of input texts
            
        Returns:
            List[Optional[ProcessedData]]: List of processing results
        """
        pass

    @abstractmethod
    def validate_response(self, response: dict) -> bool:
        """
        Validate if the response has all required fields
        
        Args:
            response (dict): Response dictionary to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        pass

    @abstractmethod
    async def get_model_info(self) -> dict:
        """
        Get information about the model configuration
        
        Returns:
            dict: Model configuration details
        """
        pass