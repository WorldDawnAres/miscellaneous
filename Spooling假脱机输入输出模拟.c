#include "stdio.h"
#include "stdlib.h"
#include "time.h"

#define PROCESSNUM 2   // ������̸���
#define OUTBUFFERNUM  30  // ������洢�ֽڸ���
#define REQBLOCKNUM   10
#define T1   3          // �����û�����0Ҫ������ļ���T1
#define T2   3          // �����û�����1Ҫ������ļ���T2

struct pcb {
    int id;     // ���̱�ʶ
    int status; // ״̬0Ϊ��ִ��̬��1Ϊ�ȴ�״̬��2Ϊ������գ�3Ϊ����̬
    int length; // �������
} PCB[PROCESSNUM + 1];

struct reqblock {
    int reqid;   // Ҫ������Ľ���
    int tname;
    int length;  // �������
    int addr;    // ����׵�ַ
} ReqBlock[REQBLOCKNUM];

struct BUFFER {
    int buf[OUTBUFFERNUM];   // �����������
    int usedNum;             // �������������ʹ�õ���Ŀ
    int head;                // ָʾ��������п��׵�ַ
} OutBuffer[PROCESSNUM];

int C3 = 10;              // ��ǰϵͳʣ������������Ϣ���������ֵΪ10
int n_out = 0, n_in = 0;  // ָʾ��ǰʹ�õ���������
int t1 = 0;               // ��ʱ������¼�û�������������ļ�����
int t2 = 0;
int t_num[2][10];

void init(int a, int b, int c, int d, int e, int f) {
    int i, j;
    for (i = 0; i < PROCESSNUM; i++) {
        OutBuffer[i].head = 0;
        OutBuffer[i].usedNum = 0;
        for (j = 0; j < OUTBUFFERNUM; j++)
            OutBuffer[i].buf[j] = 0;
    }
    for (i = 0; i < REQBLOCKNUM; i++) {
        ReqBlock[i].reqid = -1;
        ReqBlock[i].length = 0;
        ReqBlock[i].addr = 0;
    }
    for (i = 0; i < PROCESSNUM + 1; i++) {
        PCB[i].id = i;
        PCB[i].status = 0;
        PCB[i].length = 0;
    }
    t_num[0][0] = a;
    t_num[0][1] = b;
    t_num[0][2] = c;
    t_num[1][0] = d;
    t_num[1][1] = e;
    t_num[1][2] = f;
}

void request(int i) {
    printf("===============================================================================\n");
    printf("����: %d ����request���̣�д��Ľ��̿����ΪReqBlock[%d]\n", i, n_in);

    if (C3 == 0) {
        PCB[i].status = 1;
        printf("û�п��е�����飬����״̬��1\n");
        return;
    }
    C3--;

    int j, length = 0;
    int k;
    int maxLength = t_num[i][i == 0 ? t1 : t2];
    int head = OutBuffer[i].head;

    for (k = 0; k < maxLength; k++) {
        j = (rand() % 10) + 1;
        if (k == 20) {
            printf("\n���ļ���������20����������\n");
            t_num[i][i == 0 ? t1 : t2] -= 20;
            PCB[i].status = 1;
            break;
        }
        OutBuffer[i].buf[(head + k) % OUTBUFFERNUM] = j;
        printf("%d ", j);
        OutBuffer[i].usedNum++;
        if (OutBuffer[i].usedNum == OUTBUFFERNUM) {
            printf("\n�������\n");
            ReqBlock[n_in].length = k + 1;
            t_num[i][i == 0 ? t1 : t2] -= ReqBlock[n_in].length;
            ReqBlock[n_in].reqid = i;
            ReqBlock[n_in].addr = head;
            n_in = (n_in + 1) % REQBLOCKNUM;
            PCB[i].status = 1;
            return;
        }
    }
    printf("\n");

    if (i == 0) {
        printf("���� %d �ļ�%d���ַ�����: %d\n\n", i, t1, t_num[0][t1]);
        ReqBlock[n_in].length = k < 20 ? t_num[0][t1] : 20;
        t1 += (k < 20);
    } else {
        printf("���� %d �ļ�%d���ַ�����: %d\n\n", i, t2, t_num[1][t2]);
        ReqBlock[n_in].length = k < 20 ? t_num[1][t2] : 20;
        t2 += (k < 20);
    }
    ReqBlock[n_in].reqid = i;
    ReqBlock[n_in].addr = head;
    OutBuffer[i].head = (head + ReqBlock[n_in].length) % OUTBUFFERNUM;

    if (PCB[PROCESSNUM].status == 2)
        PCB[PROCESSNUM].status = 0;

    n_in = (n_in + 1) % REQBLOCKNUM;
    printf("              <<<<<<<<<<<<<<<<<<<���̽���>>>>>>>>>>>>>>>>>>>>          \n");
    printf("\n");
    printf("\n���س�������...");
    getchar();
}

