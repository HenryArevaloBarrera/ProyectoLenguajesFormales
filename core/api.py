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
            
        return jsonify({
            'success': True,
            'data': {
                'mission': results['ast']['mission'],
                'date': results.get('date', ''),
                'planets': results['ast']['planets'],
                'planets_data': [{'name': p.name, 'x': p.x, 'y': p.y, 'z': p.z} 
                               for p in results['ast'].get('planet_objects', [])],
                'blackholes': results['ast']['blackholes'],
                'blackholes_data': [{'name': bh.name, 'x': bh.x, 'y': bh.y, 'z': bh.z, 'radius': bh.radius} 
                                   for bh in results['ast'].get('blackhole_objects', [])],
                'spaceship': results['ast']['spaceship'],
                'spaceship_data': {
                    'velocity': results['ast'].get('spaceship_object', {}).velocity if hasattr(results['ast'].get('spaceship_object'), 'velocity') else None,
                    'fuel': results['ast'].get('spaceship_object', {}).fuel if hasattr(results['ast'].get('spaceship_object'), 'fuel') else None,
                    'restrictions': results['ast'].get('spaceship_object', {}).restricciones if hasattr(results['ast'].get('spaceship_object'), 'restricciones') else None
                },
                'route': results['route']['path'],
                'distance': results['route']['distance'],
                'graph': results['graph']
            },
            'warnings': results['warnings']
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