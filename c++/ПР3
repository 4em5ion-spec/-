#include <iostream>
#include <cmath>
#include <string>

/*#include <locale>
#include <codecvt>*/

using namespace std;


int task1() {

    cout << "----Task 1----" << endl << endl;

    int a;
    int b;
    int c;
    int d;
    int smallest;
    int biggest;
    int middle;


    cout << "Enter value for \"a\": ";
    cin >> a;

    cout << "Enter value for \"b\": ";
    cin >> b;

    cout << "Enter value for \"c\": ";
    cin >> c;


    cout << "\nValue for \"a\" before calculating: " << a;
    cout << "\nValue for \"b\" before calculating: " << b;
    cout << "\nValue for \"c\" before calculating: " << c << endl;


    if (a < b && b < c) {
        smallest = a;
        biggest = c;
        middle = b;
        cout << "\n\"b\" is not biggest and not smallest.\n";
        d = b;

        a = c + b;
    }
    else if (a < c && c < b) {
        smallest = a;
        biggest = b;
        middle = c;
        cout << "\n\"c\" is not biggest and not smallest.\n";
        d = c;

        a = b + c;
    }
    else if (b < a && a < c) {
        smallest = b;
        biggest = c;
        middle = a;
        cout << "\n\"a\" is not biggest and not smallest.\n";
        d = a;

        b = c + a;
    }
    else if (b < c && c < a) {
        smallest = b;
        biggest = a;
        middle = c;
        cout << "\n\"c\" is not biggest and not smallest.\n";
        d = c;

        b = a + c;
    }
    else if (c < a && a < b) {
        smallest = c;
        biggest = b;
        middle = a;
        cout << "\n\"a\" is not biggest and not smallest.\n";
        d = a;

        c = b + a;
    }
    else if (c < b && b < a) {
        smallest = c;
        biggest = a;
        middle = b;
        cout << "\n\"b\" is not biggest and not smallest.\n";
        d = b;

        c = a + b;
    }
    else {
        cout << "\nThere is no number that is not the biggest and not the smallest.\n";
    }

    
    if (sqrt(d) == int(sqrt(d))) {
        cout << "\nThe number that is not the biggest and not the smallest is a perfect square.\n";
    }
    else {
        cout << "\nThe number that is not the biggest and not the smallest is not a perfect square.\n";
    }


    if (biggest % 2 == 0) {
        cout << "\nThe biggest number is even.\n";
    }
    else {
        cout << "\nThe biggest number is odd.\n";
    }


    cout << "\nValue for \"a\" after calculating: " << a;
    cout << "\nValue for \"b\" after calculating: " << b;
    cout << "\nValue for \"c\" after calculating: " << c << endl << endl << endl;
    
    return 0;
}


int task2() {
    //std::setlocale(LC_ALL, "");

    cout << "----Task 2----" << endl << endl;

    int n;
    string text = "Zhyrnov";
  
    cout << "Enter index for searching in last name: ";
    cin >> n;

    //cout << text[n] << endl << endl;
    //cout << text.at(1) << endl << endl;

   switch (n) {
        case 0:
            cout << text[0] << text[1] << endl << endl << endl;
            break;
        case 1:
            cout << text[2] << endl << endl << endl;
            break;
        case 2:
            cout << text[3] << endl << endl << endl;
            break;
        case 3:
            cout << text[4] << endl << endl << endl;
            break;
        case 4:
            cout << text[5] << endl << endl << endl;
            break;
        case 5:
            cout << text[6] << endl << endl << endl;
            break;
        default:
            cout << "\nIndex is out of range." << endl << endl << endl;
    }

    return 0;
    
}


double task3() {

    cout << "----Task 3----" << endl << endl;

    double a;
    double b;
    double c;
    double x;

    cout << "Enter value for \"a\": ";
    cin >> a;

    cout << "Enter value for \"b\": ";
    cin >> b;

    cout << "Enter value for \"c\": ";
    cin >> c;

    cout << "Enter value for \"x\": ";
    cin >> x;


    if (a < 0 && x != 0) {
        return (-a * pow(x, 2)) + (pow(b, 2) * x);
    }
    else if (a > 0 && x == 0) {
        return x - (a / (x - c));
    }
    else {
        return 1 + (x / c);
    }

}




int main() {
    task1();

    task2();

    cout << "\nResult for Task 3: " << task3() << endl << endl;
}
