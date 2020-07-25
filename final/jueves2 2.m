clear all, close all, clc

s=tf('s');

P=2/s/(s+2);

kc=1/0.05

LA1=kc*P;  %Lazo abierto con kc

figure, margin(LA1)

[Gm,Pm,Wcg,Wcp] = margin(LA1)
MF_des=45;
Theta_k=(MF_des-Pm+5)*pi/180;


alpha=(1+sin(Theta_k))/(1-sin(Theta_k))

A=10*log10(alpha)

wcg=8.5; %rad/s

T=1/sqrt(alpha)/wcg

K=kc*(alpha*T*s+1)/(T*s+1)

LA=K*P;
LC=feedback(LA,1);
figure,margin(LA)
t=0:0.01:20;
u=t;
figure, lsim(LC,u,t)
[Y,T,X]=lsim(LC,u,t);
error=u-Y';
figure, plot(t,error)

%% analisis en lazo abierto

figure, margin(P)
hold on
margin(LA)
legend('no compensado','compensado')


%% analisis en lazo cerrado
figure, bode(P)
hold on
bode(LC)
legend('planta','compensado')



















