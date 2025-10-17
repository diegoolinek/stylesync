from flask import Blueprint, jsonify, request
from app.models.user import LoginPayload
from pydantic import ValidationError
from app import db
from bson import ObjectId
from app.models.products import Product, ProductDBModel

main_bp = Blueprint('main_bp', __name__)


# RF: o sistema deve permitir que o usuário se autentique para obter um token
@main_bp.route('/login', methods=['POST'])
def login():
    try:
        raw_data = request.get_json()
        user_data = LoginPayload(**raw_data)
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400
    except Exception as e:
        return jsonify({"error": "Erro durante a requisição do dado"}),500
    
    if user_data.username == "admin" and user_data.password == "123":
        return jsonify({"message": f"Login bem sucedido para o usuário {user_data.username}"})
    else:
        return jsonify({"error": "Credenciais inválidas"}), 401


# RF: o sistema deve permitir que o usuário visualize a lista de produtos disponíveis
@main_bp.route('/products', methods=['GET'])
def get_products():
    products_cursor = db.products.find({})
    products_list = [ProductDBModel(**product).model_dump(by_alias=True, exclude_none=True) for product in products_cursor]
        
    return jsonify(products_list)


# RF: o sistema deve permitir que o usuário adicione produtos a listagem
@main_bp.route('/products', methods=['POST'])
def create_products():
    return jsonify(message="Esta é a rota de criação de produtos")


# RF: o sistema deve permitir que o usuário visualize os detalhes de um produto
@main_bp.route('/product/<string:product_id>', methods=['GET'])
def get_product_by_id(product_id):
    try:
        oid = ObjectId(product_id)
    except Exception as e:
        return jsonify(message=f"Erro ao transformar o {product_id} em ObjectId: {e}")
    
    product = db.products.find_one({'_id': oid})
    if product:
        product_model = ProductDBModel(**product).model_dump(by_alias=True, exclude_none=True)
        return jsonify(product_model)
    else:
        return jsonify(message=f"Produto com o ID {product_id} não encontrado"), 404


# RF: o sistema deve permitir que o usuário atualize as informações de um produto
@main_bp.route('/product/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    return jsonify(message=f"Esta é a rota de atualização do produto {product_id}")


# RF: o sistema deve permitir que o usuário delete um produto
@main_bp.route('/product/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    return jsonify(message=f"Esta é a rota de deleção do produto {product_id}")


# RF: o sistema deve permitir que o usuário delete um produto
@main_bp.route('/sales/upload', methods=['POST'])
def upload_sales():
    return jsonify(message="Esta é a rota de upload de vendas")


@main_bp.route('/')
def index():
    return jsonify(message="Bem vindo ao StyleSync!")



