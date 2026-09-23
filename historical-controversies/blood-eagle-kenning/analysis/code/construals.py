import re, json, collections
exec(open('extract.py').read().split("CORP = ")[0])
def prep(t):
    return re.sub(r'\b[pq9g0O]rn(a|ar|i|u|um|s)?\b', lambda m:'orn'+(m.group(1) or ''), t)
DA=set('og er den det som til paa af han hans blev der ikke var sig kongen mod over efter fra alle sin sine jeg med de hvor'.split())
def is_da(s): return len(set(s.split()) & DA) >= 4

F = {nm: fold(prep(t)) for nm,t in [('BI',B1),('BII',B2)]}

# DATIVE forms of the beasts (the case 'ara' would be under C2/C3)
BEAST_DAT = r'\b(ara|erni|ornum|hrafni|hrofnum|ulfi|ulfum|vargi|vorgum|gera|freka|ylgi|nagri|gammi)\b'
GIVE_FEED = r'\b(gaf|gefa|gefr|gefit|gefinn|saddi|sadda|seddi|metta|mettr|foeddi|foeda|foeddr|fylla|fyldi|gleddi|gladdi|gledja|veita|veitti|bau5|baud|bjo5a|rauo|raud|rjoda|rodinn|rudu|sendi|senda|let)\b'
KILL     = r'\b(fella|feldi|feldr|drap|drepa|slo|sla|va|vega|vegit|veginn|hjo|hoggva|hogginn|myrda|banad)\b'
BLADE    = r'\b(skera|skar|skaru|sker|skerr|skorinn|skorin|skorit|skorna|skornir|rista|reist|ristu|ristinn|ristit|ristin|ristnir|grafinn|grafna|grafit|markad|markadr)\b'
# figure/surface objects that a blade verb carves ON (shield, prow, stone, wood, horn, board)
SURFACE  = r'\b(baugvang|rit|rond|rondu|randir|skjold|skjoldr|skjoldu|dreka|drekar|borsi|bordi|bord|stafn|stafni|horn|hornum|stein|steini|tre|topt|kapa|kapu|kertis|merki|maerki)\b'

def scan(pat_a, pat_b, win=70, label=''):
    out=[]
    for nm,f in F.items():
        for m in re.finditer(pat_a,f):
            a=max(0,m.start()-win); b=min(len(f),m.end()+win); ctx=f[a:b]
            if is_da(ctx): continue
            if re.search(pat_b,ctx): out.append((nm,m.group(0),ctx))
    return out

print('#'*72)
print('BASE RATES FOR THE COMPETING CONSTRUALS OF `ara` in Knutsdrapa 1')
print('   "let bak Ellu skorit ara"  -- Old Norse verse contexts only, +/-70 chars')
print('#'*72)

dat_all = scan(BEAST_DAT, r'.', label='any')
print(f'\nTotal dative-form beast lexemes in ON verse         : {len(dat_all)}')

c3 = scan(BEAST_DAT, GIVE_FEED)
print(f'C3  beast-dative near a GIVE/FEED/REDDEN verb        : {len(c3)}')
c3k = scan(BEAST_DAT, KILL)
print(f'    beast-dative near a KILL verb                    : {len(c3k)}')
c2 = scan(BEAST_DAT, BLADE)
print(f'C2  beast-dative near a BLADE/CARVE verb             : {len(c2)}')
print('    --- every C2 hit, for hand adjudication ---')
for nm,w,ctx in c2: print(f'      [{nm}] {w}: ...{ctx}...')

c1 = scan(BLADE, SURFACE)
print(f'\nC1  BLADE/CARVE verb near a carvable SURFACE noun    : {len(c1)}')
for nm,w,ctx in c1[:24]: print(f'      [{nm}] {w}: ...{ctx[40:200]}...')
json.dump(dict(c1=c1,c2=c2,c3=c3,c3k=c3k,dat_all=dat_all), open('construals.json','w'))
