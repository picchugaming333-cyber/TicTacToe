from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from kivy.graphics import Color, Rectangle
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.storage.jsonstore import JsonStore
import random
import time

def get_rank_info(level):
    if level <= 10:
        return "Bronze", "★", (0.8, 0.5, 0.2, 1)
    elif level <= 40:
        return "Silver", "★★", (0.75, 0.75, 0.8, 1)
    elif level <= 70:
        return "Gold", "★★★", (1, 0.85, 0.2, 1)
    elif level <= 100:
        return "Iron", "★★★★", (0.6, 0.6, 0.65, 1)
    elif level <= 150:
        return "Emerald", "★★★★★", (0.2, 0.8, 0.4, 1)
    elif level <= 200:
        return "Netheright", "★★★★★★", (0.6, 0.2, 0.8, 1)
    elif level <= 300:
        return "Master", "★★★★★★★", (0.9, 0.3, 0.5, 1)
    else:
        return "SuperPrime", "★★★★★★★★", (1, 0.4, 0.1, 1)

class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.layout = BoxLayout(orientation='vertical', padding=14, spacing=9)

        with self.layout.canvas.before:
            Color(0.14, 0.05, 0.22, 1)
            self.rect = Rectangle(size=self.layout.size, pos=self.layout.pos)
        self.layout.bind(size=self._update_rect, pos=self._update_rect)

        # Title - Bigger & Thicker
        self.layout.add_widget(Label(
            text="TIC TAC TOE",
            font_size="40sp",
            bold=True,
            color=(1, 0.9, 0.25, 1),
            size_hint=(1, 0.12)
        ))

        self.layout.add_widget(Label(
            text="Owner : Picchu Gaming",
            font_size="16sp",
            bold=True,
            color=(0.85, 0.75, 1, 1),
            size_hint=(1, 0.05)
        ))

        self.level_label = Label(text="Level 1", font_size="20sp", bold=True, color=(1,1,1,1), size_hint=(1, 0.06))
        self.rank_label = Label(text="Bronze ★", font_size="18sp", bold=True, color=(0.8, 0.5, 0.2, 1), size_hint=(1, 0.05))
        self.exp_label = Label(text="EXP: 0 / 10", font_size="16sp", bold=True, color=(0.8, 0.9, 1, 1), size_hint=(1, 0.05))
        self.layout.add_widget(self.level_label)
        self.layout.add_widget(self.rank_label)
        self.layout.add_widget(self.exp_label)

        self.coin_label = Label(text="Coins: 50", font_size="20sp", bold=True, color=(1, 0.85, 0.2, 1), size_hint=(1, 0.06))
        self.layout.add_widget(self.coin_label)

        # Game Mode
        self.layout.add_widget(Label(text="Game Mode", color=(1,1,1,1), font_size="16sp", bold=True, size_hint=(1, 0.05)))
        self.mode_spinner = Spinner(text="Computer Player", values=["Computer Player", "2 Players"],
                                    size_hint=(1, 0.08), background_color=(0.4, 0.2, 0.6, 1), font_size="16sp")
        self.layout.add_widget(self.mode_spinner)

        # Difficulty
        self.layout.add_widget(Label(text="Bot Difficulty", color=(1,1,1,1), font_size="16sp", bold=True, size_hint=(1, 0.05)))
        self.difficulty_spinner = Spinner(text="Normal", values=["Easy", "Normal", "Medium", "Hard", "Super Hard"],
                                          size_hint=(1, 0.08), background_color=(0.4, 0.2, 0.6, 1), font_size="16sp")
        self.layout.add_widget(self.difficulty_spinner)

        # Theme (New themes added)
        self.layout.add_widget(Label(text="Theme", color=(1,1,1,1), font_size="16sp", bold=True, size_hint=(1, 0.05)))
        self.theme_spinner = Spinner(
            text="Purple",
            values=["Purple", "White", "Black", "Blue Neon", "Green Forest"],
            size_hint=(1, 0.08),
            background_color=(0.4, 0.2, 0.6, 1),
            font_size="16sp"
        )
        self.layout.add_widget(self.theme_spinner)

        # Cheat Mode
        self.layout.add_widget(Label(text="Cheat Mode", color=(1, 0.3, 0.3, 1), font_size="16sp", bold=True, size_hint=(1, 0.05)))
        self.cheat_spinner = Spinner(text="OFF", values=["OFF", "ON"], size_hint=(1, 0.08),
                                     background_color=(0.7, 0.15, 0.15, 1), font_size="16sp")
        self.layout.add_widget(self.cheat_spinner)

        # Start Button - Bigger
        start_btn = Button(
            text="START GAME",
            font_size="22sp",
            bold=True,
            size_hint=(1, 0.11),
            background_color=(0.2, 0.7, 0.3, 1),
            on_press=self.start_game
        )
        self.layout.add_widget(start_btn)

        self.claim_btn = Button(
            text="Claim Free Coins",
            font_size="16sp",
            bold=True,
            size_hint=(1, 0.08),
            background_color=(0.9, 0.5, 0.1, 1),
            on_press=self.claim_coins
        )
        self.layout.add_widget(self.claim_btn)

        self.add_widget(self.layout)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def on_pre_enter(self, *args):
        self.refresh_stats()
        self.update_claim_button()

    def refresh_stats(self):
        app = App.get_running_app()
        level = app.level
        rank, stars, color = get_rank_info(level)
        current_exp = app.exp % 10
        self.level_label.text = f"Level {level}"
        self.rank_label.text = f"{rank} {stars}"
        self.rank_label.color = color
        self.exp_label.text = f"EXP: {current_exp} / 10"
        self.coin_label.text = f"Coins: {app.coins}"

    def update_claim_button(self):
        app = App.get_running_app()
        if app.coins > 0:
            self.claim_btn.disabled = True
            self.claim_btn.text = "Claim Free Coins"
        else:
            remaining = 300 - (time.time() - app.last_claim)
            if remaining <= 0:
                self.claim_btn.disabled = False
                self.claim_btn.text = "Claim 100 Free Coins!"
            else:
                mins = int(remaining // 60)
                secs = int(remaining % 60)
                self.claim_btn.disabled = True
                self.claim_btn.text = f"Wait {mins}:{secs:02d}"
                Clock.schedule_once(lambda dt: self.update_claim_button(), 1)

    def start_game(self, instance):
        app = App.get_running_app()
        app.selected_mode = self.mode_spinner.text
        app.selected_difficulty = self.difficulty_spinner.text
        app.selected_theme = self.theme_spinner.text
        app.cheat_mode = self.cheat_spinner.text == "ON"
        self.manager.current = "game"

    def claim_coins(self, instance):
        app = App.get_running_app()
        if app.coins <= 0:
            app.coins = 100
            app.last_claim = time.time()
            app.save_data()
            self.refresh_stats()
            self.claim_btn.disabled = True
            self.claim_btn.text = "Claimed 100 Coins!"

class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.main = BoxLayout(orientation='vertical', padding=10, spacing=5)

        with self.main.canvas.before:
            self.bg_color = Color(0.35, 0.12, 0.55, 1)
            self.bg_rect = Rectangle(size=self.main.size, pos=self.main.pos)
        self.main.bind(size=self._update_bg, pos=self._update_bg)

        top = BoxLayout(size_hint=(1, 0.06))
        self.coin_label = Label(text="Coins: 50", font_size="17sp", bold=True, color=(1, 0.85, 0.2, 1))
        self.level_label = Label(text="Lv.1", font_size="16sp", bold=True, color=(1,1,1,1))
        top.add_widget(self.coin_label)
        top.add_widget(self.level_label)
        self.main.add_widget(top)

        self.title_label = Label(text="TIC TAC TOE", font_size="24sp", bold=True, color=(1,1,1,1), size_hint=(1, 0.07))
        self.main.add_widget(self.title_label)

        self.status = Label(text="Choose your symbol", font_size="17sp", bold=True, color=(1,1,1,1), size_hint=(1, 0.07))
        self.main.add_widget(self.status)

        self.choice_box = BoxLayout(size_hint=(1, 0.09), spacing=8)
        self.btn_x = Button(text="X", font_size="30sp", bold=True, background_color=(0.9, 0.15, 0.15, 1),
                            on_press=lambda x: self.choose_symbol("X"))
        self.btn_o = Button(text="O", font_size="30sp", bold=True, background_color=(0.9, 0.15, 0.15, 1),
                            on_press=lambda x: self.choose_symbol("O"))
        self.choice_box.add_widget(self.btn_x)
        self.choice_box.add_widget(self.btn_o)
        self.main.add_widget(self.choice_box)

        self.board_grid = GridLayout(cols=3, spacing=4, size_hint=(1, 0.53), padding=4)
        with self.board_grid.canvas.before:
            self.board_color = Color(1, 1, 1, 1)
            self.board_rect = Rectangle(size=self.board_grid.size, pos=self.board_grid.pos)
        self.board_grid.bind(size=self._update_board, pos=self._update_board)

        self.buttons = []
        for i in range(9):
            btn = Button(text="", font_size="52sp", bold=True, background_normal="",
                         on_press=lambda instance, idx=i: self.player_move(idx))
            self.buttons.append(btn)
            self.board_grid.add_widget(btn)
        self.main.add_widget(self.board_grid)

        bottom = BoxLayout(size_hint=(1, 0.09), spacing=6)
        self.next_btn = Button(text="Next Level", font_size="16sp", bold=True, background_color=(0.2, 0.6, 0.9, 1),
                               on_press=self.next_level, disabled=True)
        restart_btn = Button(text="Restart", font_size="16sp", bold=True, background_color=(0.5, 0.2, 0.7, 1), on_press=self.restart)
        menu_btn = Button(text="Menu", font_size="16sp", bold=True, background_color=(0.7, 0.3, 0.2, 1), on_press=self.go_menu)
        bottom.add_widget(self.next_btn)
        bottom.add_widget(restart_btn)
        bottom.add_widget(menu_btn)
        self.main.add_widget(bottom)

        self.add_widget(self.main)

        self.board = [""] * 9
        self.player = ""
        self.bot = ""
        self.current = ""
        self.game_over = False
        self.game_started = False
        self.is_computer_mode = True

    def _update_bg(self, instance, value):
        self.bg_rect.pos = instance.pos
        self.bg_rect.size = instance.size

    def _update_board(self, instance, value):
        self.board_rect.pos = instance.pos
        self.board_rect.size = instance.size

    def on_pre_enter(self, *args):
        app = App.get_running_app()
        self.is_computer_mode = (app.selected_mode == "Computer Player")
        self.coin_label.text = f"Coins: {app.coins}"
        self.level_label.text = f"Lv.{app.level}"
        self.apply_theme(app.selected_theme)
        self.restart(None)

    def apply_theme(self, theme):
        if theme == "White":
            self.bg_color.rgba = (0.93, 0.93, 0.96, 1)
            self.board_color.rgba = (0.2, 0.2, 0.25, 1)
            cell = (0.88, 0.88, 0.92, 1)
            self.title_label.color = (0.1, 0.1, 0.15, 1)
            self.status.color = (0.15, 0.15, 0.2, 1)
        elif theme == "Black":
            self.bg_color.rgba = (0.09, 0.09, 0.11, 1)
            self.board_color.rgba = (0.7, 0.7, 0.75, 1)
            cell = (0.18, 0.18, 0.22, 1)
            self.title_label.color = (1, 1, 1, 1)
            self.status.color = (0.9, 0.9, 0.95, 1)
        elif theme == "Blue Neon":
            self.bg_color.rgba = (0.05, 0.1, 0.25, 1)
            self.board_color.rgba = (0.2, 0.7, 1, 1)
            cell = (0.1, 0.25, 0.5, 1)
            self.title_label.color = (0.4, 0.9, 1, 1)
            self.status.color = (0.7, 0.95, 1, 1)
        elif theme == "Green Forest":
            self.bg_color.rgba = (0.05, 0.18, 0.1, 1)
            self.board_color.rgba = (0.3, 0.85, 0.4, 1)
            cell = (0.12, 0.35, 0.2, 1)
            self.title_label.color = (0.5, 1, 0.6, 1)
            self.status.color = (0.7, 1, 0.75, 1)
        else:  # Purple
            self.bg_color.rgba = (0.35, 0.12, 0.55, 1)
            self.board_color.rgba = (1, 1, 1, 1)
            cell = (0.42, 0.18, 0.65, 1)
            self.title_label.color = (1, 1, 1, 1)
            self.status.color = (1, 1, 1, 1)

        for btn in self.buttons:
            btn.background_color = cell

    def choose_symbol(self, symbol):
        if self.game_started:
            return

        app = App.get_running_app()
        if self.is_computer_mode and app.coins < 5:
            self.status.text = "Need at least 5 coins to play!"
            return

        self.player = symbol
        self.bot = "O" if symbol == "X" else "X"
        self.current = self.player
        self.game_started = True

        self.btn_x.disabled = True
        self.btn_o.disabled = True

        if self.is_computer_mode:
            self.status.text = f"You: {self.player}   Bot: {self.bot}"
            if random.choice([True, False]):
                self.status.text += "\nBot starts..."
                Clock.schedule_once(lambda dt: self.bot_move(), 0.7)
            else:
                self.status.text += "\nYour turn!"
        else:
            self.status.text = f"P1: {self.player}  |  P2: {self.bot}\nPlayer 1 turn!"

    def player_move(self, index):
        if not self.game_started or self.game_over or self.board[index] != "":
            return

        if not self.is_computer_mode:
            mark = self.current
            self.place_mark(index, mark)

            if self.check_winner(mark):
                winner = "Player 1" if mark == self.player else "Player 2"
                self.end_game(f"{winner} Wins!", True)
                return

            if "" not in self.board:
                self.end_game("It's a Draw!", None)
                return

            self.current = self.bot if self.current == self.player else self.player
            turn = "Player 1" if self.current == self.player else "Player 2"
            self.status.text = f"P1: {self.player}  |  P2: {self.bot}\n{turn} turn!"
            return

        if self.current != self.player:
            return

        self.place_mark(index, self.player)

        if self.check_winner(self.player):
            self.handle_win()
            return

        if "" not in self.board:
            self.end_game("It's a Draw!", None)
            return

        self.current = self.bot
        self.status.text = "Bot is thinking..."
        Clock.schedule_once(lambda dt: self.bot_move(), 0.5)

    def bot_move(self):
        if self.game_over or not self.is_computer_mode:
            return

        move = self.get_best_move()
        self.place_mark(move, self.bot)

        if self.check_winner(self.bot):
            app = App.get_running_app()
            app.coins = max(0, app.coins - 5)
            app.save_data()
            self.coin_label.text = f"Coins: {app.coins}"
            self.end_game("Bot Wins! -5 coins", False)
            return

        if "" not in self.board:
            self.end_game("It's a Draw!", None)
            return

        self.current = self.player
        self.status.text = "Your turn!"

    def place_mark(self, index, mark):
        self.board[index] = mark
        btn = self.buttons[index]
        btn.text = mark
        btn.color = (1, 0.12, 0.12, 1)
        btn.font_size = 12
        Animation(font_size=52, duration=0.18, t='out_back').start(btn)

    def get_best_move(self):
        app = App.get_running_app()

        if app.cheat_mode:
            empty = [i for i in range(9) if self.board[i] == ""]
            return random.choice(empty)

        level = app.selected_difficulty

        for i in range(9):
            if self.board[i] == "":
                self.board[i] = self.bot
                if self.check_winner(self.bot):
                    self.board[i] = ""
                    return i
                self.board[i] = ""

        if level != "Easy":
            for i in range(9):
                if self.board[i] == "":
                    self.board[i] = self.player
                    if self.check_winner(self.player):
                        self.board[i] = ""
                        return i
                    self.board[i] = ""

        if self.board[4] == "" and level in ["Normal", "Medium", "Hard", "Super Hard"]:
            return 4

        if level in ["Medium", "Hard", "Super Hard"]:
            corners = [0, 2, 6, 8]
            random.shuffle(corners)
            for i in corners:
                if self.board[i] == "":
                    return i

        empty = [i for i in range(9) if self.board[i] == ""]
        return random.choice(empty)

    def check_winner(self, player):
        wins = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]
        for a,b,c in wins:
            if self.board[a] == self.board[b] == self.board[c] == player:
                return True
        return False

    def handle_win(self):
        app = App.get_running_app()
        app.exp += 10
        app.coins += 10
        old_level = app.level
        app.level = (app.exp // 10) + 1
        app.save_data()

        self.coin_label.text = f"Coins: {app.coins}"
        self.level_label.text = f"Lv.{app.level}"

        content = BoxLayout(orientation='vertical', padding=15, spacing=10)
        content.add_widget(Label(text="YOU WIN!", font_size="30sp", bold=True, color=(0.2, 0.9, 0.3, 1)))
        content.add_widget(Label(text="+10 EXP", font_size="20sp", bold=True, color=(0.4, 0.8, 1, 1)))
        content.add_widget(Label(text="+10 Coins", font_size="20sp", bold=True, color=(1, 0.85, 0.2, 1)))

        if app.level > old_level:
            rank, stars, _ = get_rank_info(app.level)
            content.add_widget(Label(text=f"Level Up! → Level {app.level}", font_size="18sp", bold=True, color=(1, 0.9, 0.3, 1)))
            content.add_widget(Label(text=f"New Rank: {rank} {stars}", font_size="16sp", bold=True, color=(1, 0.7, 0.3, 1)))

        close_btn = Button(text="Awesome!", size_hint=(1, 0.3), font_size="18sp", bold=True, background_color=(0.2, 0.6, 0.3, 1))
        content.add_widget(close_btn)

        popup = Popup(title="", content=content, size_hint=(0.85, 0.5), auto_dismiss=False)
        close_btn.bind(on_press=popup.dismiss)
        popup.open()

        self.end_game("You Win! +10 EXP +10 Coins", True)
        self.next_btn.disabled = False

    def end_game(self, message, won):
        self.game_over = True
        self.status.text = message

        if won is True:
            for btn in self.buttons:
                anim = Animation(background_color=(0.2, 0.75, 0.3, 1), duration=0.25)
                anim += Animation(background_color=btn.background_color, duration=0.25)
                anim.start(btn)
        elif won is False:
            for btn in self.buttons:
                anim = Animation(background_color=(0.85, 0.2, 0.2, 1), duration=0.25)
                anim += Animation(background_color=btn.background_color, duration=0.25)
                anim.start(btn)

    def next_level(self, instance):
        self.restart(None)
        self.next_btn.disabled = True

    def restart(self, instance):
        self.board = [""] * 9
        self.game_over = False
        self.game_started = False
        self.player = ""
        self.bot = ""
        self.current = ""
        self.next_btn.disabled = True

        for btn in self.buttons:
            btn.text = ""
            btn.font_size = 52
            btn.color = (1, 1, 1, 1)

        self.status.text = "Choose your symbol"
        self.btn_x.disabled = False
        self.btn_o.disabled = False

        app = App.get_running_app()
        self.apply_theme(app.selected_theme)
        self.coin_label.text = f"Coins: {app.coins}"
        self.level_label.text = f"Lv.{app.level}"

    def go_menu(self, instance):
        self.manager.current = "menu"

class TicTacToeApp(App):
    def build(self):
        self.store = JsonStore("ttt_data.json")

        if self.store.exists("data"):
            data = self.store.get("data")
            self.coins = data.get("coins", 50)
            self.last_claim = data.get("last_claim", 0)
            self.exp = data.get("exp", 0)
            self.level = data.get("level", 1)
        else:
            self.coins = 50
            self.last_claim = 0
            self.exp = 0
            self.level = 1

        self.selected_mode = "Computer Player"
        self.selected_difficulty = "Normal"
        self.selected_theme = "Purple"
        self.cheat_mode = False

        sm = ScreenManager()
        sm.add_widget(MenuScreen(name="menu"))
        sm.add_widget(GameScreen(name="game"))
        return sm

    def save_data(self):
        self.store.put("data", coins=self.coins, last_claim=self.last_claim, exp=self.exp, level=self.level)

if __name__ == "__main__":
    TicTacToeApp().run()
