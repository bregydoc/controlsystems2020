clear all, close all, clc

s=tf('s');

G=1/s/(s+1)/(0.5*s+1);
MFd=40;
kc=5;

LA1=kc*G;
figure, margin(LA1);

Phi_s=7;  % entre 5 y 12

Phi=MFd+Phi_s-180;

wcg=0.53;

A=-18.2; %25.4 y 24

alpha= 10^(A/20);

T=10/alpha/wcg;

K=kc*(alpha*T*s+1)/(T*s+1);

LA=G*K;

LC=feedback(LA,1);
damp(LC)
figure, margin(LA)

