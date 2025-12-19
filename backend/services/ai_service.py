import os
from typing import Dict, Any, List, Optional
from emergentintegrations.llm.chat import LlmChat, UserMessage, FileContentWithMimeType
from dotenv import load_dotenv
import logging

load_dotenv()
logger = logging.getLogger(__name__)

class AIService:
    def __init__(self):
        self.api_key = os.getenv("EMERGENT_LLM_KEY")
        if not self.api_key:
            raise ValueError("EMERGENT_LLM_KEY not found in environment variables")
    
    def create_chat(self, system_message: str = "You are a helpful assistant for generating event input briefs."):
        """Create a new LLM chat instance"""
        chat = LlmChat(
            api_key=self.api_key,
            session_id="gpj-brief-assistant",
            system_message=system_message
        )
        # Using GPT-4 for better quality
        chat.with_model("openai", "gpt-4o")
        return chat
    
    async def analyze_document(self, file_path: str, mime_type: str, analysis_prompt: str) -> str:
        """Analyze a document and extract relevant information"""
        try:
            # Use Gemini for document analysis (supports file attachments)
            chat = LlmChat(
                api_key=self.api_key,
                session_id="doc-analysis",
                system_message="You are an expert at analyzing documents and extracting structured information for event planning briefs."
            )
            chat.with_model("gemini", "gemini-2.5-flash")
            
            file_content = FileContentWithMimeType(
                file_path=file_path,
                mime_type=mime_type
            )
            
            message = UserMessage(
                text=analysis_prompt,
                file_contents=[file_content]
            )
            
            response = await chat.send_message(message)
            return response
        except Exception as e:
            logger.error(f"Error analyzing document: {str(e)}")
            raise
    
    async def generate_section_content(self, section_name: str, context: Dict[str, Any], prompt: Optional[str] = None) -> Dict[str, Any]:
        """Generate content for a specific brief section using AI"""
        try:
            chat = self.create_chat(
                system_message="You are an expert at creating comprehensive event input briefs. Generate detailed, professional content based on the provided context."
            )
            
            if not prompt:
                prompt = f"Generate content for the '{section_name}' section of an event input brief. Context: {context}"
            
            message = UserMessage(text=prompt)
            response = await chat.send_message(message)
            
            return {"generated_text": response, "section_name": section_name}
        except Exception as e:
            logger.error(f"Error generating section content: {str(e)}")
            raise
    
    async def extract_structured_data(self, document_content: str, section_name: str) -> Dict[str, Any]:
        """Extract structured data from document content for a specific section"""
        try:
            chat = self.create_chat(
                system_message="You are an expert at extracting structured information from documents. Extract only relevant fields and values in JSON format."
            )
            
            prompt = f"""
            Extract relevant information from the following document content for the '{section_name}' section.
            Return the data as a structured JSON object with field names as keys.
            
            Document content:
            {document_content}
            
            Return only the JSON object, no additional text.
            """
            
            message = UserMessage(text=prompt)
            response = await chat.send_message(message)
            
            # Try to parse as JSON
            import json
            try:
                return json.loads(response)
            except:
                return {"extracted_content": response}
        except Exception as e:
            logger.error(f"Error extracting structured data: {str(e)}")
            raise
    
    async def get_field_suggestions(self, field_name: str, context: Dict[str, Any]) -> List[str]:
        """Get AI suggestions for a specific field"""
        try:
            chat = self.create_chat()
            
            prompt = f"""
            Provide 3-5 suggestions for the field '{field_name}' based on this context: {context}
            Return as a comma-separated list.
            """
            
            message = UserMessage(text=prompt)
            response = await chat.send_message(message)
            
            # Split response into list
            suggestions = [s.strip() for s in response.split(',')]
            return suggestions[:5]
        except Exception as e:
            logger.error(f"Error getting field suggestions: {str(e)}")
            return []

# Singleton instance
ai_service = AIService()
