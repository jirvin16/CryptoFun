#include <iostream>
#include <limits>
int x = 100;

float factorial(int n) {
  if(n==0) return 1;  
  return n*factorial(n-1);
}

float miniSum(int a) {
  float sum=0;
  int b;
  for(b=0;b<=x-a;b++) {
    sum+=(1/(factorial(x-a-b)*factorial(b)))*std::numeric_limits<float>::max();;
    //std::cout << "sum:" << sum << std::endl;
  }
  return sum;
}

int main() {
  float a;
  float sum=0;
  for(a=0;a<=x;a++) {
    sum+=(1/factorial(a))*miniSum(a)*std::numeric_limits<float>::max();;
    //std::cout << "miniSum:" << miniSum(a) << "a:" << a << std::endl;
  }
  std::cout << sum << std::endl;         
  return 0;


}
