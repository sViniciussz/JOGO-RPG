from random import randint, choice
from os import system, name
from time import sleep

vidas_iniciais = 5
pontuacao_inicial = 0
tamanho_mapa_inicial = 4
inventario_inicial = []


class Classe:
    def inicio(self, tipo):
        self.vida = vidas_iniciais
        self.pontos = pontuacao_inicial
        self.inventario = inventario_inicial[:]
        self.posicao = [0, 0]
        tipo = tipo.lower()

        if tipo == "mago":
            self.forca = 3
            self.inteligencia = 8
            self.agilidade = 4
        elif tipo == "guerreiro":
            self.forca = 8
            self.inteligencia = 3
            self.agilidade = 4
        elif tipo == "samurai":
            self.forca = 4
            self.inteligencia = 5
            self.agilidade = 6
        else:
            raise ValueError("ESSA CLASSE NÃO EXISTE, TENTE UMA DISPONÍVEL!")

    def status(self):
        print(f"VIDA: {self.vida}")
        print(f"PONTOS: {self.pontos}")
        print(f"FORÇA: {self.forca}")
        print(f"INTELIGÊNCIA: {self.inteligencia}")
        print(f"AGILIDADE: {self.agilidade}")

    def mostrar_inventario(self):
        print(f"INVENTÁRIO: {self.inventario}")


def criar_mapa(tamanho):
    mapa = [[0] * tamanho for _ in range(tamanho)]
    jogador_posicao = [0, 0]
    mapa[jogador_posicao[0]][jogador_posicao[1]] = "P"

    while True:
        saida_x = randint(0, tamanho - 1)
        saida_y = randint(0, tamanho - 1)
        if (saida_x, saida_y) != tuple(jogador_posicao):
            break
    mapa[saida_x][saida_y] = 10

    i = 0
    while i < tamanho:
        j = 0
        while j < tamanho:
            if mapa[i][j] != "P" and mapa[i][j] != 10:
                mapa[i][j] = randint(0, 9)
            j += 1
        i += 1

    return mapa


def mostrar_mapa(mapa):
    for linha in mapa:
        print(" ".join(str(celula) for celula in linha))


def mover_jogador(jogador, direcao, mapa):
    x, y = jogador.posicao
    novo_x, novo_y = x, y

    if direcao == "norte":
        print("VOCÊ FOI PARA O NORTE!")
        novo_x -= 1
    elif direcao == "sul":
        print("VOCÊ FOI PARA O SUL!")
        novo_x += 1
    elif direcao == "leste":
        print("VOCÊ FOI PARA O LESTE!")
        novo_y += 1
    elif direcao == "oeste":
        print("VOCÊ FOI PARA O OESTE!")
        novo_y -= 1
    else:
        print("DIREÇÃO INVÁLIDA, TENTE NOVAMENTE!")
        return None

    if 0 <= novo_x < len(mapa) and 0 <= novo_y < len(mapa[0]):
        if mapa[novo_x][novo_y] == 4:
            print("VOCÊ DEU DE CARA COM A BEDROCK, TENTE OUTRO CAMINHO!")
        elif mapa[novo_x][novo_y] == 5:
            print("VOCÊ ENCONTROU UMA PAREDE, TENTE OUTRO CAMINHO!")
        elif mapa[novo_x][novo_y] == 6:
            print("VOCÊ ENCONTROU UM BAÚ COM TESOURO!")
            abrir(jogador)
            jogador.posicao = [novo_x, novo_y]
            mapa[x][y] = 0
            mapa[novo_x][novo_y] = "P"
        elif mapa[novo_x][novo_y] == 7:
            print("VOCÊ CAIU EM UMA ARMADILHA!")
            dano = randint(1, 3)
            jogador.vida -= dano
            print(f"VOCÊ PERDEU {dano} PONTOS DE VIDA!")
            jogador.posicao = [novo_x, novo_y]
            mapa[x][y] = 0
            mapa[novo_x][novo_y] = "P"
        elif mapa[novo_x][novo_y] == 8:
            tipo_inimigo = choice(["Enderman", "Phantom", "Warden"])
            print(f"VOCÊ ENCONTROU UM {tipo_inimigo}!")
            lutar(jogador, tipo_inimigo)
            jogador.posicao = [novo_x, novo_y]
            mapa[x][y] = 0
            mapa[novo_x][novo_y] = "P"
        elif mapa[novo_x][novo_y] == 9:
            print("VOCÊ ENCONTROU UM DESAFIO!")
            desafio(jogador)
            jogador.posicao = [novo_x, novo_y]
            mapa[x][y] = 0
            mapa[novo_x][novo_y] = "P"
        elif mapa[novo_x][novo_y] == 10:
            print("VOCÊ ENCONTROU A SAÍDA, GERANDO NOVO MAPA...")
            sleep(3)
            input("PRESSIONE ENTER PARA O NOVO MAPA!")
            return "saida"
        else:
            jogador.posicao = [novo_x, novo_y]
            mapa[x][y] = 0
            mapa[novo_x][novo_y] = "P"
    else:
        print("VOCÊ SAIU FORA DO MAPA, TENTE NOVAMENTE!")

    return None


def atacar(jogador):
    dano = randint(1, jogador.forca)
    print(f"VOCÊ ATACOU E CAUSOU {dano} PONTOS DE DANO!")
    jogador.pontos += dano


