#include <iostream>
#include <cmath>

using namespace std;


double task1();
int task2();
double task3();


int main() {
    cout << "Result for Task 1: " << task1() << endl << endl;

    cout << "Result for Task 2: " << task2() << endl << endl;

    cout << "Result for Task 3: " << task3() << endl << endl;
    
}


double task1() {

    cout << "----Task 1----" << endl << endl;

    double a;
    double b;


    cout << "Enter value for \"a\": ";
    cin >> a;

    cout << "Enter value for \"b\": ";
    cin >> b;


    double c = (pow(a+b, 4) - (pow(a, 4) + (4 * pow(a, 3) * b))) / ((6 * pow(a, 2) * pow(b, 2)) + (4 * a * pow(b, 3)) + pow(b, 4));

    cout << "\n";

    return c;
    
}


int task2() {

    cout << "----Task 2----" << endl << endl;

    int m;
    int n;


    cout << "Enter value for \"m\": ";
    cin >> m;

    cout << "Enter value for \"n\": ";
    cin >> n;



    cout << "\nValue for \"m\" before calculating: " << m;
    cout << "\nValue for \"n\" before calculating: " << n << endl << endl;

    int c = ++n*--m;

    cout << "Value for \"m\" after calculating: " << m;
    cout << "\nValue for \"n\" after calculating: " << n << endl << endl;

    return c;
    
}


double task3() {

    cout << "----Task 3----" << endl << endl;

    double b1;
    double q;

    cout << "Enter the first term: ";
    cin >> b1;

    cout << "Enter the ratio: ";
    cin >> q;

    if (abs(q) >= 1) {
        cout << "\nThe sum does not exist because |q| >= 1.\n";
        return NAN;
    }
    else {
        cout << "\n";
    }

    return b1 / (1 - q);

}
