clear all, close all, clc

s=tf('s');

G=10/s/(s+5);

kc=10;
psi=0.7;
MF=28;

Phi_des=100*psi;

LA1=kc*G;

figure, margin(LA1)

Phi=(Phi_des+7)-180

wcg=1.15 %1.15 %de la grafica

A=-24.6 % negativo curva debe bajar

alpha=10^(A/20)

T=10/alpha/wcg

K=kc*(alpha*T*s+1)/(T*s+1)

LA=K*G;
LC=feedback(LA,1);
damp(LC)

figure, margin(LA1)
hold on
margin(LA)











