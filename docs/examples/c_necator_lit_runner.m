f=estimate(m,10);

f=continuate(f,m);

filename = 'C_necator.mat';
save(filename,'f','m')