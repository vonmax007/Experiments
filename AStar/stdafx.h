// stdafx.h : ��׼ϵͳ�����ļ��İ����ļ���
// ���Ǿ���ʹ�õ��������ĵ�
// �ض�����Ŀ�İ����ļ�
//

#pragma once

/* Linux������ɾ��*/
#include "targetver.h"
#include <stdio.h>
#include <tchar.h>
#define _CRTDBG_MAP_ALLOC  
#include <stdlib.h>  
#include <crtdbg.h> 

// TODO:  �ڴ˴����ó�����Ҫ������ͷ�ļ�

#include <iostream>
#include <fstream>
#include <string>
#include <list>
#include <vector>
#include <queue>
#include <stdlib.h>
#include <cmath>
#include <Windows.h>	//���ͷ�ļ���Linux����Ҫɾ������������
#include <time.h>		//���ͷ�ļ���Linux����Ҫɾ��������ʱ��
using namespace std;

//�Զ�������
struct Point
{
	unsigned short i, j;		//i����,j����
	Point() {}
	Point(unsigned short _i, unsigned short _j) : i(_i), j(_j) {}
};
typedef list <Point> path;
typedef list <list <Point>> PathSet;
typedef unsigned char TileType;	//������������ʹ�õ�����
#define TTL 5					//ԤԼʧЧʱ��,����ÿ��5ʱ������¹滮һ��
#define K_way 10				//ÿ�λ������ҵ�K_way��·��
#define START_slot 1			//��ʼʱ��۴�1��ʼ
#define END_slot 10000			//�ٶ�ʵ������10000��ʱ���



								//�Զ������ͷ�ļ�
#include "AStar.h"

