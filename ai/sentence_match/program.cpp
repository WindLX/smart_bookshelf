#include <stdio.h>
#include <math.h>
#include <algorithm>

using namespace std;

#define MaxN 100
#define MaxM 100

float matrix[MaxN + 5][MaxM + 5];

int pos[MaxN + 5];

int main()
{
	freopen("in.txt", "r", stdin);
	int n, m;
	scanf("%d %d", &n, &m);
	int i, k, j;
	float ans = 0;
	for (i = 0; i < n; i++)
	{
		for (k = 0; k < m; k++)
		{
			scanf("%f", &matrix[i][k]);
		}
		ans += matrix[i][i] * matrix[i][i];
	}
	for (i = 0; i < m; i++)
		pos[i] = i;
	while (next_permutation(pos, pos + m))
	{
		float tmpans = 0;
		for (i = 0; i < n; i++)
		{
			tmpans += matrix[i][pos[i]] * matrix[i][pos[i]];
		}
		ans = max(ans, tmpans);
	}
	printf("%f", ans);
	return 0;
}