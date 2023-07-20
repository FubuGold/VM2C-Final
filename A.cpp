#include <iostream>
#include <queue>
#include <cstdio>
#include <cstring> 
#include <vector>
#define workday first
#define night second
#define id second.second
#define mp make_pair
using namespace std;
using pipii = pair<int, pair<int, int> >;
const int N = 250;
int s, t, n, m, trace[N], c[N][N], f[N][N], sizeee;
pair<int, int> NS[N];
queue<int> query, mem;
bool findPath(int source, int sink)
{
    priority_queue<pipii> q;
    for (int i = 0; i <=sizeee; i++)
        trace[i] = 0;
    trace[source] = -1;
    q.push(mp(NS[source].workday, mp(NS[source].night, source)));
    while (!q.empty())
    {
        int u = q.top().id; q.pop();
        for (int v = 1; v <= sizeee; v++)
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
void incFlow(int source, int sink)
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
void readfile()
{
    freopen("input.txt", "r", stdin);
    freopen("result_data_1_part_a.txt", "w", stdout);
    cin >> n; // số nhân lực
    int num_Conveyor; cin >> num_Conveyor; // số băng chuyền 
    while (num_Conveyor--)
    {
        


    }
    s = 0;
}
void update()
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
    return ans;
}
// skill: 1:ROT, 2: MĐH, 3: pallet
void print_answer(int d)
{
    string cday = itos(d);
    if (cday.size() == 1)
        cday = '0' + cday;
    queue<int> q;
    for (int i = 1; i <= n; i++)
    {
        if (f[s][i] > 0)
            q.push(i);
    }
    while (!q.empty())
    {
        cout << cday + ".06.2023 Ca";
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
             << " Day_chuyen_";
        int k;
        for (y = 1; y <= 3; y++)
        {
            k = 3*n + y;
            if (f[x][k] > 0)
                break;
        }
        cout << y
             << " ";
        int tmp;
        for (y = 1; y <= 3; y++)
        {
            tmp = 3*n + 3 + y;
            if (f[k][tmp] > 0)
                break;
        }
        string congviec = (y == 1) ? "Rot": (y == 2) ? "May_dong_hop": "Pallet";
        cout << congviec
             << '\n';
        q.pop();
    }

}
int main()
{
    ios_base::sync_with_stdio(0);
    cin.tie(0); cout.tie(0);
    readfile();
    for (int i = 1; i <= sizeee; i++)
    {
        NS[i].workday = 24;
        NS[i].night = 0;
    }
    for (int day = 1; day <= 28; day++)
    {
        update();
        while(findPath(s,t))
            incFlow(s,t);
        print_answer(day);
    }    

}
