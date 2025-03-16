#include <stdio.h>
#include <stdlib.h>
#include <conio.h>

#define ESC 27
#define BACKSPACE '\b'
#define ENTER '\r'
#define CLEAR 'c'
#define CLEAR_UPPER 'C'

typedef struct 
{
	double num1; 
	double num2; 
	char op; 
} Calculator;

void menu()  
{
	printf("\n");
	printf("*********************************\n");
	printf("*       欢迎使用简单计算器!     *\n");
	printf("* 本程序可以进行加、减、乘、除  *\n");
	printf("*         四种基本运算。        *\n");
	printf("*     输入数据时请注意格式，    *\n");
	printf("*   可以使用退格键删除错误输入。*\n");
	printf("*********************************\n");
	printf("\n");
}

void p()
{
	// 定义输入字符串
	printf("请输入你要计算的表达式，例如:2+3\n");
	printf("按回车键结束输入,按ESC键退出程序,按C键清零\n");
}

void get_input(Calculator* c) 
{
	// 定义输入字符串
	char input[20]; 
	// 定义输入字符串的索引
	int i = 0; 
	// 定义变量dot，用于记录是否有小数点
	int dot = 0; 
	// 定义变量sign，用于记录是否有符号
	int sign = 0; 
	// 定义变量op_flag，用于记录是否有运算符
	int op_flag = 0;
	// 调用函数p()
	p();
	while (1) 
	{
		//接收用户输入
		input[i] = getch(); 
		//如果用户输入的是回车
		if (input[i] == ENTER )
		{ 
			//将回车换行
			input[i] = '\0'; 
			//退出循环
			break;
		}
		//如果用户输入的是ESC
		else if (input[i] == ESC )
		{ 
			//显示提示信息
			printf("\n你已退出程序。\n");
			//暂停程序
			system ("pause");
			//退出程序
			exit(0);
		}
		//如果用户输入的是清除
		else if (input[i] == CLEAR || input[i] == CLEAR_UPPER )
		{ 
			//显示提示信息
			printf("\n你已清零本次计算。\n");
			//将i重置为0
			i = 0; 
			//将dot重置为0
			dot = 0; 
			//将sign重置为0
			sign = 0; 
			//将op_flag重置为0
			op_flag = 0; 
			//执行p函数
			p();
		}
		//如果用户输入的是退格
		else if (input[i] == BACKSPACE )
		{ 
			//如果i大于0
			if (i > 0) { 
				//i减1
				i--; 
				//如果i大于等于0，且input[i]是小写字母，且op_flag为0
				if (input[i] == '.') 
				{ 
					//将dot减1
					dot--;
				}
				//如果input[i]是+-*/，且op_flag为0
				else if (input[i] == '+' || input[i] == '-') 
				{ 
					//将sign减1
					sign--;
				}
				//如果input[i]是+-*/，且op_flag为0
				else if (input[i] == '+' || input[i] == '-' || input[i] == '*' || input[i] == '/') 
				{ 
					//将op_flag重置为0
					op_flag = 0;
				}
				//清除回车和换行
				printf("\b \b"); 
			}
		}
		//如果用户输入的是数字
		else if (input[i] >= '0' && input[i] <= '9') 
		{ 
			//打印用户输入的数字
			printf("%c", input[i]);
			//i加1
			i++;
		}
		//如果用户输入的是小数点
		else if (input[i] == '.') 
		{ 
			if (dot == 0 && op_flag == 0) {
				printf("%c", input[i]);
				i++;
				dot++;
			}
		}
		else if (input[i] == '+' || input[i] == '-') 
		{ 
			// 如果当前字符是符号字符，且当前操作标志为0，则打印当前字符，并将当前字符移动到下一个字符
			if (sign == 0 && op_flag == 0) {
				printf("%c", input[i]);
				i++;
				sign++;
			}
		}
		// 如果当前字符是加减乘除符号，则打印当前字符，并将当前字符移动到下一个字符，并将操作标志设置为1
		else if (input[i] == '+' || input[i] == '-' || input[i] == '*' || input[i] == '/') 
		{
			if (op_flag == 0) 
			{
				printf("%c", input[i]);
				i++;
				op_flag = 1;
				dot = 0;
				sign = 0;
			}
		}
	}
	printf("\n");
	// 读取输入的数字，并将其转换为浮点数
	sscanf(input, "%lf%c%lf", &c->num1, &c->op, &c->num2);
}

double calculate(Calculator* c) 
{
	// 定义结果变量
	double result=0; 
	// 根据传入的运算符，计算结果
	switch (c->op) 
	{ 
	// 如果是加法运算
	case '+':
		result = c->num1 + c->num2;
		break;
	// 如果是减法运算
	case '-':
		result = c->num1 - c->num2;
		break;
	// 如果是乘法运算
	case '*':
		result = c->num1 * c->num2;
		break;
	// 如果是除法运算
	case '/':
		// 如果除数为0，则输出错误信息
		if (c->num2 == 0) 
		{
			printf("错误:除数不能为零！\n");
			break;
		}
		// 如果除数不为0，则计算结果
		result = c->num1 / c->num2;
		break;
	// 如果是其他运算符，则输出错误信息
	default:
		    printf("错误:无效的运算符！\n");
	        break;
	}
	// 返回计算结果
	return result; 
}

main() 
{
	// 创建一个Calculator类型的对象c
	Calculator c; 
	// 调用menu函数
	menu();
	// 循环执行
	while (1) 
	{
		// 调用get_input函数
		get_input(&c); 
		// 调用calculate函数
		double result = calculate(&c); 
		// 输出结果
		printf("计算结果为:%.2lf\n", result); 
		// 换行
		printf("\n");
	}
}