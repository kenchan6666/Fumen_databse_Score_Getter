import json
import re
import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
from datetime import datetime
from bs4 import BeautifulSoup

class UltimateFumenExtractor:
    def __init__(self, root):
        self.root = root
        self.root.title("CYN 的铺面数据转换器")
        self.root.geometry("900x650")
        self.root.configure(bg="#0f0f1a")
        self.root.resizable(False, False)
        self.root.iconbitmap(default="R.ico")  # 可选：放一个.ico图标同目录

        # 居中
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - 450
        y = (self.root.winfo_screenheight() // 2) - 325
        self.root.geometry(f"900x650+{x}+{y}")

        self.html_path = tk.StringVar()
        self.scores_count = 0
        self.setup_ui()

    def setup_ui(self):
        # 标题区
        title_frame = tk.Frame(self.root, bg="#0f0f1a")
        title_frame.pack(pady=35)

        tk.Label(title_frame, text="CYN 的铺面数据Getter", font=("微软雅黑", 28, "bold"),
                 fg="#ff3366", bg="#0f0f1a").pack()
        tk.Label(title_frame, text="Made by CYN", font=("微软雅黑", 12),
                 fg="#8888ff", bg="#0f0f1a").pack(pady=(5, 0))

        # 副标题
        tk.Label(self.root, text="Save Score page as html from fumen-database",
                 font=("微软雅黑", 11), fg="#cccccc", bg="#0f0f1a").pack(pady=(0, 30))

        # 文件选择区（美化版）
        file_frame = tk.Frame(self.root, bg="#1a1a2e", relief="flat", bd=2)
        file_frame.pack(pady=20, padx=80, fill="x")

        tk.Label(file_frame, text="Choose your マイページ.html", font=("微软雅黑", 12),
                 fg="#00ffcc", bg="#1a1a2e").pack(anchor="w", padx=25, pady=(15, 5))

        path_frame = tk.Frame(file_frame, bg="#1a1a2e")
        path_frame.pack(fill="x", padx=25, pady=(0, 15))

        tk.Entry(path_frame, textvariable=self.html_path, font=("Consolas", 11), bg="#16213e",
                 fg="#00ffcc", relief="flat", state="readonly").pack(side="left", fill="x", expand=True)
        tk.Button(path_frame, text="浏览...", command=self.select_file,
                  bg="#ff3366", fg="white", font=("微软雅黑", 10, "bold"),
                  relief="flat", cursor="hand2").pack(side="right", padx=(10, 0))

        # 操作按钮（超炫渐变风）
        btn = tk.Button(self.root, text="Start",
                        font=("微软雅黑", 16, "bold"), bg="#ff3366", fg="white",
                        relief="flat", height=2, cursor="hand2",
                        command=self.start)
        btn.pack(pady=40, fill="x", padx=180)
        # 悬停特效
        btn.bind("<Enter>", lambda e: btn.config(bg="#ff5577"))
        btn.bind("<Leave>", lambda e: btn.config(bg="#ff3366"))

        # 状态显示区
        self.status = tk.Label(self.root, text="CYN IS WAITING...", font=("微软雅黑", 11),
                               fg="#8888ff", bg="#0f0f1a", height=2)
        self.status.pack(pady=10)

        # 结果统计（转换后显示）
        self.result_label = tk.Label(self.root, text="", font=("微软雅黑", 12, "bold"),
                                     fg="#00ffcc", bg="#0f0f1a")
        self.result_label.pack(pady=10)

        # 底部装饰
        tk.Label(self.root, text="© 2025 CYN | 专为鼓众广场打造", font=("微软雅黑", 9),
                 fg="#444466", bg="#0f0f1a").pack(side="bottom", pady=15)

    def select_file(self):
        path = filedialog.askopenfilename(
            title="选择マイページ.html",
            filetypes=[("HTML 文件", "*.html *.htm"), ("所有文件", "*.*")]
        )
        if path:
            self.html_path.set(path)
            self.status.config(text=f"已选择：{Path(path).name}", fg="#00ffcc")
            self.result_label.config(text="")

    def start(self):
        if not self.html_path.get():
            messagebox.showwarning("未选择", "请先选择 HTML 文件！")
            return

        try:
            scores = self.extract_scores(self.html_path.get())
            save_path = filedialog.asksaveasfilename(
                title="保存为 scores.json", defaultextension=".json",
                initialfile="scores.json"
            )
            if not save_path:
                return

            Path(save_path).write_text(json.dumps(scores, ensure_ascii=False, indent=2), encoding="utf-8")
            messagebox.showinfo("完成", f"共 {len(scores)} 条成绩\n已保存到：{Path(save_path).name}\n现在直接复制到计算器即可！")
            self.status.config(text="转换完成", fg="#1b5e20")

        except Exception as e:
            messagebox.showerror("错误", f"转换失败：{e}")

    def extract_scores(self, html_path):
        soup = BeautifulSoup(Path(html_path).read_text(encoding="utf-8"), "html.parser")
        rows = soup.select("div.table_grid.filter_selector")
        result = []

        for row in rows:
            try:
                a = row.find("a", href=re.compile(r"/song/\d+-\d+/"))
                if not a: continue

                href = a["href"]  # 例如：/song/1012-4/
                match = re.search(r"/song/(\d+)-(\d+)/", href)
                if not match:
                    continue
                fumen_id = int(match.group(1))
                difficulty = int(match.group(2))  # 4=表鬼，5=里鬼

                guo_id = fumen_id

                # 分数
                score_text = row.select_one(".table_totalscore").get_text(strip=True)
                high_score = int(re.sub(r"[^\d]", "", score_text))

                crown = row.find("img", src=re.compile(r"crown_"))
                rank = 4
                if crown:
                    src = crown["src"]
                    if any(x in src for x in ["gold", "donderfull", "rainbow"]): rank = 1
                    elif "silver" in src: rank = 2
                    elif "clear" in src: rank = 3
                # 数据
                good = int(row.select_one(".table_good").get_text(strip=True) or 0)
                ok = int(row.select_one(".table_ok").get_text(strip=True) or 0)
                bad = int(row.select_one(".table_bad").get_text(strip=True) or 0)
                combo = int(row.select_one(".table_combo").get_text(strip=True) or 0)

                full_combo = 1 if bad == 0 and ok == 0 else 0
                dondaful = 1 if full_combo and good == combo else 0

                level = 5 if difficulty == 5 else 4  # 4=おに, 5=裏

                result.append([
                    guo_id, level, high_score, rank,
                    good, ok, bad, good + ok + bad, combo,
                    1, 1, full_combo, dondaful,
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                ])

            except Exception as e:
                continue

        # 去重取最高分
        best = {}
        for r in result:
            key = (r[0], r[1])
            if key not in best or r[2] > best[key][2]:
                best[key] = r

        return sorted(best.values(), key=lambda x: (x[0], x[1]))

if __name__ == "__main__":
    root = tk.Tk()
    app = UltimateFumenExtractor(root)
    root.mainloop()