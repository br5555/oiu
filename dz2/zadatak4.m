%----Promjena dinamike varijable x
fuzzy_zad2 = readfis('fuzzy_zad2.fis');

y_c=linspace(-6,6,9);   % centroidi ulaza
rules=[1:9];            % broj pravila
A=-0.9*y_c;                % izlazni singletoni

% Pridjeli vrijednosti izlaznim singletonima
fuzzy_zad2.output.range = [min(A) max(A)];
for i = 1:length(fuzzy_zad2.output.mf)
    fuzzy_zad2.output.mf(i).name = ['A' mat2str(i)];
    fuzzy_zad2.output.mf(i).params = A(i);
    fuzzy_zad2.rule(i).antecedent = rules(i);
    fuzzy_zad2.rule(i).consequent = i;
    fuzzy_zad2.rule(i).weight = 1;
    fuzzy_zad2.rule(i).connection = 1;
end
% zapisi sve to nazad u fis datoteku
writefis(fuzzy_zad2,'fuzzy_zad2');

% Crtanje izoklina
figure(5);clf;
x=linspace(-3,3,70);
y1=20*x;
y2=x.*(x.^2-3*x+4);
plot(x,y1,'b',x,y2,'r');
grid on;
axis([-1 3 -4 6]);
legend('Y=20X','Y=X(X^2-3X+4)');
xlabel('X');ylabel('Y');
title('Sjecište izoklina nakon promjene parametara');


%-------  Promjena dinamike varijable y  -------------

fuzzy_zad3 = readfis('fuzzy_zad3.fis');

x_c=linspace(-6,6,9);           % centroidi ulaza
rules=[1:9];                    % broj pravila
A = -x_c.^3+3*x_c.^2-5.1*x_c;     % izlazni singletoni

% Pridjeli vrijednosti izlaznim singletonima
fuzzy_zad3.output.range = [min(A) max(A)];
for i = 1:length(fuzzy_zad3.output.mf)
    fuzzy_zad3.output.mf(i).name = ['A' mat2str(i)];
    fuzzy_zad3.output.mf(i).params = A(i);
    fuzzy_zad3.rule(i).antecedent = rules(i);
    fuzzy_zad3.rule(i).consequent = i;
    fuzzy_zad3.rule(i).weight = 1;
    fuzzy_zad3.rule(i).connection = 1;
end
% zapisi sve to nazad u fis datoteku
writefis(fuzzy_zad3,'fuzzy_zad3');

% Crtanje izoklina
figure(6);clf;
x=linspace(-3,3,70);
y1=2*x;
y2=-1.1*x;
plot(x,y1,'b',x,y2,'r');
grid on;
axis([-1 3 -4 6]);
legend('Y=2X','Y=-1.1X');
xlabel('X');ylabel('Y');
title('Sjecište izoklina nakon promjene parametara');

%----------------------------------------------------
for j=1:4
    ICX=0;ICY=0;
    if j==1 
        ICX=-0.2;
        ICY=-1;
    elseif j==2
        ICX=-2.1;
        ICY=4.5;
    elseif j==3
        ICX=1.5;
        ICY=-2.8;
    elseif j==4
        ICX=0.4;
        ICY=1;
    end
    fuzzy_zad2 = readfis('fuzzy_zad2.fis');
    y_c=linspace(-6,6,9);   % centroidi ulaza
    rules=[1:9];            % broj pravila
    A=-1*y_c;                % izlazni singletoni

    % Pridjeli vrijednosti izlaznim singletonima
    fuzzy_zad2.output.range = [min(A) max(A)];
    for i = 1:length(fuzzy_zad2.output.mf)
        fuzzy_zad2.output.mf(i).name = ['A' mat2str(i)];
        fuzzy_zad2.output.mf(i).params = A(i);
        fuzzy_zad2.rule(i).antecedent = rules(i);
        fuzzy_zad2.rule(i).consequent = i;
        fuzzy_zad2.rule(i).weight = 1;
        fuzzy_zad2.rule(i).connection = 1;
    end
    % zapisi sve to nazad u fis datoteku
    writefis(fuzzy_zad2,'fuzzy_zad2');

    t_sim=20;
    sim Zad2;
    figure(j);clf;
    plot(tout(:,1),X(:,1),'m',tout(:,1),Y(:,1),'r');
    grid on;
    xlabel('time [s]');ylabel('X odziv/ Y odziv');
    title('Odziv sustava s obzirom na poèetne uvjete');
    hold;



    fuzzy_zad2 = readfis('fuzzy_zad2.fis');

    y_c=linspace(-6,6,9);   % centroidi ulaza
    rules=[1:9];            % broj pravila
    A=-0.9*y_c;                % izlazni singletoni

    % Pridjeli vrijednosti izlaznim singletonima
    fuzzy_zad2.output.range = [min(A) max(A)];
    for i = 1:length(fuzzy_zad2.output.mf)
        fuzzy_zad2.output.mf(i).name = ['A' mat2str(i)];
        fuzzy_zad2.output.mf(i).params = A(i);
        fuzzy_zad2.rule(i).antecedent = rules(i);
        fuzzy_zad2.rule(i).consequent = i;
        fuzzy_zad2.rule(i).weight = 1;
     fuzzy_zad2.rule(i).connection = 1;
    end
    % zapisi sve to nazad u fis datoteku
    writefis(fuzzy_zad2,'fuzzy_zad2');

    t_sim=20;
    sim Zad2;
    figure(j);
    plot(tout(:,1),X(:,1),'g',tout(:,1),Y(:,1),'b');
    legend('X prije promjene parametara','Y prije promjene parametara','X poslije promjene parametara','Y poslije promjene parametara');
    grid on;
    xlabel('time [s]');ylabel('X odziv/ Y odziv');
    title('Odziv sustava s obzirom na poèetne uvjete');
