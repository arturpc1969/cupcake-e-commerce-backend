# 🧁 Cupcake E-Commerce Backend                                                                                                                                                                                                     
                                                                                                                                                                                                                                    
Backend para um sistema de e-commerce de cupcakes desenvolvido com Django e Django Ninja.                                                                                                                                           
                                                                                                                                                                                                                                    
## 📋 Índice                                                                                                                                                                                                                        
                                                                                                                                                                                                                                    
- [Sobre o Projeto](#sobre-o-projeto)                                                                                                                                                                                               
- [Tecnologias](#tecnologias)                                                                                                                                                                                                       
- [Funcionalidades](#funcionalidades)                                                                                                                                                                                               
- [Requisitos](#requisitos)                                                                                                                                                                                                         
- [Instalação](#instalação)                                                                                                                                                                                                         
- [Configuração](#configuração)                                                                                                                                                                                                     
- [Estrutura do Projeto](#estrutura-do-projeto)                                                                                                                                                                                     
- [API Endpoints](#api-endpoints)                                                                                                                                                                                                   
- [Autenticação](#autenticação)                                                                                                                                                                                                     
- [Modelos de Dados](#modelos-de-dados)                                                                                                                                                                                             
- [Testes](#testes)                                                                                                                                                                                                                 
- [Variáveis de Ambiente](#variáveis-de-ambiente)                                                                                                                                                                                   
                                                                                                                                                                                                                                    
## 🎯 Sobre o Projeto                                                                                                                                                                                                               
                                                                                                                                                                                                                                    
Sistema backend completo para e-commerce de cupcakes, oferecendo gerenciamento de produtos, pedidos, endereços de entrega e autenticação de usuários com JWT.                                                                       
                                                                                                                                                                                                                                    
## 🚀 Tecnologias                                                                                                                                                                                                                   
                                                                                                                                                                                                                                    
- **Python 3.x**                                                                                                                                                                                                                    
- **Django** - Framework web                                                                                                                                                                                                        
- **Django Ninja** - Framework para APIs REST                                                                                                                                                                                       
- **PostgreSQL** - Banco de dados                                                                                                                                                                                                   
- **JWT** - Autenticação via tokens                                                                                                                                                                                                 
- **Pytest** - Testes automatizados                                                                                                                                                                                                 
                                                                                                                                                                                                                                    
## ✨ Funcionalidades                                                                                                                                                                                                               
                                                                                                                                                                                                                                    
### Autenticação e Usuários                                                                                                                                                                                                         
- ✅ Registro de usuários                                                                                                                                                                                                           
- ✅ Login com JWT (access token e refresh token)                                                                                                                                                                                   
- ✅ Atualização de perfil                                                                                                                                                                                                          
- ✅ Alteração de senha                                                                                                                                                                                                             
- ✅ Desativação de conta                                                                                                                                                                                                           
                                                                                                                                                                                                                                    
### Produtos                                                                                                                                                                                                                        
- ✅ Listagem de produtos                                                                                                                                                                                                           
- ✅ Detalhes do produto                                                                                                                                                                                                            
- ✅ Upload de imagens                                                                                                                                                                                                              
- ✅ Sistema de promoções                                                                                                                                                                                                           
- ✅ Soft delete (produtos inativos)                                                                                                                                                                                                
                                                                                                                                                                                                                                    
### Pedidos                                                                                                                                                                                                                         
- ✅ Criação de pedidos                                                                                                                                                                                                             
- ✅ Listagem de pedidos do usuário                                                                                                                                                                                                 
- ✅ Atualização de status (usuário e staff)                                                                                                                                                                                        
- ✅ Múltiplos métodos de pagamento                                                                                                                                                                                                 
- ✅ Numeração sequencial automática                                                                                                                                                                                                
                                                                                                                                                                                                                                    
### Itens do Pedido                                                                                                                                                                                                                 
- ✅ Adicionar produtos ao pedido                                                                                                                                                                                                   
- ✅ Atualizar quantidade                                                                                                                                                                                                           
- ✅ Remover itens                                                                                                                                                                                                                  
- ✅ Validação de duplicatas                                                                                                                                                                                                        
- ✅ Controle por status do pedido                                                                                                                                                                                                  
                                                                                                                                                                                                                                    
### Endereços de Entrega                                                                                                                                                                                                            
- ✅ Cadastro de múltiplos endereços                                                                                                                                                                                                
- ✅ Atualização e remoção                                                                                                                                                                                                          
- ✅ Validação de estados brasileiros                                                                                                                                                                                               
                                                                                                                                                                                                                                    
### Administração                                                                                                                                                                                                                   
- ✅ Painel administrativo Django                                                                                                                                                                                                   
- ✅ Endpoints exclusivos para staff                                                                                                                                                                                                
- ✅ Visualização completa de pedidos                                                                                                                                                                                               
                                                                                                                                                                                                                                    
## 📦 Requisitos                                                                                                                                                                                                                    
                                                                                                                                                                                                                                    
- Python 3.8+                                                                                                                                                                                                                       
- PostgreSQL 12+                                                                                                                                                                                                                    
- pip                                                                                                                                                                                                                               
                                                                                                                                                                                                                                    
## 🔧 Instalação                                                                                                                                                                                                                    
                                                                                                                                                                                                                                    
### 1. Clone o repositório                                                                                                                                                                                                          
                                                                                                                                                                                                                                    
```bash                                                                                                                                                                                                                             
git clone https://github.com/seu-usuario/cupcake-e-commerce-backend.git                                                                                                                                                             
cd cupcake-e-commerce-backend                                                                                                                                                                                                       
                                                                                                                                                                                                                                    

2. Crie um ambiente virtual                                                                                                                                                                                                         

                                                                                                                                                                                                                                    
python -m venv venv                                                                                                                                                                                                                 
source venv/bin/activate  # Linux/Mac                                                                                                                                                                                               
# ou                                                                                                                                                                                                                                
venv\Scripts\activate  # Windows                                                                                                                                                                                                    
                                                                                                                                                                                                                                    

3. Instale as dependências                                                                                                                                                                                                          

                                                                                                                                                                                                                                    
pip install -r requirements.txt                                                                                                                                                                                                     
                                                                                                                                                                                                                                    

4. Configure o banco de dados PostgreSQL                                                                                                                                                                                            

                                                                                                                                                                                                                                    
# Crie o banco de dados                                                                                                                                                                                                             
createdb cupcake                                                                                                                                                                                                                    
                                                                                                                                                                                                                                    

5. Execute as migrações                                                                                                                                                                                                             

                                                                                                                                                                                                                                    
python manage.py migrate                                                                                                                                                                                                            
                                                                                                                                                                                                                                    

6. Crie um superusuário                                                                                                                                                                                                             

                                                                                                                                                                                                                                    
python manage.py createsuperuser                                                                                                                                                                                                    
                                                                                                                                                                                                                                    

7. Execute o servidor                                                                                                                                                                                                               

                                                                                                                                                                                                                                    
python manage.py runserver                                                                                                                                                                                                          
                                                                                                                                                                                                                                    

O servidor estará disponível em http://localhost:8000                                                                                                                                                                               


⚙️ Configuração                                                                                                                                                                                                                     

Banco de Dados                                                                                                                                                                                                                      

Configure as variáveis de ambiente ou edite config/settings.py:                                                                                                                                                                     

                                                                                                                                                                                                                                    
DATABASES = {                                                                                                                                                                                                                       
    'default': {                                                                                                                                                                                                                    
        'ENGINE': 'django.db.backends.postgresql',                                                                                                                                                                                  
        'HOST': 'localhost',                                                                                                                                                                                                        
        'NAME': 'cupcake',                                                                                                                                                                                                          
        'USER': 'postgres',                                                                                                                                                                                                         
        'PASSWORD': 'password',                                                                                                                                                                                                     
        'PORT': '5432',                                                                                                                                                                                                             
    }                                                                                                                                                                                                                               
}                                                                                                                                                                                                                                   
                                                                                                                                                                                                                                    

CORS                                                                                                                                                                                                                                

O projeto está configurado para aceitar requisições de http://localhost:3000 (frontend React/Next.js).                                                                                                                              

Para adicionar outras origens, edite em config/settings.py:                                                                                                                                                                         

                                                                                                                                                                                                                                    
CORS_ALLOWED_ORIGINS = [                                                                                                                                                                                                            
    "http://localhost:3000",                                                                                                                                                                                                        
    "https://seu-dominio.com",                                                                                                                                                                                                      
]                                                                                                                                                                                                                                   
                                                                                                                                                                                                                                    

Arquivos de Mídia                                                                                                                                                                                                                   

Imagens de produtos são armazenadas em uma conta no Cloudinary, configurado através de variáveis de ambiente.                                                                                                            


📁 Estrutura do Projeto                                                                                                                                                                                                             

                                                                                                                                                                                                                                    
cupcake-e-commerce-backend/                                                                                                                                                                                                         
├── accounts/                 # App de autenticação                                                                                                                                                                                 
│   ├── deps.py              # Dependências de autenticação                                                                                                                                                                         
│   ├── models.py            # Modelo User customizado                                                                                                                                                                              
│   ├── schemas.py           # Schemas de entrada/saída                                                                                                                                                                             
│   └── utils.py             # Funções JWT                                                                                                                                                                                          
├── api/                     # App principal da API                                                                                                                                                                                 
│   ├── models/              # Modelos de dados                                                                                                                                                                                     
│   │   ├── common.py        # BaseModel e ActiveManager                                                                                                                                                                            
│   │   ├── product.py       # Modelo Product                                                                                                                                                                                       
│   │   ├── order.py         # Modelo Order                                                                                                                                                                                         
│   │   ├── orderitem.py     # Modelo OrderItem                                                                                                                                                                                     
│   │   └── deliveryaddress.py # Modelo DeliveryAddress                                                                                                                                                                             
│   ├── schemas/             # Schemas Pydantic                                                                                                                                                                                     
│   ├── services/            # Lógica de negócio                                                                                                                                                                                    
│   ├── tests/               # Testes automatizados                                                                                                                                                                                 
│   ├── utils.py             # Decoradores e utilitários                                                                                                                                                                            
│   └── views/               # Endpoints da API                                                                                                                                                                                     
├── config/                  # Configurações Django                                                                                                                                                                                 
│   ├── settings.py          # Configurações principais                                                                                                                                                                             
│   └── urls.py              # URLs principais                                                                                                                                                                                      
└── manage.py                # CLI do Django                                                                                                                                                                                         
                                                                                                                                                                                                                                    


🔌 API Endpoints                                                                                                                                                                                                                    

Autenticação                                                                                                                                                                                                                        

                                                              
  Método   Endpoint            Descrição                Auth  
 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 
  POST     /api/auth/signup    Registrar novo usuário   Não   
  POST     /api/auth/login     Login (retorna tokens)   Não   
  POST     /api/auth/refresh   Renovar access token     Não   
                                                              

Usuários                                                                                                                                                                                                                            

                                                                        
  Método   Endpoint                     Descrição                 Auth  
 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 
  GET      /api/users/me                Dados do usuário logado   Sim   
  PUT      /api/users/me                Atualizar perfil          Sim   
  POST     /api/users/change-password   Alterar senha             Sim   
  PATCH    /api/users/me                Desativar conta           Sim   
                                                                        

Produtos                                                                                                                                                                                                                            

                                                                  
  Método   Endpoint               Descrição                Auth   
 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 
  GET      /api/products          Listar produtos ativos   Não    
  GET      /api/products/{uuid}   Detalhes do produto      Não    
  POST     /api/products          Criar produto            Staff  
  PUT      /api/products/{uuid}   Atualizar produto        Staff  
  DELETE   /api/products/{uuid}   Soft delete produto      Staff  
                                                                  

Pedidos                                                                                                                                                                                                                             

                                                                  
  Método   Endpoint            Descrição                   Auth   
 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 
  GET      /api/orders              Listar pedidos do usuário    Sim    
  GET      /api/orders/admin        Listar todos pedidos         Staff  
  GET      /api/orders/{id}         Detalhes do pedido           Sim    
  POST     /api/orders              Criar pedido                 Sim    
  PUT      /api/orders/{id}         Confirmar pedido (usuário)   Sim    
  PUT      /api/orders/admin/{id}   Atualizar status (staff)     Staff  
                                                                        

Itens do Pedido                                                                                                                                                                                                                     

                                                                      
  Método   Endpoint                 Descrição                  Auth   
 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 
  GET      /api/order-items         Listar itens dos pedidos   Sim    
  GET      /api/order-items/staff   Listar todos itens         Staff  
  GET      /api/order-items/{id}    Detalhes do item           Sim    
  POST     /api/order-items         Adicionar item ao pedido   Sim    
  PUT      /api/order-items/{id}    Atualizar quantidade       Sim    
  DELETE   /api/order-items/{id}    Remover item               Sim    
                                                                      

Endereços de Entrega                                                                                                                                                                                                                

                                                                       
  Método   Endpoint                       Descrição              Auth  
 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 
  GET      /api/delivery-addresses        Listar endereços       Sim   
  GET      /api/delivery-addresses/{id}   Detalhes do endereço   Sim   
  POST     /api/delivery-addresses        Criar endereço         Sim   
  PUT      /api/delivery-addresses/{id}   Atualizar endereço     Sim   
  DELETE   /api/delivery-addresses/{id}   Remover endereço       Sim   
                                                                       


🔐 Autenticação                                                                                                                                                                                                                     

O sistema utiliza JWT (JSON Web Tokens) com dois tipos de tokens:                                                                                                                                                                   

Access Token                                                                                                                                                                                                                        

 • Duração: 60 minutos                                                                                                                                                                                                              
 • Usado para autenticar requisições à API                                                                                                                                                                                          
 • Enviado no header: Authorization: Bearer {access_token}                                                                                                                                                                          

Refresh Token                                                                                                                                                                                                                       

 • Duração: 7 dias                                                                                                                                                                                                                  
 • Usado para obter novos access tokens                                                                                                                                                                                             
 • Não expira enquanto estiver sendo usado                                                                                                                                                                                          

Exemplo de Uso                                                                                                                                                                                                                      

                                                                                                                                                                                                                                    
# 1. Login                                                                                                                                                                                                                          
curl -X POST http://localhost:8000/api/auth/login \                                                                                                                                                                                 
  -H "Content-Type: application/json" \                                                                                                                                                                                             
  -d '{"username": "user", "password": "pass"}'                                                                                                                                                                                     
                                                                                                                                                                                                                                    
# Resposta:                                                                                                                                                                                                                         
# {                                                                                                                                                                                                                                 
#   "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",                                                                                                                                                                                   
#   "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",                                                                                                                                                                                  
#   "token_type": "bearer"                                                                                                                                                                                                          
# }                                                                                                                                                                                                                                 
                                                                                                                                                                                                                                    
# 2. Usar o access token                                                                                                                                                                                                            
curl -X GET http://localhost:8000/api/users/me \                                                                                                                                                                                    
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..."                                                                                                                                                                             
                                                                                                                                                                                                                                    
# 3. Renovar token                                                                                                                                                                                                                  
curl -X POST http://localhost:8000/api/auth/refresh \                                                                                                                                                                               
  -H "Content-Type: application/json" \                                                                                                                                                                                             
  -d '{"refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."}'                                                                                                                                                                              
                                                                                                                                                                                                                                    


💾 Modelos de Dados                                                                                                                                                                                                                 

User (Usuário)                                                                                                                                                                                                                      

                                                                                                                                                                                                                                    
- id: int                                                                                                                                                                                                                           
- uuid: UUID                                                                                                                                                                                                                        
- username: string (único)                                                                                                                                                                                                          
- email: string                                                                                                                                                                                                                     
- first_name: string                                                                                                                                                                                                                
- last_name: string                                                                                                                                                                                                                 
- is_active: boolean                                                                                                                                                                                                                
- is_staff: boolean                                                                                                                                                                                                                 
                                                                                                                                                                                                                                    

Product (Produto)                                                                                                                                                                                                                   

                                                                                                                                                                                                                                    
- id: int                                                                                                                                                                                                                           
- uuid: UUID                                                                                                                                                                                                                        
- name: string                                                                                                                                                                                                                      
- description: text                                                                                                                                                                                                                 
- price: decimal                                                                                                                                                                                                                    
- image: file                                                                                                                                                                                                                       
- promotion: boolean                                                                                                                                                                                                     
- is_active: boolean                                                                                                                                                                                                                
                                                                                                                                                                                                                                    

Order (Pedido)                                                                                                                                                                                                                      

                                                                                                                                                                                                                                    
- id: int                                                                                                                                                                                                                           
- order_number: string (auto-gerado)                                                                                                                                                                                                
- user: FK(User)                                                                                                                                                                                                                    
- delivery_address: FK(DeliveryAddress)                                                                                                                                                                                             
- payment_method: choice                                                                                                                                                                                                            
- status: choice (PENDING, CONFIRMED, PREPARATION, etc.)                                                                                                                                                                              
- total: decimal                                                                                                                                                                                                                    
- is_active: boolean                                                                                                                                                                                                                
- created_at: datetime                                                                                                                                                                                                              
- updated_at: datetime                                                                                                                                                                                                              
                                                                                                                                                                                                                                    

OrderItem (Item do Pedido)                                                                                                                                                                                                          

                                                                                                                                                                                                                                    
- id: int                                                                                                                                                                                                                           
- order: FK(Order)                                                                                                                                                                                                                  
- product: FK(Product)                                                                                                                                                                                                              
- quantity: int                                                                                                                                                                                                                     
- unit_price: decimal                                                                                                                                                                                                               
                                                                                                                                                                                                                                    

DeliveryAddress (Endereço de Entrega)                                                                                                                                                                                               

                                                                                                                                                                                                                                    
- id: int                                                                                                                                                                                                                           
- user: FK(User)                                                                                                                                                                                                                    
- address_name: string                                                                                                                                                                                                                    
- address_description: string                                                                                                                                                                                                                    
- city: string                                                                                                                                                                                                                      
- state: choice (siglas dos estados)                                                                                                                                                                                                
- zip_code: string                                                                                                                                                                                                                  
- is_active: boolean                                                                                                                                                                                                                
                                                                                                                                                                                                                                    


🧪 Testes                                                                                                                                                                                                                           

O projeto possui testes automatizados usando pytest.                                                                                                                                                                                

Executar todos os testes                                                                                                                                                                                                            

                                                                                                                                                                                                                                    
pytest                                                                                                                                                                                                                              
                                                                                                                                                                                                                                    

Executar testes específicos                                                                                                                                                                                                         

                                                                                                                                                                                                                                    
# Testes de produtos                                                                                                                                                                                                                
pytest api/tests/views/test_products.py                                                                                                                                                                                             
                                                                                                                                                                                                                                    
# Testes de pedidos                                                                                                                                                                                                                 
pytest api/tests/views/test_orders.py                                                                                                                                                                                               
                                                                                                                                                                                                                                    
# Testes de itens do pedido                                                                                                                                                                                                         
pytest api/tests/views/test_orderitems.py                                                                                                                                                                                           
                                                                                                                                                                                                                                    
# Testes de endereços                                                                                                                                                                                                               
pytest api/tests/views/test_deliveryaddresses.py                                                                                                                                                                                    
                                                                                                                                                                                                                                    

Cobertura de Testes                                                                                                                                                                                                                 

                                                                                                                                                                                                                                    
pytest --cov=api --cov=accounts                                                                                                                                                                                                     
                                                                                                                                                                                                                                    


🌍 Variáveis de Ambiente                                                                                                                                                                                                            

Crie um arquivo .env na raiz do projeto:                                                                                                                                                                                            

                                                                                                                                                                                                                                    
# Banco de Dados                                                                                                                                                                                                                    
CUPCAKE_DB_HOST=localhost                                                                                                                                                                                                           
CUPCAKE_DB_NAME=cupcake                                                                                                                                                                                                             
CUPCAKE_DB_USER=postgres                                                                                                                                                                                                            
CUPCAKE_DB_PASSWORD=password                                                                                                                                                                                                        
CUPCAKE_DB_PORT=5432                                                                                                                                                                                                                
CUPCAKE_DB_CONN_MAX_AGE=600                                                                                                                                                                                                         
                                                                                                                                                                                                                                    
# Django                                                                                                                                                                                                                            
SECRET_KEY=sua-chave-secreta-aqui                                                                                                                                                                                                   
DEBUG=True                                                                                                                                                                                                                          
ALLOWED_HOSTS=localhost,127.0.0.1                                                                                                                                                                                                   
                                                                                                                                                                                                                                    
# JWT                                                                                                                                                                                                                               
ACCESS_TOKEN_LIFETIME_MINUTES=60                                                                                                                                                                                                    
REFRESH_TOKEN_LIFETIME_DAYS=7                                                                                                                                                                                                       

# Coudinary
CLOUDINARY_API_KEY=sua-api-key-cloudinary
CLOUDINARY_API_SECRET=seu-api-secret-cloudinary
CLOUDINARY_CLOUD_NAME=seu-cloud-name-claudinary                                                                                                                                                                                                                                    


📝 Status dos Pedidos                                                                                                                                                                                                               

                                                     
  Status      Descrição                              
 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 
  DRAFT             Pedido iniciado, mas ainda não submetido
  PENDING           Pedido submetido, porém ainda não confirmado  
  CONFIRMED         Pedido confirmado         
  PREPARATION       Pedido em preparação                   
  DELIVERY          Pedido em entrega             
  WAITING_PAYMENT   Aguardando Pagamento                     
  DELIVERED         Pedido entregue                        
  FINISHED          Pedido Finalizado
  CANCELED          Pedido cancelado                       
                                                      


💳 Métodos de Pagamento                                                                                                                                                                                                             

 • CREDIT_CARD - Cartão de Crédito                                                                                                                                                                                                  
 • DEBIT_CARD - Cartão de Débito                                                                                                                                                                                                    
 • BANK_SLIP - Boleto Bancário                                                                                                                                                                                                      
 • PIX - Pix                                                                                                                                                                                                                        

────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
⭐ Desenvolvido com Django e Django Ninja

────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

👥 Autor

 • Nome: Artur de Paula Coutinho
 • RGM: 29655960
 • Curso: Engenharia de Software
 • Instituição: UNICID
