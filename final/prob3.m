clear all, close all, clc

s=tf('s');

P=10/(s+1)/(s+4)/(s+5);

ki=10;

Ts=4;
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

%% Controlador PD

kp=K_mag*cos(theta_k);
kd=K_mag*sin(theta_k)/wcf;

K=kp+kd*s;

LA=K*P;

LC=feedback(LA,1);
damp(LC)

figure, margin(LA)
figure, step(LC)

t=0:0.01:10;
u=t;

figure, lsim(LC,u,t)