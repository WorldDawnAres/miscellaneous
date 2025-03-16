#include<stdio.h>
#include<conio.h>  //控制台文件头


double num1, num2, answer = 0;
char op;
int i;  //定义一个变量用于存储scanf函数的返回值


void menu()  //定义输出欢迎界面函数
{
	printf("\n");
	printf("*********************************\n");
	printf("* 欢迎使用简单计算器！           *\n");
	printf("* 本程序可以进行加、减、乘、除    *\n");
	printf("* 四种基本运算。                 *\n");
	printf("* 输入数据时请注意格式，          *\n");
	printf("* 可以使用退格键删除错误输入。    *\n");
	printf("*********************************\n");
	printf("\n");
}


double answer_1()  //定义计算函数
{
	while (1)
	{
		printf("请输入两个数字和一个运算符（+、-、*、/):\n");
		printf("请输入你要计算的表达式，例如:2+3\n");
		printf("按回车键结束输入,按ESC键退出程序,按C键清零\n");
			char f = getch();  //获取用户输入的字符
			if (f == 27)  //esc退出程序
			{
				printf("\n你已退出程序。\n");
				break;
			}
			if (f == 'c' || f == 'C')
			{
				printf("\n你已清零本次计算。\n");
				continue;
			}
		i = scanf("%lf %c %lf", &num1, &op, &num2);  //调用scanf函数并赋值给i
		while (getchar() != 10);  //清除用户输入后的缓存
		{
			if (i == 0) //判断i是否为0
			{
				printf("错误：无效的输入！\n");  //输出错误信息
				continue;  
			}
			if (i == 2)
			{
				printf("\n错误:无法计算表达式\n"); //输出错误信息
				continue;
			}
			if (i == 3)
			{
				double ans();
				answer = ans();
				printf("\n计算结果为:%.2lf\n", answer);
			}
			if (i == 4) 
			{
			    printf("\n你已清零本次计算。\n");  //输出错误信息
				continue;
			}
		}
	}
	return 0;
}


double ans()
{
	printf("你输入的表达式是：%.2lf %c %.2lf\n", num1, op, num2); //输出用户输入的表达式
	while (1)
	{
		switch (op)  //加减乘除判断以及验证输入数值合法性
		{
		case'+':
			answer = num1 + num2;
			return answer;
			break;
		case'-':
			answer = num1 - num2;
			return answer;
			break;
		case'*':
			answer = num1 * num2;
			return answer;
			break;
		case'/':
			if (num2 == 0)
			{
				printf("\n错误:除数不能为零！\n");
				answer = 0;  //把answer变量赋值为0
				return answer;
				break;
			}
			else {
				return answer;
				break;
			}
		default:
			printf("\n错误:无效的运算符！\n");
			break;
		}
		printf("\n");
	}
}


main()
{
	menu();  //调用界面函数

	answer_1();  //调用计算函数

	printf("\n");  //换行

}