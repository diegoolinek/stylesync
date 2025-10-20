from flask import Blueprint, jsonify, request, current_app
from app.models.user import LoginPayload
from pydantic import ValidationError
from app import db
from bson import ObjectId
from app.models.products import Product, ProductDBModel, UpdateProduct
from app.models.sale import Sale
from app.decorators import token_required
from datetime import datetime, timedelta, timezone, date
import jwt
import csv
import os
import io


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
        token = jwt.encode(
            {
                "user_id": user_data.username,
                "exp": datetime.now(tz=timezone.utc) + timedelta(minutes=30)
            },
            current_app.config['SECRET_KEY'],
            algorithm="HS256"
        )
        
        return jsonify({"access_token": token}), 200
    
    return jsonify({"error": "Credenciais inválidas"}), 401


# RF: o sistema deve permitir que o usuário visualize a lista de produtos disponíveis
@main_bp.route('/products', methods=['GET'])
def get_products():
    products_cursor = db.products.find({})
    products_list = [ProductDBModel(**product).model_dump(by_alias=True, exclude_none=True) for product in products_cursor]
        
    return jsonify(products_list)


# RF: o sistema deve permitir que o usuário adicione produtos a listagem
@main_bp.route('/products', methods=['POST'])
@token_required
def create_products(token):
    try:
        product = Product(**request.get_json())
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400
    
    result = db.products.insert_one(product.model_dump())

    return jsonify({"message": "Produto criado com sucesso",
                   "id": str(result.inserted_id)}), 201


# RF: o sistema deve permitir que o usuário visualize os detalhes de um produto
@main_bp.route('/product/<string:product_id>', methods=['GET'])
def get_product_by_id(product_id):
    try:
        oid = ObjectId(product_id)
    except Exception as e:
        return jsonify({"message":f"Erro ao transformar o {product_id} em ObjectId: {e}"})
    
    product = db.products.find_one({'_id': oid})
    if product:
        product_model = ProductDBModel(**product).model_dump(by_alias=True, exclude_none=True)
        return jsonify(product_model)
    else:
        return jsonify({"message":f"Produto com o ID {product_id} não encontrado"}), 404


# RF: o sistema deve permitir que o usuário atualize as informações de um produto
@main_bp.route('/product/<string:product_id>', methods=['PUT'])
@token_required
def update_product(token, product_id):
    try:
        oid = ObjectId(product_id)
        update_data = UpdateProduct(**request.get_json())
        
    except ValidationError as e:
        return jsonify({"error":e.errors()}), 400
    
    update_result = db.products.update_one(
            {'_id': oid}, 
            {'$set': update_data.model_dump(exclude_unset=True)}
        )
    
    if update_result.matched_count == 0:
        return jsonify({"error":f"Produto com o ID {product_id} não encontrado"}), 404

    updated_product = db.products.find_one({"_id": oid})

    return jsonify(ProductDBModel(**updated_product).model_dump(by_alias=True, exclude_none=True))


# RF: o sistema deve permitir que o usuário delete um produto
@main_bp.route('/product/<string:product_id>', methods=['DELETE'])
@token_required
def delete_product(token, product_id):
    try:
        oid = ObjectId(product_id)
    except Exception:
        return jsonify({"error":"ID do produto inválido"}), 400

    delete_product = db.products.delete_one({"_id": oid})

    if delete_product.deleted_count == 0:
        return jsonify({"error":f"O produto não foi encontrado"}), 404

    return jsonify({"message":"Produto deletado com sucesso"}), 204


# RF: o sistema deve permitir a importação de vendas a partir de um arquivo CSV
@main_bp.route('/sales/upload', methods=['POST'])
@token_required
def upload_sales(token):
    if 'file' not in request.files:
        return jsonify({"error":"Nenhum arquivo enviado"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error":"Nenhum arquivo selecionado"}), 400

    if file and file.filename.endswith(".csv"):
        csv_stream = io.StringIO(file.stream.read().decode("UTF-8"), newline=None)
        csv_reader = csv.DictReader(csv_stream)
        
        sales_to_insert = []
        error = []
        
        for row_num, row in enumerate(csv_reader, 1):
            try:
                sale_data = Sale(**row)
                
                sale_dict = sale_data.model_dump()
                
                if isinstance(sale_dict['sale_date'], date):
                    sale_dict['sale_date'] = datetime.combine(sale_dict['sale_date'], datetime.min.time())

                sales_to_insert.append(sale_dict)
            except ValidationError as e:
                error.append(f"Linha {row_num} com dados inválidos: {e.errors()}")
            except Exception as e:
                error.append(f"Linha {row_num} com erro inesperado: {str(e)}")
                
        if sales_to_insert:
            try:
                db.sales.insert_many(sales_to_insert)
            except Exception as e:
                return jsonify({"error": f"{e}"}), 500

        return jsonify({
            "message":"Upload concluído com sucesso",
            "vendas importadas": len(sales_to_insert),
            "erros encontrados": error
        }), 200


@main_bp.route('/')
def index():
    return jsonify({"message":"Bem vindo ao StyleSync!"})
