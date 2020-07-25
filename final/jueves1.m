clear all, close all, clc
s=tf('s');

G=10/(s+1)/(s+2)/(s+3);

% error al escalon de 0.01

kc=59.4;

figure, margin(G)

[Gm,Pm,Wcg,Wcp] = margin(G)

LA1=kc*G;

hold on
margin(LA1)

%% compensador en atraso
Phi_des=40;

Phi=(Phi_des+7)-180

wcg=1.77 %1.15 %de la grafica

A=-30.2 % negativo curva debe bajar

alpha=10^(A/20)

T=10/alpha/wcg

K=kc*(alpha*T*s+1)/(T*s+1)

LA=K*G;
LC=feedback(LA,1);
damp(LC)

figure, margin(G)
hold on
margin(LA)
hold on
bode(K)
legend('G','K*G','K')

[Gm,Pm,Wcg,Wcp] = margin(LA)

