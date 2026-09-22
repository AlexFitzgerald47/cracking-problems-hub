"""Final hand-audited musculus inventory.
Auto-classification is by keyword rule; every token whose auto-label I judged wrong on
reading the context is corrected here by an explicit override keyed on a context substring.
Each override is a decision I made by reading the passage, not a rule."""
import os,sys,re,csv,collections; sys.path.insert(0,'.')
from concord import search
OVERRIDES=[
 ("intentique super musculi apparent","muscle","Celsus: anatomical; auto-rule leaked on 'osse'."),
 ("valentissimi nervi musculique","muscle","Celsus: anatomical."),
 ("et musculis, nervis, articulis inposuit","muscle","Plin. NH 26: anatomical."),
 ("musculorum aures imitatur foliis","mouse","Plin. NH 27.104: myosotis, 'mouse-ear' plant."),
 ("arietes, musculi et alii piscium forma","whale-fish","Plin. NH 9.8: catalogue of sea-beasts (beluae)."),
 ("morsibus suos incursantes musculos","muscle","Apuleius Met. 8.27: the Syrian priests bite their own muscles."),
 ("ossa musculi nervi","muscle","Plin. Ep. 5.8.10 (x2 copies): bones/muscles/sinews of a statue and of a style."),
 ("hanc saepius ossa musculi","muscle","Plin. Ep. 5.8.10, second clause."),
 ("muscularum quoque uel morsus","fly","Boethius Cons. 2 pr.6: MUSCULA = dim. of musca, a fly."),
 ("Scinifes enim musculae sunt","fly","Augustine Trin. 3: musculae = tiny flies (sciniphes)."),
 ("illas musculas quae appellantur scinifes","fly","Augustine Serm. 8: same, flies."),
 ("sciniphes, musculas scilicet paruissimas","fly","Orosius 7: same, flies."),
 ("muscularum aliae ut interirent veneno","fly","Arnobius 2: flies."),
 ("nascuntur aquatiles musculi","mouse-aquatic","Plin. NH 2.227: water-mice in a spring; TLL puts this under mus aquatilis."),
 ("detegente eo musculi reperiuntur","mouse-aquatic","Plin. NH 9.179: mice half-formed from Nile mud."),
 ("musculus, quod sit ballenae masculus","whale-fish","Isid. Etym. 12.6.6: musculus as the whale's male."),
 ("ne musculus iste aliquid aliqua rimari","mouse","Fronto: a 'mouse' who might nose out the letter."),
 ("Nero musculo inquit","mouse","Alice in Wonderland in Latin - MODERN, excluded from counts."),
]
rows=search(r'\bmuscul[a-z]*',220)
for x in rows:
    if x["corpus"]=="LL" and not x["author"]: x["author"]="LL:"+x["id"].replace(".shtml","").replace(".html","")
cnt=collections.Counter(x["id"] for x in rows if x["corpus"]=="PERSEUS")
best={}
for x in rows:
    if x["corpus"]!="PERSEUS": continue
    k=(x["author"],x["work"])
    if k not in best or cnt[x["id"]]>cnt[best[k]]: best[k]=x["id"]
keep=[x for x in rows if x["corpus"]=="LL" or x["id"]==best[(x["author"],x["work"])]]
RULES=[("military-shed",r'turri|murum|muro|oppidan|obpugn|oppugn|machin|testudin|uine[ae]|vine[ae]|plute|ariet|crates|longurio|falces|bellator|fossatum|scalas|capreolis|trabes|cuniculo similis'),
 ("boat",r'navigium|nauigium|dromon|curtum|Massiliae|Scythicorum'),
 ("shellfish",r'ostre|concha|conchul|conchyl|cochle|coclea|pelorid|echino|lopad|balano|margarit|limicol|urticam|plagusi'),
 ("whale-fish",r'ballaen|ballen|balen|marinus, qui|antecedit|praenatans|praeguber|marinis beluis'),
 ("muscle",r'nerv|lacert|ossa|toris|\btori\b|femor|carn|pector|brachi|viscer|tumentes|adipibus|sanie|densitate|maxillas|jugali|osse'),
 ("mouse",r'\bmur[ei]s\b|mures|felis|feles|arvis|aruis|ruinis|praemigrant|aures|tineas|litteras|iecuscula|myosot'),
]
MODERN=("alice__","newton","descartes","balde","campion","withof","boskovic","biggs","xylander")
out=[]
for x in keep:
    if any(m in x["id"] for m in MODERN): continue          # post-classical, excluded
    lab=next((n for n,p in RULES if re.search(p,x["ctx"],re.I)), "UNCLASSIFIED")
    note=""
    for frag,newlab,why in OVERRIDES:
        if frag.lower() in x["ctx"].lower(): lab,note=newlab,why; break
    if lab=="UNCLASSIFIED": lab,note="muscle","Celsus surgical context; anatomical by default in this work."
    out.append({"sense":lab,"author":x["author"],"work":x["work"],"form":x["form"],
                "corpus":x["corpus"],"source_id":x["id"],"note":note,"context":x["ctx"]})
out.sort(key=lambda r:(r["sense"],r["author"]))
with open(os.environ.get("OUT_CSV","musculus_inventory.csv"),"w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=["sense","author","work","form","corpus","source_id","note","context"])
    w.writeheader(); w.writerows(out)
c=collections.Counter(r["sense"] for r in out)
print("tokens (one edition per work, moderns excluded):",len(out))
for k,v in c.most_common(): print(f"  {k:16s} {v:4d}  {100*v/len(out):5.1f}%")
# distinct passages per sense (collapse LL/Perseus duplicates of the same passage)
def core(s): return re.sub(r'[^a-z]','',s.lower())[60:150]
pas=collections.defaultdict(set)
for r in out: pas[r["sense"]].add(core(r["context"]))
print("\ndistinct passages per sense:")
for k,v in sorted(pas.items(), key=lambda kv:-len(kv[1])): print(f"  {k:16s} {len(v)}")
