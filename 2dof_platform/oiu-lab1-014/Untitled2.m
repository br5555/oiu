clear all
clc
t=linspace(0,1,134)
num=xlsread('Book36.xlsx');
z=num(1:end,1);
xa=num(1:end,2);
ya=num(1:end,3);
x_refa=num(1:end,4);
y_refa=num(1:end,5);
phi_1a=num(1:end,6);
phi_2a=num(1:end,7);
xxa=xa-x_refa;
for i=1:133
    deltax(i)=xxa(i+1)-xxa(i);
end
deltax(134)=0;
yya=ya-y_refa;
for i=1:133
    deltay(i)=yya(i+1)-yya(i);
end
deltay(134)=0;
figure
plot(t,xxa)
title('ex')
figure
plot(t,deltax)
title('dex')
figure
plot(t,yya)
title('ey')
figure
plot(t,deltay)
title('dey')
