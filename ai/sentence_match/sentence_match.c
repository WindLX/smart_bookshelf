#include <stdio.h>
#include <math.h>
#include <stdlib.h>

#define MaxN 100
#define MaxM 100

float matrix[MaxN + 5][MaxM + 5];

int pos[MaxN + 5];

void next_permutation(int *arr, int size)
{
	int i = size - 2;
	while (i >= 0 && arr[i] >= arr[i + 1])
	{
		i--;
	}
	if (i >= 0)
	{
		int j = size - 1;
		while (arr[j] <= arr[i])
		{
			j--;
		}
		int temp = arr[i];
		arr[i] = arr[j];
		arr[j] = temp;
	}
	int start = i + 1;
	int end = size - 1;
	while (start < end)
	{
		int temp = arr[start];
		arr[start] = arr[end];
		arr[end] = temp;
		start++;
		end--;
	}
}

int main()
{
	freopen("similar_matrix.txt", "r", stdin);
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
	{
		pos[i] = i;
	}
	while (1)
	{
		float tmpans = 0;
		for (i = 0; i < n; i++)
		{
			tmpans += matrix[i][pos[i]] * matrix[i][pos[i]];
		}
		ans = fmax(ans, tmpans);
		int flag = 0;
		for (i = m - 2; i >= 0; i--)
		{
			if (pos[i] < pos[i + 1])
			{
				flag = 1;
				break;
			}
		}
		if (!flag)
		{
			break;
		}
		int minIndex = i + 1;
		for (j = i + 2; j < m; j++)
		{
			if (pos[j] > pos[i] && pos[j] < pos[minIndex])
			{
				minIndex = j;
			}
		}
		int temp = pos[i];
		pos[i] = pos[minIndex];
		pos[minIndex] = temp;
		int start = i + 1;
		int end = m - 1;
		while (start < end)
		{
			temp = pos[start];
			pos[start] = pos[end];
			pos[end] = temp;
			start++;
			end--;
		}
	}
	ans = sqrt(ans / n);
	printf("%f", ans);
	return 0;
}
