#include <stdio.h>
#include <math.h>

void leer(int *m,double *X,double *Y,double *Ery);
void ajustar(int n,double *X,double *Y,double *Ery,double A[][101],double *B);
double alfa(int n,int i,int j,double *X,double *Ery);
double beta(int n,int i,double *X,double *Y,double *Ery);
void invertir(int n,double A[][101]);
void MMult(int n,double A[][101], double *B);
void Xs(int n,int r,double *X, double *Y,double *Ery,double *B);

int main() {
  double X[100],Y[100],Ery[100],A[101][101],B[101];
  int n;
  leer(&n,X,Y,Ery);
  ajustar(n,X,Y,Ery,A,B);
  return 0;
}
void ajustar(int n,double *X,double *Y,double *Ery,double A[][101],double *B){
  int o,r,i,j;
  printf("orden del ajuste\n");
  scanf("%d", &o);
  //numero de incogitas r
  r = o + 1;
  //creacion de la matriz del sistema
  for (i = 0; i < r; i++) {
     for (j = 0; j < r; j++) {
       A[i][j] = alfa(n,i,j,X,Ery);
    //   printf("%lf  ",A[i][j]);
     }
     B[i] = beta(n,i,X,Y,Ery);
    // printf("     %lf\n",B[i]);
  }
  //invertir la matriz
  invertir(r,A);
  MMult(r,A,B);
  Xs(n,r,X,Y,Ery,B);
}
//ajustar xi square para cada ajuste
void Xs(int n,int r,double *X, double *Y,double *Ery,double *B){
  double y=0.0,xi,yi,S=0.0,e,xs,a,b,c;
  int i,j;
  a=B[0];
  b=B[1];
  c = B[2];
  for (i = 0; i < n; i++) {
    xi = X[i];
    yi = Y[i];
    e = 1.0/Ery[i];
    y = a + b*xi + c*xi*xi;
    xs = (yi-y)*e;
    xs*=xs;
    S += xs;
  }
  printf("\nXi square = %lf\n", S);
}

double alfa(int n,int i,int j,double *X,double *Ery){
  double S=0.0,e,xi=1.0,x;
  int t,c,d;
  t= i+j;
  //Sum x a la i+j entre sigma2
  for (c = 0; c < n; c++) {
    xi = 1.0;
    e = 1.0/Ery[c];
    e*=e;
    if (t>0) {
      x = X[c];
      xi = x;
      for (d = 1; d < t; d++) {
        xi*=x;
      }
    }
    xi *= e;
    S += xi;
  }
  return S;
}
double beta(int n,int i,double *X,double *Y,double *Ery){
  double S=0.0,e,x,xi=1.0,yi=1.0,xye;
  int c,d;
  //Sum yi*xi entre sigma2
  for (c = 0; c < n; c++) {
      xi = 1.0;
      yi = Y[c];
      x = X[c];
      e = Ery[c];
      e *= e;
      //x a la i
      if (i>0) {
        xi = x;
        for (d = 1; d < i; d++) {
          xi*=x;
        }
      }
       xye= xi*yi/e;
      S+=xye;
  }
  return S;
}

void MMult(int n,double A[][101], double *B){
	int i,j;
	double sum=0.0,R[100];
	for(i=0;i<n;i++){
		for(j=0;j<n;j++){
			sum += A[i][n+j]*B[j];
		}
		R[i] = sum;
		sum = 0.0;
	}
	for(i=0;i<n;i++){
		B[i] = R[i];
    printf("a(%d) = %.10f\n",i,B[i]);
	}
}

void invertir(int n, double A[][101]){
  double vec,f=0.0;
  int m,i,j,k,dx;
  m=2*n;
   for(i=0;i<n;i++){
	   for(j=0;j<n;j++){
		   if(j==i){
			      A[i][n+j]=1.0;
		   }
		   else{
			      A[i][n+j]=0.0;
		   }
	   }
   }
    for(i=0;i<n-1;i++)
    {
	    for(k=(i+1);k<n;k++)
	    {
		 if(A[i][i]==0.0){
	            dx=i;
		    while(A[dx][i]==0.0){
			  dx++;
		    }
		    for(j=i;j<m;j++){
			  vec=A[dx][j];
			  A[dx][j]=A[i][j];
			  A[i][j]=vec;
		    }
		 f=-(A[k][i]/A[i][i]);
		 }
		 else{
		 f=-(A[k][i]/A[i][i]);
		 }
		 for(j=i;j<(m);j++)
		 {
		     A[k][j] += f*A[i][j];
		 }
	    }
    }

    for(i=n-1;i>0;i--){
	    for(k=i-1;k>=0;k--){
		 f=-(A[k][i]/A[i][i]);
		 for(j=i;j<m;j++){
		     A[k][j]=(A[k][j] + (f*A[i][j]));
		 }
	    }
    }
   for(i=0;i<n;i++){
	  f=A[i][i];
	   for(j=0;j<m;j++){
	    	A[i][j]/=f;
	   }
  }
}

void leer(int *m,double *X,double *Y,double *Ery) {
  int c,n,i;
  FILE *fp;
  char nombre[20];
  printf("Nombre del archivo y cantidad de datos: \n" );
  scanf("%s %d", nombre,&n);
  *m = n;
  fp = fopen(nombre,"r");
  printf("Incertidumbres en Y [si = 0, no = 1]\n");
  scanf("%d",&c);
  if(c == 0) {
    for(i = 0; i < n; i++) {
      fscanf(fp,"%lf %lf %lf",&X[i],&Y[i],&Ery[i]);
    }
  }
  else{
    for(i = 0; i < n; i++) {
      fscanf(fp,"%lf %lf",&X[i],&Y[i]);
      Ery[i] = 1.0;
    }
  }
}
