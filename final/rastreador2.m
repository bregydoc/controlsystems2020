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

Ag=[A zeros(4,1);-C 0];
Bg=[B;0];
Cg=[C 0];
Dg=0;

G=ss(A,B,C,D);
Gg=ss(Ag,Bg,Cg,Dg);

Mc=ctrb(Gg);
Rango=rank(Mc)

OS=10;
Ts=3;

psi=log(100/OS)/sqrt(pi^2+(log(100/OS))^2);
wn=4/psi/Ts

s1=-psi*wn+i*wn*sqrt(1-psi^2);
s2=-psi*wn-i*wn*sqrt(1-psi^2);
s3=-10;
s4=-12;
s5=-15;

Pd=[s1 s2 s3 s4 s5];

KK=acker(Ag,Bg,Pd);
K=KK(1,1:4);
Ki=-KK(5);

% Lazo cerrado
Ak=[A-B*K B*Ki;-C 0];
Bk=[zeros(4,1);1]; 
Ck=[C 0]; 
Dk=0;
figure, step(Ak,Bk,Ck,Dk)

damp(Ak)
















