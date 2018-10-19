
fuzzyXY = readfis('fuzzyXY.fis')

e = linspace(0,12,9);  % centroidi pogreške
de = linspace(-5,30,9) ;

[c_cart1,c_cart2] = meshgrid(de,e);
c_cart = [c_cart1(:) c_cart2(:)];   % Kartezijev produkt centroida
[rule_idx1,rule_idx2] = meshgrid([1:9],[1:9]); 
rule_idx = [rule_idx1(:) rule_idx2(:)];	% Kartezijev produktindeksa pravila

K_reg = [-0.1114;1.148];
A = c_cart*K_reg;    % Vrijednosti izlaznih singletona

% Promjene singletona radi dobivanja boljeg odziva 



% Pridjeli vrijednosti izlaznim singletonima
fuzzyXY.output.range = [min(A) max(A)];
for i = 1:length(fuzzyXY.output.mf)
    fuzzyXY.output.mf(i).name = ['A' mat2str(i)];
    fuzzyXY.output.mf(i).params = A(i);
    fuzzyXY.rule(i).antecedent = rule_idx(i,:);
    fuzzyXY.rule(i).consequent = i;
    fuzzyXY.rule(i).weight = 1;
    fuzzyXY.rule(i).connection = 1;
end

writefis(fuzzyXY, 'fuzzyXY');