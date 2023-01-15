txt = "input.txt"
def findStart():
    with open(txt) as f:
        line = f.readline().split()[0]
        left = 0
        right = 14
        while right <= len(line)-14:
            window = line[left:right]
            unique = True
            seen = set()
            for char in window:
                if char in seen:
                    unique = False
                    continue
                else:
                    seen.add(char)
            if unique == True:
                return right
            else:
                left += 1
                right += 1

if __name__ == "__main__":
    print(findStart())

