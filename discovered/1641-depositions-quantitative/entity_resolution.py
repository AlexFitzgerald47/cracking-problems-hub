"""
Entity Resolution and Evidential Classification Pipeline for 1641 Depositions.
Processes deposition JSON records, extracts incident claims, classifies evidential removes,
computes pairwise entity similarity, clusters matching events, and outputs deduplicated metrics.
"""
import json
import math
import os
import re
import sys
from collections import defaultdict


SAMPLE_FILE = os.path.join(os.path.dirname(__file__), "sample_data.json")
RESULTS_FILE = os.path.join(os.path.dirname(__file__), "sample_results.json")

# --- Phonetic & String Similarity Helpers ---

def jaro_winkler(s1, s2):
    s1, s2 = s1.lower().strip(), s2.lower().strip()
    if s1 == s2:
        return 1.0
    len1, len2 = len(s1), len(s2)
    if len1 == 0 or len2 == 0:
        return 0.0

    match_bound = max(len1, len2) // 2 - 1
    s1_matches = [False] * len1
    s2_matches = [False] * len2

    matches = 0
    transpositions = 0

    for i in range(len1):
        start = max(0, i - match_bound)
        end = min(i + match_bound + 1, len2)
        for j in range(start, end):
            if s2_matches[j]:
                continue
            if s1[i] == s2[j]:
                s1_matches[i] = True
                s2_matches[j] = True
                matches += 1
                break

    if matches == 0:
        return 0.0

    k = 0
    for i in range(len1):
        if not s1_matches[i]:
            continue
        while not s2_matches[k]:
            k += 1
        if s1[i] != s2[k]:
            transpositions += 1
        k += 1

    m = float(matches)
    jaro = (m / len1 + m / len2 + (m - transpositions / 2.0) / m) / 3.0

    # Winkler prefix scale
    prefix = 0
    for i in range(min(4, len1, len2)):
        if s1[i] == s2[i]:
            prefix += 1
        else:
            break

    return jaro + prefix * 0.1 * (1.0 - jaro)

# Simple English/Irish Soundex for 17th-century names
def soundex(name):
    name = re.sub(r'[^A-Za-z]', '', name.upper())
    if not name:
        return "Z000"
    first = name[0]
    char_map = {
        'B': '1', 'F': '1', 'P': '1', 'V': '1',
        'C': '2', 'G': '2', 'J': '2', 'K': '2', 'Q': '2', 'S': '2', 'X': '2', 'Z': '2',
        'D': '3', 'T': '3',
        'L': '4',
        'M': '5', 'N': '5',
        'R': '6'
    }
    res = [first]
    prev = char_map.get(first, '0')
    for ch in name[1:]:
        code = char_map.get(ch, '0')
        if code != '0' and code != prev:
            res.append(code)
            prev = code
        elif code == '0':
            prev = '0'
        if len(res) == 4:
            break
    while len(res) < 4:
        res.append('0')
    return "".join(res)

# --- NLP & Feature Extractors ---

EVIDENTIAL_TIER_1_PATTERNS = [
    r'\bsaw\b', r'\bwas present\b', r'\bbeing present\b', r'\bin (the|his|her) sight\b',
    r'\beyewitness\b', r'\bwith (his|her|their) own eyes\b', r'\bwitnessed\b'
]

EVIDENTIAL_TIER_2_PATTERNS = [
    r'\bcredibly informed\b', r'\btold by\b', r'\bheard from\b', r'\bwas told\b',
    r'\breported unto\b', r'\binformed this deponent\b'
]

EVIDENTIAL_TIER_3_PATTERNS = [
    r'\bcommonly reported\b', r'\bpublic fame\b', r'\bheard it said\b', r'\bcommonly said\b',
    r'\brumored\b', r'\bspoken abroad\b'
]

ACTION_KILL_PATTERNS = [
    r'murdered', r'killed', r'drowned', r'hanged', r'shot', r'slain', r'stripped and killed',
    r'cut the throats', r'put to death', r'perished'
]

PLACES_LIST = [
    "portadown", "belturbet", "kilmore", "armagh", "lurgan", "shrule", "clones", "monaghan",
    "cavan", "lough gall", "charlemont", "newry", "eniskillen", "dundalk", "dromore", "cashel"
]

def classify_evidential_tier(text):
    text_lower = text.lower()
    for pat in EVIDENTIAL_TIER_1_PATTERNS:
        if re.search(pat, text_lower):
            return 1, "Tier 1: Direct Eyewitness"
    for pat in EVIDENTIAL_TIER_2_PATTERNS:
        if re.search(pat, text_lower):
            return 2, "Tier 2: Direct Hearsay"
    for pat in EVIDENTIAL_TIER_3_PATTERNS:
        if re.search(pat, text_lower):
            return 3, "Tier 3: General Rumor"
    return 2, "Tier 2: Direct Hearsay (Default)"

