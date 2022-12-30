#Rock paper scissors input column 1:
    #A = Rock, B = Paper, C = Scissors
#column 2:
    #X = Rock (1), Y = Paper (2), Z = Scissors (3)
#lose = 0, draw = 3, win = 6
def calculateStrategy():
    playScores = {'X':1,'Y':2,'Z':3}
    winningPlays = {'Z':'B','X':'C','Y':'A','A':'Z','B':'X','C':'Y'}
    total = 0
    with open('input.txt') as f:
        for line in f:
            # print(line,line.strip('/n'))
            play = line.strip('/n').split()
            # print(play)
            total += playScores[play[1]]
            if winningPlays[play[1]] == play[0]:
                total += 6
            elif winningPlays[play[0]] == play[1]:
                continue
            else:
                total += 3
    return total
#Rock paper scissors input column 1:
    #A = Rock, B = Paper, C = Scissors
#column 2:
    #X = Lose game, Y = draw game (2), Z = Win game (3)
#lose = 0, draw = 3, win = 6
def calculateStrategy2():
    playScores = {'X':1,'Y':2,'Z':3}
    winningPlays = {'A':'Z','B':'X','C':'Y'}
    losingPlays = {'A':'Y','B':'Z','C':'X'}
    total = 0
    with open('input.txt') as f:
        for line in f:
            # print(line,line.strip('/n'))
            play = line.strip('/n').split()
            if play[1] == 'X':
                myHand = winningPlays[play[0]]
            elif play[1] == 'Z':
                myHand = losingPlays[play[0]]
                total += 6
            else:
                myHand = ['X','Y','Z']
                myHand.remove(winningPlays[play[0]])
                myHand.remove(losingPlays[play[0]])
                myHand = myHand[0]
                total += 3
            print(play,myHand)
            total +=  playScores[myHand]
    return total
if __name__ == "__main__":
    print(calculateStrategy2())