def fugir(jogador):
    sucesso = choice([True, False])
    if sucesso:
        print("VOCÊ CONSEGUIU FUGIR!")
        return "fugiu"
    else:
        dano = randint(1, 3)
        jogador.vida -= dano
        print(f"VOCÊ NÃO CONSEGUIU FUGIR E PERDEU {dano} PONTOS DE VIDA!")
        return "falhou"


def abrir(jogador):
    item = choice(["Poção de Vida", "Espada", "Escudo", "Nada"])
    if item == "Nada":
        print("VOCÊ NÃO ENCONTROU NADA!")
    else:
        print(f"VOCÊ ENCONTROU UM(A) {item}!")
        jogador.inventario.append(item)


def usar_item(jogador):
    if not jogador.inventario:
        print("SEU INVENTÁRIO ESTÁ VAZIO!")
        return

    print("ITENS DISPONÍVEIS NO INVENTÁRIO:")
    for i, item in enumerate(jogador.inventario):
        print(f"{i + 1}. {item}")

    escolha = int(input("ESCOLHA UM ITEM PARA USAR: ")) - 1
    if 0 <= escolha < len(jogador.inventario):
        item = jogador.inventario.pop(escolha)
        if item == "Poção de Vida":
            jogador.vida = min(jogador.vida + 2, vidas_iniciais)
            print("VOCÊ USOU UMA POÇÃO DE VIDA E RECUPEROU 2 PONTOS DE VIDA!")
        elif item == "Espada":
            jogador.forca += 2
            print("VOCÊ USOU UMA ESPADA E AUMENTOU SUA FORÇA EM 2 PONTOS!")
        elif item == "Escudo":
            jogador.vida = min(jogador.vida + 1, vidas_iniciais)
            print("VOCÊ USOU UM ESCUDO E RECUPEROU 1 PONTO DE VIDA!")
    else:
        print("ESCOLHA INVÁLIDA!")


def descansar(jogador):
    sucesso = choice([True, False])
    if sucesso:
        print("VOCÊ ESTÁ DESCANSANDO...")
        sleep(2)
        jogador.vida = min(jogador.vida + 1, vidas_iniciais)
        print("VOCÊ RECUPEROU 1 PONTO DE VIDA!")
    else:
        print("VOCÊ NÃO CONSEGUIU DESCANSAR. ALGO INTERROMPEU SEU DESCANSO!")


def lutar(jogador, tipo_inimigo):
    if tipo_inimigo == "Enderman":
        inimigo_forca = randint(1, 3)
    elif tipo_inimigo == "Phantom":
        inimigo_forca = randint(4, 6)
    elif tipo_inimigo == "Warden":
        inimigo_forca = randint(7, 10)

    if jogador.forca > inimigo_forca:
        print(f"VOCÊ DERROTOU O {tipo_inimigo}!")
        jogador.pontos += 10
    else:
        dano = inimigo_forca - jogador.forca
        jogador.vida -= dano
        print(f"O {tipo_inimigo} CAUSOU {dano} PONTOS DE DANO A VOCÊ!")


def desafio(jogador):
    print("VOCÊ ENCONTROU UM DESAFIO!")
    acerto = choice([True, False])
    if acerto:
        print("VOCÊ SUPEROU O DESAFIO E GANHOU PONTOS!")
        jogador.pontos += 5
    else:
        print("VOCÊ FALHOU NO DESAFIO E PERDEU PONTOS!")
        jogador.pontos = max(jogador.pontos - 3, 0)


def main():
    print("Bem-vindo ao jogo")
    print("ESCOLHA SUA CLASSE | Guerreiro, Mago, Samurai |")
    tipo = input(": ").lower()
    jogador = Classe()
    jogador.inicio(tipo)
    tamanho_mapa = tamanho_mapa_inicial
    mapa = criar_mapa(tamanho_mapa)

    while jogador.vida > 0:
        system("cls")
        print("-="*5, "STATUS", "-="*5)
        jogador.status()
        print("\nMAPA:")
        mostrar_mapa(mapa)
        print()
        print("AÇÕES DISPONÍVEIS | Mover, Atacar, Fugir, Abrir, Descansar, Mostrar inventário, Usar item |")
        acao = input("ESCOLHA UMA AÇÃO: ").lower()

        if acao == "mover":
            print("ESCOLHA UMA DIREÇÃO PARA ONDE IR | Norte, Sul, Leste, Oeste | : ")
            direcao = input(": ").lower()
            resultado = mover_jogador(jogador, direcao, mapa)
            if resultado == "saida":
                tamanho_mapa += 1
                jogador.posicao = [0, 0]
                mapa = criar_mapa(tamanho_mapa)
        elif acao == "atacar":
            atacar(jogador)
        elif acao == "fugir":
            resultado = fugir(jogador)
            if resultado == "fugiu":
                tamanho_mapa += 1
                jogador.posicao = [0, 0]
                mapa = criar_mapa(tamanho_mapa)
        elif acao == "abrir":
            abrir(jogador)
        elif acao == "descansar":
            descansar(jogador)
        elif acao == "mostrar inventário" or acao == "mostrar inventario":
            system("cls")
            jogador.mostrar_inventario()
            input("PRESSIONE ENTER PARA CONTINUAR...")
            system("cls")
        elif acao == "usar item":
            usar_item(jogador)
        else:
            print("AÇÃO INVÁLIDA, TENTE NOVAMENTE!")
            sleep(1)
        sleep(2)
    system("cls")
    print("GAME OVER!")


main()