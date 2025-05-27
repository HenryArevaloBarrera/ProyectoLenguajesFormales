from .space_analyzer import SpaceAnalyzer

class Analyzer:
    def __init__(self):
        self.space_analyzer = SpaceAnalyzer()
        
    def mostrar_progreso_lectura(self, file_content):
        yield from self.space_analyzer.mostrar_progreso_lectura(file_content)
        
    def analyze(self, code):
        try:
            # Usamos directamente analyze() que ahora acepta strings
            return self.space_analyzer.analyze(code)
        except Exception as e:
            return {
                'error': str(e),
                'success': False
            }