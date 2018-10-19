fuzzysad = readfis('fuzzysad.fis')
v1=linspace(-0.8727,0.8727,5);
A=bv/K1_u/l1*(G/bv*cos(v1)-2.5*v1);

for i= 1:length(fuzzysad.output.mf)
    
    fuzzysad.output.mf(i).name=['A' mat2str(i)];
    fuzzysad.output.mf(i).params=A(i);
    fuzzysad.rule(i).antecedent = i;
    fuzzysad.rule(i).weight = 1;
    fuzzysad.rule(i).connection =1;
end
fuzzysad.output.range = [min(A) max(A)];
% writefis(fuzzysad, 'fuzzysad');