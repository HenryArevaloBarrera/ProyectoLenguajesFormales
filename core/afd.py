class AFD:
    def __init__(self, states, alphabet, transitions, initial_state, final_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.initial_state = initial_state
        self.final_states = final_states

    def acepta(self, cadena_tokens):
        estado_actual = self.initial_state
        for token in cadena_tokens:
            if (estado_actual, token) in self.transitions:
                estado_actual = self.transitions[(estado_actual, token)]
            else:
                return False  # No hay transición válida
        return estado_actual in self.final_states

# ----------- AFDs de ejemplo para distintas secciones (SIN 'fin') ------------------

# AFD para la sección [Global]
afd_global = AFD(
    states=['q0', 'q1', 'q2', 'q3', 'q4'],
    alphabet=['title', 'date', 'origen', 'destino'],
    transitions={
        ('q0', 'title'): 'q1',
        ('q1', 'date'): 'q2',
        ('q2', 'origen'): 'q3',
        ('q3', 'destino'): 'q4'
    },
    initial_state='q0',
    final_states=['q4']
)

# AFD para la sección [Planetas]
afd_planetas = AFD(
    states=['q0', 'q1', 'q2', 'q3', 'q4'],
    alphabet=['nombre', 'coordenadas', 'radio', 'gravedad'],
    transitions={
        ('q0', 'nombre'): 'q1',
        ('q1', 'coordenadas'): 'q2',
        ('q2', 'radio'): 'q3',
        ('q3', 'gravedad'): 'q4',
        ('q4', 'nombre'): 'q1',  # Permite empezar un nuevo planeta después de uno terminado
    },
    initial_state='q0',
    final_states=['q4']
)

# AFD para la sección [AgujerosNegros]
afd_agujerosnegros = AFD(
    states=['q0', 'q1', 'q2', 'q3'],
    alphabet=['nombre', 'coordenadas', 'radio'],
    transitions={
        ('q0', 'nombre'): 'q1',
        ('q1', 'coordenadas'): 'q2',
        ('q2', 'radio'): 'q3',
        ('q3', 'nombre'): 'q1',  # Permite empezar un nuevo agujero después de uno terminado
    },
    initial_state='q0',
    final_states=['q3']
)

# AFD para la sección [Nave]
afd_nave = AFD(
    states=["q0", "q1", "q2", "q3", "q4"],
    alphabet={"nombre", "velocidad", "combustible", "restricciones"},
    transitions={
        ("q0", "nombre"): "q1",
        ("q1", "velocidad"): "q2",
        ("q2", "combustible"): "q3",
        ("q3", "restricciones"): "q4"
    },
    initial_state="q0",
    final_states={"q4"}
)

# AFD para la sección [Textos]
afd_textos = AFD(
    states=['q0', 'q1', 'q2', 'q3', 'q4', 'q5'],
    alphabet=['introduccion', 'descripcion', 'restricciones', 'ruta', 'conclusion'],
    transitions={
        ('q0', 'introduccion'): 'q1',
        ('q1', 'descripcion'): 'q2',
        ('q2', 'restricciones'): 'q3',
        ('q3', 'ruta'): 'q4',
        ('q4', 'conclusion'): 'q5'
    },
    initial_state='q0',
    final_states=['q5']
)