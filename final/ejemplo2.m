clear all, close all, clc
s=tf('s');

G=2/s/(s+2)/(s+3); %2

kc=10;

Phi_des=35; %25

LA1=kc*G;

figure, margin(G), hold on
margin(LA1)
legend('G','kc*G')
[Gm,Pm,Wcg,Wcp] = margin(LA1)

disp('compensador en adelanto')

Theta_k=(Phi_des-Pm+15)
Theta_k=(Phi_des-Pm+15)*pi/180;

alpha=(1+sin(Theta_k))/(1-sin(Theta_k))

A=10*log10(alpha)

% calculand wcgf

wcg=2.86; %2.6

T=1/sqrt(alpha)/wcg

K=kc*(alpha*T*s+1)/(T*s+1)

LA=K*G;

figure, margin(LA1)
hold on
margin(LA)

T=feedback(G,1);
LC=feedback(LA,1);

figure, step(T,LC)
legend('sin compensador','con compensador')


%% compensador en atraso

Phi=(Phi_des+7)-180

wcg=1.08 %1.15 %de la grafica

A=-8.14 % negativo curva debe bajar

alpha=10^(A/20)

T=10/alpha/wcg

K=kc*(alpha*T*s+1)/(T*s+1)

LA=K*G;
LC=feedback(LA,1);
damp(LC)

figure, margin(LA1)
hold on
margin(LA)

t=0:0.01:100;
u=t;
y=lsim(LC,u,t);

error=u-y';
figure, plot(t,error)





