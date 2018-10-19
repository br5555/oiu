[t, x]= ode45('vdp1', [0 20], [1 0]);
figure,plot(t,x(:,1),'r',t,x(:,2),'b-.')
figure,plot(x(:,1),x(:,2))


phaseport('vdp1', [0,20],[-6 6 -6 6], 'ode45');
function phasport(equations, timespan, plotrange,solver,parameter)
clf;
axis(plotrange);
hold on;
button=1,
while button == 1,
[xinit(1), xinit(2), button]= ginput(1);
if button ~= 1 break; end;
[T, Y]= feval(solver, equations,timespan,xinit,[],parameter);
plot(Y(:,1),Y(:,2));
[T, Y]= feval(solver,equtaions, -timespan,xinit,[],parameter);
plot(Y(:,1),Y(:,2));
end;
phaseport('vdp1', [0,20],[-6 6 -6 6], 'ode45',1);
end