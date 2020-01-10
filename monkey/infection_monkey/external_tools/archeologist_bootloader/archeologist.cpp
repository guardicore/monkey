#include <iostream>
#include <fstream>

using namespace std;

void main()
{
    std::ofstream outfile ("C:/Windows/Temp/test.txt");

    outfile << "my text here!" << std::endl;

    outfile.close();
}
