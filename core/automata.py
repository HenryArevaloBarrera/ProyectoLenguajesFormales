print("[INFO] Se ha importado correctamente la clase AFD desde automata.py")

def escribir_afd_a_txt(states, alphabet, transitions, initial_state, final_states):
    contenido = []
    contenido.append("Д = (Q, Σ, δ, qo, F)\n")
    contenido.append("Q = conjunto de estados finitos\n")
    contenido.append("qo = estado inicial\n")
    contenido.append("Σ = alfabeto aceptado\n")
    contenido.append("F = conjunto de estados finales aceptados\n")
    contenido.append("δ = función de transición\n\n")

    contenido.append(f"Q = {sorted(list(states))}\n")
    contenido.append(f"Σ = {sorted(list(alphabet))}\n")
    contenido.append(f"qo = {initial_state}\n")
    contenido.append(f"F = {sorted(list(final_states))}\n")
    contenido.append("δ:\n")
    for (from_state, symbol), to_state in sorted(transitions.items()):
        contenido.append(f"    δ({from_state}, {symbol}) -> {to_state}\n")

    with open("automata.txt", "w", encoding="utf-8") as archivo:
        archivo.writelines(contenido)

class AFD:
    def __init__(self, states, alphabet, transitions, initial_state, final_states):
        print("[INFO] Se está creando una instancia de la clase AFD")
        self.states = set(states)
        self.alphabet = set(alphabet)
        self.transitions = transitions  # Diccionario: (estado, símbolo) -> estado
        self.initial_state = initial_state
        self.final_states = set(final_states)
        escribir_afd_a_txt(self.states, self.alphabet, self.transitions, self.initial_state, self.final_states)

    def acepta(self, cadena):
        print(f"[INFO] Método acepta llamado con la cadena: {cadena}")
        estado = self.initial_state
        for simbolo in cadena:
            if (estado, simbolo) in self.transitions:
                estado = self.transitions[(estado, simbolo)]
            else:
                print(f"[WARN] No existe transición desde {estado} con símbolo '{simbolo}'")
                return False
        aceptado = estado in self.final_states
        print(f"[INFO] Estado final: {estado} - {'Aceptado' if aceptado else 'No aceptado'}")
        return aceptado

    def obtener_caminos(self, max_longitud=10):
        print(f"[INFO] Buscando caminos en el AFD (máx longitud {max_longitud})")
        from collections import deque
        caminos = []
        queue = deque()
        # Cada entrada: (estado_actual, camino_actual [lista de símbolos])
        queue.append((self.initial_state, []))
        visitados = set()  # Para evitar ciclos exactos (estado + camino)

        while queue:
            actual, recorrido = queue.popleft()

            if len(recorrido) > max_longitud:
                continue

            if actual in self.final_states and recorrido:
                caminos.append(recorrido)

            for simbolo in self.alphabet:
                key = (actual, simbolo)
                if key in self.transitions:
                    siguiente = self.transitions[key]
                    # Evitar repetir planetas en la ruta
                    if simbolo not in recorrido:
                        nuevo_camino = recorrido + [simbolo]
                        estado_camino = (siguiente, tuple(nuevo_camino))
                        if estado_camino not in visitados:
                            visitados.add(estado_camino)
                            queue.append((siguiente, nuevo_camino))

        print(f"[INFO] Caminos encontrados: {len(caminos)}")
        return caminos
