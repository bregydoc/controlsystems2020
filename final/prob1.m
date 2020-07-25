clear all, close all, clc

s=tf('s');

P=400/s/(s^2+30*s+200);

ki=5;

Ts=1.7;
OS=10;

psi=log(100/OS)/sqrt(pi^2+(log(100/OS))^2);
wn=4/psi/Ts;

MF=100*psi;
wcf=wn;


P_complex=freqresp(P,wcf)
P_mag=abs(P_complex)
P_angulo=angle(P_complex)

K_mag=1/P_mag
theta_k=-pi+MF*pi/180-P_angulo

kp=K_mag*cos(theta_k);
kd=(K_mag*sin(theta_k)+ki/wcf)/wcf;

K=kp+kd*s+ki/s;

LA=K*P;

LC=feedback(LA,1);
damp(LC)

figure, margin(LA)
figure, step(LC)

t=0:0.01:30;
u=t.^2;

figure, lsim(LC,u,t)
[Y,T]=step(LC/s/s,t);

figure, plot(t,Y,'r',t,u,'b')












