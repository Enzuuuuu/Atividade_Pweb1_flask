from flask import Flask, render_template, request, redirect, url_for, session, flash

# Criar a aplicação Flask
app = Flask(__name__)

# Chave secreta para sessões (em produção, use uma chave mais segura)
app.secret_key = 'sua_chave_secreta_aqui'

# Configuração dos produtos (simulando um banco de dados)
app.config['PRODUTOS'] = {
    1: {
        'tipo': 'higiene',
        'id': 1, 
        'nome': 'Desodorante Rexona',
        'preco': 10.00, 
        'imagem_url': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTdtOKiF_oxD9HS9K4VIeb1V7Hjl1-PEGm1TQ&s'
    },
    2: {
        'tipo': 'nuclear',
        'id': 2, 
        'nome': 'Urânio enriquecido 1KG', 
        'preco': 2000000.00, 
        'imagem_url': 'https://c.files.bbci.co.uk/79CF/production/_107838113_gettyimages-844443408-1.jpg'
    },
    3: { 
        'tipo': 'nuclear',
        'id': 3, 
        'nome': 'Césio-137', 
        'preco': 5000000.00, 
        'imagem_url': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRJuPjeNIrysKx8XAvL70dms1Q1AL_kOe4tIA&s'
    },
    4: {
        'tipo': 'nuclear',
        'id': 4,
        'nome': 'Bomba de Hidrogênio',
        'preco': 10000000.00,
        'imagem_url': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQRdwnnn1Xnkwt-JutPrHOrSWVogEfsDDq2yQ&s'
    },
    5: {
        'tipo': 'nuclear',
        'id': 5,
        'nome': 'átomo de amendoim',
        'preco': 0.01,
        'imagem_url': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR3XrTuPC9wFVOOUMRlhD7ATcbmJ9VAVw5Suw&s'
    },
    6: {
        'tipo': 'nuclear',
        'id': 6,
        'nome': 'FranBaby',
        'preco': 999999999.99,
        'imagem_url': 'https://media-gru2-2.cdn.whatsapp.net/v/t61.24694-24/567323385_1156398146595020_1602469055019689819_n.jpg?ccb=11-4&oh=01_Q5Aa3QFDfm5ShTmUlL4xwqG3_E9PLokzRzJPONa9Y3qT1Qu1bg&oe=6946E8B0&_nc_sid=5e03e0&_nc_cat=106'
    }
}

# Rota principal - Lista de produtos
@app.route('/')
def index():
    produtos = app.config['PRODUTOS']
    return render_template('index.html', produtos=produtos)

# Rota para adicionar produto ao carrinho
@app.route('/adicionar/<int:produto_id>', methods=['POST'])
def adicionar_ao_carrinho(produto_id, qtd=1):
    produtos = app.config['PRODUTOS']
    
    # Recuperar carrinho da sessão (ou criar lista vazia)
    carrinho = session.get('carrinho', [])
    
    # Adicionar produto ao carrinho
    for _ in range(int(request.form.get('quantidade', 1))):
        carrinho.append(produtos[produto_id])
    
    # Salvar carrinho na sessão
    session['carrinho'] = carrinho
    
    # Mensagem de feedback
    flash('Produto adicionado ao carrinho!')
    
    return redirect(url_for('index'))

# Rota para visualizar o carrinho
@app.route('/carrinho')
def carrinho():
    carrinho = session.get('carrinho', [])
    
    # Calcular total
    total = sum(item['preco'] for item in carrinho)
    
    return render_template('carrinho.html', carrinho=carrinho, total=total)

# Rota para remover produto do carrinho
@app.route('/remover/<int:produto_id>', methods=['POST'])
def remover_do_carrinho(produto_id):
    carrinho = session.get('carrinho', [])
    
    # Procurar e remover produto
    for produto in carrinho:
        if produto['id'] == produto_id:
            carrinho.remove(produto)
            session['carrinho'] = carrinho
            flash('Produto removido do carrinho!')
            break
    else:
        flash('Produto não encontrado no carrinho.')
    
    return redirect(url_for('carrinho'))

@app.route('/remover_tudo', methods=['POST'])
def remover_tudo():
    carrinho = session.get('carrinho', [])
    
    carrinho.clear()   
    
    session['carrinho'] = carrinho 
    flash('Carrinho Limpo!')
    
    return redirect(url_for('carrinho'))

@app.route('/filtrar/<tipo>')
def filtrar(tipo):
    produtos = app.config['PRODUTOS']
    produtos_filtrados = {id: p for id, p in produtos.items() if p['tipo'] == tipo}
    return render_template('index.html', produtos=produtos_filtrados)

@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

# Executar aplicação
if __name__ == '__main__':
    app.run(debug=True)

