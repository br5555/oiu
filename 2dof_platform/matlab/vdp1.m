function xdot = vdp1(t,x)
xdot= zeros(2,1);
xdot(1)=x(2)-2*x(1);
xdot(2) = x(1)*((x(1))^2-3*x(1)+4)-x(2);
