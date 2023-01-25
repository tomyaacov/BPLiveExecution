import os
import javaobj

for file_name in os.listdir("/Users/tomyaacov/university/BPLiveExecution/examples/graph_objects"):
    with open("/Users/tomyaacov/university/BPLiveExecution/examples/graph_objects/" + file_name, "rb") as fd:
        jobj = fd.read()
        pobj = javaobj.loads(jobj)
        print(file_name, len(pobj))
