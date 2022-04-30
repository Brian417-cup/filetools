//test.exe生成的源码

#include <iostream>

using namespace std;



int main(int argc,char* argv[])
{
	for(int i=0;i<1000000;i++)
	{
		cout<<argv[1]<<endl;
		cout<<argv[2]<<endl;
	}

	return 0;
}

