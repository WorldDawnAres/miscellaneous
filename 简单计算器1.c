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
	printf("*       ��ӭʹ�ü򵥼�����!     *\n");
	printf("* ��������Խ��мӡ������ˡ���  *\n");
	printf("*         ���ֻ������㡣        *\n");
	printf("*     ��������ʱ��ע���ʽ��    *\n");
	printf("*   ����ʹ���˸��ɾ���������롣*\n");
	printf("*********************************\n");
	printf("\n");
}

void p()
{
	// ���������ַ���
	printf("��������Ҫ����ı��ʽ������:2+3\n");
	printf("���س�����������,��ESC���˳�����,��C������\n");
}

void get_input(Calculator* c) 
{
	// ���������ַ���
	char input[20]; 
	// ���������ַ���������
	int i = 0; 
	// �������dot�����ڼ�¼�Ƿ���С����
	int dot = 0; 
	// �������sign�����ڼ�¼�Ƿ��з���
	int sign = 0; 
	// �������op_flag�����ڼ�¼�Ƿ��������
	int op_flag = 0;
	// ���ú���p()
	p();
	while (1) 
	{
		//�����û�����
		input[i] = getch(); 
		//����û�������ǻس�
		if (input[i] == ENTER )
		{ 
			//���س�����
			input[i] = '\0'; 
			//�˳�ѭ��
			break;
		}
		//����û��������ESC
		else if (input[i] == ESC )
		{ 
			//��ʾ��ʾ��Ϣ
			printf("\n�����˳�����\n");
			//��ͣ����
			system ("pause");
			//�˳�����
			exit(0);
		}
		//����û�����������
		else if (input[i] == CLEAR || input[i] == CLEAR_UPPER )
		{ 
			//��ʾ��ʾ��Ϣ
			printf("\n�������㱾�μ��㡣\n");
			//��i����Ϊ0
			i = 0; 
			//��dot����Ϊ0
			dot = 0; 
			//��sign����Ϊ0
			sign = 0; 
			//��op_flag����Ϊ0
			op_flag = 0; 
			//ִ��p����
			p();
		}
		//����û���������˸�
		else if (input[i] == BACKSPACE )
		{ 
			//���i����0
			if (i > 0) { 
				//i��1
				i--; 
				//���i���ڵ���0����input[i]��Сд��ĸ����op_flagΪ0
				if (input[i] == '.') 
				{ 
					//��dot��1
					dot--;
				}
				//���input[i]��+-*/����op_flagΪ0
				else if (input[i] == '+' || input[i] == '-') 
				{ 
					//��sign��1
					sign--;
				}
				//���input[i]��+-*/����op_flagΪ0
				else if (input[i] == '+' || input[i] == '-' || input[i] == '*' || input[i] == '/') 
				{ 
					//��op_flag����Ϊ0
					op_flag = 0;
				}
				//����س��ͻ���
				printf("\b \b"); 
			}
		}
		//����û������������
		else if (input[i] >= '0' && input[i] <= '9') 
		{ 
			//��ӡ�û����������
			printf("%c", input[i]);
			//i��1
			i++;
		}
		//����û��������С����
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
			// �����ǰ�ַ��Ƿ����ַ����ҵ�ǰ������־Ϊ0�����ӡ��ǰ�ַ���������ǰ�ַ��ƶ�����һ���ַ�
			if (sign == 0 && op_flag == 0) {
				printf("%c", input[i]);
				i++;
				sign++;
			}
		}
		// �����ǰ�ַ��ǼӼ��˳����ţ����ӡ��ǰ�ַ���������ǰ�ַ��ƶ�����һ���ַ�������������־����Ϊ1
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
	// ��ȡ��������֣�������ת��Ϊ������
	sscanf(input, "%lf%c%lf", &c->num1, &c->op, &c->num2);
}

double calculate(Calculator* c) 
{
	// ����������
	double result=0; 
	// ���ݴ�����������������
	switch (c->op) 
	{ 
	// ����Ǽӷ�����
	case '+':
		result = c->num1 + c->num2;
		break;
	// ����Ǽ�������
	case '-':
		result = c->num1 - c->num2;
		break;
	// ����ǳ˷�����
	case '*':
		result = c->num1 * c->num2;
		break;
	// ����ǳ�������
	case '/':
		// �������Ϊ0�������������Ϣ
		if (c->num2 == 0) 
		{
			printf("����:��������Ϊ�㣡\n");
			break;
		}
		// ���������Ϊ0���������
		result = c->num1 / c->num2;
		break;
	// ���������������������������Ϣ
	default:
		    printf("����:��Ч���������\n");
	        break;
	}
	// ���ؼ�����
	return result; 
}

main() 
{
	// ����һ��Calculator���͵Ķ���c
	Calculator c; 
	// ����menu����
	menu();
	// ѭ��ִ��
	while (1) 
	{
		// ����get_input����
		get_input(&c); 
		// ����calculate����
		double result = calculate(&c); 
		// ������
		printf("������Ϊ:%.2lf\n", result); 
		// ����
		printf("\n");
	}
}