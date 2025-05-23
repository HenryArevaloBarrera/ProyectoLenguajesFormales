from afd_global import afd_global
from tokenizer import tokeniza_global

def valida_seccion_global(lineas):
    tokens = tokeniza_global(lineas)
    if afd_global.acepta(tokens):
        print("La sección [Global] es válida!")
    else:
        print("Error de sintaxis en la sección [Global]")