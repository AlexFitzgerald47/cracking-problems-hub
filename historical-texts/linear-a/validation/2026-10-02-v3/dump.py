import sys, json, re, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import importlib.util
spec = importlib.util.spec_from_file_location("inh", os.path.join(os.path.dirname(os.path.abspath(__file__)),"inherited_refute_scribe9.py"))
inh = importlib.util.module_from_spec(spec); spec.loader.exec_module(inh)
A = inh.load_a()
for t in sys.argv[1:]:
    v = A[t]
    print("=== ", t, " scribe=", v.get("scribe"), " findspot=", v.get("findspot"), " support=", v.get("support"))
    print("   keys:", list(v.keys()))
    ws = v["transliteratedWords"]
    print("   words:", json.dumps(ws, ensure_ascii=False))
