#include <iostream>

class A {
  public:
    int i;

  A(int i) : i(i) {}

};


int main() {

  A a(12);

  std::cout << "Hello this is a dummy C++ project!! " << a.i << std::endl;

  return 0;
}
