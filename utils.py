import redis


def gera_id():
    try:
        connection = conectar()
        chave = connection.get('chave')

        if chave:
            chave = connection.incr('chave')
            return chave
        else:
            connection.set('chave', 1)
            return 1
    except redis.exceptions.ConnectionError as e:
        print(f'Não foi possível gerar a chave: {e}')


def conectar():
    """
    Função para conectar ao servidor
    """
    connection = redis.Redis(host='localhost', port=6379)
    return connection


def desconectar(connection):
    """ 
    Função para desconectar do servidor.
    """
    connection.connection_pool.disconnect()


def listar():
    """
    Função para listar os produtos
    """
    connection = conectar()

    try:
        dados = connection.keys(pattern='produtos:*')
        if len(dados) > 0:
            print('Listando produtos...')
            print('--------------------')
            for chave in dados:
                #traz todos os dados de produto de acordo com a chave
                produto = connection.hgetall(chave)
                print(f"ID: {str(chave, 'utf-8', 'ingore')}")
                print(f"Produto: {str(produto[b'nome'], 'utf-8', 'ingore')}")
                print(f"Preço: {str(produto[b'preco'], 'utf-8', 'ingore')}")
                print(f"Estoque: {str(produto[b'estoque'], 'utf-8', 'ingore')}")
                print('-----------------------------')
        else:
            print('Não existem produtos cadastrados')
    except redis.exceptions.ConnectionError as e:
        print(f'Não foi possível listar os produtos. {e}')
    desconectar(connection)

def inserir():
    """
    Função para inserir um produto
    """  
    connection = conectar()

    nome = input('Informe o nome do produto: ')
    preco = float(input('Informe o preço: '))
    estoque = int(input('Informe o estoque: '))

    produto = {"nome": nome, "preco": preco, "estoque": estoque}
    chave = f'produtos:{gera_id()}'

    try:
        res = connection.hmset(chave, produto)
        if res:
            print(f'O produto {nome} foi inserido com sucesso!')
        else:
            print(f'Não foi possível inserir o produto')
    except redis.exceptions.ConnectionError as e:
        print(f'Não foi possível inserir o produto: {e}')


def atualizar():
    """
    Função para atualizar um produto
    """
    connection = conectar()

    chave = input('Informe a chave do produto: ')
    if not connection.exists(chave):
        print('Essa chave não existe')
    else:
        nome = input('Informe o nome do produto: ')
        preco = float(input('Informe o preço: '))
        estoque = int(input('Informe o estoque: '))

        produto = {"nome": nome, "preco": preco, "estoque": estoque}

        try:
            res = connection.hmset(chave, produto)
            if res:
                print(f'O produto {nome} foi atualizado com sucesso!')
        except redis.exceptions.ConnectionError as e:
            print(f'Não foi possível atualizar o produto: {e}')
        desconectar(connection)
    desconectar(connection)


def deletar():
    """
    Função para deletar um produto
    """  
    connection = conectar()

    chave = input('Informe a chave do produto: ')

    try:
        res = connection.delete(chave)
        if res == 1:
            print('O produto foi deletado com sucesso')
        else:
            print('Não existe produto com a chave informada.')
    except:
        print('Não existe produto com a chave informada')
    desconectar(connection)

def menu():
    """
    Função para gerar o menu inicial
    """
    print('=========Gerenciamento de Produtos==============')
    print('Selecione uma opção: ')
    print('1 - Listar produtos.')
    print('2 - Inserir produtos.')
    print('3 - Atualizar produto.')
    print('4 - Deletar produto.')
    opcao = int(input())
    if opcao in [1, 2, 3, 4]:
        if opcao == 1:
            listar()
        elif opcao == 2:
            inserir()
        elif opcao == 3:
            atualizar()
        elif opcao == 4:
            deletar()
        else:
            print('Opção inválida')
    else:
        print('Opção inválida')
