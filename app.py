from flask import Flask,render_template, request, session, redirect
import psycopg2
from Rotas import Racoes,Adubos

app = Flask(__name__)
app.register_blueprint(Racoes.bp)
app.register_blueprint(Adubos.bp)


app.secret_key = "agrolife_key_segura"

def ligar_banco():
    banco = psycopg2.connect(
        host="localhost",
        dbname="AgroLIfe",
        user="postgres",
        password="senai",
    )
    return banco


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        senha = request.form['senha']

        banco = ligar_banco()
        cursor = banco.cursor()
        cursor.execute("SELECT id_login FROM Logar WHERE login = %s AND senha = %s", (usuario, senha))
        resultado = cursor.fetchone()
        banco.close()

        if resultado:
            session['usuario'] = usuario
            return redirect('/racoes')  # Redireciona para a página principal
        else:
            return render_template('login.html', erro='Usuário ou senha incorretos.')

    return render_template('login.html')



@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
