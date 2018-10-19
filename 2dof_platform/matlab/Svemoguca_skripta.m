clc;   % Ocisti Command Window
% Osnove inteligentnog upravljanja - 1. Domaca zadaca
% Parametri sustava loptice na XY platformi

fprintf(strcat('Clearing all current variables...\n',...
    'Creating new variables for simulating the 2DOF platform!\n\n\n'))

% Clear workspace
clear all;

%-----------------------------------------------------------------------
Enable=3;
while (~(Enable==0) && ~(Enable==1) && ~(Enable==2))
    fprintf(strcat( 'Enable = 0  -odzivi uz singletone bez poboljšanja (2. zadatak)\n',...
                    'Enable = 1  -odzivi uz poboljšane singletone( 3. zadatak)\n',...
                    'Enable = 2  -odzivi uz iskljuèen pomoæni regulator (3. zadatak)\n'))
    Enable = input('Unesite vrijednost varijable Enable:\n');
    if (~(Enable==0) && ~(Enable==1) && ~(Enable==2))
        fprintf(strcat('Nije zadan zadovoljavajuæi Enable.\n',...
                       'Varijabla Enable mora imati vrijednost 0, 1 ili 2.\n'));
    end
end
             % Enable == 0  -odzivi uz singletone bez poboljšanja (2. zadatak)
             % Enable == 1  -odzivi uz poboljšane singletone( 3. zadatak)
             % Enable == 2  -odzivi uz iskljuèen pomoæni regulator (3.
             % zadatak)
            
%-----------------------------------------------------------------------

%--- Parametri loptice ---%
R = 0.0115;
ml = 0.03;          % Masa loptice
g = 9.81;
Jl = 1.5870e-6;
d = 2;
Fc = 9.9675e-8;
Fs = 1.9935e-7;
vs = 0.05;

%--- Parametri platforme ---%

r = 0.02;
l = 0.1;
a = 0.3;            % Duljina stranice platforme

%--- Parametri lineariziranog modela ---%
K_lin = -0.4671;
p1_lin = 0;
p2_lin = -2;

%--- Pocetni uvjeti ---%
x0 = 0.15;
y0 = 0.15;

%--- Parametri reference ---%
t_step = 5;
x_step = 0.05;
y_step = 0.05;

%--- Parametri kruznice ---%
A_x=0.05;
A_y=0.05;
freq_x=2*pi/10;
freq_y=2*pi/10;
phase_x=pi/2;
phase_y=0;

%--- Parametri kvadrata kao reference ---%

konstanta = 0.1; 
Ak_x= 0.1;
Ak_y = 0.1;
period_x = 16;
period_y= 16;
pw_x= 50;
pw_y = 50;
phasedelay_x= 0;
phasedelay_y= 4;


%--- Parametri simulacije ---%
t_sim = 30;

%--- Parametri regulatora ---%

% Pomocni regulator
K_komp = -14.7931;

% P regulator
Kp = -6;

% Vrijeme diskretizacije 
Td= 0.1;

%  Izracunavanje prijenosne funkcije regulatora u prvom zadatku
Gs=tf(-0.4671, [1 2 0]);
Gm = tf(2.7873^2,[1 2*2.7873*0.8261 2.7873^2]);
GR = Gm/(Gs*(1-Gm));
GR=minreal(GR);

%  Diskretizacija prijenosne funkcije regulatora
GRd=c2d(GR,Td);

% Generiranje fuzzy regulatora
fuzzy_FIS = readfis('fuzzy_FIS.fis');

e = linspace(-0.1,0.1,7);  % centroidi
de = linspace(-0.01,0.01,7) ;

[c_cart1,c_cart2] = meshgrid(e,de);
c_cart = [c_cart1(:) c_cart2(:)];   % Kartezijev produkt centroida
[rule_idx1,rule_idx2] = meshgrid([1:7],[1:7]); 
rule_idx = [rule_idx1(:) rule_idx2(:)];	% Kartezijev produktindeksa pravila

K_reg = [-2.66;-13.94];
A = c_cart*K_reg;    % Vrijednosti izlaznih singletona

% Pridjeli vrijednosti izlaznim singletonima
fuzzy_FIS.output.range = [min(A) max(A)];
for i = 1:length(fuzzy_FIS.output.mf)
    fuzzy_FIS.output.mf(i).name = ['A' mat2str(i)];
    fuzzy_FIS.output.mf(i).params = A(i);
    fuzzy_FIS.rule(i).antecedent = rule_idx(i,:);
    fuzzy_FIS.rule(i).consequent = i;
    fuzzy_FIS.rule(i).weight = 1;
    fuzzy_FIS.rule(i).connection = 1;
end

if Enable==1
    % Promjene singletona radi dobivanja boljeg odziva
    Const_x=1;
    Const_y=1;
    t_sim=15;
    sim usporedba_komp_i_fuzzy_regulator;
    ZaCrt2=ZaCrt;
    fuzzy_FIS.output.mf(22).params = A(22)+0.4;     % Ruèno podešavanje singletona
    fuzzy_FIS.output.mf(1).params = A(1)+1.6;       
    fuzzy_FIS.output.mf(49).params = A(49)-1;
   
    for i = 1:length(fuzzy_FIS.output.mf)
        A(i) = fuzzy_FIS.output.mf(i).params;
    end
    fuzzy_FIS.output.range = [min(A) max(A)];
elseif Enable==2
    % Pomocni regulator iskljuèen
    Const_x=1;
    Const_y=1;
    K_komp = 0;
    t_sim=30;
    sim usporedba_komp_i_fuzzy_regulator;
    ZaCrt2=ZaCrt;
    xxx2=xxx;
    yyy2=yyy;
    A = 10.5*c_cart*K_reg;       % Ruèno podešavanje singletona
    for i = 1:length(fuzzy_FIS.output.mf)
       fuzzy_FIS.output.mf(i).params = A(i);
    end
    fuzzy_FIS.output.range = [min(A) max(A)];

end
 
% Varijable za switch subsystem (po defaultu se simulira kruznica; 1-step, 2-kvadrat, 3-kruznica)
Const_x=3;
Const_y=3;

sim usporedba_komp_i_fuzzy_regulator

%  Zapisivanje fis matrice nazad u file
 writefis(fuzzy_FIS, 'fuzzy_FIS');
 run Crtanje_svih_slika;
