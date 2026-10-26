#include <iostream>
#include <cmath>

using namespace std;

int main()
{
    double a, b, h;
    
    cout << "Enter number A: ";
    cin >> a;
    cout << "Enter number B: ";
    cin >> b;
    cout << "Enter step H: ";
    cin >> h;
    
    if (h <= 0) {
        cout << "Error: H must be greater than 0!" << endl;
        return 1;
    }
    
    cout << "\n=========================" << endl;
    cout << "       VALUE TABLE       " << endl;
    cout << "=========================" << endl;
    cout << "X\t|\tY" << endl;
    cout << "-------------------------" << endl;
    
    for (double x = a; x <= b; x += h) {
        cout << x << "\t|\t";
        
        if (x == 0.0) {
            cout << "Undefined" << endl;
        } else {
            double y = pow(x, 3) + log(abs(x)) - 3;
            cout << y << endl;
        }
    }
    
    cout << "=========================" << endl;
    
    return 0;
}
