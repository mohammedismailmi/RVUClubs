import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
from clubs_db import get_all_clubs, add_club, update_club, delete_club

class ClubApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Student Clubs Management")
        self.geometry("600x400")
        self.create_widgets()
        self.load_clubs()

    def create_widgets(self):
        self.tree = ttk.Treeview(self, columns=('ID', 'Name', 'Core Team', 'Events'), show='headings')
        self.tree.heading('ID', text='ID')
        self.tree.heading('Name', text='Name')
        self.tree.heading('Core Team', text='Core Team')
        self.tree.heading('Events', text='Events')
        self.tree.pack(expand=True, fill=tk.BOTH)

        self.add_button = tk.Button(self, text="Add Club", command=self.add_club_dialog)
        self.add_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.update_button = tk.Button(self, text="Update Club", command=self.update_club_dialog)
        self.update_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.delete_button = tk.Button(self, text="Delete Club", command=self.delete_club)
        self.delete_button.pack(side=tk.LEFT, padx=10, pady=10)

    def load_clubs(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for club in get_all_clubs():
            self.tree.insert('', 'end', values=club)

    def add_club_dialog(self):
        dialog = ClubDialog(self, "Add Club", self.add_club)
        self.wait_window(dialog.top)
        self.load_clubs()

    def update_club_dialog(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Update Club", "Please select a club to update.")
            return
        club_id = self.tree.item(selected_item[0])['values'][0]
        dialog = ClubDialog(self, "Update Club", self.update_club, club_id)
        self.wait_window(dialog.top)
        self.load_clubs()

    def add_club(self, club_name, core_team, events):
        add_club(club_name, core_team, events)

    def update_club(self, club_id, club_name, core_team, events):
        update_club(club_id, club_name, core_team, events)

    def delete_club(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Delete Club", "Please select a club to delete.")
            return
        club_id = self.tree.item(selected_item[0])['values'][0]
        delete_club(club_id)
        self.load_clubs()

class ClubDialog:
    def __init__(self, parent, title, callback, club_id=None):
        self.top = tk.Toplevel(parent)
        self.top.title(title)
        self.callback = callback
        self.club_id = club_id

        self.label_name = tk.Label(self.top, text="Club Name")
        self.label_name.pack(padx=10, pady=5)
        self.entry_name = tk.Entry(self.top)
        self.entry_name.pack(padx=10, pady=5)

        self.label_core_team = tk.Label(self.top, text="Core Team")
        self.label_core_team.pack(padx=10, pady=5)
        self.entry_core_team = tk.Entry(self.top)
        self.entry_core_team.pack(padx=10, pady=5)

        self.label_events = tk.Label(self.top, text="Events")
        self.label_events.pack(padx=10, pady=5)
        self.entry_events = tk.Entry(self.top)
        self.entry_events.pack(padx=10, pady=5)

        self.submit_button = tk.Button(self.top, text="Submit", command=self.submit)
        self.submit_button.pack(padx=10, pady=10)

        if club_id is not None:
            club = self.get_club_details(club_id)
            if club:
                self.entry_name.insert(0, club[1])
                self.entry_core_team.insert(0, club[2])
                self.entry_events.insert(0, club[3])

    def get_club_details(self, club_id):
        clubs = get_all_clubs()
        for club in clubs:
            if club[0] == club_id:
                return club
        return None

    def submit(self):
        club_name = self.entry_name.get()
        core_team = self.entry_core_team.get()
        events = self.entry_events.get()
        if self.club_id is None:
            self.callback(club_name, core_team, events)
        else:
            self.callback(self.club_id, club_name, core_team, events)
        self.top.destroy()

if __name__ == '__main__':
    app = ClubApp()
    app.mainloop()
