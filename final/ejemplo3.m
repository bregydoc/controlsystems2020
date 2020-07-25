clear all; close all; clc;
s=tf('s');
ps=400/(s*(s^2+30*s+200))
kc=5; %calculando o erro estacionario
wcg=14;
phi=45*pi/180;
pwcg=freqresp(ps,j*wcg)
ampp=abs(pwcg)
tetap=angle(pwcg)
tetak=-pi+phi-tetap
ampk=1/ampp
tauz=(1+kc*ampp*cos(phi-tetap))/...
(-wcg*kc*ampp*sin(phi-tetap))
taup=(cos(phi-tetap)+kc*ampp)/...
(wcg*sin(phi-tetap))
ks=kc*(tauz*s+1)/(taup*s+1)

%% controlador en funcion de T e alpha
T=(ampk*cos(tetak)-kc)/(ampk*wcg*sin(tetak))
alpha=ampk*(kc*cos(tetak)-ampk)/(kc*(kc-ampk*cos(tetak)))
ks1=kc*(alpha*T*s+1)/(T*s+1)
gs=ks*ps %malha aberta
margin(gs)
ts=feedback(gs,1) %malha fechada
tss=ts/s; %rampa
t=0:0.01:1;
y=step(tss,t);
figure, plot(t,t,t,y)