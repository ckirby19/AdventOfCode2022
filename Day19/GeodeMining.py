class State():
    def __init__(self) -> None:
        self.robots = {"ore":1,"clay":0,"obsidian":0,"geode":0}
        self.resources = {"ore":0,"clay":0,"obsidian":0,"geode":0}
        self.timePassed = 0
        self.previousPurchase = "None"
        self.couldHavePurchased = "None"
        
class Blueprint():
    def __init__(self,oreRobotCost,clayRobotCost,obsidianRobotCost,geodeRobotCost,time) -> None:
        self.robotCosts = {"ore":oreRobotCost,"clay":clayRobotCost,"obsidian":obsidianRobotCost,"geode":geodeRobotCost}
        self.order = ["geode","obsidian","clay","ore"]
        self.timeLimit = time
        self.maxOreNeeded = 0

    # Binary insertion into sorted stack (ascending)
    def binaryInsert(self, stack, item, sortingIndex):
        # print(f"Inserting {item.resources} into {stack} based on {self.order[sortingIndex]}")
        if len(stack) == 0:
            stack.append(item)
        else:
            if stack[len(stack) - 1].robots[self.order[sortingIndex]] < item.robots[self.order[sortingIndex]] :
                stack.append(item)
            else:
                low = 0
                high = len(stack) - 1
                while low <= high:
                    mid = (low + high) // 2
                    if stack[mid].robots[self.order[sortingIndex]] < item.robots[self.order[sortingIndex]] :
                        low = mid + 1
                    else:
                        high = mid-1
                stack.insert(low, item)
        return stack

    def qualityLevel(self) -> None:
        # Keep track of states containing number of each robot, amount of ore,clay,obsidian and geode
        # We can get rid of states that obtain less geodes in more time
        # I need some way to keep track of the "bottleneck" or to avoid spending on ore or clay robots if not needed
        state = State()
        bestQL = 0
        stack = [state]
        while stack:
            currentState = stack.pop()
            timeLeft = self.timeLimit - currentState.timePassed
            if timeLeft == 0:
                bestQL = max(bestQL,currentState.resources["geode"])
                continue
            elif currentState.resources["geode"] + currentState.robots["geode"]*timeLeft + sum(range(timeLeft)) < bestQL:
                continue
        
            # First we add a new state where we add no new robots, in order to save our resources for later
            newStateNoPurchase = State()
            newStateNoPurchase.robots = currentState.robots.copy()
            newStateNoPurchase.resources = currentState.resources.copy()
            newStateNoPurchase.timePassed = currentState.timePassed + 1
            for robot in currentState.robots:
                newStateNoPurchase.resources[robot] += currentState.robots[robot]
            

            # Now we check to see if we can spend what we have on new robots
            couldHavePurchased = set()
            if self.timeLimit - currentState.timePassed != 1:
                for option in self.order:
                    if option not in currentState.couldHavePurchased:
                        #Can we afford this robot option?
                        if all(currentState.resources[material] >= self.robotCosts[option][material] for material in self.robotCosts[option]):
                            #Do we need this robot?
                            required = True
                            materialCalc = currentState.resources[option] + currentState.robots[option] * timeLeft
                            if option == "obsidian":
                                required = materialCalc < self.robotCosts["geode"][option] * timeLeft
                            if option == "clay":
                                required = materialCalc < self.robotCosts["obsidian"][option] * timeLeft
                            if option == "ore":
                                required = materialCalc < self.maxOreNeeded * timeLeft
                            if required == True:
                                newState = State()
                                newState.robots = currentState.robots.copy()
                                newState.resources = currentState.resources.copy()
                                for material in self.robotCosts[option]:
                                    newState.resources[material] -= self.robotCosts[option][material]
                                newState.robots[option] += 1
                                for robot in currentState.robots:
                                    newState.resources[robot] += currentState.robots[robot]
                                newState.timePassed = currentState.timePassed + 1
                                newState.previousPurchase = option
                                newState.couldHavePurchased = set()
                                stack = self.binaryInsert(stack, newState,0)
                                couldHavePurchased.add(option)

            newStateNoPurchase.previousPurchase = "None"
            newStateNoPurchase.couldHavePurchased = couldHavePurchased
            stack = self.binaryInsert(stack, newStateNoPurchase,0)
            stack = stack[-12000:]

        return bestQL
        
def createBlueprints(txt,time):
    blueprints = []
    with open(txt) as f:
        for line in f:
            line = line.strip().split()
            oreRobot = {"ore":int(line[6])}
            clayRobot = {"ore":int(line[12])}
            obsidianRobot = {"ore":int(line[18]),"clay":int(line[21])}
            geodeRobot = {"ore":int(line[27]),"obsidian":int(line[30])}
            blueprint = Blueprint(oreRobot,clayRobot,obsidianRobot,geodeRobot,time)
            blueprint.maxOreNeeded = max(oreRobot["ore"],clayRobot["ore"],obsidianRobot["ore"],geodeRobot["ore"])
            blueprints.append(blueprint)
    return blueprints

def totalQuality(blueprints):
    total = 0
    for i,blueprint in enumerate(blueprints):
        ql = blueprint.qualityLevel()
        print("QL of ",(i+1)*ql)
        total += (i+1)*ql
    return total

def totalQualityPart2(blueprints):
    total = 1
    for blueprint in blueprints[:3]:
        ql = blueprint.qualityLevel()
        print("QL of ",ql)
        total *= ql
    return total


if __name__ == "__main__":
    txt = "input2.txt"
    # blueprints = createBlueprints(txt,24)
    # print(totalQuality(blueprints))
    blueprints = createBlueprints(txt,32)
    print(totalQualityPart2(blueprints))