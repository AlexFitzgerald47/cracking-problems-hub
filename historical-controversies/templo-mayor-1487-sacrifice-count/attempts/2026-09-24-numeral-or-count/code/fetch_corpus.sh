set -u
d() { # id  filename  outname
  out="raw/$3"
  if [ -s "$out" ]; then echo "skip $3"; return; fi
  url="https://archive.org/download/$1/$(python3 -c "import urllib.parse,sys;print(urllib.parse.quote(sys.argv[1]))" "$2")"
  curl -sSL --max-time 300 -o "$out" "$url" && echo "ok   $3 $(wc -c <"$out")" || echo "FAIL $3"
}
d historiadelasind01dur "historiadelasind01dur_djvu.txt" duran_v1_scanA.txt
d historiadelasind02dur "historiadelasind02dur_djvu.txt" duran_v2_scanA.txt
d historia-de-las-indias-de-nueva-espana-tomo-i-diego-duran "Historia de las Indias de Nueva-España Tomo I - Diego Durán_djvu.txt" duran_v1_scanB.txt
d historia-de-las-indias-de-nueva-espana-tomo-ii "Historia De Las Indias De Nueva España Tomo II_djvu.txt" duran_v2_scanB.txt
d obrashistricasd01ixtlgoog "obrashistricasd01ixtlgoog_djvu.txt" ixtl_A1.txt
d obrashistricasd02ixtlgoog "obrashistricasd02ixtlgoog_djvu.txt" ixtl_A2.txt
d obrashistricasd03ixtlgoog "obrashistricasd03ixtlgoog_djvu.txt" ixtl_A3.txt
d obrashistricasd00ixtlgoog "obrashistricasd00ixtlgoog_djvu.txt" ixtl_B0.txt
d obrashistricasd00chavgoog "obrashistricasd00chavgoog_djvu.txt" ixtl_C0.txt
d obrashistricasd01chavgoog "obrashistricasd01chavgoog_djvu.txt" ixtl_C1.txt
d "mendieta-jeronimo-de.-historia-eclesiastica-indiana-2008" "Mendieta, Jerónimo de. - Historia Eclesiástica Indiana [2008]_djvu.txt" mendieta_scanA.txt
d cronicamexicana00alvaiala "cronicamexicana00alvaiala_djvu.txt" tezozomoc_scanA.txt
d "hernando-de-alvarado-tezozomoc.-cronica-mexicana-ocr-1997" "Hernando de Alvarado Tezozómoc. - Crónica Mexicana [ocr] [1997]_djvu.txt" tezozomoc_scanB.txt
d monarquia-indiana.-vol-i_202109 "Monarquia Indiana. Vol I_djvu.txt" torquemada_v1.txt
d monarquia-indiana.-vol-i_202109 "Monarquia Indiana. Vol II_djvu.txt" torquemada_v2.txt
# --- second batch (researcher-gathered, all verified by hand before use) ---
d "fray-toribio-de-benavente-motolinia.-historia-de-los-indios-de-la-nueva-espana-ocr-1988" "Fray Toribio de Benavente (Motolinía). - Historia de los indios de la Nueva España [ocr] [1988]_djvu.txt" motolinia_historia.txt
d memorialesdefra00sngoog "memorialesdefra00sngoog_djvu.txt" motolinia_memoriales.txt
d "acosta-jose-de.-historia-natural-y-moral-de-las-indias-ocr-1986" "Acosta, José de. - Historia natural y moral de las Indias [ocr] [1986]_djvu.txt" acosta.txt
d historiaeclesis00mendgoog "historiaeclesis00mendgoog_djvu.txt" mendieta_icazbalceta1870.txt
d "de-alva-ixtlilxochitl-fernando.-historia-de-la-nacion-chichimeca-ocr-1985" "De Alva Ixtlilxochitl, Fernando. - Historia de la nacion Chichimeca [ocr] [1985]_djvu.txt" ixtl_chichimeca_standalone.txt
