t=linspace(0,1,529)
num=xlsread('Book1.xlsx');
z=num(1:end,1);
xa=num(1:end,2);
ya=num(1:end,3);
x_refa=num(1:end,4);
y_refa=num(1:end,5);
phi_1a=num(1:end,6);
phi_2a=num(1:end,7);
xxa=xa-x_refa;
for i=1:529
    deltax=xxa(i+1)-xxa(i)
end
num=xlsread('Book2.xlsx');
z1=num(1:end,1);
xb=num(1:end,2);
yb=num(1:end,3);
x_refb=num(1:end,4);
y_refb=num(1:end,5);
phi_1b=num(1:end,6);
phi_2b=num(1:end,7);
num=xlsread('Book3.xlsx');
z2=num(1:end,1);
xc=num(1:end,2);
yc=num(1:end,3);
x_refc=num(1:end,4);
y_refc=num(1:end,5);
phi_1c=num(1:end,6);
phi_2c=num(1:end,7);
num=xlsread('Book4.xlsx');
z3=num(1:end,1);
xd=num(1:end,2);
yd=num(1:end,3);
x_refd=num(1:end,4);
y_refd=num(1:end,5);
phi_1d=num(1:end,6);
phi_2d=num(1:end,7);
num=xlsread('Book5.xlsx');
z4=num(1:end,1);
xe=num(1:end,2);
ye=num(1:end,3);
x_refe=num(1:end,4);
y_refe=num(1:end,5);
phi_1e=num(1:end,6);
phi_2e=num(1:end,7);
num=xlsread('Book6.xlsx');
z5=num(1:end,1);
xf=num(1:end,2);
yf=num(1:end,3);
x_reff=num(1:end,4);
y_reff=num(1:end,5);
phi_1f=num(1:end,6);
phi_2f=num(1:end,7);
num=xlsread('Book7.xlsx');
z6=num(1:end,1);
xg=num(1:end,2);
yg=num(1:end,3);
x_refg=num(1:end,4);
y_refg=num(1:end,5);
phi_1g=num(1:end,6);
phi_2g=num(1:end,7);
num=xlsread('Book8.xlsx');
z7=num(1:end,1);
xh=num(1:end,2);
yh=num(1:end,3);
x_refh=num(1:end,4);
y_refh=num(1:end,5);
phi_1h=num(1:end,6);
phi_2h=num(1:end,7);
num=xlsread('Book9.xlsx');
z8=num(1:end,1);
xi=num(1:end,2);
yi=num(1:end,3);
x_refi=num(1:end,4);
y_refi=num(1:end,5);
phi_1i=num(1:end,6);
phi_2i=num(1:end,7);
num=xlsread('Book10.xlsx');
z9=num(1:end,1);
xj=num(1:end,2);
yj=num(1:end,3);
x_refj=num(1:end,4);
y_refj=num(1:end,5);
phi_1j=num(1:end,6);
phi_2j=num(1:end,7);
num=xlsread('Book11.xlsx');
z10=num(1:end,1);
xk=num(1:end,2);
yk=num(1:end,3);
x_refk=num(1:end,4);
y_refk=num(1:end,5);
phi_1k=num(1:end,6);
phi_2k=num(1:end,7);
num=xlsread('Book12.xlsx');
z11=num(1:end,1);
xl=num(1:end,2);
yl=num(1:end,3);
x_refl=num(1:end,4);
y_refl=num(1:end,5);
phi_1l=num(1:end,6);
phi_2l=num(1:end,7);
num=xlsread('Book13.xlsx');
z12=num(1:end,1);
xm=num(1:end,2);
ym=num(1:end,3);
x_refm=num(1:end,4);
y_refm=num(1:end,5);
phi_1m=num(1:end,6);
phi_2m=num(1:end,7);
num=xlsread('Book14.xlsx');
z13=num(1:end,1);
xn=num(1:end,2);
yn=num(1:end,3);
x_refn=num(1:end,4);
y_refn=num(1:end,5);
phi_1n=num(1:end,6);
phi_2n=num(1:end,7);
num=xlsread('Book15.xlsx');
z14=num(1:end,1);
xo=num(1:end,2);
yo=num(1:end,3);
x_refo=num(1:end,4);
y_refo=num(1:end,5);
phi_1o=num(1:end,6);
phi_2o=num(1:end,7);
num=xlsread('Book16.xlsx');
z15=num(1:end,1);
xp=num(1:end,2);
yp=num(1:end,3);
x_refp=num(1:end,4);
y_refp=num(1:end,5);
phi_1p=num(1:end,6);
phi_2p=num(1:end,7);
num=xlsread('Book17.xlsx');
z16=num(1:end,1);
xr=num(1:end,2);
yr=num(1:end,3);
x_refr=num(1:end,4);
y_refr=num(1:end,5);
phi_1r=num(1:end,6);
phi_2r=num(1:end,7);
num=xlsread('Book18.xlsx');
z17=num(1:end,1);
xs=num(1:end,2);
ys=num(1:end,3);
x_refs=num(1:end,4);
y_refs=num(1:end,5);
phi_1s=num(1:end,6);
phi_2s=num(1:end,7);
num=xlsread('Book19.xlsx');
z18=num(1:end,1);
xt=num(1:end,2);
yt=num(1:end,3);
x_reft=num(1:end,4);
y_reft=num(1:end,5);
phi_1t=num(1:end,6);
phi_2t=num(1:end,7);
num=xlsread('Book20.xlsx');
z19=num(1:end,1);
xu=num(1:end,2);
yu=num(1:end,3);
x_refu=num(1:end,4);
y_refu=num(1:end,5);
phi_1u=num(1:end,6);
phi_2u=num(1:end,7);
num=xlsread('Book21.xlsx');
z20=num(1:end,1);
xh1=num(1:end,2);
yh1=num(1:end,3);
x_refh1=num(1:end,4);
y_refh1=num(1:end,5);
phi_1h1=num(1:end,6);
phi_2h1=num(1:end,7);
num=xlsread('Book22.xlsx');
z21=num(1:end,1);
xi2=num(1:end,2);
yi2=num(1:end,3);
x_refi2=num(1:end,4);
y_refi2=num(1:end,5);
phi_1i2=num(1:end,6);
phi_2i2=num(1:end,7);
num=xlsread('Book23.xlsx');
z22=num(1:end,1);
xj3=num(1:end,2);
yj3=num(1:end,3);
x_refj3=num(1:end,4);
y_refj3=num(1:end,5);
phi_1j3=num(1:end,6);
phi_2j3=num(1:end,7);
num=xlsread('Book24.xlsx');
z23=num(1:end,1);
xk4=num(1:end,2);
yk4=num(1:end,3);
x_refk4=num(1:end,4);
y_refk4=num(1:end,5);
phi_1k4=num(1:end,6);
phi_2k4=num(1:end,7);
num=xlsread('Book25.xlsx');
z24=num(1:end,1);
xl5=num(1:end,2);
yl5=num(1:end,3);
x_refl5=num(1:end,4);
y_refl5=num(1:end,5);
phi_1l5=num(1:end,6);
phi_2l5=num(1:end,7);
num=xlsread('Book26.xlsx');
z25=num(1:end,1);
xm1=num(1:end,2);
ym1=num(1:end,3);
x_refm1=num(1:end,4);
y_refm1=num(1:end,5);
phi_1m1=num(1:end,6);
phi_2m1=num(1:end,7);
num=xlsread('Book27.xlsx');
z26=num(1:end,1);
xn1=num(1:end,2);
yn1=num(1:end,3);
x_refn1=num(1:end,4);
y_refn1=num(1:end,5);
phi_1n1=num(1:end,6);
phi_2n1=num(1:end,7);
num=xlsread('Book28.xlsx');
z27=num(1:end,1);
xo1=num(1:end,2);
yo1=num(1:end,3);
x_refo1=num(1:end,4);
y_refo1=num(1:end,5);
phi_1o1=num(1:end,6);
phi_2o1=num(1:end,7);
num=xlsread('Book29.xlsx');
z28=num(1:end,1);
xp1=num(1:end,2);
yp1=num(1:end,3);
x_refp1=num(1:end,4);
y_refp1=num(1:end,5);
phi_1p1=num(1:end,6);
phi_2p1=num(1:end,7);
num=xlsread('Book30.xlsx');
z29=num(1:end,1);
xr1=num(1:end,2);
yr1=num(1:end,3);
x_refr1=num(1:end,4);
y_refr1=num(1:end,5);
phi_1r1=num(1:end,6);
phi_2r1=num(1:end,7);
num=xlsread('Book31.xlsx');
z30=num(1:end,1);
xs1=num(1:end,2);
ys1=num(1:end,3);
x_refs1=num(1:end,4);
y_refs1=num(1:end,5);
phi_1s1=num(1:end,6);
phi_2s1=num(1:end,7);
num=xlsread('Book32.xlsx');
z31=num(1:end,1);
xt1=num(1:end,2);
yt1=num(1:end,3);
x_reft1=num(1:end,4);
y_reft1=num(1:end,5);
phi_1t1=num(1:end,6);
phi_2t1=num(1:end,7);
num=xlsread('Book33.xlsx');
z32=num(1:end,1);
xu1=num(1:end,2);
yu1=num(1:end,3);
x_refu1=num(1:end,4);
y_refu1=num(1:end,5);
phi_1u1=num(1:end,6);
phi_2u1=num(1:end,7);