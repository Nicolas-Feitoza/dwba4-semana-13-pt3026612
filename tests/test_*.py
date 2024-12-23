import unittest
from flask import current_app
from app import create_app, db
from app.models import User
from app.main.forms import NameForm

class BasicTestCase(unittest.TestCase):
    def setUp(self):
        """Configura o ambiente de teste."""
        self.app = create_app('testing')  # Cria o app com configuração de teste
        self.app_context = self.app.app_context()
        self.app_context.push()  # Abre o contexto da aplicação
        db.create_all()  # Cria o banco de dados para testes
        self.client = self.app.test_client()  # Adiciona o cliente de teste

    def tearDown(self):
        """Limpa o ambiente de teste."""
        db.session.remove()  # Remove as sessões do banco
        db.drop_all()  # Dropa todas as tabelas
        self.app_context.pop()  # Retira o contexto da aplicação

    def test_app_exists(self):
        """Verifica se o aplicativo está inicializado corretamente."""
        self.assertIsNotNone(current_app)

    def test_app_is_testing(self):
        """Verifica se o aplicativo está configurado para o ambiente de teste."""
        self.assertTrue(current_app.config['TESTING'])

    def test_homepage_status_code(self):
        """Verifica o status da página inicial."""
        response = self.client.get('/')  # Certifique-se de usar o método correto para obter a resposta.
        self.assertEqual(response.status_code, 200)

    def test_db_connection(self):
        """Verifica se o banco de dados está conectado corretamente."""
        self.assertIsNotNone(db.session)

    def test_user_model(self):
        """Verifica o modelo de usuário básico e sua criação."""
        user = User(username='testuser', prontuario='ABC1234567', email='testuser@example.com')
        db.session.add(user)
        db.session.commit()

        retrieved_user = User.query.filter_by(username='testuser').first()
        self.assertIsNotNone(retrieved_user)
        self.assertEqual(retrieved_user.username, 'testuser')
        self.assertEqual(retrieved_user.prontuario, 'ABC1234567')
        self.assertEqual(retrieved_user.email, 'testuser@example.com')

    def test_email_validation(self):
        """Verifica a validação do campo de e-mail para garantir que e-mails duplicados não sejam aceitos."""
        user1 = User(username='testuser1', prontuario='ABC1234568', email='testuser1@example.com')
        db.session.add(user1)
        db.session.commit()

        form = NameForm(data={
            'name': 'Test User2',
            'prontuario': 'ABC1234569',
            'email': 'testuser1@example.com'
        })

        self.assertFalse(form.validate(), "O formulário não deve passar devido ao e-mail duplicado.")
        self.assertIn('Este e-mail já está registrado.', form.errors['email'])

    def test_prontuario_validation(self):
        """Verifica a validação do campo de prontuário para garantir que prontuários duplicados não sejam aceitos."""
        user1 = User(username='testuser1', prontuario='ABC1234568', email='testuser1@example.com')
        db.session.add(user1)
        db.session.commit()

        form = NameForm(data={
            'name': 'Test User2',
            'prontuario': 'ABC1234568',
            'email': 'testuser2@example.com'
        })

        self.assertFalse(form.validate(), "O formulário não deve passar devido ao prontuário duplicado.")
        self.assertIn('Este prontuário já está registrado.', form.errors['prontuario'])

    def test_form_validation_on_invalid_inputs(self):
        """Verifica se o formulário rejeita entradas inválidas corretamente."""
        form = NameForm(data={
            'name': '',
            'prontuario': 'ABC123456',  # Prontuário incompleto (deveria ser validado como inválido)
            'email': 'invalidemail'      # E-mail inválido
        })

        self.assertFalse(form.validate(), "O formulário não deve validar com entradas inválidas.")
        self.assertIn('O campo de nome é obrigatório.', form.errors['name'])
        self.assertIn('O prontuário deve ter 3 letras seguidas de 7 números. Exemplo: ABC1234567', form.errors['prontuario'])  # Corrigido para verificar a mensagem correta
        self.assertIn('Insira um e-mail válido.', form.errors['email'])
