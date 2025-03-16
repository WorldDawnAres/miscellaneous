import tkinter as tk
from tkinter import filedialog, messagebox
import pyperclip
import os,sys

# 全局变量来保存文件路径
selected_file_path = None

def get_resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# 默认文件路径
default_file_path = get_resource_path("same/text.txt")
#print("默认文件路径:", default_file_path)

def read_file_and_find_matches():
    global selected_file_path
    
    # 如果没有选择文件，则使用默认文件
    if not selected_file_path:
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "没有选择文件，使用默认文件进行匹配。\n")
        selected_file_path = default_file_path  # 设置默认文件路径
    
    # 从用户选择的文本文件（或默认文件）读取内容
    with open(selected_file_path, "r", encoding="utf-8") as file:
        content = file.read()
    
    # 获取剪贴板内容
    selected_text = pyperclip.paste()

    # 查找匹配内容
    matches = []
    
    # 按照空行拆分文件内容
    content_blocks = content.split("\n\n")  # Split by two consecutive newlines to separate blocks
    
    for block in content_blocks:
        if selected_text in block:
            # 如果在这个块中找到关键字，直接添加该块
            matches.append(block.strip())  # Strip extra leading/trailing whitespace
    
    # 更新文本框以显示匹配内容
    result_text.delete(1.0, tk.END)  # 清空文本框
    if matches:
        result_text.insert(tk.END, "\n\n".join(matches))
    else:
        result_text.insert(tk.END, "没有找到匹配的内容。")

def open_file_dialog():
    global selected_file_path

    # 打开文件选择对话框，让用户选择文件
    selected_file_path = filedialog.askopenfilename(
        title="选择文本文件", 
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    
    if selected_file_path:
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, f"已选择文件: {selected_file_path}\n现在你可以点击获取匹配内容按钮。")

def show_help():
    # 显示帮助信息的弹窗
    help_message = (
        "程序操作指南:\n\n"
        "1. 点击 '选择文件' 按钮选择一个文本文件，或者不添加文件，程序将默认使用指定的文件。\n"
        "2. 在浏览器答题时用鼠标选中你要搜索的关键词并右键单击复制。\n"
        "3. 点击 '获取匹配内容' 按钮，程序会查找文本文件中包含剪贴板内容的部分。\n"
        "4. 程序会显示匹配的内容，如果没有找到任何匹配项，将显示相应的提示。\n"
        "5. 在程序输出部分直接把需要的答案复制然后粘贴即可"
    )
    messagebox.showinfo("帮助", help_message)

def create_gui():
    global result_text, selected_file_path

    # 创建主窗口
    root = tk.Tk()
    root.title("内容匹配器")

    # 创建选择文件按钮
    open_file_button = tk.Button(root, text="选择文件", command=open_file_dialog)
    open_file_button.pack(pady=10)

    # 创建按钮用于获取匹配内容
    match_button = tk.Button(root, text="获取匹配内容", command=read_file_and_find_matches)
    match_button.pack(pady=10)

    # 创建帮助按钮
    help_button = tk.Button(root, text="帮助", command=show_help)
    help_button.pack(pady=10)

    # 创建文本框以显示结果
    result_text = tk.Text(root, wrap=tk.WORD, width=60, height=20)
    result_text.pack(pady=10)

    # 启动时默认加载文件，如果没有用户选择的文件
    if not selected_file_path and os.path.exists(default_file_path):
        selected_file_path = default_file_path
        result_text.insert(tk.END, f"未选择文件，已加载默认文件,现在你可以点击帮助按钮查看程序使用方法。 \n")
        #result_text.insert(tk.END, f"未选择文件，已加载默认文件: {default_file_path}\n")

    # 启动 GUI
    root.mainloop()

if __name__ == "__main__":
    create_gui()
