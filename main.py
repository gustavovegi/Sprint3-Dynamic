import heapq

# Dicionário para armazenar informações de disponibilidade de luvas (em horários)
disponibilidade_luvas = {
    '08:00': 1,  # Uma luva disponível
    '09:00': 0,  # Nenhuma luva disponível
    '10:00': 2,  # Duas luvas disponíveis
    '11:00': 1,  # Uma luva disponível
    '12:00': 0  # Nenhuma luva disponível
}

# Dicionários para armazenar informações
alunos = {}
agendamentos = {}
treinamento_niveis = ['1', '2', '3']


# Função para cadastrar alunos
def cadastrar_aluno(nome):
    if nome not in alunos:
        alunos[nome] = {
            "notas": [],
            "avaliacoes": [],
            "progresso": {"nível": 0, "pontos_acertados": 0, "pontos_errados": 0, "passos_totais": []}
        }
        print(f"Aluno(a) {nome} cadastrado com sucesso!")
    else:
        print(f"Aluno(a) {nome} já está cadastrado(a).")


# Função para agendar treinamentos
def agendar_treinamento(nome, data, horario, nivel):
    if nome not in alunos:
        print(f"Aluno(a) {nome} não encontrado(a).")
        return
    if nivel not in treinamento_niveis:
        print(f"Nível {nivel} inválido. Os níveis disponíveis são: {treinamento_niveis}")
        return
    agendamento = f"{data} às {horario} - Nível: {nivel}"
    if nome in agendamentos:
        agendamentos[nome].append(agendamento)
    else:
        agendamentos[nome] = [agendamento]
    print(f"Treinamento agendado para {nome} em {agendamento}.")


# Função para agendar a luva utilizando o algoritmo de Dijkstra
def agendar_luva(nome, data, grafo_disponibilidade, horario_inicial):
    if nome not in alunos:
        print(f"Aluno(a) {nome} não encontrado(a).")
        return

    # Implementação do algoritmo de Dijkstra para encontrar o horário com melhor disponibilidade
    fila = [(0, horario_inicial)]  # (distância ou custo, nó/horário)
    distancias = {horario: float('inf') for horario in grafo_disponibilidade}
    distancias[horario_inicial] = 0
    caminhos = {horario: [] for horario in grafo_disponibilidade}

    while fila:
        dist_atual, horario_atual = heapq.heappop(fila)
        if dist_atual > distancias[horario_atual]:
            continue

        for vizinho, peso in grafo_disponibilidade[horario_atual].items():
            distancia = dist_atual + peso
            if distancia < distancias[vizinho]:
                distancias[vizinho] = distancia
                heapq.heappush(fila, (distancia, vizinho))
                caminhos[vizinho] = caminhos[horario_atual] + [vizinho]

    # Encontrando o horário mais adequado para agendar a luva
    horario_ideal = min(distancias, key=lambda h: (distancias[h], disponibilidade_luvas.get(h, 0)))

    if disponibilidade_luvas[horario_ideal] > 0:
        disponibilidade_luvas[horario_ideal] -= 1  # Reservar a luva
        agendamento = f"{data} às {horario_ideal} - Luva reservada"
        if nome in agendamentos:
            agendamentos[nome].append(agendamento)
        else:
            agendamentos[nome] = [agendamento]
        print(f"Luva agendada para {nome} em {agendamento}.")
    else:
        print(f"Nenhuma luva disponível no horário {horario_ideal}.")


# Exemplo de uso do agendamento de luva
grafo_disponibilidade = {
    '08:00': {'09:00': 1, '10:00': 2},
    '09:00': {'10:00': 1, '11:00': 2},
    '10:00': {'11:00': 1, '12:00': 2},
    '11:00': {'12:00': 1},
    '12:00': {}
}

# Cadastrando alunos
cadastrar_aluno("Roberto Elias")

# Agendando uma luva para um treinamento de laparoscopia
agendar_luva("Roberto Elias", "02/05/2025", grafo_disponibilidade, '10:00')

# Exibindo informações de agendamentos e disponibilidade de luvas
print("\nAgendamentos após reserva de luvas:")
for aluno, agendas in agendamentos.items():
    print(f"{aluno}: {agendas}")

print("\nDisponibilidade de luvas após agendamento:")
print(disponibilidade_luvas)
