import textwrap
from abc import ABC, abstractmethod, abstractproperty
from datetime import datetime

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("\nOperação falhou! Você não tem saldo suficiente.")

        elif valor > 0:
            self._saldo -= valor
            print("\n=== Saque realizado com sucesso! ===")
            return True

        else:
            print("\nOperação falhou! O valor informado é inválido.")

        return False
    
def depositar(self, valor):
    if valor > 0:
        self._saldo += valor
        print("\n=== Depósito realizado com sucesso! ===")
    else:
        print("\nOperação falhou! O valor informado é inválido.")
    return False

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )

        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limite_saques

        if excedeu_limite:
            print("\nOperação falhou! O valor do saque excede o limite.")

        elif excedeu_saques:
            print("\nOperação falhou! Número máximo de saques excedido.")

        else:
            return super().sacar(valor)

        return False

    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                }
        )


class Transacao(ABC):

    @property
    @abstractproperty
    def valor(self):
        pass

    def registrar(self, conta):
        pass

class Saque(Transacao):

    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

def menu():
    menu = """ ===== Bem-Vindo ao Banco Python =====

    Pressione
    [1]\tSacar
    [2]\tDepósito
    [3]\tExtrato
    [4]\tCriar Usuário
    [5]\tCriar Conta-Corrente
    [6]\tDados Conta
    [0]\tSair
    =>"""
    return input(textwrap.dedent(menu))

def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo+= valor
        extrato += f"Depósito:\tR$ {valor:.2f}\n"
        print("\n=== Depósito realizado com sucesso! ===")
    else:
        print("\nOperação negada, valor informado não é válido!")

    return saldo, extrato
    
def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques
    if excedeu_saldo:
        print("Você não possui esse valor, tente novamente!")
    elif excedeu_limite:
        print("O valor está acima do seu limite, tente novamente com outro valor!")
    elif excedeu_saques:
        print("Operação falhou, numero de saques atingiu limite!")
    elif valor > 0:
        saldo -= valor
        extrato += f"Saque de R${valor: .2f}"
        numero_saques += 1
    else:
        print("\nO valor informado é inválido, tente novamente")
    return saldo, extrato

def exibir_extrato(saldo, /, *, extrato):
    print(""" ======EXTRATO====== """)
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"Seu saldo é: R$ {saldo: .2f}")
    print(""" =================== """)

def criar_usuario(usuarios):
    cpf = input("Informe seu CPF(somente números):")
    usuario = log_usuario(cpf, usuarios)
    if usuario:
        print("\nJá existe usuário com esse CPF!")
        return
    nome = input("Informe o seu nome completo: ")
    data_nascimento = input("Informe sua data de nascimento(dd-mm-aaaa): ")
    endereço = input("Informe seu endereço(logradouro, nro - bairro - cidade/sigla estado): ")
    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereço": endereço})
    print("Usuário criado com sucesso!")

def log_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário: ")

    if usuarios:
        print("Conta criada com sucesso!")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuarios}
    print("\n Usuário não encontrado, criação de conta cancelada, voltando ao MENU!")

def contas_cadastradas(contas):
    for conta in contas:
        linha = f"""
        Agência:{conta["agencia"]}\n
        Conta: {conta["numero da conta"]}\n
        Titular da Conta: {conta["usuario"]["nome"]}\n
"""
        print("=" * 100)
        print(textwrap.dedent(linha))


def main():

    clientes = []
    conta = []


    while True:
        opcao = menu()

        if opcao =="1":
            sacar(clientes)
        elif  opcao =="2":
            depositar(clientes)

        elif opcao =="3":
            exibir_extrato(clientes)

        elif opcao == "4":
            criar_usuario(clientes)

        elif opcao == "5":
            numero_conta = len(conta) + 1
            criar_conta(numero_conta, clientes, conta)

        elif opcao == "6":
            contas_cadastradas(conta)
        
        elif opcao == "0":
            break
        else:
            print("Opção inválida! Tente novamente com uma opção válida!")

main()
