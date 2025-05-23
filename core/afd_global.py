from .afd import AFD

states = ['q0', 'q1', 'q2', 'q3', 'q4', 'qF']
alphabet = ['Title', 'Fecha', 'Origen', 'Destino', 'FIN']
transitions = {
    ('q0', 'Title'): 'q1',
    ('q1', 'Fecha'): 'q2',
    ('q2', 'Origen'): 'q3',
    ('q3', 'Destino'): 'q4',
    ('q4', 'FIN'): 'qF'
}
afd_global = AFD(states, alphabet, transitions, 'q0', ['qF'])