from flask import Flask, request, render_template, redirect, url_for
import json
import os
import re

app = Flask(__name__)
ARQUIVO = 'usuarios.json'

def carregar_usuarios():
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, 'r') as f:
            return json.load(f)
    return []

def salvar_usuarios(usuarios):
    with open(ARQUIVO, 'w') as f:
        json.dump(usuarios, f, indent=4)

@app.route('/')
def index():
    usuarios = carregar_usuarios()
    return render_template('index.html', usuarios=usuarios)

@app.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        idade = request.form['idade']

        if not nome.replace(" ", "").isalpha():
            return "Nome inválido."

        if not re.match(r"\w+@\w+\.com", email):
            return "Email inválido."

        if not idade.isdigit():
            return "Idade inválida."

        usuarios = carregar_usuarios()
        usuarios.append({'Nome': nome, 'E-mail': email, 'Idade': idade})
        salvar_usuarios(usuarios)
        return redirect(url_for('index'))

    return render_template('cadastrar.html')

@app.route('/deletar/<int:indice>')
def deletar(indice):
    usuarios = carregar_usuarios()
    if 0 <= indice < len(usuarios):
        usuarios.pop(indice)
        salvar_usuarios(usuarios)
    return redirect(url_for('index'))

@app.route('/atualizar/<int:indice>', methods=['GET', 'POST'])
def atualizar(indice):
    usuarios = carregar_usuarios()
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        idade = request.form['idade']
        usuarios[indice] = {'Nome': nome, 'E-mail': email, 'Idade': idade}
        salvar_usuarios(usuarios)
        return redirect(url_for('index'))

    usuario = usuarios[indice]
    return render_template('atualizar.html', usuario=usuario, indice=indice)

if __name__ == '__main__':
    app.run(debug=True)