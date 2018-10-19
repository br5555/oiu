
fuzzy_FIS = readfis('struct.fis');

e = linspace(-10,10,20);  % centroidi pogreške
de = linspace(0,12,12) ;

[c_cart1,c_cart2] = meshgrid(de,e);
c_cart = [c_cart1(:) c_cart2(:)];   % Kartezijev produkt centroida
[rule_idx1,rule_idx2] = meshgrid([1:12],[1:20]); 
rule_idx = [rule_idx1(:) rule_idx2(:)];	% Kartezijev produktindeksa pravila

K_reg = [-0.14;-10];
A = c_cart*K_reg;    % Vrijednosti izlaznih singletonaosti izlaznih singletona

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

 


%  Zapisivanje fis matrice nazad u file
 writefis(fuzzy_FIS, 'fuzzy_FIS');

