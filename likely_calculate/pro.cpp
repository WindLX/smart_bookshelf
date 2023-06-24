#include<cstdio>
#define maxN 100
#define maxM 100
double val[maxN+5][maxM+maxN];
double dp[maxN+5][maxM+maxN];
double max(double x,double y){return x>y?x:y;}
int main(){
    int n,m;
    scanf("%d%d",&n,&m);//n<=m
    for(int i=1;i<=n;i++){
        for(int k=1;k<=m;k++){
            scanf("%lf",&val[i][k]);
        }
    }
    for(int i=0;i<=m+1;i++)dp[0][i]=0;
    for(int i=1;i<=n;i++){
        for(int k=1;k<=m+n;k++){
            dp[i][k]=max(dp[i][k-1],dp[i-1][k-1]+val[i][k]);
        }
    }
    printf("%lf",dp[n][m+n]);
    return 0;
}