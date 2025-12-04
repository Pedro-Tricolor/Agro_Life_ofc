from flask import Blueprint, request, redirect, render_template, session
import psycopg2

bp = Blueprint('Adubos', __name__)


def ligar_banco():
    return psycopg2.connect(
        host="localhost",
        dbname="AgroLIfe",
        user="postgres",
        password="senai"
    )


# Página que lista todas os adubos
@bp.route('/adubos')
def listar_adubos():
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute("SELECT * FROM aglf_adubo")
    adubos = cursor.fetchall()
    cursor.close()
    banco.close()
    return render_template('adubo.html', adubos=adubos)


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
    # PostgreSQL usa %s
    cursor.execute("SELECT * FROM logar WHERE login=%s AND senha=%s", (nome, senha))
    usuario = cursor.fetchone()
    cursor.close()
    banco.close()
    # Se encontrou usuário
    if usuario:
        session['Usuario_Logado'] = nome
        return redirect('/adicionar_adubo')
    else:
        return render_template('Login.html', Titulo="Faça seu Login", erro="Login ou senha incorretos")


@bp.route('/logout')
def logout():
    session.pop('Usuario_Logado', None)  # Remove o usuário da sessão
    return redirect('/adubos')


# Página de cadastro de adubo
@bp.route('/adicionar_adubo', methods=['GET', 'POST'])
def adicionar_racao():
    if request.method == 'POST':
        nutrientes = request.form['nutrientes']
        peso = request.form['peso']
        descricao = request.form['descricao']
        estado = request.form['estado']
        fornecedor = request.form['fornecedor']
        quantidade = request.form['quantidade']
        preco = request.form['preco']
        banco = ligar_banco()
        cursor = banco.cursor()
        cursor.execute("""
            INSERT INTO aglf_adubo
            (nutriente_adubo, decricao_adubo, estado_adubo, fornecedor_adubo, quantidade_adubo, peso_adubo, preco_adubo)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (nutrientes, descricao, estado, fornecedor, quantidade, peso, preco))
        banco.commit()
        cursor.close()
        banco.close()
        return redirect('/adubos')  # redireciona para lista de rações
    return render_template('NovoAdubo.html')


@bp.route("/excluir_adubo/<int:id>", methods=["POST"])
def excluir_adubo(id):
    try:
        banco = ligar_banco()
        cursor = banco.cursor()
        cursor.execute("DELETE FROM aglf_adubo WHERE id_adubo = %s", (id,))
        banco.commit()
        cursor.close()
        banco.close()
        return redirect("/adubos")
    except Exception as e:
        print("Erro ao deletar:", e)
        return "Erro ao deletar o adubo."


@bp.route("/editar_adubo/<int:id>", methods=["GET"])
def editar_adubo(id):
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute("SELECT * FROM aglf_adubo WHERE id_adubo = %s", (id,))
    adubo = cursor.fetchone()
    cursor.close()
    banco.close()
    return render_template("EditarAdubo.html", adubo=adubo)


@bp.route("/atualizar_adubo/<int:id>", methods=["POST"])
def atualizar_adubo(id):
    # CORREÇÃO: Use os nomes corretos e ordem lógica
    nutrientes = request.form["nutrientes"]
    descricao = request.form["descricao"]
    estado = request.form["estado"]  # Corrigido: era "caracteristica"
    fornecedor = request.form["fornecedor"]
    quantidade = request.form["quantidade"]
    preco = request.form["preco"]
    peso = request.form["peso"]

    banco = ligar_banco()
    cursor = banco.cursor()

    try:
        # CORREÇÃO: Ordem correta dos parâmetros conforme a tabela
        cursor.execute("""
            UPDATE aglf_adubo
            SET nutriente_adubo=%s, decricao_adubo=%s, estado_adubo=%s,  
                fornecedor_adubo=%s, quantidade_adubo=%s, preco_adubo=%s, peso_adubo=%s
            WHERE id_adubo=%s
        """, (nutrientes, descricao, estado, fornecedor, quantidade, preco, peso, id))

        banco.commit()
        cursor.close()
        banco.close()

        return redirect("/adubos")

    except Exception as e:
        banco.rollback()
        print(f"Erro ao atualizar adubo: {e}")
        return f"Erro ao atualizar adubo: {str(e)}", 500



