# RPG de texto no terminal
# Meu primeiro projeto em Python, feito aos poucos para aprender na prática.

import json
import os
import random

ARQUIVO_SAVE = "save.json"

# ---------- HERÓI ----------
# Valores do começo do jogo. Eles vão mudando durante a aventura.
nome = ""
vida = 100
vida_max = 100
dano = 10
xp = 0
nivel = 1
inventario = ["pocao", "pocao"]
etapa = 0  # posição do próximo monstro que o herói vai enfrentar


# ---------- MONSTROS ----------
def criar_monstros():
    # Crio a lista nova a cada jogo, assim os monstros sempre começam com a vida cheia
    return [
        {"nome": "Goblin", "vida": 30, "dano": 5},
        {"nome": "Orc", "vida": 40, "dano": 8},
        {"nome": "Dragão", "vida": 60, "dano": 12},
    ]


# ---------- FUNÇÕES DO HERÓI ----------
def mostrar_status(monstro):
    print(f"\n{nome}: {vida} HP | {monstro['nome']}: {monstro['vida']} HP")


def usar_pocao():
    # Devolve True se usou a poção e False se não tinha nenhuma
    global vida
    if "pocao" in inventario:
        inventario.remove("pocao")
        vida = min(vida + 30, vida_max)  # a vida nunca passa do máximo
        print(f"Você usou uma poção! Vida: {vida}")
        return True
    print("Você não tem poções!")
    return False


def ganhar_xp(quantidade):
    global xp, nivel, dano, vida_max, vida
    xp += quantidade
    print(f"{nome} ganhou {quantidade} de XP! (total: {xp})")

    # Quanto maior o nível, mais XP precisa para subir
    if xp >= nivel * 20:
        xp = 0
        nivel += 1
        dano += 4
        vida_max += 20
        vida = vida_max  # subir de nível recupera toda a vida
        print(f"{nome} subiu para o nível {nivel}!")


# ---------- SALVAR E CARREGAR ----------
def salvar_jogo():
    dados = {
        "nome": nome,
        "vida": vida,
        "vida_max": vida_max,
        "dano": dano,
        "xp": xp,
        "nivel": nivel,
        "inventario": inventario,
        "etapa": etapa,
    }
    with open(ARQUIVO_SAVE, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False)
    print("Jogo salvo com sucesso!")


def carregar_jogo():
    # Devolve True se carregou o save e False se não deu certo
    global nome, vida, vida_max, dano, xp, nivel, inventario, etapa

    if not os.path.exists(ARQUIVO_SAVE):
        return False

    try:
        with open(ARQUIVO_SAVE, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
        nome = dados["nome"]
        vida = dados["vida"]
        vida_max = dados["vida_max"]
        dano = dados["dano"]
        xp = dados["xp"]
        nivel = dados["nivel"]
        inventario = dados["inventario"]
        etapa = dados["etapa"]
    except (json.JSONDecodeError, KeyError):
        # save estragado ou de uma versão antiga do jogo
        print("O arquivo de save está com problema.")
        return False

    print(f"Jogo carregado! Bem-vindo de volta, {nome}!")
    return True


# ---------- BATALHA ----------
def batalha(monstro):
    # Devolve "vitoria", "fugiu" ou "derrota"
    global vida
    print(f"\nUm {monstro['nome']} apareceu!")

    while vida > 0 and monstro["vida"] > 0:
        mostrar_status(monstro)
        print(f"Poções: {inventario.count('pocao')}")
        escolha = input("1) Atacar  2) Usar poção  3) Fugir: ")

        if escolha == "1":
            golpe = random.randint(dano, dano + 8)  # o dano varia a cada golpe
            monstro["vida"] -= golpe
            print(f"Você atacou o {monstro['nome']} e causou {golpe} de dano!")

        elif escolha == "2":
            if not usar_pocao():
                continue  # sem poção não perde a vez, escolhe de novo

        elif escolha == "3":
            if random.randint(1, 100) <= 40:  # 40% de chance de fugir
                print(f"\n{nome} fugiu da batalha!")
                return "fugiu"
            print("\nVocê não conseguiu fugir!")

        else:
            print("Opção inválida, tente de novo.")
            continue

        # Se o monstro ainda está vivo, ele ataca de volta
        if monstro["vida"] > 0:
            vida -= monstro["dano"]
            print(f"{nome} tomou {monstro['dano']} de dano do {monstro['nome']}!")

    if vida > 0:
        print(f"\nVocê derrotou o {monstro['nome']}!")
        ganhar_xp(random.randint(10, 20))
        return "vitoria"

    print("\nVocê foi derrotado...")
    return "derrota"


# ---------- JOGO ----------
def novo_jogo_status():
    global vida, vida_max, dano, xp, nivel, inventario, etapa
    vida = 100
    vida_max = 100
    dano = 10
    xp = 0
    nivel = 1
    inventario = ["pocao", "pocao"]
    etapa = 0


def jogar():
    global etapa
    monstros = criar_monstros()
    print(f"\nBem-vindo ao mundo, {nome}!")

    # Começa do monstro em que o herói parou (no jogo novo, o primeiro)
    for i in range(etapa, len(monstros)):
        resultado = batalha(monstros[i])

        if resultado == "fugiu":
            print("Você escapou, mas a aventura acabou por aqui.")
            return
        if resultado == "derrota":
            print("Fim de jogo!")
            return

        etapa = i + 1  # guarda qual vai ser o próximo monstro
        salvar_jogo()

    print("\nVocê venceu todas as batalhas! Parabéns!")
    if os.path.exists(ARQUIVO_SAVE):
        os.remove(ARQUIVO_SAVE)  # aventura terminada, não precisa mais do save


def menu_inicial():
    global nome

    while True:
        print("\n=== RPG DE TEXTO ===")
        print("1) Novo Jogo")
        print("2) Continuar")
        print("3) Sair")
        opcao = input("Escolha: ")

        if opcao == "1":
            nome = input("Qual o nome do seu herói? ")
            novo_jogo_status()
            jogar()
        elif opcao == "2":
            if carregar_jogo():
                jogar()
            else:
                print("Nenhum jogo salvo para continuar. Escolha 1 para começar um novo.")
        elif opcao == "3":
            print("Até a próxima!")
            break
        else:
            print("Opção inválida, tente de novo.")


menu_inicial()
