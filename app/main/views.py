from flask import render_template, session, redirect, url_for, flash, current_app
from .. import db
from ..models import User
from ..email import send_simple_message, send_email_with_gif
from . import main
from .forms import NameForm

@main.route('/', methods=['GET', 'POST'])
def index():
    """
    Rota principal que lida com a submissão de formulário e exibe usuários cadastrados.
    """
    form = NameForm()

    if form.validate_on_submit():
        # Verifica se o prontuário já está cadastrado
        user = User.query.filter_by(prontuario=form.prontuario.data).first()

        if user is None:
            # Verifica se o nome já está cadastrado
            user_name = User.query.filter_by(username=form.name.data).first()
            if user_name is None:
                # Se o usuário não estiver registrado, cria um novo usuário no banco de dados
                user = User(username=form.name.data, prontuario=form.prontuario.data, email=form.email.data)
                db.session.add(user)  # Adiciona o novo usuário ao banco
                db.session.commit()

                session['known'] = False
                flash('Você está cadastrado! O administrador será notificado.')

                # Envia notificações para o administrador e o e-mail da escola
                email_admin = [current_app.config['FLASKY_ADMIN']]
                recipient_list = ['flaskaulasweb@zohomail.com', email_admin]

                admin_message = f"Novo usuário cadastrado:\nProntuário: {form.prontuario.data}\nNome: {form.name.data}\nE-mail: {form.email.data}"
                user_message = f"Bem-vindo(a), {form.name.data}!\nSeu cadastro foi realizado com sucesso."

                send_simple_message(to=recipient_list[0], subject="Novo Cadastro", new_user=admin_message)
                send_simple_message(to=recipient_list[1], subject="Notificação de Cadastro", new_user=admin_message)

                # Envia e-mail com GIF de boas-vindas para o usuário
                url = 'https://nicolassf.pythonanywhere.com/static/images/welcome.gif'
                send_email_with_gif(to=form.email.data, subject="Confirmação de Cadastro", body=user_message, gif_url=url)
            else:
                session['known'] = True
                flash('Nome já registrado!')  # Mensagem de erro para nome duplicado
        else:
            session['known'] = True
            flash('Prontuário já cadastrado!')

        session['name'] = form.name.data
        return redirect(url_for('.index'))  # Redireciona de volta para a página principal

    # Consulta e exibe todos os usuários cadastrados
    users = User.query.all()
    return render_template(
        'index.html',
        form=form,
        name=session.get('name'),
        known=session.get('known', False),
        users=users
    )
