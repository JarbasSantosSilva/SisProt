from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import pymysql
import os
import datetime

load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

bcrypt = Bcrypt(app)

def get_db():
    return pymysql.connect(
        host=os.getenv('DB_HOST'),
        port=int(os.getenv('DB_PORT', 3306)),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME'),
        cursorclass=pymysql.cursors.Cursor
    )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        cpf = request.form['cpf']
        email = request.form['email']
        senha = bcrypt.generate_password_hash(request.form['senha']).decode('utf-8')
        conn = get_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO usuarios (nome, cpf, email, senha, perfil) VALUES (%s, %s, %s, %s, %s)",
                (nome, cpf, email, senha, 'solicitante'))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('index'))
    return render_template('cadastro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
        usuario = cur.fetchone()
        cur.close()
        conn.close()
        if usuario and bcrypt.check_password_hash(usuario[4], senha):
            session['usuario_id'] = usuario[0]
            session['usuario_nome'] = usuario[1]
            session['usuario_perfil'] = usuario[5]
            return redirect(url_for('index'))
        else:
            flash('Email ou senha incorretos')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/nova_solicitacao', methods=['GET', 'POST'])
def nova_solicitacao():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, nome FROM tipos_solicitacao WHERE ativo = 1")
    tipos = cur.fetchall()
    cur.close()
    conn.close()
    if request.method == 'POST':
        id_tipo = request.form['id_tipo']
        descricao = request.form['descricao']
        id_usuario = session['usuario_id']
        numero_protocolo = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        conn = get_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO solicitacoes (numero_protocolo, id_usuario, id_tipo, descricao, status, data_abertura) VALUES (%s, %s, %s, %s, %s, %s)",
                    (numero_protocolo, id_usuario, id_tipo, descricao, 'aberto', datetime.datetime.now()))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('index'))
    return render_template('nova_solicitacao.html', tipos=tipos)

@app.route('/minhas_solicitacoes')
def minhas_solicitacoes():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT s.id, s.numero_protocolo, s.id_usuario, s.id_tipo, s.descricao, s.status, t.nome, s.data_abertura
        FROM solicitacoes s
        JOIN tipos_solicitacao t ON s.id_tipo = t.id
        WHERE s.id_usuario = %s
        ORDER BY s.data_abertura DESC
    """, (session['usuario_id'],))
    solicitacoes = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('minhas_solicitacoes.html', solicitacoes=solicitacoes)

@app.route('/painel_atendente')
def painel_atendente():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    if session['usuario_perfil'] != 'atendente' and session['usuario_perfil'] != 'admin':
        return redirect(url_for('index'))
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT s.id, s.numero_protocolo, s.id_usuario, s.id_tipo, s.descricao, s.status, s.data_abertura, u.nome, t.nome
        FROM solicitacoes s
        JOIN usuarios u ON s.id_usuario = u.id
        JOIN tipos_solicitacao t ON s.id_tipo = t.id
        ORDER BY s.data_abertura DESC
    """)
    solicitacoes = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('painel_atendente.html', solicitacoes=solicitacoes)

@app.route('/deferir/<int:id>')
def deferir(id):
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    conn = get_db()
    cur = conn.cursor()
    cur.execute("UPDATE solicitacoes SET status = 'deferido' WHERE id = %s", (id,))
    cur.execute("INSERT INTO tramitacoes (id_solicitacao, id_atendente, status_novo, observacao, data) VALUES (%s, %s, %s, %s, %s)",
                (id, session['usuario_id'], 'deferido', 'Solicitação deferida.', datetime.datetime.now()))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('painel_atendente'))

@app.route('/indeferir/<int:id>')
def indeferir(id):
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    conn = get_db()
    cur = conn.cursor()
    cur.execute("UPDATE solicitacoes SET status = 'indeferido' WHERE id = %s", (id,))
    cur.execute("INSERT INTO tramitacoes (id_solicitacao, id_atendente, status_novo, observacao, data) VALUES (%s, %s, %s, %s, %s)",
                (id, session['usuario_id'], 'indeferido', 'Solicitação indeferida.', datetime.datetime.now()))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('painel_atendente'))

@app.route('/historico/<int:id>')
def historico(id):
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT s.id, s.numero_protocolo, s.id_usuario, s.id_tipo, s.descricao, s.status, s.data_abertura, t.nome
        FROM solicitacoes s
        JOIN tipos_solicitacao t ON s.id_tipo = t.id
        WHERE s.id = %s
    """, (id,))
    solicitacao = cur.fetchone()
    cur.execute("""
        SELECT tr.id, tr.id_solicitacao, tr.id_atendente, tr.status_novo, tr.observacao, tr.data, u.nome
        FROM tramitacoes tr
        JOIN usuarios u ON tr.id_atendente = u.id
        WHERE tr.id_solicitacao = %s
        ORDER BY tr.data ASC
    """, (id,))
    tramitacoes = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('historico.html', solicitacao=solicitacao, tramitacoes=tramitacoes)

@app.route('/cadastro_atendente', methods=['GET', 'POST'])
def cadastro_atendente():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    if session['usuario_perfil'] != 'admin':
        return redirect(url_for('index'))
    if request.method == 'POST':
        nome = request.form['nome']
        cpf = request.form['cpf']
        email = request.form['email']
        senha = bcrypt.generate_password_hash(request.form['senha']).decode('utf-8')
        conn = get_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO usuarios (nome, cpf, email, senha, perfil) VALUES (%s, %s, %s, %s, %s)",
                    (nome, cpf, email, senha, 'atendente'))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('index'))
    return render_template('cadastro_atendente.html')

@app.route('/excluir_usuario/<int:id>')
def excluir_usuario(id):
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    if session['usuario_perfil'] != 'admin':
        return redirect(url_for('index'))
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM usuarios WHERE id = %s AND perfil = 'atendente'", (id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('listar_usuarios'))

@app.route('/listar_usuarios')
def listar_usuarios():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    if session['usuario_perfil'] != 'admin':
        return redirect(url_for('index'))
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, nome, cpf, email, perfil FROM usuarios WHERE perfil = 'atendente'")
    usuarios = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('listar_usuarios.html', usuarios=usuarios)

@app.route('/api/solicitacoes', methods=['GET'])
def api_solicitacoes():
    if 'usuario_id' not in session:
        return jsonify({'erro': 'Não autorizado'}), 401
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT s.id, s.numero_protocolo, s.descricao, s.status, s.data_abertura, t.nome
        FROM solicitacoes s
        JOIN tipos_solicitacao t ON s.id_tipo = t.id
        WHERE s.id_usuario = %s
    """, (session['usuario_id'],))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    solicitacoes = []
    for row in rows:
        solicitacoes.append({
            'id': row[0],
            'protocolo': row[1],
            'descricao': row[2],
            'status': row[3],
            'data_abertura': str(row[4]),
            'tipo': row[5]
        })
    return jsonify(solicitacoes)

@app.route('/api/protocolo/<numero>', methods=['GET'])
def api_protocolo(numero):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT s.id, s.numero_protocolo, s.descricao, s.status, s.data_abertura, t.nome
        FROM solicitacoes s
        JOIN tipos_solicitacao t ON s.id_tipo = t.id
        WHERE s.numero_protocolo = %s
    """, (numero,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    if not row:
        return jsonify({'erro': 'Protocolo não encontrado'}), 404
    return jsonify({
        'id': row[0],
        'protocolo': row[1],
        'descricao': row[2],
        'status': row[3],
        'data_abertura': str(row[4]),
        'tipo': row[5]
    })

if __name__ == '__main__':
    app.run(debug=False)