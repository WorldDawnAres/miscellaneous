#include<stdio.h>
#include<conio.h>  //����̨�ļ�ͷ


double num1, num2, answer = 0;
char op;
int i;  //����һ���������ڴ洢scanf�����ķ���ֵ


void menu()  //���������ӭ���溯��
{
	printf("\n");
	printf("*********************************\n");
	printf("* ��ӭʹ�ü򵥼�������           *\n");
	printf("* ��������Խ��мӡ������ˡ���    *\n");
	printf("* ���ֻ������㡣                 *\n");
	printf("* ��������ʱ��ע���ʽ��          *\n");
	printf("* ����ʹ���˸��ɾ���������롣    *\n");
	printf("*********************************\n");
	printf("\n");
}


double answer_1()  //������㺯��
{
	while (1)
	{
		printf("�������������ֺ�һ���������+��-��*��/):\n");
		printf("��������Ҫ����ı��ʽ������:2+3\n");
		printf("���س�����������,��ESC���˳�����,��C������\n");
			char f = getch();  //��ȡ�û�������ַ�
			if (f == 27)  //esc�˳�����
			{
				printf("\n�����˳�����\n");
				break;
			}
			if (f == 'c' || f == 'C')
			{
				printf("\n�������㱾�μ��㡣\n");
				continue;
			}
		i = scanf("%lf %c %lf", &num1, &op, &num2);  //����scanf��������ֵ��i
		while (getchar() != 10);  //����û������Ļ���
		{
			if (i == 0) //�ж�i�Ƿ�Ϊ0
			{
				printf("������Ч�����룡\n");  //���������Ϣ
				continue;  
			}
			if (i == 2)
			{
				printf("\n����:�޷�������ʽ\n"); //���������Ϣ
				continue;
			}
			if (i == 3)
			{
				double ans();
				answer = ans();
				printf("\n������Ϊ:%.2lf\n", answer);
			}
			if (i == 4) 
			{
			    printf("\n�������㱾�μ��㡣\n");  //���������Ϣ
				continue;
			}
		}
	}
	return 0;
}


double ans()
{
	printf("������ı��ʽ�ǣ�%.2lf %c %.2lf\n", num1, op, num2); //����û�����ı��ʽ
	while (1)
	{
		switch (op)  //�Ӽ��˳��ж��Լ���֤������ֵ�Ϸ���
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
				printf("\n����:��������Ϊ�㣡\n");
				answer = 0;  //��answer������ֵΪ0
				return answer;
				break;
			}
			else {
				return answer;
				break;
			}
		default:
			printf("\n����:��Ч���������\n");
			break;
		}
		printf("\n");
	}
}


main()
{
	menu();  //���ý��溯��

	answer_1();  //���ü��㺯��

	printf("\n");  //����

}