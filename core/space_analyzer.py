import math
import numpy as np
import matplotlib.pyplot as plt
from io import StringIO
from mpl_toolkits.mplot3d import Axes3D

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
        """Analiza contenido .space desde un string o archivo"""
        if isinstance(file_content, str):
            file_like = StringIO(file_content)
        else:
            file_like = file_content

        mission = self.Mission()
        current_section = "global"
        
        file_like.seek(0)
        for line in file_like:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            if line.startswith("[") and line.endswith("]"):
                current_section = line[1:-1].lower()
                continue

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

        return mission

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
        return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2 + (p1[2]-p2[2])**2)

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

    def build_graph(self, mission):
        graph = {name: [] for name in mission.planets}
        planet_names = list(mission.planets.keys())

        for i in range(len(planet_names)):
            for j in range(i+1, len(planet_names)):
                p1 = mission.planets[planet_names[i]]
                p2 = mission.planets[planet_names[j]]
                coord1, coord2 = p1.coordinates(), p2.coordinates()
                distance = self.euclidean_distance(coord1, coord2)
                
                safe = True
                if not self.DISABLE_RESTRICTION_CHECK and mission.spaceship:
                    if "evitar agujeros" in mission.spaceship.restricciones.lower():
                        safe = self.edge_safe(coord1, coord2, mission.blackholes)
                
                if safe:
                    graph[p1.name].append((p2.name, distance))
                    graph[p2.name].append((p1.name, distance))

        return graph

    def dijkstra(self, graph, start, goal):
        import heapq
        queue = [(0, start, [start])]
        visited = set()

        while queue:
            cost, node, path = heapq.heappop(queue)
            if node == goal:
                return cost, path
            if node in visited:
                continue
            visited.add(node)
            
            for neighbor, weight in graph.get(node, []):
                if neighbor not in visited:
                    heapq.heappush(queue, (cost + weight, neighbor, path + [neighbor]))

        return float('inf'), []

    def analyze(self, file_content):
        """Método principal que analiza el contenido .space"""
        mission = self.parse_space_file(file_content)
        graph = self.build_graph(mission)
        
        if mission.origin not in mission.planets or mission.destination not in mission.planets:
            raise ValueError("Origen o destino no están definidos entre los planetas")
        
        total_distance, route = self.dijkstra(graph, mission.origin, mission.destination)
        if total_distance == float('inf'):
            raise ValueError("No se encontró una ruta segura")
        
        # Mostrar la ruta por consola
        print("\n" + "="*50)
        print("RUTA ÓPTIMA ENCONTRADA")
        print(f"Origen: {mission.origin}")
        print(f"Destino: {mission.destination}")
        print(f"Distancia total: {total_distance:.2f} unidades")
        print("\nTrayectoria:")
        for i, planet in enumerate(route, 1):
            print(f"{i}. {planet}")
        print("="*50 + "\n")
        
        return {
            'date': mission.date,
            'ast': {
                'mission': mission.title,
                'planets': list(mission.planets.keys()),
                'planet_objects': list(mission.planets.values()),
                'blackholes': [bh.name for bh in mission.blackholes],
                'blackhole_objects': mission.blackholes,
                'spaceship': mission.spaceship.name if mission.spaceship else None,
                'spaceship_object': mission.spaceship
            },
            'route': {
                'path': route,
                'distance': total_distance
            },
            'graph': graph,
            'warnings': self._generate_warnings(mission)
        }

    def _generate_warnings(self, mission):
        warnings = []
        if not mission.spaceship:
            warnings.append("No se definió nave espacial")
        if len(mission.blackholes) > 3:
            warnings.append("Muchos agujeros negros detectados - riesgo alto")
        return warnings

    def generate_latex_report(self, mission, route_info):
        """Genera un reporte en LaTeX con la información de la misión y la ruta"""
        
        # Definir la cabecera del documento LaTeX
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
