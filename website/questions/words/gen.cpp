#include <bits/stdc++.h>
using namespace std;
using ll = long long;

int main()
{
    random_device rd;

    mt19937_64 e2(rd());

    uniform_int_distribution<long long int> dist(llround(1), llround(30));

    uniform_int_distribution<long long int> letter(llround(97), llround(122));

    freopen("in.txt", "w", stdout);
    for (int n = 0; n < 100; ++n) {
        if (dist(e2) >= 20) cout << " ";
        else cout << char(letter(e2));
    }
}