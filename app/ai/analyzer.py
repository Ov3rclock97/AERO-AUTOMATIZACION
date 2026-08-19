"""
AI Analysis Layer - Provider-agnostic.
Connect to Ollama, LM Studio, or any OpenAI-compatible API.
Current default: mock mode (no external dependencies).
"""
from typing import Optional


class AIAnalyzer:
    """
    AI-powered analysis engine for network configurations and diagnostics.
    Design principle: Never execute AI suggestions automatically.
    All recommendations must pass through the validation/approval workflow.
    """

    def __init__(self, provider: str = 'mock', api_url: Optional[str] = None,
                 api_key: Optional[str] = None, model: str = 'llama3'):
        self.provider = provider
        self.api_url = api_url
        self.api_key = api_key
        self.model = model

    def analyze_config(self, config: str) -> str:
        """Analyze a device configuration."""
        if self.provider == 'mock':
            lines = config.count('\n')
            return (
                f'[AI MOCK ANALYSIS] Config lines: {lines}\n'
                '- Verify all interfaces have correct IP addresses.\n'
                '- Check routing protocol configuration.\n'
                '- Review access control lists.\n'
                'NOTE: Connect an AI provider in .env for real analysis.'
            )
        return self._call_api(f'Analyze this network device configuration:\n{config}')

    def explain_error(self, error_output: str) -> str:
        """Explain a network error in plain language."""
        if self.provider == 'mock':
            return '[AI MOCK] This error may indicate a connectivity or config issue. Check device logs and interface status.'
        return self._call_api(f'Explain this network device error:\n{error_output}')

    def suggest_troubleshooting(self, symptoms: str) -> str:
        """Generate troubleshooting suggestions."""
        if self.provider == 'mock':
            return (
                '[AI MOCK] Suggested steps:\n'
                '1. Check physical connectivity and cable.\n'
                '2. Verify interface is not administratively down.\n'
                '3. Check routing table.\n'
                '4. Verify gateway reachability.'
            )
        return self._call_api(f'Suggest troubleshooting for: {symptoms}')

    def compare_configs(self, config_a: str, config_b: str) -> str:
        """Compare two configurations and summarize differences."""
        if self.provider == 'mock':
            return '[AI MOCK] Differences found. Use the diff module for exact line-by-line comparison.'
        prompt = f'Compare and summarize differences:\nCONFIG A:\n{config_a}\nCONFIG B:\n{config_b}'
        return self._call_api(prompt)

    def _call_api(self, prompt: str) -> str:
        """Call an OpenAI-compatible API."""
        try:
            import urllib.request
            import json
            payload = json.dumps({
                'model': self.model,
                'messages': [{'role': 'user', 'content': prompt}]
            }).encode()
            req = urllib.request.Request(
                self.api_url + '/v1/chat/completions',
                data=payload,
                headers={'Content-Type': 'application/json'},
                method='POST'
            )
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read())
                return data['choices'][0]['message']['content']
        except Exception as e:
            return f'[AI ERROR] Could not reach provider: {e}'
