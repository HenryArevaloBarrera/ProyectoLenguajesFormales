from .space_analyzer import SpaceAnalyzer

class Analyzer:
    def __init__(self):
        self.space_analyzer = SpaceAnalyzer()

    def analyze(self, code):
        try:
            # Usamos directamente analyze() que ahora acepta strings
            return self.space_analyzer.analyze(code)
        except Exception as e:
            return {
                'error': str(e),
                'success': False
            }