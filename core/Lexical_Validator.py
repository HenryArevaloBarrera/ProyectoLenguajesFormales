print("[INFO] Se ha importado LexicalValidator desde core/Lexical_Validator.py")
import re

class LexicalValidator:
    REQUIRED_PLANET_KEYS = ["nombre", "coordenadas", "radio", "gravedad"]
    REQUIRED_BLACKHOLE_KEYS = ["nombre", "coordenadas", "radio"]
    REQUIRED_SPACESHIP_KEYS = ["nombre", "velocidad", "combustible", "restricciones"]

    # Regex para tokens léxicos principales (simulando AFD con regex)
    IDENT_REGEX = re.compile(r"^[A-Za-zÁÉÍÓÚáéíóú0-9 _\-']+$")
    NUM_REGEX = re.compile(r"^-?\d+(\.\d+)?$")
    COORD_REGEX = re.compile(
        r"^\(\s*-?\d+(\.\d+)?\s*,\s*-?\d+(\.\d+)?\s*,\s*-?\d+(\.\d+)?\s*\)$"
    )

    @staticmethod
    def parse_coordinates(coord_str):
        # Validación léxica de coordenadas usando regex
        if not LexicalValidator.COORD_REGEX.match(coord_str):
            raise ValueError("Formato inválido para coordenadas.")
        coords = coord_str.strip("()").split(",")
        coords = [c.strip() for c in coords if c.strip() != ""]
        return [float(c) for c in coords]

    @staticmethod
    def smart_split(line):
        # Separa por comas que NO están dentro de paréntesis
        return [x.strip() for x in re.split(r',(?![^(]*\))', line)]

    @classmethod
    def validate_planet(cls, data):
        errors = []
        for key in cls.REQUIRED_PLANET_KEYS:
            if key not in data:
                errors.append(f"Falta la clave requerida: {key} en planeta '{data.get('nombre', 'desconocido')}'")
        # Validar nombre léxico
        if "nombre" in data and not cls.IDENT_REGEX.match(data["nombre"]):
            errors.append(f"El nombre '{data['nombre']}' no es un identificador válido para planeta.")
        # Validar coordenadas
        if "coordenadas" in data:
            try:
                coords = cls.parse_coordinates(data["coordenadas"])
                if len(coords) != 3:
                    errors.append(f"Las coordenadas deben tener tres valores (x, y, z) en planeta '{data.get('nombre', 'desconocido')}'.")
            except Exception:
                errors.append(f"Las coordenadas deben estar en el formato (x,y,z) en planeta '{data.get('nombre', 'desconocido')}'.")
        # Validar radio léxico
        if "radio" in data:
            if not cls.NUM_REGEX.match(data["radio"]):
                errors.append(f"El radio debe ser numérico en planeta '{data.get('nombre', 'desconocido')}'.")
            else:
                try:
                    radio = float(data["radio"])
                    if radio <= 0:
                        errors.append(f"El radio debe ser un número positivo en planeta '{data.get('nombre', 'desconocido')}'.")
                except Exception:
                    errors.append(f"El radio debe ser un número válido en planeta '{data.get('nombre', 'desconocido')}'.")
        # Validar gravedad léxico
        if "gravedad" in data:
            if not cls.NUM_REGEX.match(data["gravedad"]):
                errors.append(f"La gravedad debe ser numérica en planeta '{data.get('nombre', 'desconocido')}'.")
            else:
                try:
                    gravedad = float(data["gravedad"])
                    if gravedad <= 0:
                        errors.append(f"La gravedad debe ser un número positivo en planeta '{data.get('nombre', 'desconocido')}'.")
                except Exception:
                    errors.append(f"La gravedad debe ser un número válido en planeta '{data.get('nombre', 'desconocido')}'.")
        return errors

    @classmethod
    def validate_blackhole(cls, data):
        errors = []
        for key in cls.REQUIRED_BLACKHOLE_KEYS:
            if key not in data:
                errors.append(f"Falta la clave requerida: {key} en agujero negro '{data.get('nombre', 'desconocido')}'")
        # Validar nombre léxico
        if "nombre" in data and not cls.IDENT_REGEX.match(data["nombre"]):
            errors.append(f"El nombre '{data['nombre']}' no es un identificador válido para agujero negro.")
        # Validar coordenadas
        if "coordenadas" in data:
            try:
                coords = cls.parse_coordinates(data["coordenadas"])
                if len(coords) != 3:
                    errors.append(f"Las coordenadas deben tener tres valores (x, y, z) en agujero negro '{data.get('nombre', 'desconocido')}'.")
            except Exception:
                errors.append(f"Las coordenadas deben estar en el formato (x,y,z) en agujero negro '{data.get('nombre', 'desconocido')}'.")
        # Validar radio léxico
        if "radio" in data:
            if not cls.NUM_REGEX.match(data["radio"]):
                errors.append(f"El radio debe ser numérico en agujero negro '{data.get('nombre', 'desconocido')}'.")
            else:
                try:
                    radio = float(data["radio"])
                    if radio <= 0:
                        errors.append(f"El radio debe ser un número positivo en agujero negro '{data.get('nombre', 'desconocido')}'.")
                except Exception:
                    errors.append(f"El radio debe ser un número válido en agujero negro '{data.get('nombre', 'desconocido')}'.")
        return errors

    @classmethod
    def validate_spaceship(cls, data):
        errors = []
        for key in cls.REQUIRED_SPACESHIP_KEYS:
            if key not in data:
                errors.append(f"Falta la clave requerida: {key} en nave '{data.get('nombre', 'desconocido')}'")
        # Validar nombre léxico
        if "nombre" in data and not cls.IDENT_REGEX.match(data["nombre"]):
            errors.append(f"El nombre '{data['nombre']}' no es un identificador válido para nave.")
        # Validar velocidad léxico
        if "velocidad" in data:
            if not cls.NUM_REGEX.match(data["velocidad"]):
                errors.append(f"La velocidad debe ser numérica en nave '{data.get('nombre', 'desconocido')}'.")
            else:
                try:
                    velocidad = float(data["velocidad"])
                    if velocidad <= 0:
                        errors.append(f"La velocidad debe ser un número positivo en nave '{data.get('nombre', 'desconocido')}'.")
                except Exception:
                    errors.append(f"La velocidad debe ser un número válido en nave '{data.get('nombre', 'desconocido')}'.")
        # Validar combustible léxico
        if "combustible" in data:
            if not cls.NUM_REGEX.match(data["combustible"]):
                errors.append(f"El combustible debe ser numérico en nave '{data.get('nombre', 'desconocido')}'.")
            else:
                try:
                    combustible = float(data["combustible"])
                    if combustible <= 0:
                        errors.append(f"El combustible debe ser un número positivo en nave '{data.get('nombre', 'desconocido')}'.")
                except Exception:
                    errors.append(f"El combustible debe ser un número válido en nave '{data.get('nombre', 'desconocido')}'.")
        return errors

    def validate(self, source_code):
        print("[DEBUG] --- TEXTO RECIBIDO POR EL VALIDADOR ---")
        print(source_code)
        print("[DEBUG] ---------------------------------------")
        print("[INFO] Validando léxico completo...")
        if not source_code or not source_code.strip():
            raise ValueError("El código fuente está vacío")

        errors = []
        current_section = None

        if "???" in source_code:
            errors.append("Símbolo inválido '???' encontrado en el archivo.")

        for idx, line in enumerate(source_code.splitlines(), 1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("[") and line.endswith("]"):
                current_section = line[1:-1].lower()
                continue

            if current_section == "planetas":
                parts = self.smart_split(line)
                data = {}
                for part in parts:
                    if ":" in part:
                        k, v = part.split(":", 1)
                        data[k.strip().lower()] = v.strip()
                errors.extend(self.validate_planet(data))
            elif current_section in {"agujerosnegros", "agujeros_negros"}:
                parts = self.smart_split(line)
                data = {}
                for part in parts:
                    if ":" in part:
                        k, v = part.split(":", 1)
                        data[k.strip().lower()] = v.strip()
                errors.extend(self.validate_blackhole(data))
            elif current_section == "nave":
                parts = self.smart_split(line)
                data = {}
                for part in parts:
                    if ":" in part:
                        k, v = part.split(":", 1)
                        data[k.strip().lower()] = v.strip()
                errors.extend(self.validate_spaceship(data))

        if errors:
            error_msg = "\n".join(f"• {err}" for err in errors)
            raise ValueError(f"Errores léxicos encontrados:\n{error_msg}")

        print("[INFO] Validación léxica superada (sin errores).")
        return True