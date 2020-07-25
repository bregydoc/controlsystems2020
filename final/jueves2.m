clear all; close all; clc;

s=tf('s');
ps=400/(s*(s^2+30*s+200))

kc=5; 
wcg=14;

Pm=45; 
Pwcg=freqresp(ps,j*wcg)
Pabs=abs(Pwcg)
Theta_p=angle(Pwcg)

Kabs=1/Pabs
Theta_k=-pi+Pm*pi/180-Theta_p

alpha=Kabs*(kc*cos(Theta_k)-Kabs)/(kc*(kc-Kabs*cos(Theta_k)))
T=(Kabs*cos(Theta_k)-kc)/(Kabs*wcg*sin(Theta_k))

K=kc*(alpha*T*s+1)/(T*s+1)

G=ps;
LA=K*G;

LC=feedback(LA,1);
damp(LC)

figure, margin(G)
hold on
margin(LA)
hold on
bode(K)
legend('G','K*G','K')





