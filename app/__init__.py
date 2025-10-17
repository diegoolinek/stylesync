from flask import Flask
from pymongo import MongoClient

db = None

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    global db
    
    try:
        client = MongoClient(app.config['MONGO_URI'])
        db = client.get_default_database()
    except Exception as e:
        print(f"Erro ao realizar a conexão com o banco de dados: {e}")
        
        
    from .routes.main import main_bp
    app.register_blueprint(main_bp)
    from .routes.category_routes import category_bp
    app.register_blueprint(category_bp)
    
    return app
