clear all, close all, clc
s=tf('s');

G=10/(s+1)/(s+2)/(s+3);

% error al escalon de 0.01

kc=59.4;

Phi_des=40;

LA1=kc*G;

figure, margin(G), hold on
margin(LA1)
legend('G','kc*G')
[Gm,Pm,Wcg,Wcp] = margin(LA1)

Theta_k=(Phi_des-Pm+10)
Theta_k=(Phi_des-Pm+10)*pi/180;

disp('Theta_k>65 muy grande')

disp('compensador en atraso')

Phi=(Phi_des+7)-180

wcg=1.77 %1.15 %de la grafica

A=-29.9 % negativo curva debe bajar

alpha=10^(A/20)

T=10/alpha/wcg

K=kc*(alpha*T*s+1)/(T*s+1)

LA=K*G;
LC=feedback(LA,1);
damp(LC)

figure, margin(LA1)
hold on
margin(LA)
hold on
margin(G)
legend('kc*G','K*G','G')

T=feedback(G,1);
LC=feedback(LA,1);

figure, step(T,LC)
legend('sin compensador','con compensador')





