import os
DIR = "js_maps_new"
OUT_DIR = "py_maps_new"
maps = {}
for file_name in os.listdir(DIR):
    l = []
    with open(os.path.join(DIR, file_name), "r") as f:
        for line in f:
            new_line = line.strip("\n").replace("#", "X")
            new_line = new_line.replace("@", "a")
            new_line = new_line.replace("$", "b")
            new_line = new_line.replace(".", "t")
            l.append("X" + new_line + "X")
    l = ["X"*len(l[0])] + l + ["X"*len(l[0])]
    out_name = file_name.replace(".txt", "")
    with open(os.path.join(OUT_DIR, out_name), "w") as out_f:
        out_f.write("\n".join(l))
    maps[out_name] = l

print(maps)
