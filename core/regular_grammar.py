class RegularGrammar:
    def __init__(self, variables, terminals, productions, start):
        self.variables = set(variables)
        self.terminals = set(terminals)
        self.productions = productions
        self.start = start

    def recognizes(self, tokens, state=None):
        if state is None:
            state = self.start
        if not tokens:
            # Acepta si hay una producción vacía en el estado actual
            return any(prod == [""] for prod in self.productions.get(state, []))
        for prod in self.productions.get(state, []):
            # ---- PARTE 1: tu lógica clásica, útil para global/planetas/agujerosnegros ----
            if prod and tokens[0] == prod[0]:
                if len(prod) == 1:
                    if self.recognizes(tokens[1:], None):
                        return True
                elif len(prod) == 2:
                    if self.recognizes(tokens[1:], prod[1]):
                        return True
                elif len(prod) > 2:
                    if tokens[:len(prod)-1] == prod[:-1]:
                        if self.recognizes(tokens[len(prod)-1:], prod[-1]):
                            return True
            # ---- PARTE 2: caso especial, producción es SOLO terminales (nave, textos) ----
            if len(prod) > 0 and all(x in self.terminals for x in prod):
                if tokens[:len(prod)] == prod:
                    if len(tokens) == len(prod):
                        return True
                    # Si hay más tokens y la gramática es recursiva, sigue desde el estado inicial
                    if self.recognizes(tokens[len(prod):], None):
                        return True
        return False
    
# [GLOBAL] (exactamente 4 claves en orden)
grammar_global = RegularGrammar(
    variables=["S", "T", "D", "O", "E"],
    terminals=["title", "date", "origen", "destino"],
    productions={
        "S": [["title", "T"]],
        "T": [["date", "D"]],
        "D": [["origen", "O"]],
        "O": [["destino", "E"]],
        "E": [[""]]
    },
    start="S"
)

# [PLANETAS] (uno o más bloques de 4 claves en orden exacto)
grammar_planetas = RegularGrammar(
    variables=["S", "P"],
    terminals=["nombre", "coordenadas", "radio", "gravedad"],
    productions={
        "S": [["nombre", "coordenadas", "radio", "gravedad", "P"]],
        "P": [["nombre", "coordenadas", "radio", "gravedad", "P"], [""]]
    },
    start="S"
)

# [AGUJEROSNEGROS] (uno o más bloques de 3 claves en orden exacto)
grammar_bh = RegularGrammar(
    variables=["S", "P"],
    terminals=["nombre", "coordenadas", "radio"],
    productions={
        "S": [["nombre", "coordenadas", "radio", "P"]],
        "P": [["nombre", "coordenadas", "radio", "P"], [""]]
    },
    start="S"
)

# [NAVE] (exactamente 4 claves en orden)
grammar_nave = RegularGrammar(
    variables=["S"],
    terminals=["nombre", "velocidad", "combustible", "restricciones"],
    productions={
        "S": [["nombre", "velocidad", "combustible", "restricciones"]]
    },
    start="S"
)

# [TEXTOS] (exactamente 5 claves en orden)
grammar_textos = RegularGrammar(
    variables=["S"],
    terminals=["introduccion", "descripcion", "restricciones", "ruta", "conclusion"],
    productions={
        "S": [["introduccion", "descripcion", "restricciones", "ruta", "conclusion"]]
    },
    start="S"
)