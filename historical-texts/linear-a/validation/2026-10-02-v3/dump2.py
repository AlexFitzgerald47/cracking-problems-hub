import sys, json, os, importlib.util
spec = importlib.util.spec_from_file_location("inh", os.path.join(os.path.dirname(os.path.abspath(__file__)),"inherited_refute_scribe9.py"))
inh = importlib.util.module_from_spec(spec); spec.loader.exec_module(inh)
A = inh.load_a()
for t in sys.argv[1:]:
    v = A[t]
    print("===", t)
    for k in ("transcription","context","words","translatedWords","parsedInscription"):
        val = v.get(k)
        s = json.dumps(val, ensure_ascii=False)
        print(f"  {k}: {s[:1400]}")
