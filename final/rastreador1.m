clear all, close all, clc

m1=375;
m2=59;
k1=35000;
k2=190000;
c1=1000;

A=[0 1 0 0;
    -k1/m1 -c1/m1 k1/m1 c1/m1;
    0 0 0 1;
    k1/m2 c1/m2 -(k1+k2)/m2 -c1/m2];
B=[0 ;
    0;
    0;
    k2/m2];
C=[1 0 0 0];
D=[0];

G=ss(A,B,C,D);

Mc=ctrb(A,B);
Rango=rank(Mc)

OS=10;
Ts=3;

psi=log(100/OS)/sqrt(pi^2+(log(100/OS))^2);
wn=4/psi/Ts

s1=-psi*wn+i*wn*sqrt(1-psi^2);
s2=-psi*wn-i*wn*sqrt(1-psi^2);
s3=-10; %Polos no dominantes
s4=-12; %polos no dominantes

Pd=[s1 s2 s3 s4];

K=acker(A,B,Pd);

Ak=A-B*K;
Bk=B; 
Ck=C; 
Dk=0;
figure, step(Ak,Bk,Ck,Dk)



kp=1/dcgain(Ak,Bk,Ck,Dk)

% añadiendo Kp en el lazo cerrado

B1=kp*B;
K1=acker(A,B1,Pd) %ou K1=K/kp

Alc=A-B1*K1
Blc=B1; 
Clc=C; 
Dlc=0;

LC=ss(Alc,Blc,Clc,Dlc);
figure; step(Alc,Blc,Clc,Dlc)















