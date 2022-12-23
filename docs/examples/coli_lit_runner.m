f=estimate(m,10);

f=continuate(f,m);

filename = 'Coli_lit.mat';
save(filename,'f','m')