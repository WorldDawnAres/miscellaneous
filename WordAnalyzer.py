import tkinter as tk
from tkinter import filedialog
import os,PyPDF2,nltk,sys,pytesseract
from nltk.tokenize import word_tokenize
from collections import Counter
from pdf2image import convert_from_path
from docx import Document
from collections import Counter
import pandas as pd

def get_resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
#nltk.download('punkt',download_dir=get_resource_path("text/nltk_data"))
nltk.data.path.append(get_resource_path("search/nltk_data"))
folder_path = ''
file_path = ''
dictionary_path = get_resource_path("search/word.txt")

def extract_words_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfFileReader(file)
        text = ""
        for page in range(reader.numPages):
            text += reader.getPage(page).extractText()
    if len(text) < 10:
        images = convert_from_path(pdf_path)
        text = ""
        for i in range(len(images)):
            text += pytesseract.image_to_string(images[i])
    tokens = word_tokenize(text)
    words = [word.lower() for word in tokens if word.isalpha()]
    return words

def extract_words_from_image(image_path):
    text = pytesseract.image_to_string(image_path)
    tokens = word_tokenize(text)
    words = [word.lower() for word in tokens if word.isalpha()]
    return words


def extract_words_from_docx(docx_path):
    doc = Document(docx_path)
    text = ' '.join([paragraph.text for paragraph in doc.paragraphs])
    tokens = word_tokenize(text)
    words = [word.lower() for word in tokens if word.isalpha()]
    return words

def extract_words_from_excel(excel_path):
    df = pd.read_excel(excel_path)
    text = ' '.join(df.values.flatten().astype(str))
    tokens = word_tokenize(text)
    words = [word.lower() for word in tokens if word.isalpha()]
    return words

def extract_words_from_txt(txt_path):
    with open(txt_path, 'r',encoding='utf-8') as file:
        text = file.read()
    tokens = word_tokenize(text)
    words = [word.lower() for word in tokens if word.isalpha()]
    return words

def calculate_word_frequencies(words, dictionary_path):
    word_counts = Counter(words)
    dictionary_words = load_dictionary(dictionary_path)
    group_size = 2000
    num_groups = len(dictionary_words) // group_size + 1
    group_counts = [0]*num_groups
    for word in dictionary_words:
        if word in word_counts:
            group_index = dictionary_words.index(word) // group_size
            group_counts[group_index] += word_counts[word]
    total_words = sum(group_counts)
    frequencies = {f'第{i+1}组({min((i+1)*group_size, len(dictionary_words))}词)': count / total_words * 100 for i, count in enumerate(group_counts)}
    return frequencies

def load_dictionary(path):
    with open(path, 'r') as file:
        return [line.strip().split(' ')[1] for line in file.readlines() if len(line.strip().split(' ')) > 1]

def start_analysis():
    global file_path, folder_path
    if not file_path and not folder_path or not dictionary_path:
        tk.messagebox.showwarning("警告", "请先选择文件或文件夹和字典文件!")
        return
    all_words = []
    if file_path:
        ext = os.path.splitext(file_path)[1]
        if ext == '.pdf':
            all_words.extend(extract_words_from_pdf(file_path))
        elif ext == '.docx':
            all_words.extend(extract_words_from_docx(file_path))
        elif ext == '.xlsx':
            all_words.extend(extract_words_from_excel(file_path))
        elif ext == '.txt':
            all_words.extend(extract_words_from_txt(file_path))
        elif ext in ['.png', '.jpg', '.jpeg']:
            all_words.extend(extract_words_from_image(file_path))
        else:
            tk.messagebox.showwarning("警告", "不支持的文件格式!")
            return
    else:
        for file in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file)
            ext = os.path.splitext(file_path)[1]
            if ext == '.pdf':
                all_words.extend(extract_words_from_pdf(file_path))
            elif ext == '.docx':
                all_words.extend(extract_words_from_docx(file_path))
            elif ext == '.xlsx':
                all_words.extend(extract_words_from_excel(file_path))
            elif ext == '.txt':
                all_words.extend(extract_words_from_txt(file_path))
            elif ext in ['.png', '.jpg', '.jpeg']:
                all_words.extend(extract_words_from_image(file_path))
    frequencies = calculate_word_frequencies(all_words, dictionary_path)
    total_words = sum(frequencies.values())
    listbox.delete(0, tk.END)
    for word, count in frequencies.items():
        listbox.insert(tk.END, f"{word}: {count / total_words * 100:.2f}%")
    file_path = ''
    folder_path = ''
    label_file.config(text="")
    label_folder.config(text="")


def select_folder():
    global folder_path
    folder_path = filedialog.askdirectory()
    if folder_path:
        label_folder.config(text=f"已选择文件夹: {os.path.basename(folder_path)}")
    else:
        label_folder.config(text="未选择文件夹\n请重新选择文件夹")

def select_file():
    global file_path
    file_path = filedialog.askopenfilename(filetypes=[("All files", "*.*")])
    if file_path:
        label_file.config(text=f"已选择文件: {os.path.basename(file_path)}")
    else:
        label_file.config(text="未选择文件\n请重新选择文件")


def select_dictionary():
    global dictionary_path
    new_dictionary_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if new_dictionary_path:  # 只有当用户选择了文件，才更新dictionary_path
        dictionary_path = new_dictionary_path
        label_dictionary.config(text=f"字典文件: {os.path.basename(dictionary_path)}")
    else:
        label_dictionary.config(text="未选择自定义字典文件\n自动使用默认字典")


root = tk.Tk()
root.title("词频分析器")

root.iconphoto(True, tk.PhotoImage(file=get_resource_path("text\icon.jpg")))
frame = tk.Frame(root)
frame.pack(pady=20)
frame1 = tk.Frame(root)
frame1.pack(pady=20)

btn_analyze_single = tk.Button(frame, text="分析单个文件", command=select_file)
btn_analyze_single.pack(side=tk.LEFT, padx=10)

btn_select_folder = tk.Button(frame, text="选择文件夹", command=select_folder)
btn_select_folder.pack(side=tk.LEFT, padx=10)

btn_select_dictionary = tk.Button(frame, text="选择字典文件", command=select_dictionary)
btn_select_dictionary.pack(side=tk.LEFT, padx=10)

btn_start_analysis = tk.Button(frame, text="开始分析", command=start_analysis)
btn_start_analysis.pack(side=tk.LEFT, padx=10)

label_folder = tk.Label(frame1, text="")
label_folder.pack(side=tk.LEFT, padx=10)

label_file = tk.Label(frame1, text="")
label_file.pack(side=tk.LEFT, padx=10)

label_dictionary = tk.Label(frame1, text="自动使用默认词典\n如需使用自定义词典可单击选择字典文件")
label_dictionary.pack(side=tk.LEFT, padx=10)

listbox = tk.Listbox(frame, width=50, height=15)
listbox.pack(side=tk.LEFT)

root.mainloop()