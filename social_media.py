import tkinter as tk
from tkinter import messagebox, ttk
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
from datetime import datetime, timedelta
import sqlite3

class SocialMediaAnalyticsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Social Media Analytics")
        self.root.geometry("300x400")

        self.platforms = ['All Platforms', 'Twitter', 'Facebook', 'Instagram', 'LinkedIn', 'Snapchat',
                          'YouTube', 'TikTok', 'Reddit', 'Pinterest', 'WhatsApp', 'WeChat', 'Telegram']

        self.sort_by_options = ['likes', 'comments', 'installs', 'current_users']

        self.btn_metrics = tk.Button(self.root, text="Show Metrics", command=self.show_metrics)
        self.btn_metrics.pack(pady=5)

        self.btn_sentiment = tk.Button(self.root, text="Show Sentiment Analysis", command=self.show_sentiment_analysis)
        self.btn_sentiment.pack(pady=5)

        self.btn_trend = tk.Button(self.root, text="Trend Analysis", command=self.show_trend_analysis)
        self.btn_trend.pack(pady=5)

        self.btn_competitor = tk.Button(self.root, text="Competitor Analysis", command=self.show_competitor_analysis)
        self.btn_competitor.pack(pady=5)

        self.btn_sort = tk.Button(self.root, text="Show Sorted Data", command=self.show_data_sorted)
        self.btn_sort.pack(pady=5)

        self.up_sort = tk.Button(self.root, text="Update Data", command=self.manual_update_data)
        self.up_sort.pack(pady=5)

        self.initialize_database()

    def initialize_database(self):
        self.conn = sqlite3.connect('social_media_analytics_extended.db')
        self.c = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.c.execute('''
            CREATE TABLE IF NOT EXISTS social_media (
                id INTEGER PRIMARY KEY,
                date TEXT,
                platform TEXT,
                installs INTEGER,
                current_users INTEGER,
                likes INTEGER,
                comments INTEGER
            )
        ''')
        self.conn.commit()

    def generate_random_data(self, num_entries=100):
        dates = [datetime(2023, 1, 1) + timedelta(days=i) for i in range(num_entries)]
        data = {
            'date': dates,
            'platform': np.random.choice(self.platforms[1:], size=num_entries),
            'installs': np.random.randint(100, 10000, size=num_entries),
            'current_users': np.random.randint(1000, 50000, size=num_entries),
            'likes': np.random.randint(10, 1000, size=num_entries),
            'comments': np.random.randint(5, 200, size=num_entries)
        }
        return pd.DataFrame(data)

    def show_metrics(self):
        metrics_window = tk.Toplevel(self.root)
        metrics_window.title("Select Metrics")
        tk.Label(metrics_window, text="Select Metrics:").pack()

        metrics_listbox = tk.Listbox(metrics_window, selectmode=tk.MULTIPLE)
        metrics_listbox.insert(1, "Summary")
        metrics_listbox.insert(2, "Total Likes")
        metrics_listbox.insert(3, "Total Comments")
        metrics_listbox.insert(4, "Average Installs")
        metrics_listbox.insert(5, "Average Current Users")
        metrics_listbox.pack()

        tk.Button(metrics_window, text="Show Selected Metrics",
                  command=lambda: self.show_selected_metrics(metrics_listbox)).pack()

    def show_selected_metrics(self, metrics_listbox):
        selected_metrics = [metrics_listbox.get(i) for i in metrics_listbox.curselection()]
        if not selected_metrics:
            messagebox.showerror("Metrics Error", "No metrics selected")
            return

        df = self.generate_random_data()
        metrics_window = tk.Toplevel(self.root)
        metrics_window.title("Metrics")
        metrics_text = tk.Text(metrics_window, wrap='word')

        metrics_text.insert(tk.END, "Metrics Summary\n")
        metrics_text.insert(tk.END, "-" * 20 + "\n\n")

        if "Summary" in selected_metrics:
            metrics_text.insert(tk.END, "Summary:\n")
            metrics_text.insert(tk.END, df.describe().to_string() + "\n\n")

        if "Total Likes" in selected_metrics:
            total_likes = df['likes'].sum()
            metrics_text.insert(tk.END, f"Total Likes: {total_likes}\n")

        if "Total Comments" in selected_metrics:
            total_comments = df['comments'].sum()
            metrics_text.insert(tk.END, f"Total Comments: {total_comments}\n")

        if "Average Installs" in selected_metrics:
            avg_installs = df['installs'].mean()
            metrics_text.insert(tk.END, f"Average Installs: {avg_installs:.2f}\n")

        if "Average Current Users" in selected_metrics:
            avg_current_users = df['current_users'].mean()
            metrics_text.insert(tk.END, f"Average Current Users: {avg_current_users:.2f}\n")

        metrics_text.pack(expand=True, fill='both')

    def show_selected_metrics(self, metrics_listbox):
        selected_metrics = [metrics_listbox.get(i) for i in metrics_listbox.curselection()]
        if not selected_metrics:
            messagebox.showerror("Metrics Error", "No metrics selected")
            return

        df = self.generate_random_data()
        metrics_window = tk.Toplevel(self.root)
        metrics_window.title("Metrics")
        metrics_text = tk.Text(metrics_window, wrap='word')

        if "Summary" in selected_metrics:
            metrics_text.insert(tk.END, df.describe().to_string())

        if "Total Likes" in selected_metrics:
            total_likes = df['likes'].sum()
            metrics_text.insert(tk.END, f"\nTotal Likes: {total_likes}")

        if "Total Comments" in selected_metrics:
            total_comments = df['comments'].sum()
            metrics_text.insert(tk.END, f"\nTotal Comments: {total_comments}")

        if "Average Installs" in selected_metrics:
            avg_installs = df['installs'].mean()
            metrics_text.insert(tk.END, f"\nAverage Installs: {avg_installs}")

        metrics_text.pack(expand=True, fill='both')

    def show_sentiment_analysis(self):
        sentiment_window = tk.Toplevel(self.root)
        sentiment_window.title("Sentiment Analysis")
        tk.Label(sentiment_window, text="Select Platform:").pack()

        platform_combo = ttk.Combobox(sentiment_window, values=self.platforms)
        platform_combo.pack()

        tk.Button(sentiment_window, text="Show Sentiment Analysis",
                  command=lambda: self.show_sentiment_for_selected(platform_combo)).pack()

    def show_sentiment_for_selected(self, platform_combo):
        selected_platform = platform_combo.get()
        if not selected_platform:
            messagebox.showerror("Selection Error", "No platform selected")
            return

        df = self.generate_random_data()
        df = df[df['platform'] == selected_platform]

        sentiments = np.random.choice(['Positive', 'Negative', 'Neutral'], size=len(df))
        df['sentiment'] = sentiments
        sentiment_counts = df['sentiment'].value_counts()

        fig = px.bar(x=sentiment_counts.index, y=sentiment_counts.values,
                     labels={'x': 'Sentiment', 'y': 'Counts'},
                     title=f'Sentiment Analysis for {selected_platform}')
        fig.show()

    def show_trend_analysis(self):
        df = self.generate_random_data()
        df['date'] = pd.to_datetime(df['date'])
        df.set_index('date', inplace=True)
        daily_likes_sum = df.resample('D').sum(numeric_only=True)['likes']

        fig = px.line(x=daily_likes_sum.index, y=daily_likes_sum.values,
                      labels={'x': 'Date', 'y': 'Daily Likes'},
                      title='Trend Analysis',
                      markers=True)
        fig.update_xaxes(tickangle=45)
        fig.show()

    def show_competitor_analysis(self):
        competitor_window = tk.Toplevel(self.root)
        competitor_window.title("Competitor Analysis")
        tk.Label(competitor_window, text="Select Competitors:").pack()

        competitors_listbox = tk.Listbox(competitor_window, selectmode=tk.MULTIPLE)
        for platform in self.platforms:
            competitors_listbox.insert(tk.END, platform)
        competitors_listbox.pack()

        tk.Button(competitor_window, text="Show Selected Competitors",
                  command=lambda: self.show_selected_competitors(competitors_listbox)).pack()

    def show_selected_competitors(self, competitors_listbox):
        selected_competitors = [competitors_listbox.get(i) for i in competitors_listbox.curselection()]
        if not selected_competitors:
            messagebox.showerror("Selection Error", "No competitors selected")
            return

        df = self.generate_random_data()
        df = df[df['platform'].isin(selected_competitors)]
        competitor_group = df.groupby('platform').sum(numeric_only=True)
        likes_data = competitor_group['likes']

        fig = px.pie(values=likes_data.values, names=likes_data.index,
                     title='Competitor Analysis - Likes Distribution')
        fig.show()

    def show_data_sorted(self):
        sorted_data_window = tk.Toplevel(self.root)
        sorted_data_window.title("Sort Data")

        tk.Label(sorted_data_window, text="Sort By:").pack()
        sort_by_listbox = tk.Listbox(sorted_data_window, selectmode=tk.MULTIPLE)
        for option in self.sort_by_options:
            sort_by_listbox.insert(tk.END, option)
        sort_by_listbox.pack()

        tk.Label(sorted_data_window, text="Select Platform:").pack()
        platform_combo = ttk.Combobox(sorted_data_window, values=self.platforms)
        platform_combo.pack()

        tk.Button(sorted_data_window, text="Sort Data",
                  command=lambda: self.sort_data(sort_by_listbox, platform_combo)).pack()

    def sort_data(self, sort_by_listbox, platform_combo):
        df = self.generate_random_data()
        df['date'] = pd.to_datetime(df['date'])

        sort_by = [sort_by_listbox.get(i) for i in sort_by_listbox.curselection()]
        selected_platform = platform_combo.get()

        if selected_platform and selected_platform != 'All Platforms':
            df = df[df['platform'] == selected_platform]

        if sort_by:
            # Include 'date' and 'platform' by default
            sort_columns = ['date', 'platform'] + sort_by
            df_display = df[sort_columns].copy()
            df_display['date'] = df_display['date'].dt.strftime('%Y-%m-%d')  # Format date column
            df_display.sort_values(by=sort_by, inplace=True)

            sorted_data_window = tk.Toplevel(self.root)
            sorted_data_window.title(f"Sorted Data by {', '.join(sort_by)}")

            tree = ttk.Treeview(sorted_data_window)
            tree["columns"] = sort_columns
            tree["show"] = "headings"

            for col in sort_columns:
                tree.heading(col, text=col)
                tree.column(col, width=100)

            for index, row in df_display.iterrows():
                tree.insert("", "end", values=list(row))

            tree.pack(expand=True, fill='both')
        else:
            # If no sort criteria selected, show entire dataset with 'date' and 'platform'
            df_display = df.copy()
            df_display['date'] = df_display['date'].dt.strftime('%Y-%m-%d')  # Format date column
            df_display.sort_values(by=['date', 'platform'], inplace=True)

            sorted_data_window = tk.Toplevel(self.root)
            sorted_data_window.title(f"Sorted Data by Date and Platform")

            tree = ttk.Treeview(sorted_data_window)
            tree["columns"] = df_display.columns
            tree["show"] = "headings"

            for col in df_display.columns:
                tree.heading(col, text=col)
                tree.column(col, width=100)

            for index, row in df_display.iterrows():
                tree.insert("", "end", values=list(row))

            tree.pack(expand=True, fill='both')

    def manual_update_data(self):
            update_window = tk.Toplevel(self.root)
            update_window.title("Manual Update Data")

            tk.Label(update_window, text="Enter data to update manually:").pack()

            tk.Label(update_window, text="Date (YYYY-MM-DD):").pack()
            date_entry = tk.Entry(update_window)
            date_entry.pack()

            tk.Label(update_window, text="Platform:").pack()
            platform_combo = ttk.Combobox(update_window, values=self.platforms)
            platform_combo.pack()

            tk.Label(update_window, text="Installs:").pack()
            installs_entry = tk.Entry(update_window)
            installs_entry.pack()

            tk.Label(update_window, text="Current Users:").pack()
            current_users_entry = tk.Entry(update_window)
            current_users_entry.pack()

            tk.Label(update_window, text="Likes:").pack()
            likes_entry = tk.Entry(update_window)
            likes_entry.pack()

            tk.Label(update_window, text="Comments:").pack()
            comments_entry = tk.Entry(update_window)
            comments_entry.pack()

            tk.Button(update_window, text="Submit",
                      command=lambda: self.submit_manual_update(date_entry, platform_combo,
                                                                installs_entry,
                                                                current_users_entry,
                                                                likes_entry, comments_entry)).pack()

    def submit_manual_update(self, date_entry, platform_combo, installs_entry, current_users_entry, likes_entry,
                                 comments_entry):
            try:
                date = datetime.strptime(date_entry.get(), '%Y-%m-%d')
            except ValueError:
                messagebox.showerror("Date Format Error", "Please enter date in format YYYY-MM-DD")
                return

            platform = platform_combo.get()

            try:
                installs = int(installs_entry.get())
                current_users = int(current_users_entry.get())
                likes = int(likes_entry.get())
                comments = int(comments_entry.get())
            except ValueError:
                messagebox.showerror("Input Error",
                                     "Please enter valid numerical values for Installs, Current Users, Likes, and Comments")
                return

            self.c.execute('''INSERT INTO social_media (date, platform, installs, current_users, likes, comments) 
                                      VALUES (?, ?, ?, ?, ?, ?)''',
                           (date.strftime('%Y-%m-%d'), platform, installs, current_users, likes, comments))

            self.conn.commit()
            messagebox.showinfo("Manual Update Data", "Data updated manually")

    def run(self):
            self.root.mainloop()

if __name__ == "__main__":
            root = tk.Tk()
            app = SocialMediaAnalyticsApp(root)
            app.run()

