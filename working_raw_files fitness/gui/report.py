import tkinter as tk
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from database.member_ops import fetch_all_members


class ReportPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#f0f4f8")
        self.pack(fill="both", expand=True)

        # ================= HEADER =================
        header = tk.Frame(self, bg="#1565c0", height=90)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="📊  GYM ANALYTICS DASHBOARD",
            font=("Segoe UI", 30, "bold"),
            bg="#1565c0",
            fg="white"
        ).pack(expand=True)

        # ================= DATA =================
        self.members = fetch_all_members()
        self.calculate_metrics()

        self.display_metrics()
        self.display_charts()

    # ================= DATA CALCULATION =================
    def calculate_metrics(self):
        self.total_members = len(self.members)
        self.active_members = 0
        self.expired_members = 0
        self.new_members_this_month = 0
        self.monthly_income = {m: 0 for m in range(1, 13)}

        today = datetime.today()

        for m in self.members:
            try:
                _, _, _, s, e, fees = m[:6]
                start = datetime.strptime(s, "%d-%m-%Y")
                end = datetime.strptime(e, "%d-%m-%Y")
            except:
                continue

            if end >= today:
                self.active_members += 1
            else:
                self.expired_members += 1

            if start.month == today.month and start.year == today.year:
                self.new_members_this_month += 1

            if fees:
                amount = int(float(fees.replace("₹", "").replace(",", "")))
                if start.year == today.year:
                    self.monthly_income[start.month] += amount

    # ================= METRIC CARDS =================
    def display_metrics(self):
        container = tk.Frame(self, bg="#f0f4f8")
        container.pack(pady=25)

        cards = [
            ("👥", "Total Members", self.total_members, "#1565c0"),
            ("✅", "Active", self.active_members, "#2e7d32"),
            ("❌", "Expired", self.expired_members, "#d32f2f"),
            ("🆕", "New", self.new_members_this_month, "#0288d1"),
        ]

        for i, c in enumerate(cards):
            self.metric_card(container, *c, i)

    def metric_card(self, parent, icon, title, value, color, col):
        card = tk.Frame(parent, bg=color, width=170, height=145)
        card.grid(row=0, column=col, padx=14)
        card.pack_propagate(False)

        tk.Label(card, text=icon, font=("Segoe UI", 32), bg=color, fg="white").pack(pady=(12, 4))
        tk.Label(card, text=value, font=("Segoe UI", 26, "bold"), bg=color, fg="white").pack()
        tk.Label(card, text=title, font=("Segoe UI", 10, "bold"), bg=color, fg="white").pack(pady=(6, 10))

    # ================= CHART AREA =================
    def display_charts(self):
        charts = tk.Frame(self, bg="#f0f4f8")
        charts.pack(fill="both", expand=True, padx=20)

        left = tk.Frame(charts, bg="white")
        left.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        right = tk.Frame(charts, bg="white")
        right.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        self.draw_pie(left)
        self.draw_bar(right)
        self.draw_income()

    # ================= STATIC PIE CHART =================
    def draw_pie(self, parent):
        fig, ax = plt.subplots(figsize=(4.8, 4.8))

        ax.pie(
            [self.active_members, self.expired_members],
            labels=["Active", "Expired"],
            colors=["#43a047", "#e53935"],
            explode=(0.06, 0.06),
            autopct="%1.1f%%",
            startangle=90,
            shadow=True,
            textprops={
                "fontsize": 11,
                "fontweight": "bold",
                "color": "white"
            }
        )

        ax.set_title(
            "Active vs Expired Memberships",
            fontsize=14,
            fontweight="bold",
            pad=12
        )

        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    # ================= STATIC BAR CHART =================
    def draw_bar(self, parent):
        fig, ax = plt.subplots(figsize=(6.5, 5))

        labels = ["Total", "Active", "Expired", "New"]
        values = [
            self.total_members,
            self.active_members,
            self.expired_members,
            self.new_members_this_month
        ]

        bars = ax.bar(
            labels,
            values,
            color=["#1565c0", "#2e7d32", "#d32f2f", "#0288d1"]
        )

        ax.set_ylim(0, max(values) * 1.2)
        ax.set_title("Membership Overview", fontweight="bold")
        ax.grid(axis="y", alpha=0.3)

        for bar in bars:
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height(),
                int(bar.get_height()),
                ha="center",
                va="bottom",
                fontweight="bold"
            )

        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    # ================= STATIC MONTHLY INCOME =================
    def draw_income(self):
        frame = tk.Frame(self, bg="white")
        frame.pack(fill="both", padx=25, pady=20)

        fig, ax = plt.subplots(figsize=(11, 4))

        months = [datetime(2000, m, 1).strftime("%b") for m in self.monthly_income]
        income = list(self.monthly_income.values())

        bars = ax.bar(months, income, color="#00897b")

        ax.set_ylim(0, max(income)*1.2 if max(income) else 100)
        ax.set_title("💰 Monthly Income (This Year)", fontweight="bold")
        ax.grid(axis="y", alpha=0.3)

        for bar in bars:
            if bar.get_height() > 0:
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    bar.get_height(),
                    f"₹{int(bar.get_height())}",
                    ha="center",
                    va="bottom",
                    fontsize=9,
                    fontweight="bold"
                )

        canvas = FigureCanvasTkAgg(fig, frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
