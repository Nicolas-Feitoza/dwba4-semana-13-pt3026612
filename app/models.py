from datetime import datetime
from . import db  #

# Modelo para cargos ou papéis no sistema
class Role(db.Model):
    __tablename__ = 'roles'  # Nome da tabela no banco de dados
    id = db.Column(db.Integer, primary_key=True)  # Chave primária
    name = db.Column(db.String(64), unique=True, nullable=False)  # Nome do papel, único e obrigatório
    users = db.relationship('User', backref='role', lazy='dynamic')  # Relacionamento com a tabela User

    def __repr__(self):
        """
        Representação amigável do objeto Role.
        Retorna uma string com o nome do papel.
        """
        return f'<Role {self.name}>'

    def save(self):
        """
        Salva ou atualiza o registro no banco de dados.
        Possíveis erros:
        - IntegrityError: Se houver tentativa de salvar um papel com o mesmo nome já existente (violação de unicidade).
        - SQLAlchemyError: Qualquer outro erro de banco de dados.
        """
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()  # Reverte alterações no caso de erro
            raise RuntimeError(f"Erro ao salvar o papel '{self.name}': {str(e)}")

    def delete(self):
        """
        Remove o registro do banco de dados.
        Possíveis erros:
        - IntegrityError: Se o papel estiver associado a algum usuário (violação de integridade referencial).
        - SQLAlchemyError: Qualquer outro erro de banco de dados.
        """
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()  # Reverte alterações no caso de erro
            raise RuntimeError(f"Erro ao deletar o papel '{self.name}': {str(e)}")

# Modelo para usuários
class User(db.Model):
    __tablename__ = 'users'  # Nome da tabela no banco de dados
    id = db.Column(db.Integer, primary_key=True)  # Chave primária
    username = db.Column(db.String(64), unique=True, index=True, nullable=False)  # Nome do usuário, único e indexado
    prontuario = db.Column(db.String(10), unique=True, nullable=False)  # Prontuário único e obrigatório
    email = db.Column(db.String(120), unique=True, nullable=False)  # Email único e obrigatório
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))  # Chave estrangeira referenciando Role
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        """
        Representação amigável do objeto User.
        Retorna uma string com o nome e prontuário do usuário.
        """
        return f'<User {self.username} - Prontuário {self.prontuario}>'

    def save(self):
        """
        Salva ou atualiza o registro no banco de dados.
        Possíveis erros:
        - IntegrityError: Se houver duplicidade nos campos 'username', 'prontuario' ou 'email'.
        - SQLAlchemyError: Qualquer outro erro de banco de dados.
        """
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()  # Reverte alterações no caso de erro
            raise RuntimeError(f"Erro ao salvar o usuário '{self.username}': {str(e)}")

    def delete(self):
        """
        Remove o registro do banco de dados.
        Possíveis erros:
        - SQLAlchemyError: Qualquer erro de banco de dados durante a exclusão.
        """
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()  # Reverte alterações no caso de erro
            raise RuntimeError(f"Erro ao deletar o usuário '{self.username}': {str(e)}")

    @staticmethod
    def get_user_by_email(email):
        """
        Busca um usuário no banco de dados pelo email.

        :param email: Email do usuário a ser buscado.
        :return: Instância do usuário ou None se não encontrado.
        Possíveis erros:
        - SQLAlchemyError: Qualquer erro ao realizar a consulta no banco de dados.
        """
        try:
            return User.query.filter_by(email=email).first()
        except Exception as e:
            raise RuntimeError(f"Erro ao buscar usuário com email '{email}': {str(e)}")