end           
%----------------------------------------------------
for k=7:10
    ICX=0;ICY=0;
        if k==7 
            ICX=-0.2;
            ICY=-1;
        elseif k==8
            ICX=-2.1;
            ICY=4.5;
        elseif k==9
            ICX=1.5;
            ICY=-2.8;
        elseif k==10
            ICX=0.4;
            ICY=1;
        end

    fuzzy_zad2 = readfis('fuzzy_zad2.fis');
    y_c=linspace(-6,6,9);   % centroidi ulaza
    rules=[1:9];            % broj pravila
    A=-1*y_c;                % izlazni singletoni
    fuzzy_zad2.output.range = [min(A) max(A)];
    for i = 1:length(fuzzy_zad2.output.mf)
        fuzzy_zad2.output.mf(i).name = ['A' mat2str(i)];
        fuzzy_zad2.output.mf(i).params = A(i);
        fuzzy_zad2.rule(i).antecedent = rules(i);
        fuzzy_zad2.rule(i).consequent = i;
        fuzzy_zad2.rule(i).weight = 1;
        fuzzy_zad2.rule(i).connection = 1;
    end
    writefis(fuzzy_zad2,'fuzzy_zad2');
%--
    t_sim=20;
    sim Zad2;
    figure(k);clf;
    plot(tout(:,1),X(:,1),'m',tout(:,1),Y(:,1),'r');
    grid on;
    xlabel('time [s]');ylabel('X odziv/ Y odziv');
    hold;
    %--
    fuzzy_zad3 = readfis('fuzzy_zad3.fis');
    x_c=linspace(-6,6,9);           % centroidi ulaza
    rules=[1:9];                    % broj pravila
    A = -x_c.^3+3*x_c.^2-5*x_c;     % izlazni singletoni
    fuzzy_zad3.output.range = [min(A) max(A)];
    for i = 1:length(fuzzy_zad3.output.mf)
        fuzzy_zad3.output.mf(i).name = ['A' mat2str(i)];
        fuzzy_zad3.output.mf(i).params = A(i);
        fuzzy_zad3.rule(i).antecedent = rules(i);
        fuzzy_zad3.rule(i).consequent = i;
        fuzzy_zad3.rule(i).weight = 1;
        fuzzy_zad3.rule(i).connection = 1;
    end
    writefis(fuzzy_zad3,'fuzzy_zad3');
    %--
    t_sim=20;
    sim Zad3;
    figure(k);
    plot(tout(:,1),X(:,1),'g',tout(:,1),Y(:,1),'b');
    legend('X kod promjene dinamike varijable X','Y kod promjene dinamike varijable X','X kod promjene dinamike varijable Y','Y kod promjene dinamike varijable Y'); grid on;
    xlabel('time [s]');ylabel('X odziv/ Y odziv');
    title('Usporedba odziva sustava bez promjene parametara');
    %--
end
%----------------------------------------------------