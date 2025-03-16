#include "stdio.h"
#include "stdlib.h"
#include "time.h"

#define PROCESSNUM 2   // 输出进程个数
#define OUTBUFFERNUM  30  // 输出井存储字节个数
#define REQBLOCKNUM   10
#define T1   3          // 定义用户进程0要输出的文件数T1
#define T2   3          // 定义用户进程1要输出的文件数T2

struct pcb {
    int id;     // 进程标识
    int status; // 状态0为可执行态；1为等待状态；2为输出井空；3为结束态
    int length; // 输出长度
} PCB[PROCESSNUM + 1];

struct reqblock {
    int reqid;   // 要求输出的进程
    int tname;
    int length;  // 输出长度
    int addr;    // 输出首地址
} ReqBlock[REQBLOCKNUM];

struct BUFFER {
    int buf[OUTBUFFERNUM];   // 输出井缓冲区
    int usedNum;             // 输出井缓冲区已使用的数目
    int head;                // 指示输出井空闲块首地址
} OutBuffer[PROCESSNUM];

int C3 = 10;              // 当前系统剩余的请求输出信息块个数，初值为10
int n_out = 0, n_in = 0;  // 指示当前使用的输出请求块
int t1 = 0;               // 计时器，记录用户进程已输出的文件个数
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
    printf("进程: %d 调用request进程，写入的进程块序号为ReqBlock[%d]\n", i, n_in);

    if (C3 == 0) {
        PCB[i].status = 1;
        printf("没有空闲的请求块，进程状态置1\n");
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
            printf("\n该文件个数大于20，将被挂起\n");
            t_num[i][i == 0 ? t1 : t2] -= 20;
            PCB[i].status = 1;
            break;
        }
        OutBuffer[i].buf[(head + k) % OUTBUFFERNUM] = j;
        printf("%d ", j);
        OutBuffer[i].usedNum++;
        if (OutBuffer[i].usedNum == OUTBUFFERNUM) {
            printf("\n输出井满\n");
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
        printf("进程 %d 文件%d的字符个数: %d\n\n", i, t1, t_num[0][t1]);
        ReqBlock[n_in].length = k < 20 ? t_num[0][t1] : 20;
        t1 += (k < 20);
    } else {
        printf("进程 %d 文件%d的字符个数: %d\n\n", i, t2, t_num[1][t2]);
        ReqBlock[n_in].length = k < 20 ? t_num[1][t2] : 20;
        t2 += (k < 20);
    }
    ReqBlock[n_in].reqid = i;
    ReqBlock[n_in].addr = head;
    OutBuffer[i].head = (head + ReqBlock[n_in].length) % OUTBUFFERNUM;

    if (PCB[PROCESSNUM].status == 2)
        PCB[PROCESSNUM].status = 0;

    n_in = (n_in + 1) % REQBLOCKNUM;
    printf("              <<<<<<<<<<<<<<<<<<<进程结束>>>>>>>>>>>>>>>>>>>>          \n");
    printf("\n");
    printf("\n按回车键继续...");
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
        printf("SPOOLING输出进程为：%d\n", reqid);
        printf("调用SPOOLING进程，释放的进程块序号为ReqBlock[%d]\n", n_out);
        printf("以下为输出结果：\n");

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
    printf("\n>>>>>>>>>>>>>>>> SPOOLing系统模拟程序 <<<<<<<<<<<<<<<<<\n");
    printf("进程0创建%d个文件\n", T1);
    for (int i = 0; i < T1; i++) {
        printf("进程0文件%d的文件个数是%d\n", i, t_num[0][i]);
    }
    printf("\n进程1创建%d个文件\n", T2);
    for (int i = 0; i < T2; i++) {
        printf("进程1文件%d的文件个数是%d\n", i, t_num[1][i]);
    }
    printf("\n");
    printf("\n按回车键下一步...");
    getchar();
}

int main() {
    int a, b, c, d, e, f,choice;
    printf("选择是否使用默认数值进行模拟(其他整数: 默认数据,1:自定义数据)");
    scanf("%d", &choice);
    if (choice == 1) {
        printf("输入进程0创建的三个文件字符(输入整数并每次用逗号隔开)");
        scanf("%d,%d,%d", &a, &b, &c);
        printf("输入进程1创建的三个文件(输入整数并每次用逗号隔开)");
        scanf("%d,%d,%d", &d, &e, &f);
        while (getchar() != '\n');
        srand((unsigned)time(NULL));
        init(a, b, c, d, e, f);
        menu();
        work();
        printf("\n按回车键退出...");
        getchar();
    }else {
        while (getchar() != '\n');
        srand((unsigned)time(NULL));
        init(15, 25, 10, 6, 10, 18);
        menu();
        work();
        printf("\n按回车键退出...");
        getchar();
    }   
    return 0;
}