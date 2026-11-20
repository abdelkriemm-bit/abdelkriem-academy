"""Parse a topic-practice DSL file (see american/PRACTICE_PLAN.md) into practice sets.

Returns {"stem": str, "sets": [{"title", "level", "questions": [engine question dicts with "ce"]}]}
Choices are re-ordered deterministically so the keys are spread evenly over A-D inside every set,
except when a choice is "NO CHANGE" (kept as A) or the question is marked [fixed].
"""
import re, random

LEVELS = {"foundation": "Foundation", "exam": "Exam level", "exam level": "Exam level", "challenge": "Challenge"}


def parse(text, slug=""):
    stem = ""
    sets = []
    cur = None
    skill = ""
    q = None
    last_p = ""
    mode = None  # "p" while reading passage lines

    def finish():
        nonlocal q, last_p
        if q is None:
            return
        if not q["c"]:
            raise ValueError(f"{slug}: question without choices in {cur['title']}: {q.get('p','')[:60]}")
        if len(q["c"]) != 4:
            raise ValueError(f"{slug}: {cur['title']} q{len(cur['questions'])+1} has {len(q['c'])} choices")
        keys = [i for i, k in enumerate(q["k"]) if k]
        if len(keys) != 1:
            raise ValueError(f"{slug}: {cur['title']} q{len(cur['questions'])+1} needs exactly one * key ({keys})")
        p = q["p"].strip("\n")
        if p == "@":
            p = last_p
        last_p = p
        # "…cliffs ______ its…" with choices "cliffs," / "cliffs;" → drop the word repeated before the blank
        m = re.search(r"(\S+) ______", p)
        if m and p.count("______") == 1:
            w = re.sub(r"[^\w'-]+$", "", m.group(1))
            if w and all(re.match(re.escape(w) + r"(?![\w'-])", c) for c in q["c"]):
                p = p[:m.start(1)] + p[m.start(1) + len(w):].lstrip(" ") if m.group(1) == w else p
        item = {"q": q["q"] or stem, "c": q["c"], "a": keys[0], "ce": q["ce"],
                "e": q["ce"][keys[0]], "s": q["s"] or skill or "Practice"}
        if p:
            item["p"] = p
        if q.get("fixed"):
            item["fixed"] = True
        if not item["q"]:
            raise ValueError(f"{slug}: missing question stem")
        cur["questions"].append(item)
        q = None

    for raw in text.splitlines():
        line = raw.rstrip()
        s = line.strip()
        if s.startswith("STEM:"):
            stem = s[5:].strip(); continue
        if s.startswith("## "):
            finish()
            parts = [x.strip() for x in s[3:].split("|")]
            lvl = LEVELS.get(parts[1].lower(), parts[1]) if len(parts) > 1 else ""
            cur = {"title": parts[0], "level": lvl, "questions": []}
            sets.append(cur); mode = None; continue
        if s.startswith("### "):
            finish(); skill = s[4:].strip(); mode = None; continue
        if not s:
            if q is not None and q["c"]:
                finish()
            mode = None if q is None else mode
            if q is not None and mode == "p":
                q["p"] += "\n"
            continue
        if s.startswith("P:"):
            finish()
            q = {"p": s[2:].strip(), "q": "", "c": [], "ce": [], "k": [], "s": ""}
            mode = "p"; continue
        if s.startswith("Q:"):
            if q is None:
                q = {"p": "", "q": "", "c": [], "ce": [], "k": [], "s": ""}
            txt = s[2:].strip()
            if "[fixed]" in txt:
                q["fixed"] = True; txt = txt.replace("[fixed]", "").strip()
            q["q"] = txt; mode = "q"; continue
        m = re.match(r"^(\*?)([A-D])\)\s*(.*)$", s)
        if m and q is not None:
            body = m.group(3)
            if "||" not in body:
                raise ValueError(f"{slug}: choice without '||' reason: {s[:80]}")
            ch, why = [x.strip() for x in body.split("||", 1)]
            q["c"].append(ch); q["ce"].append(why); q["k"].append(bool(m.group(1)))
            mode = "c"; continue
        if q is not None and mode == "p":
            q["p"] += ("\n" if q["p"] else "") + s; continue
        if q is not None and mode == "q":
            q["q"] += " " + s; continue
        if q is not None and mode == "c" and q["ce"]:
            q["ce"][-1] += " " + s; continue
        raise ValueError(f"{slug}: cannot parse line: {s[:100]}")
    finish()
    for st in sets:
        balance(st["questions"], seed=f"{slug}|{st['title']}")
    return {"stem": stem, "sets": sets}


def _move(item, perm):
    item["c"] = [item["c"][i] for i in perm]
    item["ce"] = [item["ce"][i] for i in perm]
    item["a"] = perm.index(item["a"])


def balance(qs, seed=""):
    rnd = random.Random(seed)
    n = len(qs)
    target = [n // 4 + (1 if i < n % 4 else 0) for i in range(4)]
    rnd.shuffle(target)
    count = [0, 0, 0, 0]
    free = []
    for it in qs:
        if it.get("fixed") or it["c"][0].strip().upper().startswith("NO CHANGE"):
            if it["c"][0].strip().upper().startswith("NO CHANGE") and not it.get("fixed"):
                # keep NO CHANGE first, shuffle the other three
                free.append(("nc", it))
            else:
                count[it["a"]] += 1
        else:
            free.append(("all", it))
    rnd.shuffle(free)
    for kind, it in free:
        opts = [1, 2, 3] if kind == "nc" else [0, 1, 2, 3]
        if kind == "nc" and it["a"] == 0:
            pos = 0
        else:
            need = sorted(opts, key=lambda p: (count[p] - target[p], rnd.random()))
            pos = need[0]
        if kind == "nc":
            rest = [i for i in range(1, 4)]
            others = [i for i in rest if i != it["a"]]
            rnd.shuffle(others)
            if it["a"] == 0:
                perm = [0] + others
            else:
                slots = [1, 2, 3]
                perm = [0, None, None, None]
                perm[pos] = it["a"]
                for sl in slots:
                    if perm[sl] is None:
                        perm[sl] = others.pop()
        else:
            others = [i for i in range(4) if i != it["a"]]
            rnd.shuffle(others)
            perm = [None] * 4
            perm[pos] = it["a"]
            for sl in range(4):
                if perm[sl] is None:
                    perm[sl] = others.pop()
        _move(it, perm)
        count[pos] += 1
    for it in qs:
        it.pop("fixed", None)
