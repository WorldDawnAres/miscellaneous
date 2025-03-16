import tkinter
import re
import tkinter.messagebox

window = tkinter.Tk() 
window.title("表达式转换和计算") 
window.geometry("480x360")
prec = {"*": 3, "/": 3, "+": 2, "-": 2, "(": 1,")": 1,"#":0}

class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[-1]

    def is_empty(self):
        return self.items == []

    def size(self):
        return len(self.items)
    
#中缀转后缀并返回后缀表达式
def infix_to_postfix(infix):
    # 创建一个空栈
    op_stack = Stack()
    postfix_list = []
    # 将中缀表达式用空格分隔，得到一个单词列表
    token_list = re.split("(\d+\.?\d*|\*|/|\+|-|\(|\))", infix)
    # 去除空字符串
    token_list = [token for token in token_list if token]
    # 从左到右遍历这个列表，对于每个单词：
    for token in token_list:
        # 如果是操作数，直接加入到后缀表达式列表中
        if re.match("\d+\.?\d*", token):
            postfix_list.append(token)
        # 如果是左括号，直接压入栈中
        elif token == "(":
            op_stack.push(token)
        # 如果是右括号，弹出栈中的操作符，直到遇到左括号，将操作符加入到后缀表达式列表中
        elif token == ")":
            top_token = op_stack.pop()
            while top_token != "(":
                postfix_list.append(top_token)
                top_token = op_stack.pop()
        # 如果是操作符，比较它和栈顶操作符的优先级，如果栈不为空且栈顶操作符的优先级大于等于当前操作符，就弹出栈顶操作符，加入到后缀表达式列表中，重复这个过程，直到栈为空或栈顶操作符的优先级小于当前操作符，然后将当前操作符压入栈中
        else:
            while (not op_stack.is_empty()) and (prec[op_stack.peek()] >= prec[token]):
                postfix_list.append(op_stack.pop())
            op_stack.push(token)
    # 当遍历完列表后，将栈中剩余的操作符依次弹出，加入到后缀表达式列表中
    while not op_stack.is_empty():
        postfix_list.append(op_stack.pop())
    return postfix_list

# 计算后缀表达式并返回值
def postfix_eval(postfix):
    operand_stack = Stack()
    # 从左到右遍历后缀表达式列表，对于每个单词：
    for token in postfix:
        # 如果是操作数，将其转换为浮点数，压入栈中
        if re.match("\d+\.?\d*", token):
            operand_stack.push(float(token))
        # 如果是操作符，从栈中弹出两个操作数，注意弹出的顺序，第一个弹出的是右操作数，第二个弹出的是左操作数。然后根据操作符进行相应的运算，将结果压入栈中
        else:
            operand2 = operand_stack.pop()
            operand1 = operand_stack.pop()
            if token == "*":
                result = operand1 * operand2
            elif token == "/":
                result = operand1 / operand2
            elif token == "+":
                result = operand1 + operand2
            else:
                result = operand1 - operand2
            operand_stack.push(result)
    return operand_stack.pop()

# 定义回调函数
def convert_and_calculate():
    try:
        try:
            # 获取输入的中缀表达式
            infix = entry.get()
        except Exception as e:
            tkinter.messagebox.showerror("错误", "获取输入的中缀表达式时出现错误：" + str(e) + "\n请检查你的输入是否正确,是否包含非法字符,是否以'#'开头和结尾。")
            return
        try:
            postfix = infix_to_postfix(infix)
        except Exception as e:
            tkinter.messagebox.showerror("错误", "转换为后缀表达式时出现错误：" + str(e) + "\n请检查你的输入是否正确,是否括号匹配,是否运算符缺失。")
            return
        try:
            result = postfix_eval(postfix)
        except Exception as e:
            tkinter.messagebox.showerror("错误", "计算后缀表达式的值时出现错误：" + str(e) + "\n请检查你的输入是否正确,是否操作数非法,是否除数为零。")
            return
        # 显示后缀表达式和计算结果
        label_postfix.config(text="后缀表达式：" + " ".join(postfix))
        label_result.config(text="计算结果：" + str(result)) # 将计算结果转换为字符串，并显示在标签上
        # 清空列表框
        listbox.delete(0, tkinter.END)
        # 显示栈的变化过程,创建一个临时的栈，用于存储操作符和界限符
        temp_stack = Stack()
        # 初始化栈的容量为表达式的长度
        temp_stack.size = len(infix)
        # 从左到右遍历中缀表达式中的每个字符
        for i in range(len(infix)):
            c = infix[i]
            # 如果是操作数，不影响栈的变化，直接跳过
            if re.match("\d+\.?\d*", c):
                continue
            # 如果是左括号，直接压入栈中，并在列表框中显示栈的内容
            elif c == "(":
                temp_stack.push(c)
                listbox.insert(tkinter.END, "第" + str(i + 1) + "步：" + " ".join(temp_stack.items))
            # 如果是右括号，弹出栈中的操作符，直到遇到左括号，并在列表框中显示栈的内容
            elif c == ")":
                top_token = temp_stack.pop()
                while top_token != "(":
                    listbox.insert(tkinter.END, "第" + str(i + 1) + "步：" + " ".join(temp_stack.items))
                    top_token = temp_stack.pop()
                listbox.insert(tkinter.END, "第" + str(i + 1) + "步：" + " ".join(temp_stack.items))
            # 如果是操作符，比较它和栈顶操作符的优先级，如果栈不为空且栈顶操作符的优先级大于等于当前操作符，就弹出栈顶操作符，并在列表框中显示栈的内容，重复这个过程，直到栈为空或栈顶操作符的优先级小于当前操作符，然后将当前操作符压入栈中，并在列表框中显示栈的内容
            else:
                while (not temp_stack.is_empty()) and (prec[temp_stack.peek()] >= prec[c]):
                    temp_stack.pop()
                    listbox.insert(tkinter.END, "第" + str(i + 1) + "步：" + " ".join(temp_stack.items))
                temp_stack.push(c)
                listbox.insert(tkinter.END, "第" + str(i + 1) + "步：" + " ".join(temp_stack.items))
        # 当遍历完表达式后，将栈中剩余的操作符依次弹出，并在列表框中显示栈的内容
        while not temp_stack.is_empty():
            temp_stack.pop()
            listbox.insert(tkinter.END, "第" + str(len(infix) + 1) + "步：" + " ".join(temp_stack.items))
    except Exception as e:
        tkinter.messagebox.showerror("错误", "显示后缀表达式和计算结果时出现错误：" + str(e))
def show_help():
    message="本程序可以进行正常的加减乘除计算\n主要是将用户输入的表达式转换为后缀表达式,并计算后缀表达式的值\n可输入0-9的数字,可输入字符有+-*/()\n输入时请注意格式,否则会报错提示"
    tkinter.messagebox.showinfo("使用帮助", message)

entry = tkinter.Entry(window)
entry.place(x=20, y=20, width=300, height=30)
button = tkinter.Button(window, text="转换和计算", command=convert_and_calculate)  
button.place(x=340, y=20, width=100, height=30)
button = tkinter.Button(window, text="程序使用帮助", command=show_help)  
button.place(x=340, y=60, width=100, height=30)
label_postfix = tkinter.Label(window, text="后缀表达式:") 
label_postfix.place(x=20, y=90, width=440, height=30)
label_result = tkinter.Label(window, text="计算结果为:") 
label_result.place(x=20, y=120, width=440, height=30)
listbox = tkinter.Listbox(window) 
listbox.place(x=20, y=170, width=440, height=170)
window.mainloop()