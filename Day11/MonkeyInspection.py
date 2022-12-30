import math


class Monkey():
    def __init__(self,name,items,operation,test) -> None:
        self.name = name
        self.items = items
        self.operation = operation
        self.test = test
        self.inspections = 0

def CreateMonkeys(txt):
    monkeys = []
    LCM = 1
    with open(txt) as f:
        allText = f.readlines()
        for i in range(0,len(allText),7):
            monkeyTxt = allText[i:i+7]
            name = monkeyTxt[0][:8]
            items = monkeyTxt[1].split()[2:]
            for i in range(len(items)):
                item = int(items[i].strip(","))
                items[i] = item
            operation = monkeyTxt[2].split()[-2:]
            testDiv = int(monkeyTxt[3].split()[-1])
            LCM *= testDiv
            testTrue = int(monkeyTxt[4].split()[-1])
            testFalse = int(monkeyTxt[5].split()[-1])
            test = [testDiv,testTrue,testFalse]
            newMonkey = Monkey(name,items,operation,test)
            monkeys.append(newMonkey)
    return monkeys,LCM

def runRound(monkeys,LCM):
    for monkey in monkeys:
        for i in range(len(monkey.items)):
            item = monkey.items[i]
            monkey.inspections += 1
            if monkey.operation[1] == "old":
                factor = int(item)
            else:
                factor = int(monkey.operation[1])

            if monkey.operation[0] == "+":
                item += factor
            else:
                item *= factor
            item = math.floor(item % LCM)
            if item % monkey.test[0] == 0:
                throwTo = monkey.test[1]
            else:
                throwTo = monkey.test[2]
            monkeys[throwTo].items.append(item)
        monkey.items = []
    return monkeys 

if __name__ == "__main__":
    txt = "input.txt"
    monkeys,LCM = CreateMonkeys(txt)
    for i in range(10000):
        monkeys = runRound(monkeys,LCM)
    mostActive = [0,0]
    for monkey in monkeys:
        if monkey.inspections > mostActive[0]:
            mostActive[1] = mostActive[0]
            mostActive[0] = monkey.inspections
        elif monkey.inspections > mostActive[1]:
            mostActive[1] = monkey.inspections
    print(mostActive[0]*mostActive[1])
