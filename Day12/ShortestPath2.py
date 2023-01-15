from collections import deque
dirs = [(0,1),(1,0),(0,-1),(-1,0)]

with open("input.txt") as f:
    s = f.read().strip()


g = [list(x) for x in s.split("\n")]
n = len(g)
m = len(g[0])

possibleStarts = []

for i in range(n):
    for j in range(m):
        if g[i][j] == "S":
            g[i][j] = "a"
            possibleStarts.append((i,j))
        elif g[i][j] == "a":
            possibleStarts.append((i,j))
        elif g[i][j] == "E":
            tx,ty = (i,j)
            g[i][j] = "z"

g = [[ord(c) - ord("a") for c in r] for r in g]
lowest = 100000
for (sx,sy) in possibleStarts:
    dstToLoc = dict()
    dstToLoc[(sx,sy)] = 0

    #Now g is a bunch of values
    queue = deque([(sx,sy)])

    while queue:
        cx,cy = queue.popleft()
        if (cx,cy) == (tx,ty):

            if dstToLoc[(tx,ty)] < lowest:
                lowest = dstToLoc[(tx,ty)]
                print(lowest)
                break
        for dx,dy in dirs:
            nx, ny = cx + dx, cy + dy
            if nx in range(n) and ny in range(m):
                if g[cx][cy] >= g[nx][ny] - 1:
                    ndst = dstToLoc[(cx,cy)] + 1
                    if (nx,ny) in dstToLoc and dstToLoc[(nx,ny)] > ndst or (nx,ny) not in dstToLoc:
                        queue.append((nx,ny))
                        dstToLoc[(nx,ny)] = ndst



