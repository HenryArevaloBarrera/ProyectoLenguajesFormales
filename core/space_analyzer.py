import math
import time
import numpy as np
import os
from io import StringIO
from .automata import AFD
from core.Lexical_Validator import LexicalValidator
from .tokenizer import tokeniza_global, tokeniza_planetas, tokeniza_agujerosnegros, tokeniza_nave, tokeniza_textos
from .space_visualizer import draw_space_graph
from .afd import afd_global, afd_planetas, afd_agujerosnegros, afd_nave, afd_textos
from .regular_grammar import grammar_global, grammar_planetas, grammar_bh, grammar_nave, grammar_textos
from .moore_machine import MooreMachine
from .mealy_machine import MealyMachine
# ------------- AFDs y Tokenizers Sintácticos para cada sección -------------
class AFDSyntax:
    def __init__(self):
        self.space_analyzer = SpaceAnalyzer()

        # [Global]
        self.afd_global = afd_global
        # [Planetas]
        self.afd_planetas = afd_planetas
        # [AgujerosNegros]
        self.afd_agujerosnegros = afd_agujerosnegros
        # [Nave]
        self.afd_nave = afd_nave
        # [Textos]
        self.afd_textos = afd_textos

    def get_afd(self, section):
        return {
            'global': self.afd_global,
            'planetas': self.afd_planetas,
            'agujerosnegros': self.afd_agujerosnegros,
            'agujeros_negros': self.afd_agujerosnegros,
            'nave': self.afd_nave,
            'textos': self.afd_textos
        }.get(section, None)

def tokenize_section(section_name, lines):
    if section_name == "global":
        return tokeniza_global(lines)
    elif section_name == "planetas":
        return tokeniza_planetas(lines)
    elif section_name == "agujerosnegros":
        return tokeniza_agujerosnegros(lines)
    elif section_name == "nave":
        return tokeniza_nave(lines)
    elif section_name == "textos":
        return tokeniza_textos(lines)
    else:
        return []  # o error

# --------------------------- Clase principal -------------------------------

