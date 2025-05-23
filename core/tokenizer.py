def tokeniza_global(lineas):
    tokens = []
    for linea in lineas:
        l = linea.strip().lower()
        if l.startswith("title:"):
            tokens.append("title")
        elif l.startswith("date:"):
            tokens.append("date")
        elif l.startswith("origen:"):
            tokens.append("origen")
        elif l.startswith("destino:"):
            tokens.append("destino")
    tokens.append("fin")
    print("TOKENS GLOBAL:", tokens) 
    return tokens

def tokeniza_planetas(lineas):
    tokens = []
    for linea in lineas:
        l = linea.strip().lower()
        # Dividir la línea en partes separadas por comas
        partes = [parte.strip() for parte in l.split(',')]
        for parte in partes:
            if parte.startswith("nombre:"):
                tokens.append("nombre")
            elif parte.startswith("coordenadas:"):
                tokens.append("coordenadas")
            elif parte.startswith("radio:"):
                tokens.append("radio")
            elif parte.startswith("gravedad:"):
                tokens.append("gravedad")
    tokens.append("fin")
    return tokens



def tokeniza_agujerosnegros(lineas):
    print("LINEAS AGUJEROS NEGROS:", lineas)
    tokens = []
    for linea in lineas:
        l = linea.strip().lower()
        if "nombre:" in l:
            tokens.append("nombre")
        if "coordenadas:" in l:
            tokens.append("coordenadas")
        if "radio:" in l:
            tokens.append("radio")
        if "masa:" in l:
            tokens.append("masa")
    tokens.append("fin")
    print("TOKENS AGUJEROS:", tokens)
    return tokens


def tokeniza_nave(lineas):
    """
    Tokeniza la línea única de la sección [nave] con todos los campos separados por comas.
    """
    tokens = []
    if not lineas:
        return ["fin"]

    # Tomamos solo la primera línea porque se espera una sola línea con todos los campos
    contenido = lineas[0].strip().lower()
    partes = [p.strip() for p in contenido.split(",")]

    for parte in partes:
        if parte.startswith("nombre:"):
            tokens.append("nombre")
        elif parte.startswith("velocidad:"):
            tokens.append("velocidad")
        elif parte.startswith("combustible:"):
            tokens.append("combustible")
        elif parte.startswith("restricciones:"):
            tokens.append("restricciones")
        else:
            tokens.append("desconocido")  # útil para detectar errores
    tokens.append("fin")
    return tokens

def tokeniza_textos(lineas):
    """
    Tokeniza las líneas de la sección [Textos] para el AFD sintáctico.
    """
    tokens = []
    for linea in lineas:
        l = linea.strip().lower()
        if l.startswith("introduccion:"):
            tokens.append("introduccion")
        elif l.startswith("descripcion:"):
            tokens.append("descripcion")
        elif l.startswith("restricciones:"):
            tokens.append("restricciones")
        elif l.startswith("ruta:"):
            tokens.append("ruta")
        elif l.startswith("conclusion:"):
            tokens.append("conclusion")
    tokens.append("fin")
    return tokens