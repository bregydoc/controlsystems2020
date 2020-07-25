clear all, close all, clc

A=[-0.4 0 -0.01;
    1 0 0;
    -1.4 9.8 -0.02];

B=[6.3;0;9.8];
C=[0 0 1];
D=0;

G=ss(A,B,C,D);

Mc=ctrb(A,B);
Rango=rank(Mc)

Pd=[-1+i -1-i -2];  % Polos deseados del controlador
K=acker(A,B,Pd)

mo=obsv(A,C);
rang_obs=rank(mo)

Po=5*Pd;
L=acker(A',C',Po)
L=L';

%Lazo cerrado

Aa=[A -B*K;
    L*C A-B*K-L*C];
[f,c]=size(Aa);

Ba=zeros(f,1);
Ca=[C -D*K];
Da=0;

LC=ss(Aa,Ba,Ca,Da);
damp(LC);


x0=[1 2 3];
xx0=[-1 -2 -3];
X0=[x0 xx0]';

figure, initial(LC,X0)

[y,t,x] = initial(LC,X0,5);

figure, plot(t,x(:,1),'b',t,x(:,4),'r')
legend('real x1','estimado x1')









