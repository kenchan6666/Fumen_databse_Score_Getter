# UI.py - 完全保留你原来的界面（一模一样！）
import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
from FumenExtractor import FumenScoreExtractor
from datetime import datetime
import json

class FumenExtractorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CYN 的铺面数据Getter")
        self.root.geometry("900x650")
        self.root.configure(bg="#0f0f1a")
        self.root.resizable(False, False)
        try:
            self.root.iconbitmap("assets/R.ico")
        except:
            pass

        # 居中
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - 450
        y = (self.root.winfo_screenheight() // 2) - 325
        self.root.geometry(f"900x650+{x}+{y}")

        self.html_path = tk.StringVar()
        self.scores_count = 0
        self.setup_ui()

    def setup_ui(self):
        # 标题区（你原来的）
        title_frame = tk.Frame(self.root, bg="#0f0f1a")
        title_frame.pack(pady=35)

        tk.Label(title_frame, text="CYN 的铺面数据Getter", font=("微软雅黑", 28, "bold"),
                 fg="#ff3366", bg="#0f0f1a").pack()
        tk.Label(title_frame, text="Made by CYN", font=("微软雅黑", 12),
                 fg="#8888ff", bg="#0f0f1a").pack(pady=(5, 0))

        # 副标题（你原来的）
        tk.Label(self.root, text="Save Score page as html from fumen-database",
                 font=("微软雅黑", 11), fg="#cccccc", bg="#0f0f1a").pack(pady=(0, 30))

        # 文件选择区（你原来的）
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

        # 开始按钮（你原来的）
        tk.Button(self.root, text="开始生成",
                  font=("微软雅黑", 14, "bold"), bg="#4CAF50", fg="white", height=2,
                  command=self.start).pack(pady=40, fill="x", padx=200)

        # 状态栏（你原来的）
        self.status = tk.Label(self.root, text="等待选择文件...", fg="#8888ff", bg="#0f0f1a", font=("微软雅黑", 11))
        self.status.pack(pady=10)

        # 结果显示（你原来的）
        self.result_label = tk.Label(self.root, text="", font=("微软雅黑", 12), fg="#00ffcc", bg="#0f0f1a")
        self.result_label.pack(pady=10)

    def select_file(self):
        path = filedialog.askopenfilename(
            title="选择保存的网页文件",
            filetypes=[("HTML 文件", "*.html *.htm")]
        )
        if path:
            self.html_path.set(path)
            self.status.config(text=f"已选择：{Path(path).name}", fg="#00ffcc")

    def start(self):
        if not self.html_path.get():
            messagebox.showwarning("未选择文件", "请先选择网页文件！")
            return

        try:
            extractor = FumenScoreExtractor()
            scores = extractor.extract(self.html_path.get())

            count = len(scores)
            full = sum(1 for s in scores if s[2] >= 1000000 and s[5] == 0 and s[6] == 0)

            save_path = filedialog.asksaveasfilename(
                title="保存为 scores.json",
                defaultextension=".json",
                initialfile="鼓众广场专用_scores.json"
            )
            if not save_path:
                return

            Path(save_path).write_text(json.dumps(scores, ensure_ascii=False, indent=2), encoding="utf-8")

            self.status.config(text="转换完成！", fg="#3fb950")
            self.result_label.config(text=f"成功生成 {count} 条成绩！\n其中 {full} 首满分/Infinity")
            messagebox.showinfo("大成功！", f"完美生成 {count} 条成绩！\n其中 {full} 首满分\n快去鼓众广场同步吧！")

        except Exception as e:
            messagebox.showerror("错误", f"转换失败：{str(e)}")
            self.status.config(text="转换失败", fg="#ff3366")