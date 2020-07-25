clear all, close all, clc

s=tf('s');

num=(s+10)*(s+11);
den=s*(s+3)*(s+6)*(s+9);

kc=1000*3*6*9/10/11

G=num/den;

OS=10;

psi=log(100/OS)/sqrt(pi^2+log(100/OS)^2);

MFd=100*psi

LA1=kc*G;

figure, margin(LA1)

%%  compensador en atraso

Phi=(MFd+7)-180

wcg=0.977 %1.15 %de la grafica

A=-59.7 % negativo curva debe bajar

alpha=10^(A/20)

T=10/alpha/wcg

K=kc*(alpha*T*s+1)/(T*s+1)

LA=K*G;
LC=feedback(LA,1);
damp(LC)

figure, margin(LA1)
hold on
margin(LA)
legend('sin compensacion','con compensacion')


