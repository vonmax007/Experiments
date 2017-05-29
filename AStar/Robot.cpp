#pragma once
#include "StdAfx.h"


void PrintMap(unsigned char ** map, int real_row, int real_col)
{	//输出地图
	int i, j;
	for (i = 0; i<real_row; i++)
	{
		for (j = 0; j<real_col; j++)
		{
			if (map[i][j] == Tile_Open || map[i][j] == Tile_UP ||
				map[i][j] == Tile_DOWN || map[i][j] == Tile_LEFT
				|| map[i][j] == Tile_RIGHT || map[i][j] == Tile_UP_LEFT
				|| map[i][j] == Tile_UP_RIGHT || map[i][j] == Tile_DOWN_LEFT
				|| map[i][j] == Tile_DOWN_RIGHT) {
				printf("□");
			}
			else if (map[i][j] == Tile_Lock) {
				printf("■");
			}
			else if (map[i][j] == Tile_Start) {
				printf("☆");
			}
			else if (map[i][j] == Tile_End) {
				printf("★");
			}
			else if (map[i][j] == Tile_Path) {
				printf("●");
			}
		}
		printf("\n");
	}
	printf("\n\n");
}



int main(int argc, char** argv)
{
	//_CrtSetBreakAlloc(775);
	int map_row = 10, map_col = 10;
	unsigned char ** real_map = nullptr;
	list <list <Point>> ps;//每次机器人找到的路径集合;
						   //生成指定大小的资源地图
						   //产生指定大小的虚拟地图
	{
		int real_row = (map_row - 1) * 3 + 1;
		int real_col = (map_col - 1) * 3 + 1;

		real_map = new unsigned char *[real_row];//开辟地图空间
												 //this->ResEntity_list = new ResEntity *[real_row];
		for (int i = 0; i < real_row; ++i)
		{
			real_map[i] = new unsigned char[real_col];
			//this->ResEntity_list[i] = new ResEntity[real_col];
		}

		for (int i = 0; i < real_row; ++i)
			for (int j = 0; j < real_col; ++j)
			{
				if (i % 3 == 0 && i % 6 == 0 && j % 3 != 0)
					real_map[i][j] = Tile_LEFT;	//←
				else if (i % 3 == 0 && i % 6 != 0 && j % 3 != 0)
					real_map[i][j] = Tile_RIGHT;	//→
				else if (j % 3 == 0 && j % 6 == 0 && i % 3 != 0)
					real_map[i][j] = Tile_DOWN;	//←
				else if (j % 3 == 0 && j % 6 != 0 && i % 3 != 0)
					real_map[i][j] = Tile_UP;	//↑

				else if (i % 3 == 0 && i % 6 == 0 && j % 3 == 0 && j % 6 != 0)
					real_map[i][j] = Tile_UP_LEFT;	//→
				else if (i % 3 == 0 && i % 6 == 0 && j % 3 == 0 && j % 6 == 0)
					real_map[i][j] = Tile_DOWN_LEFT;	//→
				else if (i % 3 == 0 && i % 6 != 0 && j % 3 == 0 && j % 6 != 0)
					real_map[i][j] = Tile_UP_RIGHT;	//→
				else if (i % 3 == 0 && i % 6 != 0 && j % 3 == 0 && j % 6 == 0)
					real_map[i][j] = Tile_DOWN_RIGHT;	//→
				else
				{
					real_map[i][j] = Tile_Lock;
					//this->ResEntity_list[i][j].Rtype = 5;//垃圾资源
					continue;
				}
			}
		PrintMap(real_map, real_row, real_col);
	}
	
	AStar a;
	ps = a.findKPath(20, real_map, (map_row - 1) * 3 + 1, (map_col - 1) * 3 + 1, 0, 0, 21, 21);
	cout << ps.size() << endl;
	
	_CrtDumpMemoryLeaks();
	return 0;
}


