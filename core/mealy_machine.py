import time

class MealyMachine:
    def __init__(self, states, input_alphabet, transitions, outputs, initial_state, required_sections=None):
        self.states = set(states)
        self.input_alphabet = [s.lower() for s in input_alphabet]
        self.transitions = transitions  # dict: (state, symbol) -> next_state
        self.outputs = outputs          # dict: (state, symbol) -> output
        self.initial_state = initial_state
        self.required_sections = [s.lower() for s in (required_sections if required_sections else input_alphabet)]

    def process(self, lines):
        current_state = self.initial_state
        output_sequence = []
        found_sections = []
        for line in lines:
            symbol = self.detect_section(line)
            if symbol:
                found_sections.append(symbol)
                key = (current_state, symbol)
                if key in self.transitions:
                    if key in self.outputs:
                        output_sequence.append(self.outputs[key])
                        print(self.outputs[key])
                        time.sleep(0.5)  # Pausa de 0.5 segundo por sección
                    current_state = self.transitions[key]
        # Verifica si faltan secciones requeridas
        missing = set(self.required_sections) - set(found_sections)
        if missing:
            msg = f"[ERROR][MEALY] Faltan las siguientes secciones en el archivo: {', '.join(missing)}"
            output_sequence.append(msg)
            print(msg)
        # Verifica si el ORDEN es el correcto
        expected = self.required_sections
        filtered_found = [s for s in found_sections if s in expected]
        if filtered_found != expected:
            msg = "[ERROR][MEALY] Las secciones no están en el orden correcto. Orden esperado: " + ", ".join(expected)
            output_sequence.append(msg)
            print(msg)
        return output_sequence

    @staticmethod
    def detect_section(line):
        sections = ['[global]', '[planetas]', '[agujerosnegros]', '[nave]', '[textos]']
        line = line.strip().lower()
        return line if line in sections else None