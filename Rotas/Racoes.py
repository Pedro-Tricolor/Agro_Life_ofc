from flask import Blueprint, request, redirect, render_template, session, url_for
import psycopg2

bp = Blueprint('Racoes', __name__)


def ligar_banco():
    return psycopg2.connect(
        host="localhost",
        dbname="AgroLIfe",
        user="postgres",
        password="senai"
    )


# ------------------------------
# ROTA: LISTAR RAÇÕES
# ------------------------------
@bp.route('/racoes')
def listar_racoes():
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute("SELECT * FROM aglf_racao")
    racoes = cursor.fetchall()
    cursor.close()
    banco.close()
    return render_template('racoes.html', racoes=racoes)


# ------------------------------
# ROTA: LOGIN
# ------------------------------
@bp.route('/login')
def login():
    return render_template('Login.html', Titulo="Faça seu Login")


# ------------------------------
# ROTA: AUTENTICAR LOGIN
# ------------------------------
@bp.route('/autenticar', methods=["POST"])
def autenticar():
    nome = request.form['usuario']
    senha = request.form['senha']
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute("SELECT * FROM logar WHERE login=%s AND senha=%s", (nome, senha))
    usuario = cursor.fetchone()
    cursor.close()
    banco.close()
    if usuario:
        session['Usuario_Logado'] = nome
        return redirect('/adicionar_racao')
    else:
        return render_template('Login.html', Titulo="Faça seu Login", erro="Login ou senha incorretos")


@bp.route('/logout')
def logout():
    session.pop('Usuario_Logado', None)
    return redirect('/racoes')


# ------------------------------
# ROTA: ADICIONAR RAÇÃO (PROTEGIDA)
# ------------------------------
@bp.route('/adicionar_racao', methods=['GET', 'POST'])
def adicionar_racao():
    if "Usuario_Logado" not in session:
        return redirect('/login')
    if request.method == 'POST':
        materia_prima = request.form['materia_prima']
        peso = request.form['peso']
        descricao = request.form['descricao']
        tipo = request.form['tipo']
        fornecedor = request.form['fornecedor']
        quantidade = request.form['quantidade']
        preco = request.form['preco']
        banco = ligar_banco()
        cursor = banco.cursor()
        cursor.execute("""
            INSERT INTO aglf_racao 
            (materia_prima_racao, decricao_racao, tipo_racao, fornecedor_racao, quantidade_racao, preco_racao, peso_racao)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (materia_prima, descricao, tipo, fornecedor, quantidade, preco, peso))
        banco.commit()
        cursor.close()
        banco.close()
        return redirect('/racoes')
    return render_template('NovaRacao.html')


@bp.route("/excluir_racao/<int:id>", methods=["POST"])
def excluir_racao(id):
    try:
        banco = ligar_banco()
        cursor = banco.cursor()
        cursor.execute("DELETE FROM aglf_racao WHERE id_racao = %s", (id,))
        banco.commit()
        cursor.close()
        banco.close()
        return redirect("/racoes")
    except Exception as e:
        print("Erro ao deletar:", e)
        return "Erro ao deletar o Ração."


@bp.route("/editar_racao/<int:id>", methods=["GET"])
def editar_racao(id):
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute("SELECT * FROM aglf_racao WHERE id_racao = %s", (id,))
    racao = cursor.fetchone()
    cursor.close()
    banco.close()
    return render_template("EditarRacao.html", racao=racao)


@bp.route("/atualizar_racao/<int:id>", methods=["POST"])
def atualizar_racao(id):
    materia_prima = request.form["materia-prima"]
    descricao = request.form["descricao"]
    tipo = request.form["tipo"]
    fornecedor = request.form["fornecedor"]
    quantidade = request.form["quantidade"]
    preco = request.form["preco"]
    peso = request.form["peso"]
    banco = ligar_banco()
    cursor = banco.cursor()
    try:
        cursor.execute("""
            UPDATE aglf_racao
            SET materia_prima_racao=%s, decricao_racao=%s, tipo_racao=%s, fornecedor_racao=%s, 
                quantidade_racao=%s, preco_racao=%s, peso_racao=%s
            WHERE id_racao=%s
        """, (materia_prima, descricao, tipo, fornecedor, quantidade, preco, peso, id))
        banco.commit()
        cursor.close()
        banco.close()
        return redirect("/racoes")
    except Exception as e:
        banco.rollback()
        print(f"Erro ao atualizar: {e}")
        return f"Erro ao atualizar: {e}", 500
