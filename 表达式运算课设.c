#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#define MAX_SIZE 100
typedef struct {
    float items[MAX_SIZE];
    int top;
} Stack;
void initialize(Stack* stack) {
    stack->top = -1;
}
void push(Stack* stack, float item) {
    if (stack->top == MAX_SIZE - 1) {
        printf("ջ����\n");
        return;
    }
    stack->items[++stack->top] = item;
}
float pop(Stack* stack) {
    if (stack->top == -1) {
        printf("ջ����\n");
        return 0;
    }
    return stack->items[stack->top--];
}
float peek(Stack* stack) {
    if (stack->top == -1) {
        printf("ջΪ��\n");
        return 0;
    }
    return stack->items[stack->top];
}
int isEmpty(Stack* stack) {
    return stack->top == -1;
}
int isOperand(char ch) {
    if (isdigit(ch)) {
        return 1;
    }
    if (ch == '-') {
        int i = 0;
        int parenthesesCount = 0;
        char expression[MAX_SIZE];
        while (expression[i] != '\0') {
            if (expression[i] == '(') {
                parenthesesCount++;
            } else if (expression[i] == ')') {
                parenthesesCount--;
            } else if (expression[i] == ch) {
                break;
            }
            i++;
        }
        if (parenthesesCount > 0 && isdigit(expression[i + 1])) {
            return 1;
        }
    }
    return 0;
}
int isOperator(char ch) {
    return (ch == '+' || ch == '-' || ch == '*' || ch == '/');
}
int getPrecedence(char ch) {
    switch (ch) {
        case '+':
        case '-':
            return 1;
        case '*':
        case '/':
            return 2;
        default:
            return 0;
    }
}
void infixToPostfix(char* infix, char* postfix) {
    Stack stack;
    initialize(&stack);
    int i, j;
    for (i = 0, j = 0; infix[i] != '\0'; i++) {
        char ch = infix[i];
        if (ch == ' ') {
            continue;
        }
        if (isOperand(ch)) {
            if (ch == '-') {
                postfix[j++] = ch;
                i++;
                ch = infix[i];
            }
            while (isOperand(infix[i])) {
                postfix[j++] = infix[i++];
            }
            postfix[j++] = ' ';
            i--;
        } else if (isOperator(ch)) {
            while (!isEmpty(&stack) && getPrecedence(peek(&stack)) >= getPrecedence(ch)) {
                postfix[j++] = pop(&stack);
                postfix[j++] = ' ';
            }
            push(&stack, ch);
        } else if (ch == '(') {
            push(&stack, ch);
        } else if (ch == ')') {
            while (!isEmpty(&stack) && peek(&stack) != '(') {
                postfix[j++] = pop(&stack);
                postfix[j++] = ' ';
            }
            if (!isEmpty(&stack) && peek(&stack) != '(') {
                printf("��Ч�ı��ʽ\n");
                return;
            }
            pop(&stack);
        } else {
            printf("��Ч���ַ�: %c\n", ch);
            return;
        }
    }
    while (!isEmpty(&stack)) {
        if (peek(&stack) == '(') {
            printf("��Ч�ı��ʽ\n");
            return;
        }
        postfix[j++] = pop(&stack);
        postfix[j++] = ' ';
    }
    postfix[j] = '\0';
}
float evaluatePostfix(char* postfix) {
    Stack stack;
    initialize(&stack);
    int i;
    for (i = 0; postfix[i] != '\0'; i++) {
        char ch = postfix[i];
        if (ch == ' ') {
            continue;
        }
        if (isOperand(ch)) {
            float num = 0;
            int sign = 1;
            if (ch == '-') {
                // ������
                sign = -1;
                i++;
                ch = postfix[i];
            }
            while (isOperand(postfix[i])) {
                num = num * 10 + (postfix[i] - '0');
                i++;
            }
            num = num * sign;
            push(&stack, num);
            i--;
        } else if (isOperator(ch)) {
            if (isEmpty(&stack)) {
                printf("��Ч�ı��ʽ\n");
                return 0;
            }
            float operand2 = pop(&stack);
            if (isEmpty(&stack)) {
                printf("��Ч�ı��ʽ");
                return 0;
            }
            float operand1 = pop(&stack);
            float result;
            if (ch == '/' && operand2 == 0) {
                printf("��������Ϊ��");
                return 0;
            }
            switch (ch) {
                case '+':
                    result = operand1 + operand2;
                    break;
                case '-':
                    result = operand1 - operand2;
                    break;
                case '*':
                    result = operand1 * operand2;
                    break;
                case '/':
                    result = operand1 / operand2;
                    break;
            }
            push(&stack, result);
            printf("ջ: ");
            int j;
            for (j = 0; j <= stack.top; j++) {
                printf("%.2f ", stack.items[j]);
            }
            printf("\n");
            printf("��%d��: %c %.2f %.2f = %.2f\n", i + 1, ch, operand1, operand2, result);
        }
    }
    if (isEmpty(&stack)) {
        printf("��Ч�ı��ʽ\n");
        return 0;
    }
    return pop(&stack);
}

