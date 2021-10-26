#include <bits/stdc++.h>
using namespace std;
using ll = long long;

int main() {
    freopen("in.txt", "r", stdin);
    freopen("out.txt", "w", stdout);
    string s;
    cin >> s;
    int i = 1;
    int ans = 0;
    if (s[0] != ' ') ans++;
    while (i < s.size()) {
        if (s[i] != ' ' && s[i-1] == ' ')
            ans++;
    }
    cout << ans;
}