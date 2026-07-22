import pytest
from project import create_character, drink_potion, chest, player_action, battle, change_stats
from classes import Character, Armor, Weapon, Potions, Choice

@pytest.fixture
def character():
    # Cria um Guerreiro (Força 6, Resistência 20)
    # Homem (Base +10 Proteção)
    # 25 Anos (Base +8 Proteção)
    # Proteção Base Esperada: 20 + 10 + 8 = 38
    return Character("Testcharacter", "Male", 25, "Warrior")

def inputs_tester(monkeypatch, list_inputs):
    
    inputs = iter(list_inputs)
    def mock_test(prompt):
        if "Press a button to continue" in prompt:
            return ""
        return next(inputs)
    monkeypatch.setattr('builtins.input', mock_test)

def test_protection(character):
    """
    Testa a fórmula complexa de proteção:
    Stats(20) + Gender_Male(10) + Age_25(8) = 38
    Ao equipar Couro (10), deve ir para 48.
    """
    assert character.protection == 38, "Erro na proteção base (Stats + Gênero + Idade)"

    # Equipar armadura de couro
    leather = Armor("Leather")
    character.inventory["Armor"] = leather
    # Força o recálculo (o setter protection faz isso no seu código ao equipar?)
    # Nota: No seu código, ao equipar, você chama self.protection = self.stats
    # Vamos simular o comportamento de take_item sem o input primeiro
    character.protection = character.stats

    assert character.protection == 48, "Erro ao somar armadura na proteção"

def test_healing_potion_logic(character):
    """
    Testa se beber poção cura e remove o item.
    """
    heal_potion = Potions("Healing")
    character.inventory["Potions"].append(heal_potion)
    character.hp = 1 # Vida quase vazia

    # Executa a ação
    drink_potion(character, heal_potion)

    # Verificações
    assert character.hp > 1, "A poção não curou nada"
    assert len(character.inventory["Potions"]) == 0, "A poção não sumiu do inventário"


# --- GRUPO 2: TESTES DE INPUT COM MONKEYPATCH (INTERATIVOS) ---
# Aqui usamos o 'dublê' para digitar pelo usuário.

def test_choice_resilience(monkeypatch):
    """
    TESTE CRÍTICO DO CHOICE:
    Simula um usuário "chato" que digita:
    1. "a" (Letra inválida) -> Deve capturar erro e perguntar de novo
    2. "5" (Número fora das opções) -> Deve ignorar e perguntar de novo
    3. "1" (Opção válida) -> Deve aceitar e retornar
    """
    # A fila de respostas que o "dublê" vai digitar
    respostas = iter(["a", "5", "1"])

    # Substitui o input real pelo nosso dublê
    monkeypatch.setattr('builtins.input', lambda _: next(respostas))

    # Chama a função. Se ela quebrar, o teste falha.
    resultado = Choice("Teste", "Opção Correta", "Opção 2")

    assert resultado == "Opção Correta"

def test_create_character_flow(monkeypatch):
    """
    Testa a criação inteira de um personagem.
    Inputs Simulados:
    1. Nome: "Arthur"
    2. Gênero: "1" (Male)
    3. Idade: "30"
    4. Classe: "3" (Warrior)
    5. Confirmar Classe: "1" (Sim)
    """
    inputs = iter(["David", "1", "30", "3", "1"])

    inputs_tester(monkeypatch, inputs)
    player = create_character()

    assert player.name == "David"
    assert player.classe.stats["strength"] == 6 # Warrior tem 6 de força
    assert player.inventory["Money"] == 0 # Começa pobre

def test_inventory_full_replace(monkeypatch, character):
    """
    Testa o limite de 5 poções.
    Cenário: Inventário cheio (5 poções). Tenta pegar a 6ª.
    Decisão: Sim (trocar) -> Escolhe a 1ª poção para sair.
    """
    # Encher inventário com 5 poções de Força
    for _ in range(5):
        character.inventory["Potions"].append(Potions("Strength"))

    nova_pocao = Potions("Healing")

    # Inputs: "1" (Sim, quero trocar), "1" (Trocar pela primeira da lista)
    inputs = iter(["1", "1"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    character.take_item(nova_pocao)

    # Verifica se tem uma Healing potion no inventário agora
    tipos_pocoes = [p._type for p in character.inventory["Potions"]]
    assert "Healing" in tipos_pocoes
    assert len(character.inventory["Potions"]) == 5 # Deve manter 5, não 6

def test_chest(monkeypatch, character):
    inputs = iter(["1", "1", "3"])
    inputs_tester(monkeypatch, inputs)
    chest(character)
    assert character.inventory['Money'] > 0
    assert character.inventory['Armor'] != None or character.inventory['Weapon'] != None or len(character.inventory['Potions']) > 0

    character.inventory = "reset"

    inputs2 = iter(["3", "1", "2", "1", "1", "1"])
    def mock_randint(a, b):
        if a == 1:
            match b:
                case 9:
                    return 1
                case 8:
                    return 5
                case 7:
                    return 7
        if a == 10 and b == 100:
            return 50
    monkeypatch.setattr("random.randint", mock_randint)
    inputs_tester(monkeypatch, inputs2)
    chest(character)
    assert character.inventory['Money'] == 50
    assert character.inventory['Armor'].type == "Leather" 
    assert character.inventory['Weapon'].type ==  "Sword"
    assert character.inventory['Potions'][0].type == "Resistance" 
    
def test_player_action(monkeypatch, character):
    opponent = Character("opp", "Male", 20, "Archer")
    change_stats(opponent, 0, 0, 0, 0, 0)
    initialhp = opponent.hp
    character.stats["aim"] = 100
    inputs = iter(["1", "1"])
    inputs_tester(monkeypatch, inputs)
    retorno = player_action(character, opponent)

    assert opponent.hp < initialhp
    assert retorno == "player attacked"

    def mock_randint(a,b):
        return 3
    monkeypatch.setattr("random.randint", mock_randint)
    inputs = iter(["3", "1"])
    inputs_tester(monkeypatch, inputs)
    resultado1 = player_action(character, opponent)
    
    def mock_randint(a,b):
        return 1
    monkeypatch.setattr("random.randint", mock_randint)
    inputs = iter(["3", "1"])
    inputs_tester(monkeypatch, inputs)
    resultado2 = player_action(character, opponent)
    
    assert resultado1 == True
    assert resultado2 == False


def test_battle(monkeypatch, character):
    opponent = Character("opp", "Male", 20, "Archer")
    change_stats(opponent, 0, 0, 0, 0, 0)
    opponent.hp = 1
    character.stats["aim"] = 100
    inputs = iter(["1", "1"])
    inputs_tester(monkeypatch, inputs)
    resultado = battle(character, opponent, xp=150)
    
    assert resultado == "Villain Died"
    assert character.inventory["XP"] == 150