void menu() {
    printf("\n");
    printf("*********************************\n");
    printf("* ��ӭʹ�ñ��ʽ��������        *\n");
    printf("* ��������Խ��мӡ������ˡ���  *\n");
    printf("* ���ֻ������㡣                *\n");
    printf("* ��������ʱ��ע���ʽ��        *\n");
    printf("* ����ʹ���˸��ɾ���������롣  *\n");
    printf("*********************************\n");
    printf("\n");
    printf("*********************************************************************************\n");
    printf("*����������:                                                                    *\n");
    printf("*����һ����׺���ʽ���м��㡣���ʽ���԰�������(0-9)�������(+��-��*��/)�����š�*\n");
    printf("*����:2 + (3 * 4)��                                                             *\n");
    printf("*���븺��ʱ��Ҫ��(0-����)��ʽ����,����-3�ڱ������а�(0-3)���롣                 *\n");
    printf("*���� 'exit' �˳�����                                                         *\n");
    printf("*********************************************************************************\n");
    printf("\n");
}
int isExpressionValid(char* expression) {
    int i;
    int len = strlen(expression);
    if (len == 0) {
        printf("���ʽΪ��\n");
        return 0;
    }
    int parenthesesCount = 0;
    for (i = 0; i < len; i++) {
        char ch = expression[i];
        if (ch == '(') {
            parenthesesCount++;
        } else if (ch == ')') {
            parenthesesCount--;
            if (parenthesesCount < 0) {
                printf("��Ч�ı��ʽ\n");
                return 0;
            }
        } else if (ch != ' ' && !isOperand(ch) && !isOperator(ch)) {
            printf("��Ч���ַ�: %c\n", ch);
            return 0;
        }
    }
    if (parenthesesCount != 0) {
        printf("��Ч�ı��ʽ\n");
        return 0;
    }
    return 1;
}
void clearInputBuffer() {
    int c;
    while ((c = getchar()) != '\n' && c != EOF) {}
}
int main() {
    char expression[MAX_SIZE];
    char postfix[MAX_SIZE];
    menu();
    while (1) {
        printf("������ʽ: ");
        fgets(expression, sizeof(expression), stdin);
        expression[strcspn(expression, "\n")] = '\0';
        if (strcmp(expression, "exit") == 0) {
            break;
        }
        if (!isExpressionValid(expression)) {
            continue;
        }
        if (strlen(expression) == 1 && isOperand(expression[0])) {
            printf("��Ч�ı��ʽ\n");
            continue;
        }
        infixToPostfix(expression, postfix);
        if (strlen(postfix) > 0) {
            float result = evaluatePostfix(postfix);
            if (result != 0) {
                printf("��׺���ʽ: %s\n", postfix);
                printf("���: %.2f\n", result);
            }
            printf("\n");
        }
    }
    return 0;
}