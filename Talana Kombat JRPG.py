# The task is to take a JSON file with "punches" and "movements" from two different players
# and given some rules for special strikes, hitpoints per punch and a set of conditions, determine
# who will strike first (it's one move + attack per player per turn), narrate the fight, and
# determine who won and how much energy points the winner would have left.
#
# Movements are: W = up, A = left, S = down, D = right
# Player 1 always faces to the right & Player always faces to the left
# All punches are effective (no need to consider distance)
# Each player starts with 6 energy points
# Each strike / special strike consist of a buttpm or combination of buttons (movement + punch) as follows:
#
# Player 1
# Punch Name    Points    Button / Combination
# Taladoken       3           DSD + P
# Remuyuken       2           SD + K
# Punch           1             P
# Kick            1             K
#
# Player 2
# Remuyuken       3           SA + K
# Taladoken       2           ASA + P
# Punch           1             P
# Kick            1             K


import pandas as pd
import time
import random


def fight(data):
    sinonimos = ['abate a su rival con', 'sacude a su contrincante con', 'golpea con', 'conecta',\
                 'castiga a través de', 'avanza y da', 'combina a su oponente con', 'impacta', 'asesta']
    nada = ['no hace nada', 'parece que se ha quedado dormido', 'permanece inmóvil', 'apenas respira']
    movimientos = ['W', 'A', 'S', 'D']
    golpes = [['DSDP', 'SDK', 'P', 'K'],
              ['SAK', 'ASAP', 'P', 'K']]
    nombres_golpes = [['Taladoken', 'Remuyuken', 'puño', 'patada'],
                      ['Remuyuken', 'Taladoken', 'puño', 'patada']]
    comb = [3, 2]
    players = ['Tonyn', 'Arnaldor']
    max_energy = 6
    hp_players = [max_energy, max_energy]
    flag = True
    df = [pd.DataFrame(data['player1']), pd.DataFrame(data['player2'])]
    turnos = max(len(df[0]), len(df[1]))

    if first_punch(data) == 2:
        golpes.reverse()
        nombres_golpes.reverse()
        comb.reverse()
        players.reverse()
        df.reverse()

    for i in range(turnos):
        for j in range(2):

            # I inserted a small pause to give some suspense to the fight
            time.sleep(1)

            try:
                if df[j].movimientos[i][-comb[j]:] + df[j].golpes[i] == golpes[j][0]:
                    print("{} {} un {}".format(players[j], random.choice(sinonimos), nombres_golpes[j][0]))
                    hp_players[1-j] -= 3
                elif df[j].movimientos[i][-comb[1-j]:] + df[j].golpes[i] == golpes[j][1]:
                    print("{} {} un {}".format(players[j], random.choice(sinonimos), nombres_golpes[j][1]))
                    hp_players[1-j] -= 2
                elif df[j].golpes[i] == golpes[j][2]: # Puño (1 punto)
                    print("{} {} un {}".format(players[j], random.choice(sinonimos), nombres_golpes[j][2]))
                    hp_players[1-j] -= 1
                elif df[j].golpes[i] == golpes[j][3]:
                    print("{} {} una {}".format(players[j], random.choice(sinonimos), nombres_golpes[j][3]))
                    hp_players[1-j] -= 1
                elif any(x in df[j].movimientos[i] for x in movimientos):
                    print("{} se mueve".format(players[j]))
                else:
                    print("{} {}".format(players[j], random.choice(nada)))

                if hp_players[1-j] <= 0:
                    if hp_players[j] == 1:
                        print("\033[1mEl ganador es {} y le queda 1 punto de energía\033[0m\n".format(players[j]))
                    elif hp_players[j] == max_energy:
                        print("\033[1m¡Y es una VICTORIA PERFECTA para {}!\033[0m\n".format(players[j]))
                    else:
                        print("\033[1mEl ganador es {} y le quedan {} puntos de energía\033[0m\n".format(players[j], hp_players[j]))
                    return players[j], hp_players[j]
            except:
                if flag:
                    print("Opsss... parece que {} se ha desconectado".format(players[j]))
                    flag = False
    
    print("\033[1mTanto {} como {} han quedado con vida\033[0m\n".format(players[0], players[1]))
    return None


