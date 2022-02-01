f=estimate(m,10);

f=continuate(f,m);

filename = 'TestFile.mat';
save(filename,'f','m')