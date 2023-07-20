#include <iostream>
#include <queue>
#include <cstdio>


using namespace std;
const int N = 250;
int s, t, n, m, trace[N], c[N][N], f[N][N];
bool findPath(int source, int sink)
{
    queue<int> q;
    for (int i = 0; i <=n; i++)
        trace[i] = 0;
    trace[source] = -1;
    q.push(source);
    while (!q.empty())
    {
        int u = q.front(); q.pop();
        for (int v = 1; v <= 2*n; v++)
        {
            if (c[u][v] > f[u][v] && !trace[v])
            {
                trace[v] = u;
                if (v == sink)
                    return true;
                q.push(v);
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

}
// skill: 1:ROT, 2: MĐH, 3: pallet
void print_answer()
{
    queue<int> q;
    for (int i = 1; i <= n; i++)
    {
        if (f[s][i] > 0)
            q.push(i);
    }

}
int main()
{
    ios_base::sync_with_stdio(0);
    cin.tie(0); cout.tie(0);
    readfile();
    for (int day = 1; day <= 28; day++)
    {
        update();
        while(findPath(s,t))
            incFlow(s,t);
        print_answer();
    }

    

}
