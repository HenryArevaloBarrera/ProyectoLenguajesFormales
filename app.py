from flask import Flask, send_from_directory, jsonify
from core.api import api
import os

app = Flask(__name__, static_folder='static')
app.register_blueprint(api, url_prefix='/api')

@app.route('/')
def serve_frontend():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    # No interceptar rutas de la API
    if path.startswith("api/"):
        return jsonify({"error": "Ruta no encontrada"}), 404
    return send_from_directory(app.static_folder, path)

# Manejo global de errores 500 para debug y respuesta JSON clara al frontend
@app.errorhandler(500)
def error_500(e):
    import traceback
    print("[ERROR 500]", traceback.format_exc())
    return jsonify({
        "success": False,
        "error": "Error interno en el servidor",
        "trace": traceback.format_exc()
    }), 500

# (Opcional) Manejo de rutas no encontradas (404)
@app.errorhandler(404)
def error_404(e):
    return jsonify({"success": False, "error": "Ruta no encontrada"}), 404

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Render define PORT automáticamente
    app.run(host="0.0.0.0", port=port, debug=True)