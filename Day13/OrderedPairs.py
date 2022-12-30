import ast

def FindOrderedPairsSum(txt):
    orderedPairs = []
    with open(txt) as f:
        allText = f.readlines()
        for i in range(0,len(allText),3):
            pairIndex = int(i/3+1)
            left = ast.literal_eval(allText[i])
            right = ast.literal_eval(allText[i+1])
            if IsPairOrdered(left,right):
                orderedPairs.append(pairIndex)
    print(orderedPairs)
    return sum(orderedPairs)

def binaryInsertion(element,sortedArray):
    left = 0
    right = len(sortedArray)
    while left < right:
        middle = left + (right-left)//2
        if IsPairOrdered(element,sortedArray[middle]):
            #This pair is in order, so element should be left of middle
            right = middle
        else:
            #This pair is not in order, so element should be right of middle or in middles place
            left = middle + 1
            # print(left,middle,right)
            
    newArray = sortedArray[:left] + [element] + sortedArray[left:]
    # print(newArray)
    return newArray,(left+1)

def CalculateDecoderKey(txt):
    # Now for part 2 we have to order ALL of our elements, then add distress signals
    orderedOutput = []
    with open(txt) as f:
        for line in f:
            line = line.strip()
            if line:
                element = ast.literal_eval(line)
                if len(orderedOutput) == 0:
                    orderedOutput.append(element)
                else:
                    orderedOutput, _ = binaryInsertion(element,orderedOutput)
    orderedOutput,distressIndex1 =  binaryInsertion([[2]],orderedOutput)
    orderedOutput,distressIndex2 = binaryInsertion([[6]],orderedOutput)
    print(orderedOutput)
    return distressIndex1*distressIndex2

def IsPairOrdered(left,right):
    leftIndex = 0
    rightIndex = 0
    while leftIndex < len(left) and rightIndex < len(right):
        if isinstance(left[leftIndex],int) and isinstance(right[rightIndex],int):
            leftVal = left[leftIndex]
            rightVal = right[rightIndex]
            if leftVal == rightVal:
                leftIndex += 1
                rightIndex += 1
                continue
            else:
                return leftVal < rightVal
                
        elif isinstance(left[leftIndex],list) and isinstance(right[rightIndex],list):
            nextTest = IsPairOrdered(left[leftIndex],right[rightIndex])
            if nextTest is not None:
                return nextTest
            else:
                leftIndex += 1
                rightIndex += 1
                continue
        else:
            #one is list, one is int
            if isinstance(left[leftIndex],int):
                nextTest = IsPairOrdered([left[leftIndex]],right[rightIndex])
            else:
                nextTest = IsPairOrdered(left[leftIndex],[right[rightIndex]])

            if nextTest is not None:
                return nextTest
            else:
                leftIndex += 1
                rightIndex += 1
                continue 

    if leftIndex >= len(left) - 1 and rightIndex != len(right):
        return True
    elif rightIndex >= len(right) - 1 and leftIndex != len(left):
        return False
    else:
        return None



if __name__ == "__main__":
    txt = "input.txt"
    # print(FindOrderedPairsSum(txt))
    print(CalculateDecoderKey(txt))