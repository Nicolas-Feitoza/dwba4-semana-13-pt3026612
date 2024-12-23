import os
import unittest
from app import create_app, db
from app.models import User  # Importa seus modelos

# Configuração de ambiente de teste
class TestConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False  # Desabilita CSRF para testes

# Configura o ambiente e cria o aplicativo para testes
app = create_app('testing')
app.config.from_object(TestConfig)

# Contexto de teste para executar os testes de forma isolada
def setup():
    db.create_all()  # Cria todas as tabelas antes dos testes

@app.before_request
def before_request():
    db.session.rollback()  # Faz rollback para garantir isolamento em cada teste

@app.teardown_request
def teardown_request(exception=None):
    db.session.remove()  # Remove a sessão após cada requisição/teste

# Adiciona todas as configurações necessárias e classes de testes
class TestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()  # Cria tabelas para o teste atual
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()  # Limpa tabelas após o teste
        self.ctx.pop()

