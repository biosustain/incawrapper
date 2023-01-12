f=estimate(m,10);

f=continuate(f,m);

filename = 'simple_model.mat';
save(filename,'f','m')