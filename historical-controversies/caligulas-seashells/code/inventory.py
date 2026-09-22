import sys,re,collections,json,csv; sys.path.insert(0,'.')
from concord import search
rows=search(r'\bmuscul[a-z]*',220)
for x in rows:
    if x["corpus"]=="LL" and not x["author"]:
        x["author"]="LL:"+x["id"].replace(".shtml","").replace(".html","")
# one edition per Perseus work: keep the file with most tokens
cnt=collections.Counter(x["id"] for x in rows if x["corpus"]=="PERSEUS")
best={}
for x in rows:
    if x["corpus"]!="PERSEUS": continue
    k=(x["author"],x["work"])
    if k not in best or cnt[x["id"]]>cnt[best[k]]: best[k]=x["id"]
keep=[x for x in rows if x["corpus"]=="LL" or x["id"]==best[(x["author"],x["work"])]]
# drop LL duplicates of works already present in Perseus
PER_WORKS={("Tertullian","De Carne Christi"):"tertullian__tertullian.carne",
           ("Columella, Lucius Junius Moderatus","Res Rustica"):"columella__columella.rr"}
keep=[x for x in keep if not (x["corpus"]=="LL" and any(x["id"].startswith(v) for v in PER_WORKS.values()))]
SENSE_RULES=[
 ("military-shed", r'turri|murum|muro|oppidan|obpugn|oppugn|machin|testudin|uine[ae]|vine[ae]|plute|arriet|ariet|crates|longurio|falces|bellator|fossatum|scalas|lateribus lutoque|capreolis|trabes'),
 ("boat",          r'navigium|nauigium|dromon|classis|curtum|Massiliae|Scythicorum|nauis|navis'),
 ("shellfish",     r'ostre|concha|conchul|conchyl|cochle|coclea|pelorid|echino|lopad|balano|margarit|limicol|urticam|plagusi|testa|conqu'),
 ("whale-fish",    r'ballaen|ballen|balen|belua|belu|pisc|marinus qui|antecedit|praenatans|praeguber'),
 ("muscle",        r'nerv|lacert|ossa|toris|tori|cutis|femor|corpus|carn|pector|brachi|viscer|humor|tumentes|robust|adipibus|membran|sanie|dissic|densitate'),
 ("mouse/small-animal", r'\bmur|mures|felis|feles|arvis|aruis|terra|ruinis|praemigrant|aures|tineas|litteras|rimari|bestia|iecuscula|myosot'),
 ("fly(muscula)",  r'sciniphes|morsus|veneno|reptantium'),
]
def classify(ctx):
    hits=[n for n,p in SENSE_RULES if re.search(p,ctx,re.I)]
    return hits
out=[]
for x in keep:
    out.append({"author":x["author"],"work":x["work"],"cit":x["cit"],"form":x["form"],
                "corpus":x["corpus"],"id":x["id"],"auto":"|".join(classify(x["ctx"])),
                "ctx":x["ctx"]})
with open("musculus_inventory_auto.csv","w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=list(out[0].keys())); w.writeheader(); w.writerows(out)
print("unique tokens:",len(out))
c=collections.Counter(o["auto"].split("|")[0] if o["auto"] else "UNCLASSIFIED" for o in out)
for k,v in c.most_common(): print(f"  {k:24s} {v}")
print("\nAMBIGUOUS/UNCLASSIFIED (need my eye):")
for o in out:
    if not o["auto"] or len(o["auto"].split("|"))>2:
        print(f"  [{o['author'][:26]:26s}] {o['form']:12s} {o['auto'][:40]:40s} {o['ctx'][140:330]}")
