#include <iostream>
#include <queue>
#include <cstdio>
#include <cstring> 
#include <vector>
#include <iomanip>
#define workday first
#define night second
#define id second.second
#define mp make_pair
using namespace std;
typedef pair<int, pair<int, int> > pipii;
const int N = 2000;
int s, t, n, m, trace[N], f[N][N], sizeee;
int ava[4][4];
int ablework[N];
int num_Conveyor; 
pair<int, int> NS[N];
queue<int> query, mem;
bool findPath(vector< vector<int> > c, int source, int sink)
{
    priority_queue<pipii> q;
    for (int i = 0; i <=sizeee; i++)
        trace[i] = 0;
    trace[source] = -1;
    q.push(mp(NS[source].workday, mp(NS[source].night, source)));
    while (!q.empty())
    {
        int u = q.top().id; q.pop();
        for (int v = 0; v <= sizeee; v++)
        {
            if (c[u][v] > f[u][v] && !trace[v])
            {
                trace[v] = u;
                if (v == sink)
                    return true;
                q.push(mp(NS[v].workday, mp(NS[v].night, v)));
            }
        }
    }
    return false;
}
void incFlow(vector< vector<int> > c, int source, int sink)
{
    int delta, u, v;
    for (v = sink; v != source; v = trace[v])
        delta = min(delta,c[trace[v]][v]-f[trace[v]][v]);
    for (v = sink; v != source; v = trace[v])
    {
        f[trace[v]][v]+=delta;
		f[v][trace[v]]-=delta;
    }
}
void readfile(vector< vector<int> >& c)
{
    freopen("input.txt", "r", stdin);
    freopen("result_data_1_part_a.txt", "w", stdout);
    c.assign(N, vector<int>(N));
    cin >> n; // số nhân lực
    cin >> num_Conveyor; // số băng chuyền 
    for (int i = 0; i < num_Conveyor; i++)
    {
        for(int skill = 0; skill < 3; skill++)
        {
            int num; cin >> num;
            while (num--)
            {
                int emp; cin >> emp;
                ablework[emp]++;
                for (int y = 1; y <= 3; y++)
                    c[n + 3*(emp-1) + y][4*n + 9*i + skill*3 + y] = 1;
            }
        }
    }
    for (int i = 0; i < num_Conveyor; i++)
        for (int j = 0; j < 3; j++)
            cin >> ava[i][j];
    s = 0;
    t = 4*n + 9 * num_Conveyor + 1;
    sizeee = t;
}
void update(vector< vector<int> >& c)
{
    while (!mem.empty())
    {
        int i = mem.front(); mem.pop();
        c[i][n+(i-1)*3+1] = 1;
    }
    while (!query.empty())
    {
        int i = query.front(); query.pop();
        c[i][n+(i-1)*3+1] = 0;
        mem.push(i);
    }

}
string itos(int i)
{
    string ans = "";
    while (i)
    {
        ans = char((i%10)+48) + ans;
        i /= 10;
    }    
    if (ans.size() == 1)
        ans = '0' + ans;
    return ans;
}
// skill: 1:ROT, 2: MĐH, 3: pallet
void print_answer(int d)
{
    string cday = itos(d);

    // ------------------
    queue<int> q;
    for (int i = 1; i <= n; i++)
    {
        if (f[s][i] == 1)
            q.push(i);
    }
    while (!q.empty())
    {
        cout << cday + ".06.2023 Ca_";
        int i = q.front();
        int x, y;
        for (y = 1; y <=3; y++)
        {
            x = n + (i-1)*3 + y;
            if (f[i][x] > 0)
                break;
        } 
        if (y == 3)
        {
            NS[i].second -= 1;
            query.push(i);
        } 
        cout << y
             << " V" + itos(i) + " "
             << "Day_chuyen_";
        //--------------------
        int z;
        for (z = y; z < t; z += 3)
            if (f[x][4*n+z] > 0)
                break;
        cout << (z+8)/9
             << ' ';
        y = (z+2)/3;
        string congviec = (y == 1) ? "Rot": (y == 2) ? "May_dong_hop": "Pallet";
        cout << congviec
             << '\n';
        q.pop();
    }

}
void solve(vector< vector<int> > c)
{
    for (int i = 0; i <=sizeee; i++)
        for (int j = 0; j <= sizeee; j++)
            f[i][j] = 0;
    for (int i = 0; i < num_Conveyor; i++)
    {
        int num; cin >> num; 
        while (num--)
        {
            int shift; cin >> shift;
            int skill = 0;
                for (int j = 4*n+shift; j < sizeee; j += 3)
                    {
                        c[j][t] = ava[i][skill++];
                        // c[j+1][t] = ava[i][1];
                        // c[j+2][t] = ava[i][2];
                        skill %=3;
                        // cout << i << ' ' << skill << ' ' << ava[i][skill] << '\n';
                        // cout << skill << ' ' << ava[i][skill] << ' ';
                    }
        }
    }
    while(findPath(c,s,t))
        incFlow(c,s,t);
    for (int i = 4*n+1; i <= 4*n+10; i++)
    {
        for (int j = 4*n+0; j <= 4*n+10; j++)
            cout << c[i][j] << ' ';
        cout << '\n';
    }
}
int main()
{
    time_t a = clock(), b;
    ios_base::sync_with_stdio(0);
    cin.tie(0); cout.tie(0);
    vector< vector<int> > c; 
    readfile(c);
    for (int i = 1; i <= n; i++)
    {
        c[s][i] = 1;
        NS[i].workday = 24;
        NS[i].night = 0;
        for (int y = 1; y <= 3; y++)
            c[i][n+3*(i-1)+y] = 1;
    }
    for (int i = n+1; i <= sizeee; i++)
    {
        NS[i].workday = 24;
        NS[i].night = 0;
    }
    for (int day = 1; day <= 1; day++) // check
    {
        update(c);
        solve(c);
        print_answer(day);
    }   
    b = clock(); 
    double time = (b - a)*1.0/ CLOCKS_PER_SEC;
    cerr << setprecision(3) << fixed << time;
}
