import random
import tkinter as tk
from tkinter import messagebox, font, simpledialog

# 游戏参数设置
INITIAL_BALANCE = 1000  # 初始资金
WIN_PROB = 0.1  # 获胜概率（三个图标一致的概率）
ODDS = 5  # 获胜赔率（三个图标一致时获得下注金额的倍数）
SPIN_DELAY = 100  # 轮盘转动动画的延迟时间（毫秒）

# 颜色配置
BG_COLOR = "#2E3440"  # 背景色
TEXT_COLOR = "#D8DEE9"  # 文字颜色
BUTTON_COLOR = "#5E81AC"  # 按钮颜色
WIN_COLOR = "#A3BE8C"  # 获胜颜色
LOSE_COLOR = "#BF616A"  # 亏损颜色

# 老虎机图标
SYMBOLS = ["🍒", "🍋", "🍊", "🍇", "🔔", "⭐", "🥑"]

class GamblingGameUI:
    def __init__(self, root):
        self.root = root
        self.root.title("赌狗游戏")
        self.root.geometry("800x900")  # 增加窗口宽度以容纳曲线图
        self.root.configure(bg=BG_COLOR)

        # 初始化余额
        self.balance = INITIAL_BALANCE
        self.is_spinning = False  # 是否正在转动
        self.current_bet = 0  # 当前下注金额
        self.balance_history = [INITIAL_BALANCE]  # 资金历史记录
        self.is_auto_gambling = False  # 是否正在自动赌博
        self.auto_times = 0  # 自动赌博次数
        self.auto_count = 0  # 当前自动赌博次数
        self.initial_balance = INITIAL_BALANCE  # 自动赌博初始余额

        # 设置字体
        self.title_font = font.Font(family="Helvetica", size=20, weight="bold")
        self.balance_font = font.Font(family="Helvetica", size=16)
        self.symbol_font = font.Font(family="Helvetica", size=50)

        # 创建 UI 组件
        self.create_widgets()

        # 创建资金曲线图
        self.create_balance_chart()

    def create_widgets(self):
        """创建 UI 组件"""
        # 标题
        self.title_label = tk.Label(
            self.root,
            text="🎰 赌狗游戏 🎰",
            font=self.title_font,
            bg=BG_COLOR,
            fg=TEXT_COLOR,
        )
        self.title_label.pack(pady=20)

        # 余额显示
        self.balance_label = tk.Label(
            self.root,
            text=f"💰 当前余额: {self.balance:.2f} 元",
            font=self.balance_font,
            bg=BG_COLOR,
            fg=TEXT_COLOR,
        )
        self.balance_label.pack(pady=10)

        # 老虎机轮盘
        self.slot_frame = tk.Frame(self.root, bg=BG_COLOR)
        self.slot_frame.pack(pady=20)

        self.slot_labels = []
        for i in range(3):  # 三个轮盘
            label = tk.Label(
                self.slot_frame,
                text="🎰",
                font=self.symbol_font,
                bg=BG_COLOR,
                fg=TEXT_COLOR,
            )
            label.pack(side="left", padx=10)
            self.slot_labels.append(label)

        # 下注输入框
        self.bet_entry = tk.Entry(
            self.root, font=self.balance_font, justify="center", width=20
        )
        self.bet_entry.pack(pady=10)

        # 下注按钮
        self.bet_button = tk.Button(
            self.root,
            text="🎲 开始赌博",
            font=self.balance_font,
            bg=BUTTON_COLOR,
            fg=TEXT_COLOR,
            command=self.start_spin,
        )
        self.bet_button.pack(pady=10)

        # 自动赌博按钮
        self.auto_bet_button = tk.Button(
            self.root,
            text="⚡ 自动赌博",
            font=self.balance_font,
            bg=BUTTON_COLOR,
            fg=TEXT_COLOR,
            command=self.auto_gamble,
        )
        self.auto_bet_button.pack(pady=10)

        # 停止自动赌博按钮
        self.stop_auto_bet_button = tk.Button(
            self.root,
            text="🛑 停止自动赌博",
            font=self.balance_font,
            bg=BUTTON_COLOR,
            fg=TEXT_COLOR,
            command=self.stop_auto_gamble,
            state="disabled",  # 初始状态为禁用
        )
        self.stop_auto_bet_button.pack(pady=10)

        # 结果显示
        self.result_label = tk.Label(
            self.root, text="", font=self.balance_font, bg=BG_COLOR, fg=TEXT_COLOR
        )
        self.result_label.pack(pady=20)

        # 退出按钮
        self.quit_button = tk.Button(
            self.root,
            text="🚪 拿钱跑路",
            font=self.balance_font,
            bg=BUTTON_COLOR,
            fg=TEXT_COLOR,
            command=self.quit_game,
        )
        self.quit_button.pack(pady=10)

    def create_balance_chart(self):
        """创建资金曲线图"""
        self.chart_frame = tk.Frame(self.root, bg=BG_COLOR)
        self.chart_frame.pack(pady=20)

        self.chart_canvas = tk.Canvas(self.chart_frame, width=600, height=200, bg=BG_COLOR)
        self.chart_canvas.pack()

        self.chart_x = 50
        self.chart_y = 150
        self.chart_width = 500
        self.chart_height = 100
        self.chart_canvas.create_rectangle(self.chart_x, self.chart_y - self.chart_height, self.chart_x + self.chart_width, self.chart_y, outline=TEXT_COLOR)

        self.chart_points = []
        self.update_balance_chart()

    def update_balance_chart(self):
        """更新资金曲线图"""
        if self.chart_canvas:
            self.chart_canvas.delete("line")  # 删除旧的线条
            self.chart_canvas.delete("point")  # 删除旧的点

            max_balance = max(self.balance_history)
            min_balance = min(self.balance_history)
            range_balance = max_balance - min_balance

            if range_balance == 0:
                range_balance = 1  # 防止除以零

            self.chart_points = []
            for i, balance in enumerate(self.balance_history):
                if len(self.balance_history) == 1:
                    x = self.chart_x
                else:
                    x = self.chart_x + (i / (len(self.balance_history) - 1)) * self.chart_width
                y = self.chart_y - ((balance - min_balance) / range_balance) * self.chart_height
                self.chart_points.append((x, y))
                self.chart_canvas.create_oval(x - 2, y - 2, x + 2, y + 2, fill=TEXT_COLOR, tags="point")

            if len(self.chart_points) > 1:
                self.chart_canvas.create_line(self.chart_points, fill=TEXT_COLOR, tags="line")

    def start_spin(self):
        """开始转动轮盘"""
        if self.is_spinning:
            return

        try:
            self.current_bet = float(self.bet_entry.get())  # 获取下注金额
            if self.current_bet <= 0 or self.current_bet > self.balance:
                messagebox.showwarning("⚠️ 错误", "无效的下注金额！")
                return

            # 扣除下注金额
            self.balance -= self.current_bet
            self.balance_history.append(self.balance)  # 记录资金变化
            self.balance_label.config(text=f"💰 当前余额: {self.balance:.2f} 元")

            # 开始转动动画
            self.is_spinning = True
            self.bet_button.config(state="disabled")
            self.spin_count = 0
            self.animate_spin()

        except ValueError:
            messagebox.showwarning("⚠️ 错误", "请输入有效数字！")

    def animate_spin(self):
        """轮盘转动动画"""
        if self.spin_count < 20:  # 转动 20 次
            for label in self.slot_labels:
                label.config(text=random.choice(SYMBOLS))
            self.spin_count += 1
            self.root.after(SPIN_DELAY, self.animate_spin)
        else:
            # 根据概率决定是否获胜
            if random.random() < WIN_PROB:
                # 获胜情况：三个图标一致
                winning_symbol = random.choice(SYMBOLS)
                self.final_symbols = [winning_symbol] * 3
            else:
                # 未获胜情况：随机生成三个不同的图标
                self.final_symbols = random.choices(SYMBOLS, k=3)

            # 显示最终结果
            for i, label in enumerate(self.slot_labels):
                label.config(text=self.final_symbols[i])

            # 检查是否获胜
            if len(set(self.final_symbols)) == 1:  # 三个图标一致
                win_amount = self.current_bet * ODDS
                self.balance += win_amount
                self.balance_history.append(self.balance)  # 记录资金变化
                self.result_label.config(text=f"🎉 获胜 +{win_amount:.2f} 元", fg=WIN_COLOR)
            else:
                self.result_label.config(text=f"💸 亏损 -{self.current_bet:.2f} 元", fg=LOSE_COLOR)

            # 更新余额显示
            self.balance_label.config(text=f"💰 当前余额: {self.balance:.2f} 元")

            # 更新资金曲线图
            self.update_balance_chart()

            # 检查是否输光
            if self.balance <= 0:
                self.game_over()
            else:
                # 重置状态
                self.is_spinning = False
                if self.bet_button.winfo_exists():  # 确保按钮仍然存在
                    self.bet_button.config(state="normal")

    def auto_gamble(self):
        """自动赌博"""
        try:
            self.current_bet = float(self.bet_entry.get())  # 获取下注金额
            if self.current_bet <= 0 or self.current_bet > self.balance:
                messagebox.showwarning("⚠️ 错误", "无效的下注金额！")
                return

            # 获取自动赌博次数
            times = simpledialog.askinteger("自动赌博", "请输入自动赌博的次数:", minvalue=1, maxvalue=1000)
            if times is None:
                return

            # 记录初始余额
            self.initial_balance = self.balance

            # 进行自动赌博
            self.auto_times = times
            self.auto_count = 0
            self.is_auto_gambling = True  # 标记是否在自动赌博
            self.stop_auto_bet_button.config(state="normal")  # 启用停止按钮
            self.auto_bet_button.config(state="disabled")  # 禁用自动赌博按钮
            self.bet_button.config(state="disabled")  # 禁用单次赌博按钮

            self.auto_gamble_step()

        except ValueError:
            messagebox.showwarning("⚠️ 错误", "请输入有效数字！")

    def auto_gamble_step(self):
        """自动赌博的每一步"""
        if self.auto_count < self.auto_times and self.balance > 0 and self.is_auto_gambling:
            # 扣除下注金额
            self.balance -= self.current_bet
            self.balance_history.append(self.balance)  # 记录资金变化

            # 根据概率决定是否获胜
            if random.random() < WIN_PROB:
                # 获胜情况：三个图标一致
                win_amount = self.current_bet * ODDS
                self.balance += win_amount
                self.balance_history.append(self.balance)  # 记录资金变化

            # 更新余额显示
            self.balance_label.config(text=f"💰 当前余额: {self.balance:.2f} 元")

            # 更新资金曲线图
            self.update_balance_chart()

            # 检查是否输光
            if self.balance <= 0:
                self.game_over()
                return

            # 更新计数
            self.auto_count += 1

            # 延迟后继续下一步
            self.root.after(100, self.auto_gamble_step)
        else:
            # 停止自动赌博
            self.stop_auto_gamble()

    def stop_auto_gamble(self):
        """停止自动赌博"""
        self.is_auto_gambling = False
        self.stop_auto_bet_button.config(state="disabled")  # 禁用停止按钮
        self.auto_bet_button.config(state="normal")  # 启用自动赌博按钮
        self.bet_button.config(state="normal")  # 启用单次赌博按钮

        # 显示结果
        if self.balance >= self.initial_balance:
            self.result_label.config(text=f"🎉 自动赌博结束，最终余额: {self.balance:.2f} 元", fg=WIN_COLOR)
        else:
            self.result_label.config(text=f"💸 自动赌博结束，最终余额: {self.balance:.2f} 元", fg=LOSE_COLOR)

        # 检查是否输光
        if self.balance <= 0:
            self.game_over()

    def game_over(self):
        """游戏结束逻辑"""
        # 创建一个大弹窗
        game_over_window = tk.Toplevel(self.root)
        game_over_window.title("游戏结束")
        game_over_window.geometry("1600x400")
        game_over_window.configure(bg=BG_COLOR)
        game_over_window.attributes("-topmost", True)  # 确保弹窗在最前面

        # 设置弹窗内容
        game_over_label = tk.Label(
            game_over_window,
            text="🙉菜就多练🙉",
            font=("Helvetica", 180, "bold"),  # 设置大字体
            bg=BG_COLOR,
            fg=LOSE_COLOR,
        )
        game_over_label.pack(pady=50)

        # 更新结果标签
        self.result_label.config(text="😭 菜", fg=LOSE_COLOR)
        messagebox.showinfo("游戏结束", "你已输光所有资金！\n\n💡 温馨提示：十赌九输，珍惜生活，远离赌博！")
        self.root.destroy()

    def quit_game(self):
        """退出游戏"""
        if messagebox.askyesno("退出", f"你确定要带着 {self.balance:.2f} 元离开吗？"):
            messagebox.showinfo("游戏结束",
                                "老板把你打了一顿，拿走了你剩下所有的钱！\n\n温馨提示：十赌九输，珍惜生活，远离赌博！")
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = GamblingGameUI(root)
    root.mainloop()