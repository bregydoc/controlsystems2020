clear all, close all, clc

s=tf('s');

G=10/s/(s+5);
psi=0.7;
kc=10;

LA1=kc*G;
figure, margin(LA1);
MFd=100*psi;
Phi_s=7;  % entre 5 y 12

Phi=MFd+Phi_s-180;

wcg=1.13;

A=-24.8 %25.4 y 24

alpha= 10^(A/20);

T=10/alpha/wcg;

K=kc*(alpha*T*s+1)/(T*s+1);

LA=G*K;

LC=feedback(LA,1);
damp(LC)

figure, margin(LA)

t=0:0.01:100;
u=t;

y=lsim(LC,u,t);
figure, lsim(LC,u,t)

error=u-y';
figure, plot(t,error)






















