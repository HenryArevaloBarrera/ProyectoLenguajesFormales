import time

class MealyMachine:
    def __init__(self, states, input_alphabet, transitions, outputs, initial_state, required_sections=None):
        self.states = set(states)
        self.input_alphabet = set(input_alphabet)
        self.transitions = transitions  # dict: (state, symbol) -> next_state
        self.outputs = outputs          # dict: (state, symbol) -> output
        self.initial_state = initial_state
        self.required_sections = set(required_sections) if required_sections else set(input_alphabet)

    def process(self, lines):
        current_state = self.initial_state
        output_sequence = []
        found_sections = set()
        for line in lines:
            symbol = self.detect_section(line)
            if symbol:
                found_sections.add(symbol)
                key = (current_state, symbol)
                if key in self.transitions:
                    if key in self.outputs:
                        output_sequence.append(self.outputs[key])
                        print(self.outputs[key])
                        time.sleep( 0.5)  # Pausa de  0.5 segundo por sección
                    current_state = self.transitions[key]
        # Al final, verifica si faltó alguna sección requerida
        missing = self.required_sections - found_sections
        if missing:
            msg = f"[ERROR][MEALY] Faltan las siguientes secciones en el archivo: {', '.join(missing)}"
            output_sequence.append(msg)
            print(msg)
        return output_sequence

    @staticmethod
    def detect_section(line):
        sections = ['[global]', '[planetas]', '[agujerosnegros]', '[nave]', '[textos]']
        line = line.strip().lower()
        return line if line in sections else None