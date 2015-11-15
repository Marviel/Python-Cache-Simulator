dupes = 0
with open('addresses.txt') as f:
    seen = set()
    for line in f:
        line_lower = line.lower()
        if line_lower in seen:
            print(line)
            dupes += 1
        else:
            seen.add(line_lower)

print("num dupes: %d"%(dupes))