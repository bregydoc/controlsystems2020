clear all, close all, clc

s=tf('s');

num=1;
den=s*(s+3)*(s+15)*(s+20);

G=num/den;

kc=4*3*15*20;

LA1=kc*G;

MFd=37;

figure, margin(LA1)
[Gm,Pm,Wcg,Wcp] = margin(LA1);

Theta_k=(MFd-Pm+12)*pi/180

alpha=(1+sin(Theta_k))/(1-sin(Theta_k))

A=10*log10(alpha)

% calculand wcgf

wcg=3.59;

T=1/sqrt(alpha)/wcg

K=kc*(alpha*T*s+1)/(T*s+1)

LA=K*G;

figure, margin(LA1)
hold on
margin(LA)
legend('sin compensador','con compensador')

T=feedback(G,1);
LC=feedback(LA,1);

figure, step(T,LC)
legend('sin compensador','con compensador')
