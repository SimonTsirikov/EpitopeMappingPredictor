
with open("epitope3d_ids", "r") as f:
    their = set(map(lambda x: x.strip("\n"), f.readlines()))
with open("names_nonempty.txt", 'r') as f:
    ours = set(map(lambda x: x.strip("\n"), f.readlines()))

for item in ours.difference(their):
    print(item)
    