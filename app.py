from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def init_db():
    conn = sqlite3.connect('barbearia.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cliente (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            telefone TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS barbeiro (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            especialidade TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cliente', methods=['GET', 'POST'])
def cliente():
    if request.method == 'POST':
        nome = request.form['nome']
        telefone = request.form['telefone']
        if not nome or not telefone:
            flash('Nome e telefone são obrigatórios')
        else:
            conn = sqlite3.connect('barbearia.db')
            cursor = conn.cursor()
            cursor.execute('INSERT INTO cliente (nome, telefone) VALUES (?, ?)', (nome, telefone))
            conn.commit()
            conn.close()
            flash('Cliente adicionado com sucesso')
        return redirect(url_for('cliente'))
    
    conn = sqlite3.connect('barbearia.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM cliente')
    clientes = cursor.fetchall()
    conn.close()
    return render_template('cliente.html', clientes=clientes)

@app.route('/barbeiro', methods=['GET', 'POST'])
def barbeiro():
    if request.method == 'POST':
        nome = request.form['nome']
        especialidade = request.form['especialidade']
        if not nome or not especialidade:
            flash('Nome e especialidade são obrigatórios')
        else:
            conn = sqlite3.connect('barbearia.db')
            cursor = conn.cursor()
            cursor.execute('INSERT INTO barbeiro (nome, especialidade) VALUES (?, ?)', (nome, especialidade))
            conn.commit()
            conn.close()
            flash('Barbeiro adicionado com sucesso')
        return redirect(url_for('barbeiro'))
    
    conn = sqlite3.connect('barbearia.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM barbeiro')
    barbeiros = cursor.fetchall()
    conn.close()
    return render_template('barbeiro.html', barbeiros=barbeiros)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
