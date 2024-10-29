import os
import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext
from tkinter import ttk


class Team:
    def __init__(self, short_name, full_name):
        self.short_name = short_name
        self.full_name = full_name
        self.played = 0
        self.wins = 0
        self.draws = 0
        self.losses = 0
        self.goals_for = 0
        self.goals_against = 0
        self.points = 0

    def update_stats(self, goals_for, goals_against, result_points):
        self.played += 1
        self.goals_for += goals_for
        self.goals_against += goals_against
        self.points += result_points
        if result_points == WIN_POINTS:
            self.wins += 1
        elif result_points == DRAW_POINTS:
            self.draws += 1
        elif result_points == LOSS_POINTS:
            self.losses += 1


def load_settings():
    global TEAM_COUNT, WIN_POINTS, DRAW_POINTS, LOSS_POINTS
    with open("ayarlar.txt") as f:
        settings = f.readlines()
        TEAM_COUNT = int(settings[0].strip())
        WIN_POINTS = int(settings[1].strip())
        DRAW_POINTS = int(settings[2].strip())
        LOSS_POINTS = int(settings[3].strip())


def load_teams():
    teams = {}
    with open("takimlar.txt") as f:
        for line in f:
            short_name, full_name = line.strip().split()
            teams[short_name] = Team(short_name, full_name)
    return teams


def process_match_input(home, home_goals, away, away_goals):
    if (home, away) in played_matches:
        print(f"Warning: {home} and {away} have already played this match.")
        return

    played_matches.add((home, away))

    home_goals, away_goals = int(home_goals), int(away_goals)
    if home_goals > away_goals:
        home_result, away_result = WIN_POINTS, LOSS_POINTS
    elif home_goals < away_goals:
        home_result, away_result = LOSS_POINTS, WIN_POINTS
    else:
        home_result, away_result = DRAW_POINTS, DRAW_POINTS

    teams[home].update_stats(home_goals, away_goals, home_result)
    teams[away].update_stats(away_goals, home_goals, away_result)


def process_matches_from_file(filename="maclar.txt"):
    with open(filename) as f:
        for line in f:
            match_data = line.strip().split()
            if len(match_data) == 4:
                process_match_input(*match_data)
            else:
                print("Invalid format in file. Please ensure each line is in format 'A 3 B 2'.")


def display_standings(order="points", uppercase=False):
    sorted_teams = sorted(teams.values(), key=lambda x: (-x.points, x.short_name))
    print("Team | P | W | D | L | GF | GA | GD | Points")
    for team in sorted_teams:
        name = team.full_name.upper() if uppercase else team.full_name
        print(f"{name} | {team.played} | {team.wins} | {team.draws} | {team.losses} | "
              f"{team.goals_for} | {team.goals_against} | {team.goals_for - team.goals_against} | {team.points}")


class LeagueApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sanal Süper Lig Tablosu")
        self.root.geometry("800x400")

        # Ayarları ve takımları yükle
        load_settings()
        global teams, played_matches
        teams = load_teams()
        played_matches = set()

        # Başlık
        title_label = tk.Label(root, text="Sanal Süper Lig Tablosu", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)

        # Maçları dosyadan işleyen düğme
        process_matches_button = tk.Button(root, text="Maçları Yükle ve İşle", command=self.process_matches)
        process_matches_button.pack(pady=5)

        # Puan tablosunu gösteren düğme
        show_standings_button = tk.Button(root, text="Puan Durumunu Göster", command=self.display_standings)
        show_standings_button.pack(pady=5)

        # Lig tablosu için Treeview
        columns = ("Takım", "Oynanan", "Galibiyet", "Beraberlik", "Mağlubiyet", "Atılan", "Yenilen", "Averaj", "Puan")
        self.standings_table = ttk.Treeview(root, columns=columns, show="headings")
        for col in columns:
            self.standings_table.heading(col, text=col)
            self.standings_table.column(col, anchor="center", width=80)
        self.standings_table.pack(fill="both", expand=True)

    def process_matches(self):
        # Takım istatistiklerini sıfırla
        for team in teams.values():
            team.played = team.wins = team.draws = team.losses = 0
            team.goals_for = team.goals_against = team.points = 0

        # Daha önce oynanan maçları sıfırla
        played_matches.clear()

        # Maçları tekrar işle
        try:
            process_matches_from_file("maclar.txt")
            messagebox.showinfo("Bilgi", "Maçlar başarıyla işlendi!")
        except Exception as e:
            messagebox.showerror("Hata", f"Maçlar işlenirken bir hata oluştu: {e}")

    def display_standings(self):
        # Tabloyu temizle
        for row in self.standings_table.get_children():
            self.standings_table.delete(row)

        # Sıralanmış takımları tabloya ekle
        sorted_teams = sorted(teams.values(), key=lambda x: (-x.points, x.short_name))
        for team in sorted_teams:
            self.standings_table.insert(
                "", "end",
                values=(
                    team.full_name, team.played, team.wins, team.draws, team.losses,
                    team.goals_for, team.goals_against, team.goals_for - team.goals_against, team.points
                )
            )


if __name__ == "__main__":
    root = tk.Tk()
    app = LeagueApp(root)
    root.mainloop()