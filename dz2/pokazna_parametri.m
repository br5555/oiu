%%=========================================================================
% Stvaranje FIS strukture
%
% Na vjezbi je FIS struktura stvorena uz puno koristenja FIS editora, sto
% nije moguce reproducirati u ovoj skripti. Zbog toga cemo FIS strukturu
% ucitati iz datoteke, uz navodjenje nekih kljucnih naredbi u komentarima

fuzzyPI1 = readfis('fuzzyPI1.fis');

%--- Racunanje koeficijenata singletona za emulaciju PI1 kontrolera ---
c_e = linspace(-4,4,45);   % Centroidi pogreske
rule_idx1=[1:45]; 
A = -3*c_e.^3+3*c_e.^2-4*c_e;    % Vrijednosti izlaznih singletona

% Pridjeli vrijednosti izlaznim singletonima
fuzzyPI1.output.range = [min(A) max(A)];
for i = 1:length(fuzzyPI1.output.mf)
    fuzzyPI1.output.mf(i).name = ['A' mat2str(i)];
    fuzzyPI1.output.mf(i).params = A(i);
    fuzzyPI1.rule(i).antecedent = rule_idx1(i);
    fuzzyPI1.rule(i).consequent = i;
    fuzzyPI1.rule(i).weight = 1;
    fuzzyPI1.rule(i).connection = 1;
end

% Sada je moguce simulirati Simulink model s neizrazitim regulatorom i
% analizirati odzive. Neizraziti regulator bi trebao kvalitativno oponasati
% djelovanje PI1 regulatora.