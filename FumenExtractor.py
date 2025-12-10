# FumenExtractor.py - fumen-database 解析器
from bs4 import BeautifulSoup
from pathlib import Path
from datetime import datetime
import re

class FumenScoreExtractor:
    def extract(self, html_path):
        soup = BeautifulSoup(Path(html_path).read_text(encoding="utf-8"), "html.parser")
        rows = soup.select("div.table_grid.filter_selector")
        result = []

        for row in rows:
            try:
                a = row.find("a", href=re.compile(r"/song/\d+-\d+/"))
                if not a: continue
                href = a["href"]
                match = re.search(r"/song/(\d+)-(\d+)/", href)
                if not match: continue
                guo_id = int(match.group(1))
                difficulty = int(match.group(2))
                if difficulty not in [4, 5]: continue

                score_text = row.select_one(".table_totalscore").get_text(strip=True)
                high_score = int(re.sub(r"[^\d]", "", score_text))

                crown = row.find("img", src=re.compile(r"crown_"))
                rank = 4
                if crown:
                    src = crown["src"]
                    if any(x in src for x in ["gold", "donderfull", "rainbow"]): rank = 1
                    elif "silver" in src: rank = 2
                    elif "clear" in src: rank = 3

                good = int(row.select_one(".table_good").get_text(strip=True) or 0)
                ok = int(row.select_one(".table_ok").get_text(strip=True) or 0)
                bad = int(row.select_one(".table_bad").get_text(strip=True) or 0)
                combo = int(row.select_one(".table_combo").get_text(strip=True) or 0)

                full_combo = 1 if bad == 0 and ok == 0 else 0
                dondaful = 1 if full_combo and good == combo else 0

                level = 5 if difficulty == 5 else 4

                result.append([
                    guo_id, level, high_score, rank,
                    good, ok, bad, good + ok + bad, combo,
                    1, 1, full_combo, dondaful,
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                ])
            except:
                continue

        # 去重取最高分
        best = {}
        for r in result:
            key = (r[0], r[1])
            if key not in best or r[2] > best[key][2]:
                best[key] = r

        return sorted(best.values(), key=lambda x: (x[0], x[1]))