from flask import Flask, render_template, request, redirect, session, flash, url_for
# para dinamizar as routes usamos url_for
# para renderizar paginas html no flask
# use o render_template e por padrão na pasta templates o flask vai saber onde
# esta, basta passar o nome
# trecho da app, para definir a porta use esse codigo
# app.run(host='0.0.0.0', port=8080)
# < !-- para dinamizar o codigo use duplo colchetes {{}}-- >
#{% %} é usado para dinamizar uma estrutura de repetição
#chamamos adiretiva os simbulos que usamos para dinamizar 
#o metodo GET é para buscar alguma coisa no servidor
#Post é para passar alguma infomação para o servidor
#o flask so aceita get a menos que indiquemos que ele pode aceitar get linha 
# bootstrap é um mini framework que faz algumas estilizações minimas automaricamento
# ?proxima=novo é uma query string , que grava a ultima pagina antes do logout
class Jogo:
    def __init__(self, nome, categoria, console):
        self.nome = nome
        self.categoria = categoria
        self.console = console

jogo1 = Jogo('teris', 'logica', 'atari')
jogo2 = Jogo('goo', 'açao', 'ps2')
lista = [jogo1, jogo2]

app = Flask(__name__)
app.secret_key = 'admin'

@app.route('/')
def index():
    return render_template('lista.html', titulo='Jogos', jogos=lista) 

@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima= url_for('novo')))
    return render_template('novo.html', titulo='Novo',)

@app.route('/criar', methods=['POST',])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogo(nome, categoria, console)

    lista.append(jogo)
    return redirect(url_for('index'))
# altera o debug para true facilita as coisa, o debuger reinicia a aplicação
#a cada alteração salva
#<input type="hidden" name="proxima" valor="{{proxima}}"
# o valor que eu quero que pegue eu coloco dentro do {{}} para comunicar o html e o python
@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)

@app.route('/autenticar', methods=['POST'])
def autenticar():
    if 'alohomora' == request.form['senha']:
        session['usuario_logado'] = request.form['usuario']
        flash(session['usuario_logado'] + ' Logado com sucesso')
        proxima_pagina = request.form['proxima']
        return redirect(proxima_pagina)
    else:
        flash('senha ou usuario invalido')
        return redirect('autenticar.html')

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso')
    return redirect(url_for('index'))

app.run(debug=True)