def extract_claims(deposition):
    text = deposition.get("text", "")
    dep_id = deposition.get("id", "")
    deponent = deposition.get("metadata", {}).get("Deponent", "Unknown Deponent")

    claims = []
    # Split text into sentences/paragraphs
    sentences = re.split(r'\.\s+', text)

    for idx, stmt in enumerate(sentences):
        stmt_lower = stmt.lower()

        # Check if sentence mentions killing/death action
        action_found = False
        for act in ACTION_KILL_PATTERNS:
            if act in stmt_lower:
                action_found = True
                break

        if not action_found:
            continue

        # Extract number of casualties
        count = 1
        num_match = re.search(r'\b(one|two|three|four|five|six|seven|eight|nine|ten|twelve|twenty|thirty|forty|fifty|hundred|1|2|3|4|5|6|7|8|9|10|12|20|30|40|50|100)\b', stmt_lower)
        if num_match:
            word = num_match.group(1)
            word_to_num = {
                "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
                "twelve": 12, "twenty": 20, "thirty": 30, "forty": 40, "fifty": 50, "hundred": 100,
                "1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "12": 12, "20": 20, "30": 30, "40": 40, "50": 50, "100": 100
            }
            count = word_to_num.get(word, 1)

        # Extract place
        extracted_place = "Unknown"
        for pl in PLACES_LIST:
            if pl in stmt_lower:
                extracted_place = pl.capitalize()
                break

        # Extract potential victim names (Capitalized words near killing terms)
        names = re.findall(r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\b', stmt)
        # Filter out common non-name words
        ignore_words = {"The", "And", "This", "Deponent", "Rebels", "Irish", "Protestant", "October", "November", "Michaelmas"}
        victim_names = [n for n in names if n not in ignore_words and len(n) > 3]

        tier_num, tier_label = classify_evidential_tier(stmt)

        claims.append({
            "claim_id": f"{dep_id}_c{idx}",
            "dep_id": dep_id,
            "deponent": deponent,
            "tier": tier_num,
            "tier_label": tier_label,
            "count": count,
            "place": extracted_place,
            "victims": victim_names[:2],
            "snippet": stmt[:150]
        })

    return claims

# --- Entity Matching & Graph Clustering ---

def compute_similarity(c1, c2):
    # 1. Spatial Similarity
    p1, p2 = c1["place"], c2["place"]
    if p1 != "Unknown" and p2 != "Unknown":
        s_space = 1.0 if p1.lower() == p2.lower() else jaro_winkler(p1, p2)
    else:
        s_space = 0.5  # Neutral default

    # 2. Victim Name Similarity
    v1_list, v2_list = c1["victims"], c2["victims"]
    s_victim = 0.0
    if v1_list and v2_list:
        max_sim = 0.0
        for v1 in v1_list:
            for v2 in v2_list:
                sim = jaro_winkler(v1, v2)
                if soundex(v1) == soundex(v2):
                    sim = max(sim, 0.90)
                if sim > max_sim:
                    max_sim = sim
        s_victim = max_sim
    else:
        s_victim = 0.4

    # Composite Score
    composite = 0.50 * s_space + 0.50 * s_victim
    return composite

def cluster_claims(claims, threshold=0.70):
    n = len(claims)
    adj = defaultdict(list)

    # Build graph edges
    for i in range(n):
        for j in range(i + 1, n):
            # Only compare claims from DIFFERENT depositions
            if claims[i]["dep_id"] == claims[j]["dep_id"]:
                continue
            sim = compute_similarity(claims[i], claims[j])
            if sim >= threshold:
                adj[i].append(j)
                adj[j].append(i)

    # Connected Components Clustering
    visited = [False] * n
    clusters = []

    for i in range(n):
        if not visited[i]:
            cluster = []
            queue = [i]
            visited[i] = True
            while queue:
                curr = queue.pop(0)
                cluster.append(claims[curr])
                for neighbor in adj[curr]:
                    if not visited[neighbor]:
                        visited[neighbor] = True
                        queue.append(neighbor)
            clusters.append(cluster)

    return clusters

# --- Benchmark Pipeline Execution ---

def run_pipeline():
    if len(sys.argv) > 1:
        if sys.argv[1] in {"-h", "--help"}:
            print(f"Usage: {os.path.basename(__file__)} [depositions.json]")
            return None
        target_file = sys.argv[1]
        explicit_target = True
    else:
        all_file = os.path.join(os.path.dirname(__file__), "all_depositions.json")
        if os.path.exists(all_file):
            target_file = all_file
        else:
            target_file = SAMPLE_FILE
        explicit_target = False


    if not os.path.exists(target_file):
        if explicit_target:
            raise SystemExit(f"Input data file not found: {target_file}")
        print(f"Sample data file {target_file} not found. Creating synthetic benchmark sample...")
        # Create a realistic benchmark sample representing 10 depositions reporting overlap at Portadown and Belturbet
        synthetic_depositions = [
            {
                "id": "836001",
                "metadata": {"Deponent": "William Sesford", "County": "Armagh"},
                "text": "William Sesford of Portadown in the County of Armagh deposeth that he saw with his own eyes eighty Protestants murdered and thrown off the bridge at Portadown by the rebels under Captain Toole O'Nial in November 1641."
            },
            {
                "id": "836002",
                "metadata": {"Deponent": "Elizabeth Price", "County": "Armagh"},
                "text": "Elizabeth Price deposeth that she was credibly informed that eighty-five Protestants, including John Smith and William Taylor, were drowned at Portadown bridge about Michaelmas 1641."
            },
            {
                "id": "836003",
                "metadata": {"Deponent": "John Wright", "County": "Armagh"},
                "text": "John Wright of Armagh saw one hundred Protestants forced into the river at Portadown bridge by the rebel forces of Felim O'Nial."
            },
            {
                "id": "812002",
                "metadata": {"Deponent": "George Creichton", "County": "Cavan"},
                "text": "George Creichton minister of Belturbet deposeth that thirty Protestants were killed at Belturbet bridge by Philip MacHugh O'Reilly."
            },
            {
                "id": "812003",
                "metadata": {"Deponent": "Thomas Walsh", "County": "Cavan"},
                "text": "Thomas Walsh deposeth he was told by rebels that thirty-five persons were put to death at Belturbet bridge."
            },
            {
                "id": "836004",
                "metadata": {"Deponent": "Anne Read", "County": "Armagh"},
                "text": "Anne Read saw John Smith murdered at Lurgan by rebels in October 1641."
            },
            {
                "id": "836005",
                "metadata": {"Deponent": "Robert Maxwell", "County": "Armagh"},
                "text": "Robert Maxwell deposeth that it was commonly reported that multitudes amounting to thousands were drowned in the rivers of Ulster."
            }
        ]
        with open(target_file, "w", encoding="utf-8") as f:
            json.dump(synthetic_depositions, f, indent=2)

    with open(target_file, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    if isinstance(raw_data, dict):
        depositions = list(raw_data.values())
    else:
        depositions = raw_data

    print(f"Processing {len(depositions)} depositions from {target_file}...")
    all_claims = []
    for dep in depositions:
        claims = extract_claims(dep)
        all_claims.extend(claims)


    print(f"Extracted {len(all_claims)} incident claims.")

    # Calculate Naive Aggregation Sum
    naive_total_deaths = sum(c["count"] for c in all_claims)

    # Classify by Evidential Removal
    tier1_claims = [c for c in all_claims if c["tier"] == 1]
    tier2_claims = [c for c in all_claims if c["tier"] == 2]
    tier3_claims = [c for c in all_claims if c["tier"] == 3]

    tier1_naive_sum = sum(c["count"] for c in tier1_claims)
    tier2_naive_sum = sum(c["count"] for c in tier2_claims)
    tier3_naive_sum = sum(c["count"] for c in tier3_claims)

    # Perform Entity Resolution Clustering
    clusters = cluster_claims(all_claims, threshold=0.70)

    deduplicated_total_deaths = 0
    cluster_summaries = []

    for idx, cl in enumerate(clusters):
        max_deaths_in_cluster = max(c["count"] for c in cl)
        deduplicated_total_deaths += max_deaths_in_cluster
        places = sorted(set(c["place"] for c in cl if c["place"] != "Unknown"))
        deponents = [c["deponent"] for c in cl]
        tiers = [c["tier_label"] for c in cl]

        cluster_summaries.append({
            "cluster_id": f"Cluster_{idx+1}",
            "num_claims": len(cl),
            "places": places,
            "deponents": deponents,
            "tiers": tiers,
            "naive_sum": sum(c["count"] for c in cl),
            "deduplicated_count": max_deaths_in_cluster,
            "claims": cl
        })

    inflation_ratio = (naive_total_deaths / deduplicated_total_deaths) if deduplicated_total_deaths > 0 else 1.0

    results = {
        "num_depositions_processed": len(depositions),
        "num_claims_extracted": len(all_claims),
        "naive_total_deaths": naive_total_deaths,
        "deduplicated_total_deaths": deduplicated_total_deaths,
        "inflation_ratio": round(inflation_ratio, 2),
        "evidential_vector": {
            "tier1_eyewitness_claims": len(tier1_claims),
            "tier1_eyewitness_naive_deaths": tier1_naive_sum,
            "tier2_hearsay_claims": len(tier2_claims),
            "tier2_hearsay_naive_deaths": tier2_naive_sum,
            "tier3_rumor_claims": len(tier3_claims),
            "tier3_rumor_naive_deaths": tier3_naive_sum,
        },
        "clusters": cluster_summaries
    }

    with open(RESULTS_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print("\n================ PIPELINE BENCHMARK RESULTS ================")
    print(f"Depositions Processed: {len(depositions)}")
    print(f"Extracted Incident Claims: {len(all_claims)}")
    print(f"Naive Aggregated Deaths: {naive_total_deaths}")
    print(f"Deduplicated Cluster Deaths: {deduplicated_total_deaths}")
    print(f"Double-Counting Inflation Ratio: {inflation_ratio:.2f}x")
    print(f"Evidential Vector (Eyewitness vs Hearsay): Tier 1 Eyewitness={tier1_naive_sum}, Tier 2 Hearsay={tier2_naive_sum}, Tier 3 Rumor={tier3_naive_sum}")
    print("===========================================================")

    return results

if __name__ == "__main__":
    run_pipeline()