class SpaceAnalyzer:
    DISABLE_RESTRICTION_CHECK = False

    class Planet:
        def __init__(self, name, x, y, z, radius=0, gravity=0):
            self.name = name
            self.x = x
            self.y = y
            self.z = z
            self.radius = radius
            self.gravity = gravity

        def coordinates(self):
            return np.array([self.x, self.y, self.z])

    class BlackHole:
        def __init__(self, name, x, y, z, radius):
            self.name = name
            self.x = x
            self.y = y
            self.z = z
            self.radius = radius

        def coordinates(self):
            return np.array([self.x, self.y, self.z])

    class Spaceship:
        def __init__(self, name, velocity=0, fuel=0, restrictions=""):
            self.name = name
            self.velocity = velocity
            self.fuel = fuel
            self.restricciones = restrictions

    class Mission:
        def __init__(self):
            self.title = ""
            self.date = ""
            self.origin = ""
            self.destination = ""
            self.planets = {}
            self.blackholes = []
            self.spaceship = None
            self.texts = {}

    def mostrar_progreso_lectura(self, file_content):
            lines = file_content.splitlines() if isinstance(file_content, str) else file_content.readlines()
            states = ['inicio', 'global', 'planetas', 'agujerosnegros', 'nave', 'textos']
            input_alphabet = ['[global]', '[planetas]', '[agujerosnegros]', '[nave]', '[textos]']
            transitions = {
                ('inicio', '[global]'): 'global',
                ('global', '[planetas]'): 'planetas',
                ('planetas', '[agujerosnegros]'): 'agujerosnegros',
                ('agujerosnegros', '[nave]'): 'nave',
                ('nave', '[textos]'): 'textos',
            }
            outputs_moore = {
                'inicio': 'Inicio de archivo, esperando sección...',
                'global': 'Leyendo sección [Global]',
                'planetas': 'Leyendo sección [Planetas]',
                'agujerosnegros': 'Leyendo sección [AgujerosNegros]',
                'nave': 'Leyendo sección [Nave]',
                'textos': 'Leyendo sección [Textos]',
            }
            outputs_mealy = {
                ('inicio', '[global]'): 'Entrando a sección [Global]',
                ('global', '[planetas]'): 'Cambiando a sección [Planetas]',
                ('planetas', '[agujerosnegros]'): 'Cambiando a sección [AgujerosNegros]',
                ('agujerosnegros', '[nave]'): 'Cambiando a sección [Nave]',
                ('nave', '[textos]'): 'Cambiando a sección [Textos]',
            }
            initial_state = 'inicio'
            required_sections = set(input_alphabet)

            mealy_state = initial_state
            moore_state = initial_state
            found_sections = set()
            # Primer mensaje de Moore
            yield {"type": "moore", "message": outputs_moore[moore_state]}
            time.sleep(0.5)

            for line in lines:
                symbol = MooreMachine.detect_section(line)
                if symbol:
                    found_sections.add(symbol)
                    # Mealy: emite y transiciona
                    mealy_key = (mealy_state, symbol)
                    if mealy_key in transitions:
                        if mealy_key in outputs_mealy:
                            msg = outputs_mealy[mealy_key]
                            yield {"type": "mealy", "message": msg}
                            time.sleep(0.5)
                        mealy_state = transitions[mealy_key]
                    # Moore: transiciona y emite
                    moore_key = (moore_state, symbol)
                    if moore_key in transitions:
                        moore_state = transitions[moore_key]
                        msg = outputs_moore[moore_state]
                        yield {"type": "moore", "message": msg}
                        time.sleep(0.5)

            # Al final, chequeo de secciones faltantes
            missing = required_sections - found_sections
            if missing:
                moore_error = f"[ERROR][MOORE] Faltan las siguientes secciones en el archivo: {', '.join(missing)}"
                mealy_error = f"[ERROR][MEALY] Faltan las siguientes secciones en el archivo: {', '.join(missing)}"
                yield {"type": "moore", "message": moore_error}
                yield {"type": "mealy", "message": mealy_error}
            yield {"type": "done", "message": "Análisis de progreso completado."}

    def _validate_section_grammar(self, section, lines):
        tokens = tokenize_section(section, lines)  # Usa el tokenizador adecuado
        if section == "global":
            if not grammar_global.recognizes(tokens):
                raise ValueError(f"Estructura inválida en la sección [{section}] según la gramática regular.")
        elif section == "planetas":
                if not grammar_planetas.recognizes(tokens):
                    raise ValueError(f"Estructura inválida en la sección [{section}] (planeta incompleto o campos desordenados) según la gramática regular.")
        elif section in {"agujerosnegros", "agujeros_negros"}:
            for i in range(0, len(tokens)):
                if not grammar_bh.recognizes(tokens):
                    raise ValueError(f"Estructura inválida en la sección [{section}] (agujero negro incompleto o campos desordenados) según la gramática regular.")
        elif section == "nave":
            if not grammar_nave.recognizes(tokens):
                print("[DEBUG][NAVE] tokens:", tokens)
                raise ValueError(f"Estructura inválida en la sección [{section}] según la gramática regular.")
        elif section == "textos":
            if not grammar_textos.recognizes(tokens):
                raise ValueError(f"Estructura inválida en la sección [{section}] según la gramática regular.")
        print(f"[DEBUG][GRAMMAR] Sección: {section}, Tokens: {tokens}")
    @staticmethod
    def split_outside_parentheses(s):
        parts = []
        current = []
        level = 0
        for char in s:
            if char == ',' and level == 0:
                parts.append(''.join(current).strip())
                current = []
            else:
                if char == '(':
                    level += 1
                elif char == ')':
                    if level > 0:
                        level -= 1
                current.append(char)
        if current:
            parts.append(''.join(current).strip())
        return parts

    def parse_space_file(self, file_content):
        """Analiza contenido .space desde un string o archivo después de validación léxica y validación sintáctica con AFDs."""
        if isinstance(file_content, str):
            source_code = file_content
            file_like = StringIO(file_content)
        else:
            source_code = file_content.read()
            file_like = StringIO(source_code)

        # Validación léxica antes del parseo
        validator = LexicalValidator()
        try:
            validator.validate(source_code)
        except Exception as e:
            raise ValueError(f"Error léxico detectado: {e}")

        afd_syntax = AFDSyntax()
        mission = self.Mission()
        current_section = "global"
        section_lines = []
        file_like.seek(0)

        for line in file_like:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            if line.startswith("[") and line.endswith("]"):
                # Antes de cambiar, valida la sección previa
                if section_lines:
                    
                    self._validate_section_syntax(current_section, section_lines, afd_syntax)
                    self._validate_section_grammar(current_section, section_lines)
                current_section = line[1:-1].lower()
                section_lines = []
                continue

            section_lines.append(line)
            # Validar la sección actual
            # Parseo semántico (si la sección es válida sintácticamente)
            if current_section == "global":
                self._parse_global_line(line, mission)
            elif current_section == "planetas":
                self._parse_planet_line(line, mission)
            elif current_section in {"agujerosnegros", "agujeros_negros"}:
                self._parse_blackhole_line(line, mission)
            elif current_section == "nave":
                self._parse_spaceship_line(line, mission)
            elif current_section == "textos":
                self._parse_text_line(line, mission)

        # Validar última sección
        if section_lines:
            self._validate_section_syntax(current_section, section_lines, afd_syntax)
            self._validate_section_grammar(current_section, section_lines)
        return mission

    def _validate_section_syntax(self, section, lines, afd_syntax):
        afd = afd_syntax.get_afd(section)
        if afd:
            tokens = tokenize_section(section, lines)
            if not afd.acepta(tokens):
                raise ValueError(f"Error sintáctico en la sección [{section}]")
        # En caso de que alguna sección no tenga AFD definido, no se valida sintácticamente

    def _parse_global_line(self, line, mission):
        if ":" in line:
            key, val = line.split(":", 1)
            key = key.strip().lower()
            val = val.strip()
            if key == "title":
                mission.title = val
            elif key in {"fecha", "date"}:
                mission.date = val
            elif key == "origen":
                mission.origin = val
            elif key == "destino":
                mission.destination = val

    def _parse_planet_line(self, line, mission):
        parts = self.split_outside_parentheses(line)
        data = {}
        for part in parts:
            if ":" in part:
                key, val = part.split(":", 1)
                data[key.strip().lower()] = val.strip()

        name = data.get("nombre", "")
        coords = self._parse_coordinates(data.get("coordenadas", "(0,0,0)"))
        radius = float(data.get("radio", 0))
        gravity = float(data.get("gravedad", 0))
        mission.planets[name] = self.Planet(name, *coords, radius, gravity)

    def _parse_blackhole_line(self, line, mission):
        parts = self.split_outside_parentheses(line)
        data = {}
        for part in parts:
            if ":" in part:
                key, val = part.split(":", 1)
                data[key.strip().lower()] = val.strip()

        name = data.get("nombre", "")
        coords = self._parse_coordinates(data.get("coordenadas", "(0,0,0)"))
        radius = float(data.get("radio", 0))
        mission.blackholes.append(self.BlackHole(name, *coords, radius))

    def _parse_spaceship_line(self, line, mission):
        parts = self.split_outside_parentheses(line)
        data = {}
        for part in parts:
            if ":" in part:
                key, val = part.split(":", 1)
                data[key.strip().lower()] = val.strip()

        name = data.get("nombre", "")
        velocity = float(data.get("velocidad", 0))
        fuel = float(data.get("combustible", 0))
        restrictions = data.get("restricciones", "")
        mission.spaceship = self.Spaceship(name, velocity, fuel, restrictions)

    def _parse_text_line(self, line, mission):
        if ":" in line:
            key, val = line.split(":", 1)
            mission.texts[key.strip().lower()] = val.strip()

    def _parse_coordinates(self, coord_str):
        coords = coord_str.strip("()").split(",")
        if len(coords) < 3:
            coords = [0, 0, 0]
        return list(map(float, coords))

    @staticmethod
    def euclidean_distance(p1, p2):
        return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2 + (p1[2] - p2[2]) ** 2)

    def edge_safe(self, p1, p2, blackholes, margin=5):
        d = p2 - p1
        d_norm_sq = np.dot(d, d)
        if d_norm_sq == 0:
            return True

        for bh in blackholes:
            bh_center = bh.coordinates()
            t = np.dot(bh_center - p1, d) / d_norm_sq
            t = max(0, min(1, t))
            closest = p1 + t * d
            distance = np.linalg.norm(bh_center - closest)
            if distance < bh.radius + margin:
                return False
        return True

    def build_afd_de_planetas(self, mission):
        print("\n[INFO] Construyendo el AFD de planetas (usando la clase AFD)...")
        states = list(mission.planets.keys())
        alphabet = list(mission.planets.keys())
        transitions = {}

        restricciones = (mission.spaceship.restricciones if mission.spaceship else "").lower()
        max_gravedad = 5  
        max_distancia = 60 

        for from_name, from_planet in mission.planets.items():
            for to_name, to_planet in mission.planets.items():
                if from_name == to_name:
                    continue

                es_seguro = True

                # Restricción 1: evitar agujeros
                if "evitar agujeros" in restricciones:
                    es_seguro = self.edge_safe(
                        from_planet.coordinates(),
                        to_planet.coordinates(),
                        mission.blackholes
                    )

                # Restricción 2: solo gravedad baja
                if es_seguro and "solo gravedad baja" in restricciones:
                    if to_planet.gravity > max_gravedad:
                        es_seguro = False

                # Restricción 3: solo rutas cortas
                if es_seguro and "solo rutas cortas" in restricciones:
                    distancia = self.euclidean_distance(from_planet.coordinates(), to_planet.coordinates())
                    if distancia > max_distancia:
                        es_seguro = False

                if es_seguro:
                    transitions[(from_name, to_name)] = to_name

        initial_state = mission.origin
        final_states = [mission.destination]
        afd = AFD(states, alphabet, transitions, initial_state, final_states)
        print("[INFO] Instancia de AFD creada y lista para usarse.\n")
        return afd

    def analyze(self, file_content):
        self.mostrar_progreso_lectura(file_content)
        print("[INFO] Iniciando análisis... Validando léxico y sintaxis.")
        validator = LexicalValidator()
        try:
            validator.validate(file_content)
            print("[INFO] Validación léxica superada.")
        except Exception as e:
            print(f"[ERROR] Error léxico detectado: {e}")
            raise ValueError(f"Error léxico detectado: {e}")

        mission = self.parse_space_file(file_content)
        afd = self.build_afd_de_planetas(mission)
        print("[INFO] Usando la clase AFD para encontrar rutas óptimas...\n")
        caminos = afd.obtener_caminos(max_longitud=len(mission.planets) + 2)
        if not caminos:
            raise ValueError("No se encontró una ruta segura (autómata).")
        mejor = min(caminos, key=len)

        # Grafo como dict para frontend
        graph = {name: [] for name in mission.planets}
        for (from_name, to_name), _ in afd.transitions.items():
            graph[from_name].append(to_name)

        route_path = [mission.origin] + mejor
        real_distance = self._real_route_distance(route_path, mission)

        planet_coords = {name: planet.coordinates() for name, planet in mission.planets.items()}
        current_dir = os.path.dirname(__file__)
        filename = os.path.join(current_dir, '..', 'static', 'mi_mapa_3d.png')
        filename = os.path.normpath(filename)
        draw_space_graph(graph, route_path, planet_coords, filename=filename)

        # --- NUEVO RETURN (alineado con tu frontend) ---
        return {
            'date': mission.date,
            'intro': mission.texts.get("instrucciones", mission.texts.get('introduccion', '')),
            
            'mission': mission.title,
            'planets': list(mission.planets.keys()),
            'planets_data': [vars(p) for p in mission.planets.values()],
            'origen': mission.origin,
            'destino': mission.destination,
            'blackholes': [bh.name for bh in mission.blackholes],
            'blackholes_data': [vars(bh) for bh in mission.blackholes],
            'spaceship': mission.spaceship.name if mission.spaceship else None,
            'spaceship_data': vars(mission.spaceship) if mission.spaceship else {},
            'route': route_path,
            'distance': real_distance,
            'graph': graph,
            'warnings': self._generate_warnings(mission),
            'texts': mission.texts
        }
    
    def _real_route_distance(self, route_path, mission):
        total = 0.0
        for i in range(len(route_path) - 1):
            name_a = route_path[i]
            name_b = route_path[i+1]
            planet_a = mission.planets.get(name_a)
            planet_b = mission.planets.get(name_b)
            if planet_a and planet_b:
                total += self.euclidean_distance(
                    planet_a.coordinates(),
                    planet_b.coordinates()
                )
        return total

    def _generate_warnings(self, mission):
        warnings = []
        if not mission.spaceship:
            warnings.append("No se definió nave espacial")
        if len(mission.blackholes) > 3:
            warnings.append("Muchos agujeros negros detectados - riesgo alto")
        return warnings

    def generate_latex_report(self, mission, route_info):
        """Genera un reporte en LaTeX con la información de la misión y la ruta"""
        latex_content = r"""
\documentclass{article}
\usepackage{graphicx}
\usepackage{amsmath}
\usepackage{float}

\title{Informe de Misión Espacial}
\author{Generado por SpaceAnalyzer}
\date{\today}

\begin{document}

\maketitle

\section*{Título de la Misión}
""" + mission.title + r"""

\section*{Fecha}
""" + mission.date + r"""

\section*{Detalles de la Misión}
\textbf{Origen:} """ + mission.origin + r"""
\textbf{Destino:} """ + mission.destination + r"""

\section*{Planetas Involucrados}
\begin{itemize}
""" + "".join([f"    \item {p}\n" for p in mission.planets.keys()]) + r"""
\end{itemize}

\section*{Agujeros Negros}
\begin{itemize}
""" + "".join([f"    \item {bh.name}\n" for bh in mission.blackholes]) + r"""
\end{itemize}

\section*{Ruta Óptima}
\textbf{Ruta:} """ + " $\rightarrow$ ".join(route_info['path']) + r"""
\textbf{Distancia Total:} """ + f"{route_info['distance']:.2f}" + r""" unidades

\end{document}
"""
        return latex_content