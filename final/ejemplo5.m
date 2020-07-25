clear all, close all, clc

m=0.089;
M=0.77;
g=9.81;
l=0.32;

A=[0 1 0 0; 0 0 -m*g/M 0;
    0 0 0 1; 0 0 g*(M+m)/M/l 0];

B=[0;1/M;0;-1/M/l];
C=[0 0 1 0];
D=0;

G=ss(A,B,C,D);
damp(G)

OS=10;
Ts=3;

psi=log(100/OS)/sqrt(pi^2+log(100/OS)^2);
wn=4/psi/Ts;

s1=-wn*psi+i*wn*sqrt(1-psi^2);
s2=-wn*psi-i*wn*sqrt(1-psi^2);
Co=ctrb(A,B) 
rango=rank(Co)
s=tf('s');

phi=(s-s1)*(s-s2)*(s+9)*(s+10)

phiA=A^4+21.67*A^3+145.8*A^2+336.7*A+457.8*eye(4)

K=[0 0 0 1]*inv(Co)*phiA

% Pd=[s1 s2 -90 -100];
% K=acker(A,B,Pd)

Alc=A-B*K;
Blc=zeros(4,1);
Clc=C;
Dlc=0;

LC=ss(Alc,Blc,Clc,Dlc);
damp(LC);
x0=[0.05;0;0.6;0]
figure, initial(LC,x0)










