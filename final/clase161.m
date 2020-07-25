clear all, close all, clc

s=tf('s');

G=1.2*(s+2)/(s+1)/(s+3)/(s+7);

[A,B,C,D]=tf2ss(G.num{1,1},G.den{1,1});

Gss=ss(A,B,C,D);

Ao=[A zeros(3,1);-C 0];
Bo=[B;0];

OS=3;
Ts=3.5;

psi=log(100/OS)/sqrt(pi^2+(log(100/OS))^2);
wn=4/psi/Ts;

s1=-psi*wn+i*wn*sqrt(1-psi^2);
s2=-psi*wn-i*wn*sqrt(1-psi^2);
s3=-10;
s4=-12;

Pd=[s1 s2 s3 s4];

Co=ctrb(Ao,Bo);
rango=rank(Co)

KK=acker(Ao,Bo,Pd)

K=KK(1,1:3);
Ki=-KK(1,4);

% Lazo cerrado
Ak=[A-B*K B*Ki;-C 0];
Bk=[zeros(3,1);1]; 
Ck=[C 0]; 
Dk=0;

Gk=ss(Ak,Bk,Ck,Dk);
figure, step(Gk)

damp(Ak)

%% etapa del observador
mo=obsv(A,C);
rang_obs=rank(mo)

Pdo=5*Pd(1,1:3)

L=acker(A',C',Pdo)
L=L';

Alc=[A -B*K B*Ki;
    L*C A-B*K-L*C B*Ki;
    -C zeros(1,3) 0];

Blc=[zeros(3,1);
    zeros(3,1);
    1];
Clc=[C zeros(1,3) 0];
Dlc=0;

Glc=ss(Alc,Blc,Clc,Dlc);

figure, step(Glc)

figure, step(Gk,Glc)
legend('Gk','Glc')















