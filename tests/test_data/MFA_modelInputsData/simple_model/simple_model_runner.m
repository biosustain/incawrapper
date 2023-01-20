f=estimate(m,10);

f=continuate(f,m);

s=simulate(m)

filename = 'simple_model.mat';
save(filename,'f','m','s')