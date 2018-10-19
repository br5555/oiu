% Parametri laboratorijske makete helikoptera

% Gravitacijska konstanta
g = 9.81;

% Duljine
l1 = 0.295;
l2 = 0.280;
l3 = 0.120;

% Mase
m1 = 0.120;
m2 = 0.020;
m3 = 0.056;

% Moment inercije
I = m1*l1^2 + m2*l2^2 + m3*l3^2;

% Koeficijenti viskoznog trenja
bv = 0.05;
bh = 0.05;

% Glavni propeler
u1_max = 12;
u1_min = 0;
K1_u = 0.14/l1; % Karakteristika glavnog motora+propelera (uzgon)
K1_z = 0.014*l1/l2; % Karakteristika glavnog motora+propelera (zakret)
dz1_z = 0.07;

% Repni propeler
u2_max = 5;
u2_min = -5;
K2_z = 0.05;
dz2_z = 0.08;

% Poniranje
theta0 = -5*pi/180;
theta_min = -50*pi/180;
theta_max = 50*pi/180;



