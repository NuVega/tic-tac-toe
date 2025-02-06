import tkinter as tk
from tkinter import ttk, messagebox

# Основное окно
window = tk.Tk()
window.title("Крестики-нолики")
window.geometry("400x500")
window.resizable(False, False)
window.configure(bg="#2C2F33")  # Тёмный фон

# Настройка стилей через ttk
style = ttk.Style()
style.theme_use('clam')  # Базовая тема, которую можно кастомизировать

# Стиль для кнопок
style.configure("TButton",
                background="#7289DA",
                foreground="white",
                font=("Helvetica", 14, "bold"),
                padding=10)
style.map("TButton", background=[("active", "#5B6EAE")])
# Стиль для меток
style.configure("TLabel",
                background="#2C2F33",
                foreground="white",
                font=("Helvetica", 14))
style.configure("Header.TLabel",
                font=("Helvetica", 18, "bold"),
                background="#2C2F33",
                foreground="white")

# Глобальные переменные игры
current_player = None  # Будет установлен в начале раунда
player_choice = tk.StringVar(value="X")  # Выбор игрока (по умолчанию "X")
wins = {"X": 0, "O": 0}
game_active = False  # Флаг: раунд активен или нет
board = []  # Игровое поле (список строк с кнопками)

def start_round():
    """Начинает новый раунд: очищает поле, устанавливает первого игрока и скрывает кнопку старта."""
    global current_player, game_active
    for i in range(3):
        for j in range(3):
            board[i][j].config(text="", state="normal", bg="#99AAB5", relief="flat")
    current_player = player_choice.get()  # Первый ход согласно выбору
    game_active = True
    status_label.config(text=f"Ход: {current_player}")
    start_button.pack_forget()  # Скрываем кнопку старта

def end_round():
    """Заканчивает раунд и возвращает кнопку старта для следующего раунда."""
    global game_active
    game_active = False
    start_button.pack(pady=5)

def update_status():
    """Обновляет надписи с текущим ходом и счётом."""
    status_label.config(text=f"Ход: {current_player}")
    score_label.config(text=f"Счёт – X: {wins['X']}   O: {wins['O']}")

def check_winner():
    """Проверяет наличие победителя. Если есть победитель, возвращает 'X' или 'O', иначе None."""
    # Проверка строк
    for i in range(3):
        if board[i][0]["text"] != "" and board[i][0]["text"] == board[i][1]["text"] == board[i][2]["text"]:
            return board[i][0]["text"]
    # Проверка столбцов
    for j in range(3):
        if board[0][j]["text"] != "" and board[0][j]["text"] == board[1][j]["text"] == board[2][j]["text"]:
            return board[0][j]["text"]
    # Проверка диагоналей
    if board[0][0]["text"] != "" and board[0][0]["text"] == board[1][1]["text"] == board[2][2]["text"]:
        return board[0][0]["text"]
    if board[0][2]["text"] != "" and board[0][2]["text"] == board[1][1]["text"] == board[2][0]["text"]:
        return board[0][2]["text"]
    return None

def board_full():
    """Возвращает True, если все клетки заполнены."""
    for i in range(3):
        for j in range(3):
            if board[i][j]["text"] == "":
                return False
    return True

def on_click(row, col):
    """Обработчик нажатия на клетку игрового поля."""
    global current_player, wins, game_active
    if not game_active:
        return  # Если игра не активна, клики не обрабатываются
    if board[row][col]["text"] != "":
        return  # Если клетка уже занята, ничего не делаем

    # Устанавливаем символ и отключаем клетку
    board[row][col].config(text=current_player, state="disabled", disabledforeground="white")
    winner = check_winner()
    if winner:
        wins[winner] += 1
        update_status()
        messagebox.showinfo("Игра окончена", f"Победитель: {winner}!")
        if wins[winner] == 3:
            messagebox.showinfo("Турнир окончен", f"Игрок {winner} выиграл турнир!")
            reset_scores()
        end_round()
        return
    elif board_full():
        messagebox.showinfo("Игра окончена", "Ничья!")
        end_round()
        return

    # Переключаем игрока
    current_player = "O" if current_player == "X" else "X"
    update_status()

def reset_scores():
    """Сбрасывает счет побед."""
    global wins
    wins = {"X": 0, "O": 0}
    update_status()

# Верхняя панель: выбор символа, статус и кнопки управления
top_frame = tk.Frame(window, bg="#2C2F33")
top_frame.pack(pady=10)

# Панель выбора символа
choice_frame = tk.Frame(top_frame, bg="#2C2F33")
choice_frame.pack(pady=5)
ttk.Label(choice_frame, text="Выберите символ: ").pack(side=tk.LEFT, padx=5)
rb_x = ttk.Radiobutton(choice_frame, text="Крестик", variable=player_choice, value="X")
rb_o = ttk.Radiobutton(choice_frame, text="Нолик", variable=player_choice, value="O")
rb_x.pack(side=tk.LEFT, padx=5)
rb_o.pack(side=tk.LEFT, padx=5)

# Метки статуса и счета
status_label = ttk.Label(top_frame, text="Сейчас ходит:", style="Header.TLabel")
status_label.pack(pady=5)
score_label = ttk.Label(top_frame, text="Счёт – X: 0   O: 0")
score_label.pack(pady=5)

# Кнопка "Начать игру" (появляется, если раунд не активен)
start_button = ttk.Button(top_frame, text="Начать игру", command=start_round)
start_button.pack(pady=5)

# Кнопка сброса турнира (сброс счета)
reset_button = ttk.Button(top_frame, text="Сбросить игру", command=lambda: [reset_scores(), end_round(), start_round()])
reset_button.pack(pady=5)

# Поле для игры
board_frame = tk.Frame(window, bg="#2C2F33")
board_frame.pack(pady=10)
for i in range(3):
    row_buttons = []
    row = []
    for j in range(3):
        btn = tk.Button(board_frame, text="", font=("Helvetica", 24, "bold"),
                        width=4, height=2, bg="#99AAB5", relief="flat",
                        command=lambda r=i, c=j: on_click(r, c))
        btn.grid(row=i, column=j, padx=5, pady=5)
        row.append(btn)
    board.append(row)

window.mainloop()