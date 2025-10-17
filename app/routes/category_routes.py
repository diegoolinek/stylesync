from flask import Blueprint, jsonify 


category_bp = Blueprint('category_bp', __name__, url_prefix='/categories') 


@category_bp.route('/', methods=['GET']) 
def get_categories(): 
    return jsonify({"message": "Retorna a lista de todas as categorias."}) 


@category_bp.route('/', methods=['POST']) 
def create_category(): 
    return jsonify({"message": "Cria uma nova categoria."}) 
