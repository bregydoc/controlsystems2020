clear all, close all, clc

num=[10 20];
den=[1 10 24 0];

G=tf(num,den);

[A,B,C,D]=tf2ss(num,den);

Gss=ss(A,B,C,D);

damp(Gss)

figure, step(Gss)

OS=10;
Ts=2;

psi=log(100/OS)/sqrt(pi^2+log(100/OS)^2);
wn=4/psi/Ts;

s1=-psi*wn+i*wn*sqrt(1-psi^2)
s2=-psi*wn-i*wn*sqrt(1-psi^2)
s3=-20;

pd=[s1 s2 s3];

Co=ctrb(A,B);
rango=rank(Co)

K=acker(A,B,pd)

Alc=A-B*K;
Blc=zeros(3,1);
Clc=C;
Dlc=D;

LC=ss(Alc,Blc,Clc,Dlc);

damp(LC)

t=0:0.01:10;
x0=[0.1 -0.2 0.1];

figure, initial(LC,x0)

%% Diseño del observador 

mo=obsv(A,C);
rang_obs=rank(mo)

Pdo=5*pd;

L=acker(A',C',Pdo)
L=L';


%% analisis

Alc=[A -B*K;
    L*C A-B*K-L*C];
Blc=zeros(6,1);
Clc=[C -D*K];
Dlc=0;

LCo=ss(Alc,Blc,Clc,Dlc);

damp(LCo)

x0_obs=[0.1 -0.2 0.1 0.1 -0.2 0.1];
[yco,t,xco]=initial(LCo,x0_obs);
[yso,t,xso]=initial(LC,x0);


figure, plot(t,yso,'r',t,yco,'b*')
legend('sin obs','con obs')

