void spooling() {
    if (C3 == 10) {
        PCB[2].status = (PCB[0].status == 3 && PCB[1].status == 3) ? 3 : 2;
        return;
    }

    printf("*******************************************************************************\n");
    while (C3 < 10) {
        int reqid = ReqBlock[n_out].reqid;
        int addr = ReqBlock[n_out].addr;
        int length = ReqBlock[n_out].length;

        printf("addr: %d\n", addr);
        printf("SPOOLING�������Ϊ��%d\n", reqid);
        printf("����SPOOLING���̣��ͷŵĽ��̿����ΪReqBlock[%d]\n", n_out);
        printf("����Ϊ��������\n");

        for (int k = 0; k < length; k++) {
            printf("%d ", OutBuffer[reqid].buf[(addr + k) % OUTBUFFERNUM]);
        }
        printf("\n");
        OutBuffer[reqid].usedNum -= length;

        C3++;
        n_out = (n_out + 1) % REQBLOCKNUM;
    }

    if (PCB[0].status == 1)
        PCB[0].status = 0;
    if (PCB[1].status == 1)
        PCB[1].status = 0;

    printf("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n\n");
}

void work() {
    srand((unsigned)time(NULL));
    while (1) {
        int i = rand() % 100;
        if (i <= 40 && PCB[0].status == 0 && t1 < 3)
            request(0);
        else if (i <= 80 && PCB[1].status == 0 && t2 < 3)
            request(1);
        else if (i > 80 && PCB[2].status == 0)
            spooling();

        int isFinish = (t1 == T1) && (t2 == T2);
        PCB[0].status = (t1 == T1) ? 3 : PCB[0].status;
        PCB[1].status = (t2 == T2) ? 3 : PCB[1].status;

        if (isFinish)
            return;
    }
}

void menu() {
    printf("\n>>>>>>>>>>>>>>>> SPOOLingϵͳģ����� <<<<<<<<<<<<<<<<<\n");
    printf("����0����%d���ļ�\n", T1);
    for (int i = 0; i < T1; i++) {
        printf("����0�ļ�%d���ļ�������%d\n", i, t_num[0][i]);
    }
    printf("\n����1����%d���ļ�\n", T2);
    for (int i = 0; i < T2; i++) {
        printf("����1�ļ�%d���ļ�������%d\n", i, t_num[1][i]);
    }
    printf("\n");
    printf("\n���س�����һ��...");
    getchar();
}

int main() {
    int a, b, c, d, e, f,choice;
    printf("ѡ���Ƿ�ʹ��Ĭ����ֵ����ģ��(��������: Ĭ������,1:�Զ�������)");
    scanf("%d", &choice);
    if (choice == 1) {
        printf("�������0�����������ļ��ַ�(����������ÿ���ö��Ÿ���)");
        scanf("%d,%d,%d", &a, &b, &c);
        printf("�������1�����������ļ�(����������ÿ���ö��Ÿ���)");
        scanf("%d,%d,%d", &d, &e, &f);
        while (getchar() != '\n');
        srand((unsigned)time(NULL));
        init(a, b, c, d, e, f);
        menu();
        work();
        printf("\n���س����˳�...");
        getchar();
    }else {
        while (getchar() != '\n');
        srand((unsigned)time(NULL));
        init(15, 25, 10, 6, 10, 18);
        menu();
        work();
        printf("\n���س����˳�...");
        getchar();
    }   
    return 0;
}