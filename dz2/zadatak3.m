fuzzyPI2 = readfis('fuzzyPI2.fis');

x_c=linspace(-5,5,45);           % centroidi ulaza
rules=[1:45];                    % broj pravila
A = -0.3*x_c.^3+3.5*x_c.^2-5*x_c ;     % izlazni singletoni

% Pridjeli vrijednosti izlaznim singletonima
fuzzyPI2.output.range = [min(A) max(A)];
for i = 1:length(fuzzyPI2.output.mf)
    fuzzyPI2.output.mf(i).name = ['A' mat2str(i)];
    fuzzyPI2.output.mf(i).params = A(i);
    fuzzyPI2.rule(i).antecedent = rules(i);
    fuzzyPI2.rule(i).consequent = i;
    fuzzyPI2.rule(i).weight = 1;
    fuzzyPI2.rule(i).connection = 1;
end
% zapisi sve to nazad u fis datoteku
writefis(fuzzyPI2,'fuzzyPI2');


% % Crtanje izoklina
% figure(1);clf;
% x=linspace(-3,3,70);
% y1=2*x;
% y2=-x;
% plot(x,y1,'b',x,y2,'r');
% grid on;
% axis([-1 3 -4 6]);
% legend('Y=2X','Y=-X');
% xlabel('X');ylabel('Y');
% title('Sjecište izoklina');

% Crtanje odziva sustava
% ICX=0.4;
% ICY=1.4;
% t_sim=30;
% sim Zad3;
% figure(2);clf;
% plot(tout(:,1),X(:,1),'b',tout(:,1),Y(:,1),'r');
% legend('X, X0=0.4','Y, Y0=1.4'); grid on;
% xlabel('time [s]');ylabel('X odziv/ Y odziv');
% title('Odziv sustava s obzirom na poèetne uvjete');

% ICX=-15;
% ICY=-50;
% t_sim=30;
% sim Zad3;
% figure(3);clf;
% plot(tout(:,1),X(:,1),'b',tout(:,1),Y(:,1),'r');
% legend('X, X0=-15','Y, Y0=-50'); grid on;
% xlabel('time [s]');ylabel('X odziv/ Y odziv');
% title('Odziv sustava s obzirom na poèetne uvjete');
% 
% ICX=15;
% ICY=50;
% t_sim=30;
% sim Zad3;
% figure(4);clf;
% plot(tout(:,1),X(:,1),'b',tout(:,1),Y(:,1),'r');
% legend('X, X0=15','Y, Y0=50'); grid on;
% xlabel('time [s]');ylabel('X odziv/ Y odziv');
% title('Odziv sustava s obzirom na poèetne uvjete');

% ICX=0;
% ICY=0;
% t_sim=30;
% sim Zad3;
% figure(5);clf;
% plot(tout(:,1),X(:,1),'b',tout(:,1),Y(:,1),'r');
% legend('X, X0=0','Y, Y0=0'); grid on;
% xlabel('time [s]');ylabel('X odziv/ Y odziv');
% title('Odziv sustava s obzirom na pocetne uvjete');