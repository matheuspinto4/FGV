#include <iostream>

void soma(int& x);

int main(){
    
    int x = 10;
    
    std::cout<<x<<std::endl;
    soma(x);
    std::cout<<x;

    return 0;
}

void soma(int& x)
{
    x++;
}