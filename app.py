from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Produto

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///estoque.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'sua_chave_secreta'  # Necessário para usar flash messages
db.init_app(app)

# Rota para a página inicial
@app.route('/')
def home():
    categorias = db.session.query(Produto.categoria).distinct().all()
    return render_template('index.html', categorias=categorias)

# Rota para registrar a entrada de produtos
@app.route('/entrada', methods=['GET', 'POST'])
def entrada_produto():
    if request.method == 'POST':
        try:
            nome = request.form['nome']
            categoria = request.form['categoria']
            valor_compra = float(request.form['valor_compra'])
            valor_venda = float(request.form['valor_venda'])
            lote = request.form['lote']
            quantidade = int(request.form['quantidade'])
        except KeyError as e:
            return f"Campo ausente no formulário: {e}", 400
        except ValueError as e:
            return f"Erro de conversão de valor: {e}", 400

        # Adiciona o novo produto com um ID único
        produto = Produto(nome=nome, categoria=categoria, valor_compra=valor_compra, valor_venda=valor_venda, lote=lote, quantidade=quantidade)
        db.session.add(produto)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('entrada.html')


# Rota para registrar a saída de produtos
@app.route('/saida', methods=['GET', 'POST'])
def saida_produto():
    if request.method == 'POST':
        try:
            nome = request.form['nome']
            lote = request.form['lote']
            quantidade = int(request.form['quantidade'])
        except KeyError as e:
            return f"Campo ausente no formulário: {e}", 400
        except ValueError as e:
            return f"Erro de conversão de valor: {e}", 400

        produto = Produto.query.filter_by(nome=nome, lote=lote).first()
        if produto:
            produto.quantidade -= quantidade
            if produto.quantidade <= 0:
                db.session.delete(produto)
                db.session.commit()
                flash(f"Produto {produto.nome} do lote {produto.lote} removido do estoque!", 'warning')
            elif produto.quantidade <= 5:
                db.session.commit()
                flash(f"O produto {produto.nome} do lote {produto.lote} está acabando no estoque!", 'warning')
            else:
                db.session.commit()
                flash(f"Produto {produto.nome} do lote {produto.lote} atualizado na saída!", 'success')
        else:
            flash("Produto não encontrado!", 'error')

        return redirect(url_for('home'))
    return render_template('saida.html')

# Rota para visualizar o estoque
@app.route('/estoque')
def estoque():
    produtos = Produto.query.all()
    return render_template('estoque.html', produtos=produtos)

# Rota para visualizar produtos por categoria
@app.route('/produtos_por_categoria/<categoria>')
def produtos_por_categoria(categoria):
    produtos = Produto.query.filter_by(categoria=categoria).all()
    return render_template('produtos_por_categoria.html', produtos=produtos)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Cria as tabelas no banco de dados
    app.run(debug=True)
