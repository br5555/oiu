fuzzyPI1 = readfis('fuzzyPI1.fis');



y_c=linspace(-4,4,45);  % centroidi ulaza
rules=[1:45];            % broj pravila
A=-1*y_c;               % izlazni singletoni

% Pridjeli vrijednosti izlaznim singletonima
fuzzyPI1.output.range = [min(A) max(A)];
for i = 1:length(fuzzyPI1.output.mf)
    fuzzyPI1.output.mf(i).name = ['A' mat2str(i)];
    fuzzyPI1.output.mf(i).params = A(i);
    fuzzyPI1.rule(i).antecedent = rules(i);
    fuzzyPI1.rule(i).consequent = i;
    fuzzyPI1.rule(i).weight = 1;
    fuzzyPI1.rule(i).connection = 1;
end
% zapisi sve to nazad u fis datoteku
writefis(fuzzyPI1,'fuzzyPI1');


% % Crtanje izoklina
% figure(1);clf;
% x=linspace(-3,3,70);
% y1=0;
% y2=x.*(x.^2-3*x+4);
% plot(x,y2,'r');
% grid on; hold;
% yL = ylim;
% line([0 0], yL);
% axis([-1 3 -4 6]);
% legend('Y=X(X^2-3X+4)','X=0');
% xlabel('X');ylabel('Y');
% title('Sjecište izoklina');

% Crtanje odziva sustava
ICX=0.4;
ICY=1;
t_sim=30;
sim Zad2;
figure(2);clf;
plot(tout(:,1),X(:,1),'b',tout(:,1),Y(:,1),'r');
legend('X, X0=0.4','Y, Y0=1'); grid on;
xlabel('time [s]');ylabel('X odziv/ Y odziv');
title('Odziv sustava s obzirom na poèetne uvjete');

ICX=1.5;
ICY=-2.8;
t_sim=30;
sim Zad2;
figure(3);clf;
plot(tout(:,1),X(:,1),'b',tout(:,1),Y(:,1),'r');
legend('X, X0=1.5','Y, Y0=-2.8'); grid on;
xlabel('time [s]');ylabel('X odziv/ Y odziv');
title('Odziv sustava s obzirom na poèetne uvjete');

ICX=-2.1;
ICY=4.5;
t_sim=30;
sim Zad2;
figure(4);clf;
plot(tout(:,1),X(:,1),'b',tout(:,1),Y(:,1),'r');
legend('X, X0=-2.1','Y, Y0=4.5'); grid on;
xlabel('time [s]');ylabel('X odziv/ Y odziv');
title('Odziv sustava s obzirom na poèetne uvjete');

ICX=2;
ICY=4;
t_sim=30;
sim Zad2;
figure(5);clf;
plot(tout(:,1),X(:,1),'b',tout(:,1),Y(:,1),'r');
legend('X, X0=2','Y, Y0=4'); grid on;
xlabel('time [s]');ylabel('X odziv/ Y odziv');
title('Odziv sustava s obzirom na pocetne uvjete');