# Our directories form a tree like structure, with / at the top
# each directory has leaves (files) and sub directories which contain leaves
# we run this recursively and return the sum of all files in that directory

class Node():
    def __init__(self) -> None:
        self.subDirs = dict() #A dictionary of names to nodes
        self.sumOfFiles = 0
        self.totalSize = 0
        self.parent = None
        self.name = None

    def __str__(self) -> str:
        subDirs = "SubDirs: " + str(self.subDirs) + "\n"
        sumFiles = "Sum of Files: " + str(self.sumOfFiles) + "\n"
        if self.parent:
            parentName = "Name of parent: " + self.parent.name
        else:
            parentName = "No parent"
        return ("The directory " + self.name + " Has: \n" + subDirs + sumFiles + parentName)

def BuildTree(txt):
    topDir = None
    currentDir = None
    with open(txt) as f:
        lineNumber = 0
        for line in f:
            lineNumber += 1
            line = line.strip('/n').split()
            if line[0] == "$":
                if line[1] == "cd":
                    if line[2] != "..":
                        if currentDir == None:
                            currentDir = Node()
                            currentDir.name = "/"
                            topDir = currentDir
                        else:
                            currentDir = currentDir.subDirs[line[2]]
                    else:
                        currentDir = currentDir.parent
            elif line[0] == "dir":
                newNode = Node()
                newNode.name = line[1]
                newNode.parent = currentDir
                currentDir.subDirs[line[1]] = newNode
            else:
                currentDir.sumOfFiles += int(line[0])
    
    return topDir

def navigateTree(Node,dirs100K,requiredSpaceMatch,requiredSpace):
    thisNodeTotal = Node.sumOfFiles
    if Node.subDirs:
        for n in Node.subDirs.values():
            otherNode, dirs100K,requiredSpaceMatch,requiredSpace = navigateTree(n,dirs100K,requiredSpaceMatch,requiredSpace)
            thisNodeTotal += otherNode.totalSize
    if thisNodeTotal <= 100000:
        dirs100K.append(thisNodeTotal)
    Node.totalSize = thisNodeTotal
    if Node.totalSize > requiredSpace:
        requiredSpaceMatch.append(Node.totalSize)
    return Node,dirs100K,requiredSpaceMatch,requiredSpace

def SizeOfDeletedDir(topDir):
    unusedSpace = 70000000 - topDir.totalSize
    requiredSpace = 30000000 - unusedSpace
    _,_,dirs,_ = navigateTree(topDir,[],[],requiredSpace)
    return min(dirs)



if __name__ == "__main__":
    txt = "input.txt"
    topDir = BuildTree(txt)
    topDir,dirs100K,_,_ = navigateTree(topDir,[],[],0)
    print(topDir.totalSize,SizeOfDeletedDir(topDir))
    # TopDir,dirs100K = navigateTree(BuildTree(txt),[])[1]
    # print(sum(dirs100K))