clear all, close all, clc

s=tf('s');

G=10/s/(s+1)/(s+3)

figure, margin(G)

kc=10^(1.58/20)

k1=10^(-(20-1.58)/20)

LA=k1*G;

figure, margin(LA)

k2=10^(-7.9/20)

LA=k2*G;
figure, margin(LA)

