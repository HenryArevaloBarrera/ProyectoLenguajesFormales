from flask import Blueprint, request, jsonify
from .analyzer import Analyzer

api = Blueprint('api', __name__)
analyzer = Analyzer()

@api.route('/analyze', methods=['POST'])
def analyze_route():
    # Verificar el tipo de contenido
    if not request.is_json:
        return jsonify({'error': 'Content-Type must be application/json'}), 400
    
    data = request.get_json()
    
    # Verificar que el campo 'code' existe
    if not data or 'code' not in data:
        return jsonify({
            'success': False,
            'error': 'Missing required field: code'
        }), 400
    
    try:
        results = analyzer.analyze(data['code'])
        
        if 'error' in results:
            return jsonify(results), 400

        # DEVUELVE TODO EL DICCIONARIO PLANO DEL BACKEND
        return jsonify({
            'success': True,
            'data': results
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
    return response