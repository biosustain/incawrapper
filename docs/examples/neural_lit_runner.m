f=estimate(m,10);

f=continuate(f,m);

filename = 'Neural.mat';
save(filename,'f','m')