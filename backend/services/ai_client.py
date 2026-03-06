"""
AI Service Clients - Version Fixée Marseille 2050
"""
import os
import json
import subprocess
import tempfile
import base64

class WhisperClient:
    def __init__(self):
        self.api_key = os.getenv("WHISPER_API_KEY", "tristanlovesia")
        self.api_url = os.getenv("WHISPER_API_URL", "http://37.26.187.4:8000/api/speech-to-text")

    async def transcribe(self, audio_data: bytes) -> dict:
        tmp_path = None
        try:
            # 💡 CORRECTION : On utilise .webm car le navigateur envoie du WebM
            with tempfile.NamedTemporaryFile(suffix='.webm', delete=False) as tmp:
                tmp.write(audio_data)
                tmp_path = tmp.name
            
            # 💡 CORRECTION : On prévient l'API que c'est du WebM
            cmd = [
                'curl', '-s', '-X', 'POST', self.api_url,
                '-H', f'Authorization: Bearer {self.api_key}',
                '-F', f'file=@{tmp_path};type=audio/webm',
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            if result.returncode != 0: raise Exception(result.stderr)
            
            response_data = json.loads(result.stdout)
            return {'text': response_data.get('text', ''), 'confidence': 0.95}
        except Exception as e:
            raise Exception(f"Whisper failed: {str(e)}")
        finally:
            if tmp_path and os.path.exists(tmp_path): os.remove(tmp_path)

class ZImageTurboClient:
    def __init__(self):
        self.api_key = os.getenv("ZIMAGETURBO_API_KEY", "tristanlovesia")
        self.api_url = os.getenv("ZIMAGETURBO_API_URL", "http://37.26.187.4:8000/api/prompt-to-image")
        self.model = "Tongyi-MAI/Z-Image-Turbo"

    async def generate(self, prompt: str) -> dict:
        try:
            payload = json.dumps({"prompt": prompt, "model": self.model, "steps": 4})
            
            cmd = [
                'curl', '-s', '-X', 'POST', self.api_url,
                '-H', 'Content-Type: application/json',
                '-H', f'Authorization: Bearer {self.api_key}',
                '-d', payload
            ]
            
            result = subprocess.run(cmd, capture_output=True, timeout=120)
            
            if result.returncode != 0:
                raise Exception(f"Curl error: {result.stderr}")

            if result.stdout.startswith(b'{'):
                data = json.loads(result.stdout)
                
                # 💡 CORRECTION : On gère la clé 'images' (qui contient le Base64)
                if 'images' in data:
                    img_b64 = data['images'][0]
                    return {
                        'image_url': f"data:image/png;base64,{img_b64}",
                        'model': self.model
                    }
                # (Au cas où l'API changerait et renverrait image_url un jour)
                elif 'image_url' in data:
                    return {'image_url': data['image_url'], 'model': self.model}
                    
                if 'error' in data:
                    raise Exception(data['error'])
                raise Exception(f"Format JSON inconnu: {data}")

            # Sinon, c'est l'image brute (PNG/JPG).
            img_b64 = base64.b64encode(result.stdout).decode('utf-8')
            return {
                'image_url': f"data:image/png;base64,{img_b64}",
                'model': self.model
            }
        except Exception as e:
            raise Exception(f"Image generation failed: {str(e)}")

class GpuLlmClient:
    def __init__(self):
        self.api_url = os.getenv("LLM_API_URL", "http://37.26.187.4:8000")
        self.api_token = "tristanlovesia"
        self.model = "llama3.1:8b"

    async def chat_completion(self, messages: list, model: str = None) -> dict:
        try:
            payload = json.dumps({'model': model or self.model, 'messages': messages})
            cmd = [
                'curl', '-s', '-X', 'POST', f'{self.api_url}/v1/chat/completions',
                '-H', 'Content-Type: application/json',
                '-H', f'Authorization: Bearer {self.api_token}',
                '-d', payload
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            response_data = json.loads(result.stdout)
            content = response_data.get('choices', [{}])[0].get('message', {}).get('content', '')
            return {'content': content, 'model': self.model}
        except Exception as e:
            raise Exception(f"Llama failed: {str(e)}")

# Instances globales pour main.py
whisper_client = WhisperClient()
zimageturbo_client = ZImageTurboClient()
gpu_llm_client = GpuLlmClient()
# On redirige llama_client vers le nouveau client GPU
llama_client = gpu_llm_client