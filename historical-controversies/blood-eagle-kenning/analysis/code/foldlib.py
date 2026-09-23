# --- OCR folding for Old Norse search -------------------------------------
THORN = ['|>','j>','{>','J3','f)','(>','i>','J>','£>',']>','>','J?','j?','|?']
def fold(t):
    t = t.replace('­','')
    for s in THORN: t = t.replace(s,'th')
    trans = {
      'þ':'th','Þ':'th','ð':'d','Ð':'d','ø':'o','Ø':'o','œ':'oe','Œ':'oe',
      'æ':'ae','Æ':'ae','ǫ':'o','Ǫ':'o','ö':'o','Ö':'o','å':'a','Å':'a',
      'á':'a','é':'e','í':'i','ó':'o','ú':'u','ý':'y','Á':'a','É':'e','Í':'i',
      'Ó':'o','Ú':'u','Ý':'y','ä':'a','ü':'u','ë':'e',
    }
    t = ''.join(trans.get(c,c) for c in t)
    t = t.lower()
    # common OCR digit-for-letter inside words
    t = re.sub(r'(?<=[a-z])5(?=[a-z])','d',t)
    t = re.sub(r'(?<=[a-z])9(?=[a-z])','o',t)
    t = re.sub(r'(?<=[a-z])0(?=[a-z])','o',t)
    t = re.sub(r'(?<=[a-z])6(?=[a-z])','o',t)
    t = re.sub(r'(?<=[a-z])1(?=[a-z])','l',t)
    t = re.sub(r'[^a-z0-9\s]',' ',t)
    t = re.sub(r'\s+',' ',t)
    return t

