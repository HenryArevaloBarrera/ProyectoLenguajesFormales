import time

class MooreMachine:
    def __init__(self, states, input_alphabet, transitions, outputs, initial_state, required_sections=None):
        self.states = set(states)
        self.input_alphabet = set(input_alphabet)
        self.transitions = transitions  # dict: (state, symbol) -> next_state
        self.outputs = outputs          # dict: state -> output
        self.initial_state = initial_state
        self.required_sections = set(required_sections) if required_sections else set(input_alphabet)

    def process(self, lines):
        current_state = self.initial_state
        output_sequence = [self.outputs[current_state]]
        print(self.outputs[current_state])
        time.sleep( 0.5)
        found_sections = set()
        for line in lines:
            symbol = self.detect_section(line)
            if symbol:
                found_sections.add(symbol)
                key = (current_state, symbol)
                if key in self.transitions:
                    current_state = self.transitions[key]
                    msg = self.outputs[current_state]
                    output_sequence.append(msg)
                    print(msg)
                    time.sleep( 0.5)
        # Al final, verifica si faltó alguna sección requerida
        missing = self.required_sections - found_sections
        if missing:
            msg = f"[ERROR][MOORE] Faltan las siguientes secciones en el archivo: {', '.join(missing)}"
            output_sequence.append(msg)
            print(msg)
        return output_sequence

    @staticmethod
    def detect_section(line):
        sections = ['[global]', '[planetas]', '[agujerosnegros]', '[nave]', '[textos]']
        line = line.strip().lower()
        return line if line in sections else None