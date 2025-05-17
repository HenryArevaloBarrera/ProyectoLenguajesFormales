print("[INFO] Se ha importado LexicalValidator desde core/Lexical_Validator.py")

class LexicalValidator:
    REQUIRED_PLANET_KEYS = ["nombre", "coordenadas", "radio", "gravedad"]
    REQUIRED_BLACKHOLE_KEYS = ["nombre", "coordenadas", "radio"]
    REQUIRED_SPACESHIP_KEYS = ["nombre", "velocidad", "combustible", "restricciones"]

    @staticmethod
    def parse_coordinates(coord_str):
        try:
            coords = coord_str.strip("()").split(",")
            return [float(c) for c in coords]
        except Exception:
            raise ValueError("Formato inválido para coordenadas.")

    @staticmethod
    def validate_planet(data):
        errors = []
        for key in LexicalValidator.REQUIRED_PLANET_KEYS:
            if key not in data:
                errors.append(f"Falta la clave requerida: {key} en planeta '{data.get('nombre', 'desconocido')}'")
        if "coordenadas" in data:
            try:
                coords = LexicalValidator.parse_coordinates(data["coordenadas"])
                if len(coords) != 3:
                    errors.append(f"Las coordenadas deben tener tres valores (x, y, z) en planeta '{data.get('nombre', 'desconocido')}'.")
            except Exception:
                errors.append(f"Las coordenadas deben estar en el formato (x,y,z) en planeta '{data.get('nombre', 'desconocido')}'.")
        if "radio" in data:
            try:
                radio = float(data["radio"])
                if radio <= 0:
                    errors.append(f"El radio debe ser un número positivo en planeta '{data.get('nombre', 'desconocido')}'.")
            except Exception:
                errors.append(f"El radio debe ser un número válido en planeta '{data.get('nombre', 'desconocido')}'.")
        if "gravedad" in data:
            try:
                gravedad = float(data["gravedad"])
                if gravedad <= 0:
                    errors.append(f"La gravedad debe ser un número positivo en planeta '{data.get('nombre', 'desconocido')}'.")
            except Exception:
                errors.append(f"La gravedad debe ser un número válido en planeta '{data.get('nombre', 'desconocido')}'.")
        return errors

    @staticmethod
    def validate_blackhole(data):
        errors = []
        for key in LexicalValidator.REQUIRED_BLACKHOLE_KEYS:
            if key not in data:
                errors.append(f"Falta la clave requerida: {key} en agujero negro '{data.get('nombre', 'desconocido')}'")
        if "coordenadas" in data:
            try:
                coords = LexicalValidator.parse_coordinates(data["coordenadas"])
                if len(coords) != 3:
                    errors.append(f"Las coordenadas deben tener tres valores (x, y, z) en agujero negro '{data.get('nombre', 'desconocido')}'.")
            except Exception:
                errors.append(f"Las coordenadas deben estar en el formato (x,y,z) en agujero negro '{data.get('nombre', 'desconocido')}'.")
        if "radio" in data:
            try:
                radio = float(data["radio"])
                if radio <= 0:
                    errors.append(f"El radio debe ser un número positivo en agujero negro '{data.get('nombre', 'desconocido')}'.")
            except Exception:
                errors.append(f"El radio debe ser un número válido en agujero negro '{data.get('nombre', 'desconocido')}'.")
        return errors

    @staticmethod
    def validate_spaceship(data):
        errors = []
        for key in LexicalValidator.REQUIRED_SPACESHIP_KEYS:
            if key not in data:
                errors.append(f"Falta la clave requerida: {key} en nave '{data.get('nombre', 'desconocido')}'")
        if "velocidad" in data:
            try:
                velocidad = float(data["velocidad"])
                if velocidad <= 0:
                    errors.append(f"La velocidad debe ser un número positivo en nave '{data.get('nombre', 'desconocido')}'.")
            except Exception:
                errors.append(f"La velocidad debe ser un número válido en nave '{data.get('nombre', 'desconocido')}'.")
        if "combustible" in data:
            try:
                combustible = float(data["combustible"])
                if combustible <= 0:
                    errors.append(f"El combustible debe ser un número positivo en nave '{data.get('nombre', 'desconocido')}'.")
            except Exception:
                errors.append(f"El combustible debe ser un número válido en nave '{data.get('nombre', 'desconocido')}'.")
        return errors

    @staticmethod
    def validate_texts(texts, required_keys):
        errors = []
        for key in required_keys:
            if key not in texts:
                errors.append(f"Falta el texto requerido: {key}")
        return errors

    def validate(self, source_code):
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
                parts = line.split(",")
                data = {}
                for part in parts:
                    if ":" in part:
                        k, v = part.split(":", 1)
                        data[k.strip().lower()] = v.strip()
                errors.extend(self.validate_planet(data))
            elif current_section in {"agujerosnegros", "agujeros_negros"}:
                parts = line.split(",")
                data = {}
                for part in parts:
                    if ":" in part:
                        k, v = part.split(":", 1)
                        data[k.strip().lower()] = v.strip()
                errors.extend(self.validate_blackhole(data))
            elif current_section == "nave":
                parts = line.split(",")
                data = {}
                for part in parts:
                    if ":" in part:
                        k, v = part.split(":", 1)
                        data[k.strip().lower()] = v.strip()
                errors.extend(self.validate_spaceship(data))
            # Puedes agregar más secciones si quieres

        if errors:
            # Mostrar errores como lista con punticos
            error_msg = "\n".join(f"• {err}" for err in errors)
            raise ValueError(f"Errores léxicos encontrados:\n{error_msg}")

        print("[INFO] Validación léxica superada (sin errores).")
        return True