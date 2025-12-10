# CYN_Hiroba_OneClick.py - 终极一键版（点击按钮 → 自动打开网页 → 更新后自动生成 JSON）
import tkinter as tk
from tkinter import messagebox, filedialog
import webbrowser
import threading
import time
from pathlib import Path
import os


class HirobaOneClickSync:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("CYN 官方ひろば一键同步神器 v6.0")
        self.root.geometry("1000x700")
        self.root.configure(bg="#0d1117")
        self.root.resizable(False, False)
        try:
            self.root.iconbitmap("R.ico")
        except:
            pass

        self.setup_ui()
        self.root.mainloop()

    def setup_ui(self):
        tk.Label(self.root, text="CYN 官方ひろば一键同步神器", font=("微软雅黑", 30, "bold"),
                 fg="#ff3366", bg="#0d1117").pack(pady=50)
        tk.Label(self.root, text="点击按钮 → 自动打开ひろば → 你更新成绩 → 自动生成鼓众广场专用 JSON",
                 font=("微软雅黑", 14), fg="#58a6ff", bg="#0d1117").pack(pady=20)

        tk.Button(self.root, text="一键开始同步（自动打开网页）", width=40, height=3,
                  font=("微软雅黑", 18, "bold"), bg="#c9252d", fg="white",
                  command=self.start_sync).pack(pady=80)

        self.status = tk.Label(self.root, text="等待开始...", font=("微软雅黑", 12), fg="#8888ff", bg="#0d1117")
        self.status.pack(pady=20)

        self.log = tk.Text(self.root, font=("Consolas", 11), bg="#161b22", fg="#f0f6fc", height=12)
        self.log.pack(fill="both", expand=True, padx=100, pady=20)

    def log(self, msg):
        self.log.insert("end", f"[{datetime.now().strftime('%H:%M:%S')}] {msg}\n")
        self.log.see("end")

    def start_sync(self):
        self.log("正在打开 donderhiroba.jp ...")
        webbrowser.open("https://donderhiroba.jp/score_list.php")

        self.status.config(text="网页已打开！请登录 → 浏览成绩 → 点击右上角「更新」按钮")
        self.log("请在网页上：")
        self.log("   1. 登录你的 Bandai Namco ID")
        self.log("   2. 进入成绩页")
        self.log("   3. 点击右上角「更新」按钮")
        self.log("   4. 更新完成后，回来点击下方按钮")

        # 第二个按钮：用户手动确认已更新
        tk.Button(self.root, text="我已更新完成，生成 JSON！", width=40, height=2,
                  font=("微软雅黑", 16, "bold"), bg="#238636", fg="white",
                  command=self.generate_json).pack(pady=20)

    def generate_json(self):
        try:
            self.log("正在查找最新保存的网页文件...")
            downloads = str(Path.home() / "Downloads")
            files = [f for f in os.listdir(downloads) if "ドンだーひろば" in f or "score_list" in f]
            if not files:
                messagebox.showwarning("未找到", "请确认你已「另存为 → 网页，全部」保存到下载文件夹")
                return

            latest_file = max([os.path.join(downloads, f) for f in files], key=os.path.getctime)
            self.log(f"找到最新文件：{Path(latest_file).name}")

            # 用你的 FumenExtractor 解析（通用！）
            from FumenExtractor import FumenScoreExtractor
            scores = FumenScoreExtractor().extract(latest_file)

            save_path = filedialog.asksaveasfilename(
                title="保存为 scores.json",
                defaultextension=".json",
                initialfile="鼓众广场专用_hiroba成绩.json"
            )
            if not save_path: return

            Path(save_path).write_text(json.dumps(scores, ensure_ascii=False, indent=2), encoding="utf-8")

            full = sum(1 for s in scores if s[2] >= 1000000 and s[5] == 0 and s[6] == 0)
            self.log(f"成功生成 {len(scores)} 条成绩！其中 {full} 首满分")
            messagebox.showinfo("大成功！", f"完美生成 {len(scores)} 条成绩！\n快去鼓众广场同步吧！")

        except Exception as e:
            messagebox.showerror("错误", f"转换失败：{e}")


if __name__ == "__main__":
    HirobaOneClickSync()