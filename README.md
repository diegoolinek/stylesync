# StyleSync - API de Gerenciamento de Produtos

## 📋 Sobre o Projeto

O **StyleSync** é uma API REST desenvolvida em Flask para gerenciamento de produtos e vendas. O sistema permite autenticação de usuários, CRUD completo de produtos, importação de vendas via CSV e gerenciamento de categorias.

## 🚀 Funcionalidades

### 🔐 Autenticação
- Sistema de login com JWT
- Tokens com expiração de 30 minutos
- Middleware de autenticação para rotas protegidas

### 📦 Gerenciamento de Produtos
- **GET** `/products` - Listar todos os produtos
- **POST** `/products` - Criar novo produto (requer autenticação)
- **GET** `/product/<id>` - Visualizar produto específico
- **PUT** `/product/<id>` - Atualizar produto (requer autenticação)
- **DELETE** `/product/<id>` - Deletar produto (requer autenticação)

### 📊 Gerenciamento de Vendas
- **POST** `/sales/upload` - Importar vendas via arquivo CSV (requer autenticação)

## 🛠️ Tecnologias Utilizadas

- **Flask** - Framework web Python
- **MongoDB** - Banco de dados NoSQL
- **PyMongo** - Driver Python para MongoDB
- **Pydantic** - Validação de dados e serialização
- **JWT** - Autenticação via tokens
- **Python-dotenv** - Gerenciamento de variáveis de ambiente
- **CSV** - Processamento de arquivos CSV

## 📁 Estrutura do Projeto

```
stylesync-flask/
├── app/
│   ├── __init__.py              # Configuração da aplicação Flask
│   ├── decorators.py            # Decorators de autenticação
│   ├── models/                  # Modelos de dados
│   │   ├── category.py          # Modelo de categoria
│   │   ├── products.py          # Modelo de produto
│   │   ├── sale.py              # Modelo de venda
│   │   └── user.py              # Modelo de usuário
│   └── routes/                  # Rotas da API
│       ├── main.py              # Rotas principais (produtos, vendas, auth)
│       └── category_routes.py   # Rotas de categorias
├── config.py                    # Configurações da aplicação
├── run.py                       # Arquivo principal para execução
└── tests/                       # Diretório de testes
```

## ⚙️ Configuração e Instalação

### Pré-requisitos
- Python 3.8+
- MongoDB
- Git

### 1. Clone o repositório
```bash
git clone https://github.com/diegoolinek/stylesync.git
cd stylesync
```

### 2. Crie um ambiente virtual
```bash
python -m venv venv
```

### 3. Ative o ambiente virtual
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 4. Instale as dependências
```bash
pip install -r requirements.txt
```

### 5. Configure as variáveis de ambiente
Crie um arquivo `.env` na raiz do projeto:
```env
MONGO_URI=mongodb://usuario:senha@host:porta/database
SECRET_KEY=chave_secreta
```

### 6. Execute a aplicação
```bash
python run.py
```

A API estará disponível em `http://localhost:5000`

## 📚 Documentação da API

### Autenticação

#### Login
```http
POST /login
Content-Type: application/json

{
    "username": "admin",
    "password": "123"
}
```

**Resposta:**
```json
{
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### Produtos

#### Listar Produtos
```http
GET /products
```

#### Criar Produto
```http
POST /products
Authorization: Bearer <token>
Content-Type: application/json

{
    "name": "Produto Exemplo",
    "price": 99.90,
    "description": "Descrição do produto",
    "stock": 10
}
```

#### Visualizar Produto
```http
GET /product/<product_id>
```

#### Atualizar Produto
```http
PUT /product/<product_id>
Authorization: Bearer <token>
Content-Type: application/json

{
    "name": "Nome Atualizado",
    "price": 89.90
}
```

#### Deletar Produto
```http
DELETE /product/<product_id>
Authorization: Bearer <token>
```

### Vendas

#### Importar Vendas via CSV
```http
POST /sales/upload
Authorization: Bearer <token>
Content-Type: multipart/form-data

file: arquivo.csv
```

**Formato do CSV:**
```csv
sale_date,product_id,quantity,total_value
2024-01-15,507f1f77bcf86cd799439011,2,199.80
2024-01-16,507f1f77bcf86cd799439012,1,99.90
```


## 🔒 Segurança

- Autenticação baseada em JWT
- Tokens com expiração automática (30 minutos)
- Validação de dados com Pydantic
- Headers de autorização obrigatórios para operações sensíveis

## 🧪 Testes

Para executar os testes:
```bash
python -m pytest tests/
```

## 📝 Modelos de Dados

### Produto
```python
{
    "name": str,           # Nome do produto
    "price": float,        # Preço
    "description": str,    # Descrição (opcional)
    "stock": int           # Quantidade em estoque
}
```

### Venda
```python
{
    "sale_date": date,     # Data da venda
    "product_id": str,     # ID do produto
    "quantity": int,       # Quantidade vendida
    "total_value": float   # Valor total
}
```

### Categoria
```python
{
    "name": str,           # Nome da categoria
    "description": str     # Descrição (opcional)
}
```


## 📄 Licença

Este projeto está sob a licença MIT.

## 👥 Autor

- **Diego Olinek** - *Desenvolvedor* - [GitHub](https://github.com/diegoolinek)
