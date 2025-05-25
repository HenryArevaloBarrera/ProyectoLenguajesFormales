import re

print("[INFO] Se ha importado LexicalValidator desde core/Lexical_Validator.py")

class LexicalValidator:
    REQUIRED_PLANET_KEYS = ["nombre", "coordenadas", "radio", "gravedad"]
    REQUIRED_BLACKHOLE_KEYS = ["nombre", "coordenadas", "radio"]
    REQUIRED_SPACESHIP_KEYS = ["nombre", "velocidad", "combustible", "restricciones"]
    REQUIRED_TEXT_KEYS = ["introduccion", "descripcion", "restricciones", "ruta", "conclusion"]

    # Caracteres prohibidos para LaTeX en nombres y textos
    LATEX_PROHIBITED_CHARS = r'[_&%$#{}~^\\]'
    LATEX_CHAR_REGEX = re.compile(LATEX_PROHIBITED_CHARS)

    IDENT_REGEX = re.compile(r"^[A-Za-zÁÉÍÓÚáéíóú0-9 \-']+$")  # Quitado el guion bajo
    NUM_REGEX = re.compile(r"^-?\d+(\.\d+)?$")
    COORD_REGEX = re.compile(
        r"^\(\s*-?\d+(\.\d+)?\s*,\s*-?\d+(\.\d+)?\s*,\s*-?\d+(\.\d+)?\s*\)$"
    )

    @staticmethod
    def parse_coordinates(coord_str):
        if not LexicalValidator.COORD_REGEX.match(coord_str):
            raise ValueError("Formato inválido para coordenadas.")
        coords = coord_str.strip("()").split(",")
        coords = [c.strip() for c in coords if c.strip() != ""]
        return [float(c) for c in coords]

    @staticmethod
    def smart_split(line):
        return [x.strip() for x in re.split(r',(?![^(]*\))', line)]

    @classmethod
    def has_latex_forbidden_chars(cls, value):
        return bool(cls.LATEX_CHAR_REGEX.search(value))

    @classmethod
    def validate_planet(cls, data):
        errors = []
        for key in cls.REQUIRED_PLANET_KEYS:
            if key not in data:
                errors.append(f"Falta la clave requerida: {key} en planeta '{data.get('nombre', 'desconocido')}'")
        if "nombre" in data:
            if not cls.IDENT_REGEX.match(data["nombre"]):
                errors.append(f"El nombre '{data['nombre']}' no es un identificador válido para planeta.")
            if cls.has_latex_forbidden_chars(data["nombre"]):
                errors.append(f"El nombre '{data['nombre']}' contiene caracteres prohibidos para LaTeX (como _ & % $ # {{ }} ~ ^ \\) en planeta.")
        if "coordenadas" in data:
            try:
                coords = cls.parse_coordinates(data["coordenadas"])
                if len(coords) != 3:
                    errors.append(f"Las coordenadas deben tener tres valores (x, y, z) en planeta '{data.get('nombre', 'desconocido')}'.")
            except Exception:
                errors.append(f"Las coordenadas deben estar en el formato (x,y,z) en planeta '{data.get('nombre', 'desconocido')}'.")
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
        if "nombre" in data:
            if not cls.IDENT_REGEX.match(data["nombre"]):
                errors.append(f"El nombre '{data['nombre']}' no es un identificador válido para agujero negro.")
            if cls.has_latex_forbidden_chars(data["nombre"]):
                errors.append(f"El nombre '{data['nombre']}' contiene caracteres prohibidos para LaTeX (como _ & % $ # {{ }} ~ ^ \\) en agujero negro.")
        if "coordenadas" in data:
            try:
                coords = cls.parse_coordinates(data["coordenadas"])
                if len(coords) != 3:
                    errors.append(f"Las coordenadas deben tener tres valores (x, y, z) en agujero negro '{data.get('nombre', 'desconocido')}'.")
            except Exception:
                errors.append(f"Las coordenadas deben estar en el formato (x,y,z) en agujero negro '{data.get('nombre', 'desconocido')}'.")
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
        if "nombre" in data:
            if not cls.IDENT_REGEX.match(data["nombre"]):
                errors.append(f"El nombre '{data['nombre']}' no es un identificador válido para nave.")
            if cls.has_latex_forbidden_chars(data["nombre"]):
                errors.append(f"El nombre '{data['nombre']}' contiene caracteres prohibidos para LaTeX (como _ & % $ # {{ }} ~ ^ \\) en nave.")
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

    @classmethod
    def validate_texts(cls, data):
        errors = []
        keys_found = set(data.keys())
        for key in cls.REQUIRED_TEXT_KEYS:
            if key not in data:
                errors.append(f"Falta la clave requerida: {key} en sección [Textos]")
        for key in data:
            if key not in cls.REQUIRED_TEXT_KEYS:
                errors.append(f"Clave inesperada '{key}' en sección [Textos]")
            if cls.has_latex_forbidden_chars(data[key]):
                errors.append(f"El texto de '{key}' contiene caracteres prohibidos para LaTeX (como _ & % $ # {{ }} ~ ^ \\).")
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
        textos_data = {}

        if "???" in source_code:
            errors.append("Símbolo inválido '???' encontrado en el archivo.")

        for idx, line in enumerate(source_code.splitlines(), 1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("[") and line.endswith("]"):
                if current_section == "textos" and textos_data:
                    errors.extend(self.validate_texts(textos_data))
                    textos_data = {}
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
            elif current_section == "textos":
                if ":" in line:
                    k, v = line.split(":", 1)
                    key = k.strip().lower()
                    if key in textos_data:
                        errors.append(f"Clave duplicada '{key}' en sección [Textos]")
                    textos_data[key] = v.strip()

        if current_section == "textos" and textos_data:
            errors.extend(self.validate_texts(textos_data))

        if errors:
            error_msg = "\n".join(f"• {err}" for err in errors)
            raise ValueError(f"Errores léxicos encontrados:\n{error_msg}")

        print("[INFO] Validación léxica superada (sin errores).")
        return True