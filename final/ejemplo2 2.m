clear all, close all, clc

s=tf('s');

ki=10;

P=10/(s+1)/(s+4)/(s+5);

ki=10;

OS=8;
Ts=3;

psi=log(100/OS)/sqrt(pi^2+(log(100/OS))^2)

wn=4/psi/Ts

wcg=wn;
MF=100*psi

P_complex=freqresp(P,wcg);
P_mag=abs(P_complex);
P_ang=angle(P_complex);

K_mag=1/P_mag

Theta_k=MF*pi/180-P_ang-pi

kp=K_mag*cos(Theta_k);

kd=(K_mag*sin(Theta_k)+ki/wcg)/wcg;

K=kp+kd*s+ki/s;

LA=K*P;

LC=feedback(LA,1);

damp(LC)

figure, step(LC)
figure, margin(LA)

t=0:0.01:10;

figure, lsim(LC,t,t)
figure, step(LC/s/s)

