def binaryInsert(valueToInsert,stack,index,order):
    """
    Insert into a stack of sorted values, sorted based on value[index] and in either ascending or descending order.
    
    
    Return: sorted array with value inserted
    """
    left = 0
    right = len(stack)
    while left < right:
        middle = left + (right-left)//2
        if isinstance(valueToInsert,list):
            middleValue = stack[middle][index]
            valueToInsert = valueToInsert[index]
        else:
            middleValue = stack[middle]
        
        if middleValue > valueToInsert:
            if order == "ascending":
                right = middle
            else:
                left = middle + 1
        elif middleValue < valueToInsert:
            if order == "ascending":
                left = middle + 1
            else:
                right = middle
        else:
            return stack[:middle] + [valueToInsert] + stack[middle:]
    return stack[:left] + [valueToInsert] + stack[left:]
    
