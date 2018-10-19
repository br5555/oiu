% Crtanje izoklina
figure(1);clf;
x=linspace(-3,3,70);
y1=2*x;
y2=x.*(x.^2-3*x+4);
plot(x,y1,'b',x,y2,'r');
grid on;
axis([-1 3 -4 6]);
legend('Y=2X','Y=X(X^2-3X+4)');
xlabel('X');ylabel('Y');
title('Sjecište izoklina');

% Crtanje odziva sustava
ICX=0.4;
ICY=1;
t_sim=20;
sim zad1;
figure(2);clf;
plot(tout(:,1),X(:,1),'b',tout(:,1),Y(:,1),'r');
legend('X, X0=0.4','Y, Y0=1'); grid on;
xlabel('time [s]');ylabel('X odziv/ Y odziv');
title('Odziv sustava s obzirom na poèetne uvjete');

ICX=1.5;
ICY=2.8;
t_sim=20;
sim zad1;
figure(3);clf;
plot(tout(:,1),X(:,1),'b',tout(:,1),Y(:,1),'r');
legend('X, X0=1.5','Y, Y0=2.8'); grid on;
xlabel('time [s]');ylabel('X odziv/ Y odziv');
title('Odziv sustava s obzirom na poèetne uvjete');

ICX=2.1;
ICY=4.5;
t_sim=3.2;
sim zad1;
figure(4);clf;
plot(tout(:,1),X(:,1),'b',tout(:,1),Y(:,1),'r');
legend('X, X0=2.1','Y, Y0=4.5'); grid on;
xlabel('time [s]');ylabel('X odziv/ Y odziv');
title('Odziv sustava s obzirom na poèetne uvjete');
axis([0 3.2 0 95 ]);

ICX=-0.2;
ICY=-0.6;
t_sim=2.7;
sim zad1;
figure(5);clf;
plot(tout(:,1),X(:,1),'b',tout(:,1),Y(:,1),'r');
legend('X, X0=-0.2','Y, Y0=-0.6'); grid on;
xlabel('time [s]');ylabel('X odziv/ Y odziv');
title('Odziv sustava s obzirom na poèetne uvjete');
axis([0 2.7 0 -90 ]);