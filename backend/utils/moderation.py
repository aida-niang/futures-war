"""
Moderation utilities for content safety
"""

import os
import json
import subprocess
from typing import Optional, List
from dotenv import load_dotenv

load_dotenv()


class ContentModerator:
    """Handles content safety filtering using LLM"""

    def __init__(self):
        self.api_url = os.getenv("LLM_API_URL", "http://localhost:8000")
        self.api_token = os.getenv("LLM_API_TOKEN", "")
        self.model = os.getenv("LLM_MODEL", "llama3.1:8b")

    def moderate(self, text: str) -> dict:
        """
        Moderate text content for safety violations using LLM
        
        Args:
            text: Text to moderate
            
        Returns:
            dict with moderation results
        """
        try:
            # Create moderation prompt for LLM
            moderation_prompt = f"""You are a content moderator. Analyze this text for safety issues:
- Violence, threats, or harm
- Hateful speech or discrimination
- Illegal activity
- Explicit content
- Abuse or harassment

Text: "{text}"

Respond with JSON: {{"is_safe": true/false, "reason": "brief explanation"}}"""
            
            messages = [
                {"role": "user", "content": moderation_prompt}
            ]
            
            payload = {
                "model": self.model,
                "messages": messages
            }
            payload_json = json.dumps(payload)
            
            # Call LLM via curl
            cmd = [
                'curl',
                '-s',
                '-X', 'POST',
                f'{self.api_url}/v1/chat/completions',
                '-H', 'Content-Type: application/json'
            ]
            
            if self.api_token:
                cmd.extend(['-H', f'Authorization: Bearer {self.api_token}'])
            
            cmd.extend(['-d', payload_json])
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode != 0:
                # Fallback to safe if error
                return {
                    'is_safe': True,
                    'reason': 'Moderation service unavailable - allowing content',
                    'flagged_content': None,
                    'score': 1.0
                }
            
            response_data = json.loads(result.stdout)
            content = response_data.get('choices', [{}])[0].get('message', {}).get('content', '{}')
            
            # Parse LLM response
            try:
                result_json = json.loads(content)
                is_safe = result_json.get('is_safe', True)
                reason = result_json.get('reason', 'Content safety check completed')
            except:
                # If LLM response isn't valid JSON, assume safe
                is_safe = True
                reason = "Could not parse moderation response"
            
            return {
                'is_safe': is_safe,
                'reason': reason,
                'flagged_content': None if is_safe else ['unsafe_content'],
                'score': 1.0 if is_safe else 0.0
            }
        except Exception as e:
            # Fallback: allow content if moderation fails
            return {
                'is_safe': True,
                'reason': f'Moderation failed: {str(e)[:50]}',
                'flagged_content': None,
                'score': 1.0
            }


def moderate_text(text: str) -> dict:
    """Convenience function for text moderation"""
    moderator = ContentModerator()
    return moderator.moderate(text)