def first_punch(data): 
    df1 = pd.DataFrame(data['player1'])
    df2 = pd.DataFrame(data['player2'])
    
    # CONDICIÓN N° 1
    # Para determinar quien lanza el primer golpe
    # Primero verificamos quien utilizó la menor cantidad de botones
    if len(df1.movimientos[0]) + len(df1.golpes[0]) < len(df2.movimientos[0]) + len(df2.golpes[0]):
        return 1
    elif len(df2.movimientos[0]) + len(df2.golpes[0]) < len(df1.movimientos[0]) + len(df1.golpes[0]):
        return 2
    else:
        # CONDICIÓN N° 2
        # En caso que la suma de pulsaciones de botones de ambos jugadores sean iguales
        # Verificamos quien realizó la menor cantidad de movimientos
        if len(df1.movimientos[0]) < len(df2.movimientos[0]):
            return 1
        elif len(df2.movimientos[0]) < len(df1.movimientos[0]):
            return 2    
        else:
            # CONDICIÓN N° 3
            # Si aun continúan empatados se verifica la condición: "con menos golpes"
            # Debo aclarar que esta condición parece resultar contradictoria e innecesaria por tres razones:
            # 1. Porque según esto un jugador con 0 golpes atacaría primero otro jugador que sí haya golpeado,
            #    pero, ¿cómo podría atacar primero un jugador que no ha lanzado ningún golpe?, y
            # 2. Porque tampoco se puede referir a la cantidad total de golpes durante la pelea porque es imposible
            #    que un juego determine quien golpea primero basado en una condición que solo se puede conocer al
            #    final de la pelea.
            # 3. Porque si la suma movimientos + golpes son iguales y los movimientos también son iguales,
            #    entonces, necesariamente, los golpes también son iguales. Si A + B = C + D y, además,
            #    A = C, entonces B = D.
            # En todo se asumirá que al decir "Parte atacando" se refiere a que entra primero al algoritmo:
            if len(df1.golpes[0]) < len(df2.golpes[0]):
                return 1
            elif len(df2.golpes[0]) < len(df1.golpes[0]):
                return 2
            else:
                # Si luego de las tres comparaciones aun continúan empatados entonces player 1 ataca primero
                return 1


a = {"player1":{"movimientos":["D","DSD","S","DSD","SD"],"golpes":["K","P","","K","P"]},"player2": {"movimientos":["SA","SA","SA","ASA","SA"],"golpes":["K","","K","P","P"]}}
b = {"player1":{"movimientos":["SDD", "DSD", "SA", "DSD"] ,"golpes":["K", "P", "K", "P"]}, "player2":{"movimientos":["DSD", "WSAW", "ASA", "", "ASA", "SA"],"golpes":["P", "K", "K", "K", "P", "K"]}} 
c = {"player1":{"movimientos":["DSD", "S"] ,"golpes":["P", ""]}, "player2":{"movimientos":["", "ASA", "DA", "AAA", "", "SA"],"golpes":["P", "", "P", "K", "K", "K"]}}
d = {"player1":{"movimientos":["SDD", "DSD", "SA", "DSD"] ,"golpes":["K", "P", "K", "P"]}, "player2":{"movimientos":["DSD", "WSAW", "", "", "ASA", "SA"],"golpes":["", "", "", "", "", ""]}}
e = {"player1":{"movimientos":["DSD", "S"] ,"golpes":["P", ""]}, "player2":{"movimientos":["", "ASA"],"golpes":["P", ""]}}


fight(a)
fight(b)
fight(c)
fight(d)
fight(e)
