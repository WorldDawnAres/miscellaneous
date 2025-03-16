import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import random
import os

def load_words(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    words = {}
    for line in lines:
        parts = line.strip().split(':')
        if len(parts) >= 4:
            index = parts[0]
            word = parts[1]
            pos = parts[2]
            meanings = parts[3].split(';')
            words[index] = (word, pos, meanings)
    return words

def load_known_words(filename):
    if not os.path.exists(filename):
        open(filename, 'w', encoding='utf-8').close()
    with open(filename, 'r', encoding='utf-8') as file:
        known_words = file.read().splitlines()
    return known_words

def save_known_words(filename, known_words):
    with open(filename, 'w', encoding='utf-8') as file:
        for word in known_words:
            file.write(word + '\n')

def get_choices(correct_pos, correct_meanings, all_meanings):
    choices = [correct_pos + ':' + random.choice(correct_meanings)]
    while len(choices) < 4:
        random_meaning = random.choice(all_meanings)
        if random_meaning not in choices:
            choices.append(random_meaning)
    random.shuffle(choices)
    return choices, correct_pos + ':' + correct_meanings[0]

def load_error_words(filename):
    if not os.path.exists(filename):
        open(filename, 'w', encoding='utf-8').close()
    with open(filename, 'r', encoding='utf-8') as file:
        error_words = file.read().splitlines()
    return error_words

def save_error_words(filename, error_words):
    with open(filename, 'w', encoding='utf-8') as file:
        for word in error_words:
            file.write(word + '\n')

def check_answer(user_choice, choices, correct_choice):
    if choices[ord(user_choice) - 97] == correct_choice:
        result_label.config(text="正确！🎉")
        if str(index - 1) in error_words:
            if str(index - 1) in corrected_words:
                known_words.append(str(index - 1))
                save_known_words('known_words.txt', known_words)
                corrected_words.remove(str(index - 1))
                save_corrected_words('corrected_words.txt', corrected_words)
            else:
                corrected_words.append(str(index - 1))
                save_corrected_words('corrected_words.txt', corrected_words)
        else:
            known_words.append(str(index - 1))
            save_known_words('known_words.txt', known_words)
    else:
        result_label.config(text=f"错误。正确答案是: {correct_choice}")
        error_words.append(str(index - 1))
        save_error_words('error_words.txt', error_words)
    update_ui()


def update_ui():
    global index
    while str(index) in known_words:
        index += 1
    word, pos, correct_meanings = words[str(index)]
    word_label.config(text=f"序号: {index} \n单词: {word}")

    choices, correct_choice = get_choices(pos, correct_meanings, all_meanings)
    for i, choice in enumerate(choices, start=1):
        buttons[i-1].config(text=f"{chr(96+i)}. {choice}", command=lambda i=i: check_answer(chr(96+i), choices, correct_choice))
    index += 1

def know_word():
    known_words.append(str(index - 1))
    save_known_words('known_words.txt', known_words)
    update_ui()

def error_words():
    error_words.append(str(index - 1))
    save_error_words('error_words.txt', error_words)
    update_ui()

def load_corrected_words(filename):
    if not os.path.exists(filename):
        open(filename, 'w', encoding='utf-8').close()
    with open(filename, 'r', encoding='utf-8') as file:
        corrected_words = file.read().splitlines()
    return corrected_words

def save_corrected_words(filename, corrected_words):
    with open(filename, 'w', encoding='utf-8') as file:
        for word in corrected_words:
            file.write(word + '\n')

def switch_theme():
    global dark_theme
    dark_theme = not dark_theme
    if dark_theme:
        window.configure(background='brown')
        style.theme_use('alt')
    else:
        window.configure(background='white')

def select_file():
    global words, all_meanings, index
    filename = filedialog.askopenfilename(filetypes=[('Text Files', '*.txt')])
    if filename:
        words = load_words(filename)
        all_meanings = [pos + ':' + meaning for _, (_, pos, meanings) in words.items() for meaning in meanings]
        index = 1
        update_ui()

def main():
    global words, all_meanings, window, word_label, buttons, result_label, index, known_words, dark_theme, style, error_words, corrected_words
    words = load_words('./words/word.txt') 
    known_words = load_known_words('known_words.txt')
    error_words = load_error_words('error_words.txt')
    corrected_words = load_corrected_words('corrected_words.txt')
    all_meanings = [pos + ':' + meaning for _, (_, pos, meanings) in words.items() for meaning in meanings] 
    window = tk.Tk()
    window.title("快速背单词")
    window.geometry("700x300")
    style = ttk.Style(window)
    dark_theme = False
    word_label = ttk.Label(window)
    buttons = [ttk.Button(window) for _ in range(4)]
    result_label = ttk.Label(window)
    known_button = ttk.Button(window, text="我会这个单词", command=know_word)
    unknown_button = ttk.Button(window, text="我不会这个单词", command=update_ui)
    theme_button = ttk.Button(window, text="切换主题", command=switch_theme)
    file_button = ttk.Button(window, text="选择单词文件", command=select_file)
    word_label.pack()
    for button in buttons:
        button.pack()
    known_button.pack()
    unknown_button.pack()
    theme_button.pack()
    file_button.pack()
    result_label.pack()
    index = 1
    update_ui()
    window.mainloop()
    print("所有单词已完成。")

if __name__ == "__main__":
    main()