import csv
RULES=[  # (substring key, verdict, reason)
 ('ellu bak',          'TARGET',            'Sigvatr, Knutsdrapa st.1 -- the disputed passage itself'),
 ('bak ellu',          'TARGET',            'Sigvatr, Knutsdrapa st.1 -- the disputed passage itself'),
 ('ara braedis',       'NOT-AGENT:kenning', '"ara braedis" = eagle-feeder, a WARRIOR kenning; skar has the ship/king as subject (salt skar hufi)'),
 ('hrafn gaelir',      'NOT-AGENT:kenning', '"hrafn gaelir" = raven-gladdener, WARRIOR kenning; rista has the gilded prows as subject'),
 ('hnitsol ara fitjar','NOT-AGENT:kenning', '"ara fitjar" inside a kenning; hjo has a warrior as subject'),
 ('sargammr enn',      'NOT-AGENT:separate','sargammr "wound-vulture" tramps (thramma); klauf has gunnsproti (sword) as subject, different clause'),
 ('vissak hrafn',      'NOT-AGENT:name',    'Hrafn is a MAN\'S NAME here (Gisli/Bjorn material): "I knew Hrafn to strike me"; hoggva is his sword-blow'),
 ('hrafni thas',       'NOT-AGENT:name',    'same passage: dative of the personal name Hrafn'),
 ('hrafn hoggva',      'NOT-AGENT:name',    'same passage: personal name Hrafn as subject of hoggva'),
 ('saddi gera',        'NOT-AGENT:separate','"saddi gera" = HE sated the wolf (feeding); "benjar skera" = HE cut wounds. Both have the king as subject'),
 ('vargfaedir',        'NOT-AGENT:separate','"skar eggjum" subject = eggjandi (the inciter); wolf is PATIENT of raud granar (reddened jaws)'),
 ('vargfoedir',        'NOT-AGENT:separate','"skar eggjum" subject = eggjandi (the inciter); wolf is PATIENT of raud granar (reddened jaws)'),
 ('ulfs fot vid sker', 'FALSE-POSITIVE',    '"sker" here is the NOUN skerry, and Ulfsfot/Sota are place-names'),
 ('thaut ulfr',        'NOT-AGENT:separate','wolf howls over corpses; klauf has the warrior as subject'),
 ('ulfr of hraevi',    'NOT-AGENT:separate','wolf howls over corpses; klauf has the warrior as subject'),
 ('ulfr of hraevum',   'NOT-AGENT:separate','wolf howls over corpses; klauf has the warrior as subject'),
 ('vargr fagnaoi',     'NOT-AGENT:separate','"vargr fagnadi tafni" = wolf rejoiced in prey; hjoggum ver = Kraakumal refrain, human subject'),
 ('vargr fagnadi',     'NOT-AGENT:separate','"vargr fagnadi tafni" = wolf rejoiced in prey; hjoggum ver = Kraakumal refrain, human subject'),
 ('eggja orn at sver', 'WINDOW-ARTEFACT',   'blade verb (hjoggu) belongs to the NEXT stanza; a stanza number intervenes'),
 ('qrn drekkr sylg',   'WINDOW-ARTEFACT',   'blade token is the tail of the previous stanza; this stanza is pure feeding: orn drekkr, ylgr faer undorn, ulfr rydr kjopt, ari getr verd'),
 ('orn drekkr sylg',   'WINDOW-ARTEFACT',   'blade token is the tail of the previous stanza; this stanza is pure feeding: orn drekkr, ylgr faer undorn, ulfr rydr kjopt, ari getr verd'),
 ('veigar hrafna',     'NOT-AGENT:separate','hrafna is a kenning determinant; grafna "engraved" is not a blade verb governed by the bird'),
 ('hrafns aett',       'NOT-AGENT:separate','"hrafns aett" = the raven\'s kin (carrion birds); hjorr skar leggi -- the SWORD cuts legs'),
 ('hrafns sut',        'NOT-AGENT:separate','hrafns in a kenning; hjo has a warrior as subject'),
 ('gaf vargi',         'NOT-AGENT:separate','"gaf vargi segg" = gave a man to the wolf (feeding, dative); hoggva has the warrior as subject'),
 ('raunmargan gaf',    'NOT-AGENT:separate','"gaf vargi segg" = gave a man to the wolf (feeding, dative); hoggva has the warrior as subject'),
 ('skorin vas skoglar','NOT-AGENT:separate','"Skoglar kapa" = the shield was cut in battle; beasts are in a neighbouring clause'),
 ('geira skorin',      'NOT-AGENT:separate','"Skoglar kapa" = the shield was cut in battle; beasts are in a neighbouring clause'),
 ('lind skerr i styr', 'NOT-AGENT:separate','"lind skerr" = the shield cuts; wolf elsewhere in the stanza'),
 ('sundr rjufa spjor', 'NOT-AGENT:separate','"lind skerr" = the shield cuts; wolf elsewhere in the stanza'),
 ('elin bak',          'TARGET',            'Sigvatr, Knutsdrapa st.1 -- OCR variant of "Ellu bak" in the replicate scan'),
 ('vissak hrafu',      'NOT-AGENT:name',    'OCR variant; Hrafn is a personal name, subject of hoggva'),
 ('vargfae ir',        'NOT-AGENT:separate','OCR-broken "vargfaedir"; skar eggjum subject = eggjandi, wolf is patient of raud granar'),
 ('ulfs fot vi5 sker', 'FALSE-POSITIVE',    '"sker" is the NOUN skerry; Ulfsfot/Sota are place-names'),
 ('morgum vargi',      'NOT-AGENT:separate','"raud granar morgum vargi" = reddened the jaws for many a wolf (dative, feeding); skar has eggjandi as subject'),
]
rows=list(csv.DictReader(open('beast_blade_adjudication.tsv'),delimiter='\t'))
un=0
for r in rows:
    c=r['context']
    for key,v,why in RULES:
        if key in c:
            r['verdict']=v; r['reason']=why; break
    else:
        r['verdict']='UNASSIGNED'; r['reason']=''; un+=1
with open('beast_blade_adjudication.tsv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=['scan','beast','blade','verdict','reason','context'],delimiter='\t'); w.writeheader(); w.writerows(rows)
import collections
print(collections.Counter(r['verdict'] for r in rows))
print('\nUNASSIGNED rows needing hand review:')
for r in rows:
    if r['verdict']=='UNASSIGNED': print(' ', r['scan'], r['beast'], r['blade'], '|', r['context'][:190])
