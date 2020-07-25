clc;clear all;close all;

m1 = 375; m2 = 59; k1 = 35000; k2 = 190000; c = 1000;
%%
A = [0 1 0 0;
	-(k1+k2)/m2 -c/m2 k1/m2 c/m2;
	0 0 0 1;
	k1/m1 c/m1 -k1/m1 -c/m1];
B = [0; k2/m2; 0; 0];
C = [0 0 1 0];
D = 0;

%% Determinación de los polos
os = 15; te=4;
qsi = log(100/os)/sqrt(pi^2 + log(100/os)^2);
wn = 4/(qsi*te);

%polosd = [-qsi*wn+wn*sqrt(1-qsi^2)i -qsi*wn-wn*sqrt(1-qsi^2)]; %polos deseados
p1 = -qsi*wn+wn*sqrt(1-qsi^2)*i;
p2 = -qsi*wn-wn*sqrt(1-qsi^2)*i;
p3 = -9;
p4 = -10;
polosd = [p1 p2 p3 p4];

%% Ganancia de realimentación
K = acker(A,B,polosd)
Ak = A-B*K;
Bk = [0; 0; 0; 0;];
Ck = [0 0 1 0];                 % para extraer la salida x1 y x3
Dk = [0];

%% Respuesta a una condición inicial
CI = [0.05 0 .6 0]                % condición inicial
[y,x,t] = initial(Ak,Bk,Ck,Dk,CI);      % respuesta a una condición inicial

figure; subplot(311); initial(Ak,Bk,Ck,Dk,CI);         % respuesta de la velocidade a una condición inicial
        %subplot(312); initial(Ak,Bk,-K,Dk,CI);         % Señal de control
        u=-K*x';
        subplot(312); plot(t,u); title('esfuerzo de control');
        subplot(313); plot(t,x); title('evolución de los estados');
