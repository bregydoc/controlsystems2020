%realimentación de estados - regulador
clear all; close all; clc;
m = 0.089; M = 0.77; g = 9.81; l = 0.32;
%% Matrices del sistema linearizado
A = [0  1  0  0;
     0  0 -m*g/M 0;
     0  0  0  1;
     0  0  g*(M+m)/(M*l) 0];
 
B = [0; 1/M; 0; -1/(M*l)];
C = [0 0 1 0];
D = 0;

%% matriz de controlabilidad
M = ctrb(A,B); 
detM = det(M); % rank(M)

%% Determinación de los polos
os = 10; te=3;

qsi = log(100/os)/sqrt(pi^2 + log(100/os)^2);

wn = 4/(qsi*te);

p1 = -qsi*wn+wn*sqrt(1-qsi^2)*i;
p2 = -qsi*wn-wn*sqrt(1-qsi^2)*i;
p3 = -9;
p4 = -10;
polosd = [p1 p2 p3 p4];
%% Ganancia de realimentación
K = acker(A,B,polosd); % place(A,B,polosd)
Ak = A-B*K;
Bk = [0; 0; 0; 0;];
Ck = C;                 % para extraer la salida x3
Dk = 0;

%% Respuesta a una condición inicial
%     x    xp theta thetap
CI = [0.05 0  .6    0] ;               % condición inicial
[y,x,t] = initial(Ak,Bk,Ck,Dk,CI);      % respuesta a una condición inicial

figure; subplot(311); initial(Ak,Bk,Ck,Dk,CI);         % respuesta de la velocidade a una condición inicial
        %subplot(312); initial(Ak,Bk,-K,Dk,CI);         % Señal de control
        u=-K*x';
        subplot(312); plot(t,u); title('esfuerzo de control');
        subplot(313); plot(t,x); title('evolución de los estados');
