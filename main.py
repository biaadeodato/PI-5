import random

# Criação do tabuleiro Kamisado com cores
tabuleiro = [
    ["laranja", "azul", "roxo", "rosa", "amarelo", "vermelho", "verde", "marrom"],
    ["vermelho", "laranja", "rosa", "verde", "azul", "amarelo", "marrom", "roxo"],
    ["verde", "rosa", "laranja", "vermelho", "roxo", "marrom", "amarelo", "azul"],
    ["rosa", "roxo", "azul", "laranja", "marrom", "verde", "vermelho", "amarelo"],
    ["amarelo", "vermelho", "verde", "marrom", "laranja", "azul", "roxo", "rosa"],
    ["azul", "amarelo", "marrom", "roxo", "vermelho", "laranja", "rosa", "verde"],
    ["roxo", "marrom", "amarelo", "azul", "verde", "rosa", "laranja", "vermelho"],
    ["marrom", "verde", "vermelho", "amarelo", "rosa", "roxo", "azul", "laranja"]
]

# Exibição do tabuleiro com bordas e peças
def exibir_tabuleiro():
    print("    " + "     ".join([str(i + 1) for i in range(8)]))  # Cabeçalho das colunas
    print("  +" + "-----+" * 8)  # Linha superior
    for i, linha in enumerate(tabuleiro):
        linha_formatada = []
        for j in range(8):
            torre_exibida = False
            for jogador, torres in pecas.items():
                for torre in torres:
                    if torre["linha"] == i and torre["coluna"] == j:
                        linha_formatada.append("  X  " if jogador == "jogador1" else "  0  ")
                        torre_exibida = True
                        break
                if torre_exibida:
                    break
            if not torre_exibida:
                linha_formatada.append(f" {linha[j][:3]} ")
        print(f"{chr(97 + i)} |" + "|".join(linha_formatada) + "|")
        print("  +" + "-----+" * 8)

# Inicialização das peças (8 torres para cada jogador)
pecas = {
    "jogador1": [{"linha": 0, "coluna": i, "cor": tabuleiro[0][i]} for i in range(8)],  # Torres na linha "a"
    "computador": [{"linha": 7, "coluna": i, "cor": tabuleiro[7][i]} for i in range(8)]  # Torres na linha "h"
}

# Sorteio para definir quem começa o jogo
def sortear_inicio():
    return random.choice(["jogador1", "computador"])

# Regras de movimentação (quantas casas quiserem, sem obstáculos)
def movimentar_peca(jogador, torre, nova_linha, nova_coluna):
    linha_atual, coluna_atual = torre["linha"], torre["coluna"]

    # Verificar limites do tabuleiro
    if nova_linha < 0 or nova_linha > 7 or nova_coluna < 0 or nova_coluna > 7:
        print("Movimento inválido! Fora dos limites.")
        return False

    # Verificar se o caminho está livre
    delta_linha = nova_linha - linha_atual
    delta_coluna = nova_coluna - coluna_atual
    if delta_coluna != 0 and delta_linha != 0 and abs(delta_coluna) != abs(delta_linha):
        print("Movimento inválido! Deve ser reto ou diagonal.")
        return False
    for i in range(1, abs(delta_linha)):
        passo_linha = linha_atual + i * (1 if delta_linha > 0 else -1)
        passo_coluna = coluna_atual + i * (1 if delta_coluna > 0 else -1)
        for jogador, torres in pecas.items():
            for t in torres:
                if t["linha"] == passo_linha and t["coluna"] == passo_coluna:
                    print("Movimento inválido! Há uma torre no caminho.")
                    return False

    # Atualizar a posição da torre
    torre["linha"] = nova_linha
    torre["coluna"] = nova_coluna
    torre["cor"] = tabuleiro[nova_linha][nova_coluna]
    return True

# Lógica para o computador movimentar baseado na cor obrigatória
def jogada_computador(forcar_cor=None):
    print("\nTurno do computador!")
    if forcar_cor:
        print(f"Computador é obrigado a mover uma torre da cor {forcar_cor}.")
    for i, torre in enumerate(pecas["computador"]):
        if not forcar_cor or torre["cor"] == forcar_cor:
            for linha in range(8):
                for coluna in range(8):
                    if tabuleiro[linha][coluna] == torre["cor"] and linha < torre["linha"]:
                        if movimentar_peca("computador", torre, linha, coluna):
                            print(f"Computador moveu a torre para ({chr(97 + linha)}, {coluna + 1})!")
                            return
    print("O computador não conseguiu se mover!")

# Verificação de vitória
def verificar_vitoria(jogador):
    for torre in pecas[jogador]:
        if jogador == "jogador1" and torre["linha"] == 7:
            print("Parabéns! Você venceu ao alcançar o lado oposto!")
            return True
        elif jogador == "computador" and torre["linha"] == 0:
            print("O computador venceu ao alcançar o lado oposto!")
            return True
    return False

# Loop principal do jogo
def jogo_kamisado():
    exibir_tabuleiro()
    turno = sortear_inicio()
    print(f"\n{turno.capitalize()} começará o jogo!")
    cor_forcada = None  # Define a cor obrigatória após o primeiro movimento

    while True:
        print(f"\nTurno de {turno}")
        for i, torre in enumerate(pecas[turno]):
            print(f"Torre {i + 1}: posição ({chr(97 + torre['linha'])}, {torre['coluna'] + 1}), cor {torre['cor']}")
        if turno == "jogador1":
            if cor_forcada:
                print(f"Você é obrigado a mover uma torre da cor {cor_forcada}.")
            torre_index = int(input("Escolha a torre para mover (1-8): ")) - 1
            nova_linha = input("Digite a nova linha (a-h): ").lower()
            nova_coluna = int(input("Digite a nova coluna (1-8): ")) - 1
            nova_linha = ord(nova_linha) - 97
            if movimentar_peca(turno, pecas[turno][torre_index], nova_linha, nova_coluna):
                cor_forcada = pecas[turno][torre_index]["cor"]
                exibir_tabuleiro()
                if verificar_vitoria(turno):
                    break
                turno = "computador"
        else:
            jogada_computador(cor_forcada)
            cor_forcada = pecas["computador"][0]["cor"]  # Atualiza a cor obrigatória para o jogador
            exibir_tabuleiro()
            if verificar_vitoria(turno):
                break
            turno = "jogador1"

    print("Fim do jogo!")

# Início do jogo
jogo_kamisado()