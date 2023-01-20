clear functions

r = reaction({... % define reactions
'1.0*FRU.ext (C1:a C2:b C3:c C4:d C5:e C6:f) -> 1.0*F6P (C1:a C2:b C3:c C4:d C5:e C6:f) ';...
'1.0*GLY.ext (C1:a C2:b C3:c) -> 1.0*GLY (C1:a C2:b C3:c) ';...
'1.0*GLY (C1:a C2:b C3:c) -> 1.0*DHAP (C1:a C2:b C3:c) ';...
'1.0*3PG (C1:a C2:b C3:c) -> 1.0*G3P (C1:a C2:b C3:c) ';...
'1.0*3PG (C1:a C2:b C3:c) -> 1.0*PEP (C1:a C2:b C3:c) ';...
'1.0*PEP (C1:a C2:b C3:c) -> 1.0*3PG (C1:a C2:b C3:c) ';...
'1.0*PEP (C1:a C2:b C3:c) -> 1.0*PYR (C1:a C2:b C3:c) ';...
'1.0*PYR (C1:a C2:b C3:c) -> 1.0*PEP (C1:a C2:b C3:c) ';...
'1.0*PYR (C1:a C2:b C3:c) -> 1.0*ACCOA (C1:b C2:c) + 1.0*CO2 (C1:a) ';...
'1.0*OAA (C1:a C2:b C3:c C4:d) + 1.0*ACCOA (C1:e C2:f) -> 1.0*CIT (C1:d C2:c C3:b C4:f C5:e C6:a) ';...
'1.0*CIT (C1:a C2:b C3:c C4:d C5:e C6:f) -> 1.0*ISCIT (C1:a C2:b C3:c C4:d C5:e C6:f) ';...
'1.0*ISCIT (C1:a C2:b C3:c C4:d C5:e C6:f) -> 1.0*CIT (C1:a C2:b C3:c C4:d C5:e C6:f) ';...
'1.0*ISCIT (C1:a C2:b C3:c C4:d C5:e C6:f) -> 1.0*AKG (C1:a C2:b C3:c C4:d C5:e) + 1.0*CO2 (C1:f) ';...
'1.0*F6P (C1:a C2:b C3:c C4:d C5:e C6:f) -> 1.0*G6P (C1:a C2:b C3:c C4:d C5:e C6:f) ';...
'1.0*AKG (C1:a C2:b C3:c C4:d C5:e) -> 1.0*SUCOA (C1:b C2:c C3:d C4:e) + 1.0*CO2 (C1:a) ';...
'1.0*SUCOA (C1:a C2:b C3:c C4:d) -> 1.0*SUC (C1:a C2:b C3:c C4:d) ';...
'1.0*SUC (C1:a C2:b C3:c C4:d) -> 1.0*MAL (C1:a C2:b C3:c C4:d) ';...
'1.0*MAL (C1:a C2:b C3:c C4:d) -> 1.0*SUC (C1:a C2:b C3:c C4:d) ';...
'1.0*MAL (C1:a C2:b C3:c C4:d) -> 1.0*OAA (C1:a C2:b C3:c C4:d) ';...
'1.0*OAA (C1:a C2:b C3:c C4:d) -> 1.0*MAL (C1:a C2:b C3:c C4:d) ';...
'1.0*G6P (C1:a C2:b C3:c C4:d C5:e C6:f) -> 1.0*6PG (C1:a C2:b C3:c C4:d C5:e C6:f) ';...
'1.0*6PG (C1:a C2:b C3:c C4:d C5:e C6:f) -> 1.0*PYR (C1:a C2:b C3:c) + 1.0*G3P (C1:d C2:e C3:f) ';...
'1.0*ISCIT (C1:a C2:b C3:c C4:d C5:e C6:f) -> 1.0*GLYOXY (C1:a C2:b) + 1.0*SUC (C1:e C2:d C3:c C4:f) ';...
'1.0*GLYOXY (C1:a C2:b) + 1.0*ACCOA (C1:c C2:d) -> 1.0*MAL (C1:a C2:b C3:d C4:c) ';...
'1.0*G6P (C1:a C2:b C3:c C4:d C5:e C6:f) -> 1.0*F6P (C1:a C2:b C3:c C4:d C5:e C6:f) ';...
'1.0*MAL (C1:a C2:b C3:c C4:d) -> 1.0*PYR (C1:a C2:b C3:c) + 1.0*CO2 (C1:d) ';...
'1.0*PEP (C1:a C2:b C3:c) + 1.0*CO2 (C1:d) -> 1.0*OAA (C1:a C2:b C3:c C4:d) ';...
'1.0*OAA (C1:a C2:b C3:c C4:d) -> 1.0*PEP (C1:a C2:b C3:c) + 1.0*CO2 (C1:d) ';...
'1.0*OAA (C1:a C2:b C3:c C4:d) -> 1.0*PYR (C1:a C2:b C3:c) + 1.0*CO2 (C1:d) ';...
'1.0*RU5P (C1:a C2:b C3:c C4:d C5:e) -> 1.0*R5P (C1:a C2:b C3:c C4:d C5:e) ';...
'1.0*R5P (C1:a C2:b C3:c C4:d C5:e) -> 1.0*RU5P (C1:a C2:b C3:c C4:d C5:e) ';...
'1.0*RU5P (C1:a C2:b C3:c C4:d C5:e) -> 1.0*X5P (C1:a C2:b C3:c C4:d C5:e) ';...
'1.0*X5P (C1:a C2:b C3:c C4:d C5:e) -> 1.0*RU5P (C1:a C2:b C3:c C4:d C5:e) ';...
'1.0*X5P (C1:a C2:b C3:c C4:d C5:e) + 1.0*R5P (C1:f C2:g C3:h C4:i C5:j) -> 1.0*G3P (C1:c C2:d C3:e) + 1.0*S7P (C1:a C2:b C3:f C4:g C5:h C6:i C7:j) ';...
'1.0*G3P (C1:c C2:d C3:e) + 1.0*S7P (C1:a C2:b C3:f C4:g C5:h C6:i C7:j) -> 1.0*X5P (C1:a C2:b C3:c C4:d C5:e) + 1.0*R5P (C1:f C2:g C3:h C4:i C5:j) ';...
'1.0*F16P (C1:a C2:b C3:c C4:d C5:e C6:f) -> 1.0*F6P (C1:a C2:b C3:c C4:d C5:e C6:f) ';...
'1.0*S7P (C1:a C2:b C3:c C4:d C5:e C6:f C7:g) + 1.0*G3P (C1:h C2:i C3:j) -> 1.0*E4P (C1:d C2:e C3:f C4:g) + 1.0*F6P (C1:a C2:b C3:c C4:h C5:i C6:j) ';...
'1.0*E4P (C1:d C2:e C3:f C4:g) + 1.0*F6P (C1:a C2:b C3:c C4:h C5:i C6:j) -> 1.0*S7P (C1:a C2:b C3:c C4:d C5:e C6:f C7:g) + 1.0*G3P (C1:h C2:i C3:j) ';...
'1.0*E4P (C1:f C2:g C3:h C4:i) + 1.0*X5P (C1:a C2:b C3:c C4:d C5:e) -> 1.0*F6P (C1:a C2:b C3:f C4:g C5:h C6:i) + 1.0*G3P (C1:c C2:d C3:e) ';...
'1.0*F6P (C1:a C2:b C3:f C4:g C5:h C6:i) + 1.0*G3P (C1:c C2:d C3:e) -> 1.0*E4P (C1:f C2:g C3:h C4:i) + 1.0*X5P (C1:a C2:b C3:c C4:d C5:e) ';...
'1.0*DHAP (C1:e C2:f C3:g) + 1.0*E4P (C1:a C2:b C3:c C4:d) -> 1.0*S7P (C1:g C2:f C3:e C4:a C5:b C6:c C7:d) ';...
'1.0*RU5P (C1:a C2:b C3:c C4:d C5:e) -> 1.0*RUBP (C1:a C2:b C3:c C4:d C5:e) ';...
'1.0*RUBP (C1:a C2:b C3:c C4:d C5:e) + 1.0*CO2 (C1:f) -> 1.0*3PG (C1:f C2:b C3:a) + 1.0*3PG (C1:c C2:d C3:e) ';...
'1.0*AKG (C1:a C2:b C3:c C4:d C5:e) -> 1.0*GLU (C1:a C2:b C3:c C4:d C5:e) ';...
'1.0*AKG (C1:a C2:b C3:c C4:d C5:e) -> 1.0*PRO (C1:a C2:b C3:c C4:d C5:e) ';...
'1.0*AKG (C1:a C2:b C3:c C4:d C5:e) + 1.0*CO2 (C1:f) -> 1.0*ARG (C1:a C2:b C3:c C4:d C5:e C6:f) ';...
'1.0*F16P (C1:a C2:b C3:c C4:d C5:e C6:f) -> 1.0*DHAP (C1:c C2:b C3:a) + 1.0*G3P (C1:d C2:e C3:f) ';...
'1.0*OAA (C1:a C2:b C3:c C4:d) -> 1.0*ASP (C1:a C2:b C3:c C4:d) ';...
'1.0*PYR (C1:a C2:b C3:c) -> 1.0*ALA (C1:a C2:b C3:c) ';...
'1.0*3PG (C1:a C2:b C3:c) -> 1.0*SER (C1:a C2:b C3:c) ';...
'1.0*3PG (C1:a C2:b C3:c) -> 1.0*CYS (C1:a C2:b C3:c) ';...
'1.0*3PG (C1:a C2:b C3:c) -> 1.0*GL (C1:a C2:b) + 1.0*MTHF (C1:c) ';...
'1.0*OAA (C1:a C2:b C3:c C4:d) -> 1.0*GL (C1:a C2:b) + 1.0*ACCOA (C1:c C2:d) ';...
'1.0*OAA (C1:a C2:b C3:c C4:d) -> 1.0*THR (C1:a C2:b C3:c C4:d) ';...
'1.0*OAA (C1:a C2:b C3:c C4:d) + 1.0*MTHF (C1:e) -> 1.0*MET (C1:a C2:b C3:c C4:d C5:e) ';...
'1.0*OAA (C1:a C2:b C3:c C4:d) + 1.0*PYR (C1:e C2:f C3:g) -> 1.0*LYS (C1:b C2:c C3:d C4:g C5:f C6:e) + 1.0*CO2 (C1:a) ';...
'1.0*PYR (C1:a C2:b C3:c) + 1.0*PYR (C1:d C2:e C3:f) -> 1.0*VAL (C1:a C2:b C3:c C4:e C5:f) + 1.0*CO2 (C1:d) ';...
'1.0*DHAP (C1:c C2:b C3:a) + 1.0*G3P (C1:d C2:e C3:f) -> 1.0*F16P (C1:a C2:b C3:c C4:d C5:e C6:f) ';...
'1.0*PYR (C1:a C2:b C3:c) + 1.0*PYR (C1:d C2:e C3:f) -> 1.0*ISV (C1:a C2:b C3:e C4:f C5:c) + 1.0*CO2 (C1:d) ';...
'1.0*ISV (C1:a C2:b C3:c C4:d C5:e) + 1.0*ACCOA (C1:f C2:g) -> 1.0*LEU (C1:f C2:g C3:b C4:c C5:d C6:e) + 1.0*CO2 (C1:a) ';...
'1.0*OAA (C1:a C2:b C3:c C4:d) + 1.0*PYR (C1:e C2:f C3:g) -> 1.0*ILE (C1:a C2:b C3:f C4:c C5:d C6:g) + 1.0*CO2 (C1:e) ';...
'1.0*E4P (C1:a C2:b C3:c C4:d) + 1.0*PEP (C1:e C2:f C3:g) -> 1.0*SHKM (C1:e C2:f C3:g C4:a C5:b C6:c C7:d) ';...
'1.0*SHKM (C1:a C2:b C3:c C4:d C5:e C6:f C7:g) + 1.0*PEP (C1:h C2:i C3:j) -> 1.0*CHRM (C1:a C2:b C3:c C4:d C5:e C6:f C7:g C8:h C9:i C10:j) ';...
'1.0*CHRM (C1:a C2:b C3:c C4:d C5:e C6:f C7:g C8:h C9:i C10:j) -> 1.0*PHE (C1:h C2:i C3:j C4:b C5:c C6:d C7:e C8:f C9:g) + 1.0*CO2 (C1:a) ';...
'1.0*CHRM (C1:a C2:b C3:c C4:d C5:e C6:f C7:g C8:h C9:i C10:j) -> 1.0*TYR (C1:h C2:i C3:j C4:b C5:c C6:d C7:e C8:f C9:g) + 1.0*CO2 (C1:a) ';...
'1.0*CHRM (C1:a C2:b C3:c C4:d C5:e C6:f C7:g C8:h C9:i C10:j) -> 1.0*ANTHR (C1:a C2:b C3:c C4:d C5:e C6:f C7:g) + 1.0*G3P (C1:h C2:i C3:j) ';...
'1.0*ANTHR (C1:a C2:b C3:c C4:d C5:e C6:f C7:g) + 1.0*R5P (C1:h C2:i C3:j C4:k C5:l) -> 1.0*CPADR5P (C1:a C2:b C3:c C4:d C5:e C6:f C7:g C8:h C9:i C10:j C11:k C12:l) ';...
'1.0*CPADR5P (C1:a C2:b C3:c C4:d C5:e C6:f C7:g C8:h C9:i C10:j C11:k C12:l) -> 1.0*INDG (C1:a C2:b C3:c C4:d C5:f C6:g C7:h C8:i C9:j C10:k C11:l) + 1.0*CO2 (C1:e) ';...
'1.0*DHAP (C1:a C2:b C3:c) -> 1.0*G3P (C1:a C2:b C3:c) ';...
'1.0*INDG (C1:a C2:b C3:c C4:d C5:f C6:g C7:h C8:i C9:j C10:k C11:l) -> 1.0*TRP (C1:a C2:b C3:c C4:d C5:f C6:g C7:h C8:i C9:j C10:k C11:l) ';...
'1.0*R5P (C1:a C2:b C3:c C4:d C5:e) + 1.0*MTHF (C1:f) -> 1.0*HIS (C1:e C2:d C3:c C4:b C5:a C6:f) ';...
'1.0*ACCOA -> 1.0*PHB_B ';...
'1.0*G3P (C1:a C2:b C3:c) -> 1.0*DHAP (C1:a C2:b C3:c) ';...
'1.0*G3P (C1:a C2:b C3:c) -> 1.0*3PG (C1:a C2:b C3:c) ';...
});

m = model(r); % set up model

% take care of symmetrical metabolites
m.mets{'SUCOA'}.sym = list('rotate180', atommap('C1:C4 C2:C3 C3:C2 C4:C1'));
m.mets{'SUC'}.sym = list('rotate180', atommap('C1:C4 C2:C3 C3:C2 C4:C1'));

% define unbalanced reactions

% define lower bounds
m.rates.flx.lb = [...
0,...
0.99,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
];

%define upper bounds
m.rates.flx.ub = [...
1000,...
1.01,...
1000,...
1000,...
1000,...
1000,...
1000,...
1000,...
1000,...
1000,...
1000,...
1000,...
1000,...
1000,...
1000,...
1000,...
1000,...
1000,...
1000,...
1000,...
1000,...
1000,...
1000,...
1000,...
1000,...
1000,...
1000,...
1000,...
1000,...
1000,...
1000,...
1000,...
1000,...
1000,...
1000,...
1000,...
1000,...
1000,...
1000,...
1000,...
1000,...
1000,...
1000,...
1000,...
1000,...
1000,...
1000,...
1000,...
1000,...
1000,...
1000,...
1000,...
1000,...
1000,...
1000,...
1000,...
1000,...
1000,...
1000,...
1000,...
1000,...
1000,...
1000,...
1000,...
1000,...
1000,...
1000,...
1000,...
1000,...
1000,...
1000,...
1000,...
1000,...
1000,...
];

% define flux vals
m.rates.flx.val = [...
0,...
1,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
0,...
];

% include/exclude reactions
m.rates.on = [...
true,...
true,...
true,...
true,...
true,...
true,...
true,...
true,...
true,...
true,...
true,...
true,...
true,...
true,...
true,...
true,...
true,...
true,...
true,...
true,...
true,...
true,...
true,...
true,...
true,...
true,...
true,...
true,...
true,...
true,...
true,...
true,...
true,...
true,...
true,...
true,...
true,...
true,...
true,...
true,...
true,...
true,...
true,...
true,...
true,...
true,...
true,...
true,...
true,...
true,...
true,...
true,...
true,...
true,...
true,...
true,...
true,...
true,...
true,...
true,...
true,...
true,...
true,...
true,...
true,...
true,...
true,...
true,...
true,...
true,...
true,...
true,...
true,...
true,...
];

% define reaction ids
m.rates.id = {...
'ex_1',...
'ex_2',...
'R1',...
'R10',...
'R11',...
'R12',...
'R13',...
'R14',...
'R15',...
'R16',...
'R17',...
'R18',...
'R19',...
'R2',...
'R20',...
'R21',...
'R22',...
'R23',...
'R24',...
'R25',...
'R26',...
'R27',...
'R28',...
'R29',...
'R3',...
'R30',...
'R31',...
'R32',...
'R33',...
'R34',...
'R35',...
'R36',...
'R37',...
'R38',...
'R39',...
'R4',...
'R40',...
'R41',...
'R42',...
'R43',...
'R44',...
'R45',...
'R46',...
'R47',...
'R48',...
'R49',...
'R5',...
'R50',...
'R51',...
'R52',...
'R53',...
'R54',...
'R55',...
'R56',...
'R57',...
'R58',...
'R59',...
'R6',...
'R60',...
'R61',...
'R62',...
'R63',...
'R64',...
'R65',...
'R66',...
'R67',...
'R68',...
'R69',...
'R7',...
'R70',...
'R71',...
'R72',...
'R8',...
'R9',...
};

m.rates.flx.val = mod2stoich(m); % make sure the fluxes are feasible
m.options.fit_starts = 10; % 10 restarts during the estimation procedure

% define which fragments of molecules were measured in which experiment
d = msdata({...
'Alanine232: ALA @ C1 C2';
'Alanine260: ALA @ C1 C2 C3';
'Asparticacid302: ASP @ C1 C2';
'Asparticacid390: ASP @ C1 C2 C3';
'Asparticacid418: ASP @ C1 C2 C3 C4';
'Glutamicacid330: GLU @ C1 C2 C3 C4';
'Glutamicacid432: GLU @ C1 C2 C3 C4 C5';
'Glycine218: GL @ C1';
'Glycine246: GL @ C1 C2';
'Histidine338: HIS @ C1 C2 C3 C4 C5';
'Histidine440: HIS @ C1 C2 C3 C4 C5 C6';
'Isoleucine274: ILE @ C1 C2 C3 C4 C5';
'Leucine274: LEU @ C1 C2 C3 C4 C5';
'Methionine320: MET @ C1 C2 C3 C4 C5';
'Phenylalanine302: PHE @ C1 C2';
'Phenylalanine308: PHE @ C1 C2 C3 C4 C5 C6 C7 C8';
'Phenylalanine336: PHE @ C1 C2 C3 C4 C5 C6 C7 C8 C9';
'Serine362: SER @ C1 C2';
'Serine390: SER @ C1 C2 C3';
'Threonine376: THR @ C1 C2 C3';
'Threonine404: THR @ C1 C2 C3 C4';
'Valine260: VAL @ C1 C2 C3 C4';
'Valine288: VAL @ C1 C2 C3 C4 C5';
});

% initialize mass distribution vector
d.idvs = idv;

% define tracers used in the experiments
t = tracer({...
'[1,2-13C]glycerol: GLY.ext.EX @ C1 C2';...
});

% define fractions of tracers used
t.frac = [ 1 ];

% define experiments for fit data
f = data(' ex_2 ');

% add fit values
f.val = [...
1,...
];
% add fit stds
f.std = [...
0.01,...
];

% initialize experiment with t and add f and d
x = experiment(t);
x.data_flx = f;
x.data_ms = d;

% assing all the previous values to a specific experiment
m.expts(1) = x;

m.expts(1).id = {'[1,2-13C]glycerol'};

% add experimental data for annotated fragments
m.expts(1).data_ms(1).idvs.id(1,1) = {'Alanine232_0_0_[1,2-13C]glycerol'};
m.expts(1).data_ms(1).idvs.time(1,1) = 0;
m.expts(1).data_ms(1).idvs.val(1,1) = 0.049500;
m.expts(1).data_ms(1).idvs.std(1,1) = 0.002200;
m.expts(1).data_ms(1).idvs.val(2,1) = 0.500200;
m.expts(1).data_ms(1).idvs.std(2,1) = 0.001;
m.expts(1).data_ms(1).idvs.val(3,1) = 0.450400;
m.expts(1).data_ms(1).idvs.std(3,1) = 0.002300;
m.expts(1).data_ms(2).idvs.id(1,1) = {'Alanine260_0_0_[1,2-13C]glycerol'};
m.expts(1).data_ms(2).idvs.time(1,1) = 0;
m.expts(1).data_ms(2).idvs.val(1,1) = 0.022100;
m.expts(1).data_ms(2).idvs.std(1,1) = 0.001300;
m.expts(1).data_ms(2).idvs.val(2,1) = 0.131700;
m.expts(1).data_ms(2).idvs.std(2,1) = 0.005600;
m.expts(1).data_ms(2).idvs.val(3,1) = 0.729000;
m.expts(1).data_ms(2).idvs.std(3,1) = 0.013100;
m.expts(1).data_ms(2).idvs.val(4,1) = 0.117145;
m.expts(1).data_ms(2).idvs.std(4,1) = 0.007000;
m.expts(1).data_ms(3).idvs.id(1,1) = {'Asparticacid302_0_0_[1,2-13C]glycerol'};
m.expts(1).data_ms(3).idvs.time(1,1) = 0;
m.expts(1).data_ms(3).idvs.val(1,1) = 0.087900;
m.expts(1).data_ms(3).idvs.std(1,1) = 0.002000;
m.expts(1).data_ms(3).idvs.val(2,1) = 0.488300;
m.expts(1).data_ms(3).idvs.std(2,1) = 0.001;
m.expts(1).data_ms(3).idvs.val(3,1) = 0.423800;
m.expts(1).data_ms(3).idvs.std(3,1) = 0.002100;
m.expts(1).data_ms(4).idvs.id(1,1) = {'Asparticacid390_0_0_[1,2-13C]glycerol'};
m.expts(1).data_ms(4).idvs.time(1,1) = 0;
m.expts(1).data_ms(4).idvs.val(1,1) = 0.032600;
m.expts(1).data_ms(4).idvs.std(1,1) = 0.001;
m.expts(1).data_ms(4).idvs.val(2,1) = 0.233500;
m.expts(1).data_ms(4).idvs.std(2,1) = 0.002900;
m.expts(1).data_ms(4).idvs.val(3,1) = 0.493700;
m.expts(1).data_ms(4).idvs.std(3,1) = 0.002100;
m.expts(1).data_ms(4).idvs.val(4,1) = 0.240100;
m.expts(1).data_ms(4).idvs.std(4,1) = 0.001800;
m.expts(1).data_ms(5).idvs.id(1,1) = {'Asparticacid418_0_0_[1,2-13C]glycerol'};
m.expts(1).data_ms(5).idvs.time(1,1) = 0;
m.expts(1).data_ms(5).idvs.val(1,1) = 0.013000;
m.expts(1).data_ms(5).idvs.std(1,1) = 0.001;
m.expts(1).data_ms(5).idvs.val(2,1) = 0.082700;
m.expts(1).data_ms(5).idvs.std(2,1) = 0.001800;
m.expts(1).data_ms(5).idvs.val(3,1) = 0.346000;
m.expts(1).data_ms(5).idvs.std(3,1) = 0.003100;
m.expts(1).data_ms(5).idvs.val(4,1) = 0.433900;
m.expts(1).data_ms(5).idvs.std(4,1) = 0.003300;
m.expts(1).data_ms(5).idvs.val(5,1) = 0.124300;
m.expts(1).data_ms(5).idvs.std(5,1) = 0.001400;
m.expts(1).data_ms(6).idvs.id(1,1) = {'Glutamicacid330_0_0_[1,2-13C]glycerol'};
m.expts(1).data_ms(6).idvs.time(1,1) = 0;
m.expts(1).data_ms(6).idvs.val(1,1) = 0.011300;
m.expts(1).data_ms(6).idvs.std(1,1) = 0.001;
m.expts(1).data_ms(6).idvs.val(2,1) = 0.086500;
m.expts(1).data_ms(6).idvs.std(2,1) = 0.001;
m.expts(1).data_ms(6).idvs.val(3,1) = 0.319700;
m.expts(1).data_ms(6).idvs.std(3,1) = 0.001500;
m.expts(1).data_ms(6).idvs.val(4,1) = 0.412800;
m.expts(1).data_ms(6).idvs.std(4,1) = 0.001600;
m.expts(1).data_ms(6).idvs.val(5,1) = 0.169700;
m.expts(1).data_ms(6).idvs.std(5,1) = 0.001;
m.expts(1).data_ms(7).idvs.id(1,1) = {'Glutamicacid432_0_0_[1,2-13C]glycerol'};
m.expts(1).data_ms(7).idvs.time(1,1) = 0;
m.expts(1).data_ms(7).idvs.val(1,1) = 0.003700;
m.expts(1).data_ms(7).idvs.std(1,1) = 0.001;
m.expts(1).data_ms(7).idvs.val(2,1) = 0.027900;
m.expts(1).data_ms(7).idvs.std(2,1) = 0.001;
m.expts(1).data_ms(7).idvs.val(3,1) = 0.156800;
m.expts(1).data_ms(7).idvs.std(3,1) = 0.001700;
m.expts(1).data_ms(7).idvs.val(4,1) = 0.363900;
m.expts(1).data_ms(7).idvs.std(4,1) = 0.001300;
m.expts(1).data_ms(7).idvs.val(5,1) = 0.341800;
m.expts(1).data_ms(7).idvs.std(5,1) = 0.001900;
m.expts(1).data_ms(7).idvs.val(6,1) = 0.105900;
m.expts(1).data_ms(7).idvs.std(6,1) = 0.001300;
m.expts(1).data_ms(8).idvs.id(1,1) = {'Glycine218_0_0_[1,2-13C]glycerol'};
m.expts(1).data_ms(8).idvs.time(1,1) = 0;
m.expts(1).data_ms(8).idvs.val(1,1) = 0.102500;
m.expts(1).data_ms(8).idvs.std(1,1) = 0.005200;
m.expts(1).data_ms(8).idvs.val(2,1) = 0.897400;
m.expts(1).data_ms(8).idvs.std(2,1) = 0.005200;
m.expts(1).data_ms(9).idvs.id(1,1) = {'Glycine246_0_0_[1,2-13C]glycerol'};
m.expts(1).data_ms(9).idvs.time(1,1) = 0;
m.expts(1).data_ms(9).idvs.val(1,1) = 0.043200;
m.expts(1).data_ms(9).idvs.std(1,1) = 0.002500;
m.expts(1).data_ms(9).idvs.val(2,1) = 0.473200;
m.expts(1).data_ms(9).idvs.std(2,1) = 0.003500;
m.expts(1).data_ms(9).idvs.val(3,1) = 0.483500;
m.expts(1).data_ms(9).idvs.std(3,1) = 0.004100;
m.expts(1).data_ms(10).idvs.id(1,1) = {'Histidine338_0_0_[1,2-13C]glycerol'};
m.expts(1).data_ms(10).idvs.time(1,1) = 0;
m.expts(1).data_ms(10).idvs.val(1,1) = 0.001800;
m.expts(1).data_ms(10).idvs.std(1,1) = 0.001;
m.expts(1).data_ms(10).idvs.val(2,1) = 0.036800;
m.expts(1).data_ms(10).idvs.std(2,1) = 0.003000;
m.expts(1).data_ms(10).idvs.val(3,1) = 0.172200;
m.expts(1).data_ms(10).idvs.std(3,1) = 0.004200;
m.expts(1).data_ms(10).idvs.val(4,1) = 0.364000;
m.expts(1).data_ms(10).idvs.std(4,1) = 0.004700;
m.expts(1).data_ms(10).idvs.val(5,1) = 0.313600;
m.expts(1).data_ms(10).idvs.std(5,1) = 0.003700;
m.expts(1).data_ms(10).idvs.val(6,1) = 0.111400;
m.expts(1).data_ms(10).idvs.std(6,1) = 0.002700;
m.expts(1).data_ms(11).idvs.id(1,1) = {'Histidine440_0_0_[1,2-13C]glycerol'};
m.expts(1).data_ms(11).idvs.time(1,1) = 0;
m.expts(1).data_ms(11).idvs.val(1,1) = 0.001600;
m.expts(1).data_ms(11).idvs.std(1,1) = 0.001200;
m.expts(1).data_ms(11).idvs.val(2,1) = 0.013700;
m.expts(1).data_ms(11).idvs.std(2,1) = 0.002100;
m.expts(1).data_ms(11).idvs.val(3,1) = 0.075400;
m.expts(1).data_ms(11).idvs.std(3,1) = 0.003600;
m.expts(1).data_ms(11).idvs.val(4,1) = 0.282500;
m.expts(1).data_ms(11).idvs.std(4,1) = 0.002900;
m.expts(1).data_ms(11).idvs.val(5,1) = 0.404700;
m.expts(1).data_ms(11).idvs.std(5,1) = 0.008700;
m.expts(1).data_ms(11).idvs.val(6,1) = 0.206100;
m.expts(1).data_ms(11).idvs.std(6,1) = 0.001400;
m.expts(1).data_ms(11).idvs.val(7,1) = 0.015800;
m.expts(1).data_ms(11).idvs.std(7,1) = 0.003500;
m.expts(1).data_ms(12).idvs.id(1,1) = {'Isoleucine274_0_0_[1,2-13C]glycerol'};
m.expts(1).data_ms(12).idvs.time(1,1) = 0;
m.expts(1).data_ms(12).idvs.val(1,1) = 0.003900;
m.expts(1).data_ms(12).idvs.std(1,1) = 0.001;
m.expts(1).data_ms(12).idvs.val(2,1) = 0.027900;
m.expts(1).data_ms(12).idvs.std(2,1) = 0.001;
m.expts(1).data_ms(12).idvs.val(3,1) = 0.153200;
m.expts(1).data_ms(12).idvs.std(3,1) = 0.002400;
m.expts(1).data_ms(12).idvs.val(4,1) = 0.361300;
m.expts(1).data_ms(12).idvs.std(4,1) = 0.001100;
m.expts(1).data_ms(12).idvs.val(5,1) = 0.343500;
m.expts(1).data_ms(12).idvs.std(5,1) = 0.001;
m.expts(1).data_ms(12).idvs.val(6,1) = 0.110300;
m.expts(1).data_ms(12).idvs.std(6,1) = 0.003500;
m.expts(1).data_ms(13).idvs.id(1,1) = {'Leucine274_0_0_[1,2-13C]glycerol'};
m.expts(1).data_ms(13).idvs.time(1,1) = 0;
m.expts(1).data_ms(13).idvs.val(1,1) = 0.002200;
m.expts(1).data_ms(13).idvs.std(1,1) = 0.001;
m.expts(1).data_ms(13).idvs.val(2,1) = 0.024800;
m.expts(1).data_ms(13).idvs.std(2,1) = 0.001100;
m.expts(1).data_ms(13).idvs.val(3,1) = 0.167800;
m.expts(1).data_ms(13).idvs.std(3,1) = 0.001200;
m.expts(1).data_ms(13).idvs.val(4,1) = 0.370800;
m.expts(1).data_ms(13).idvs.std(4,1) = 0.001;
m.expts(1).data_ms(13).idvs.val(5,1) = 0.330200;
m.expts(1).data_ms(13).idvs.std(5,1) = 0.001200;
m.expts(1).data_ms(13).idvs.val(6,1) = 0.104100;
m.expts(1).data_ms(13).idvs.std(6,1) = 0.001;
m.expts(1).data_ms(14).idvs.id(1,1) = {'Methionine320_0_0_[1,2-13C]glycerol'};
m.expts(1).data_ms(14).idvs.time(1,1) = 0;
m.expts(1).data_ms(14).idvs.val(1,1) = 0.006600;
m.expts(1).data_ms(14).idvs.std(1,1) = 0.001;
m.expts(1).data_ms(14).idvs.val(2,1) = 0.041800;
m.expts(1).data_ms(14).idvs.std(2,1) = 0.001800;
m.expts(1).data_ms(14).idvs.val(3,1) = 0.206200;
m.expts(1).data_ms(14).idvs.std(3,1) = 0.001200;
m.expts(1).data_ms(14).idvs.val(4,1) = 0.388500;
m.expts(1).data_ms(14).idvs.std(4,1) = 0.003200;
m.expts(1).data_ms(14).idvs.val(5,1) = 0.292100;
m.expts(1).data_ms(14).idvs.std(5,1) = 0.002400;
m.expts(1).data_ms(14).idvs.val(6,1) = 0.064700;
m.expts(1).data_ms(14).idvs.std(6,1) = 0.003200;
m.expts(1).data_ms(15).idvs.id(1,1) = {'Phenylalanine302_0_0_[1,2-13C]glycerol'};
m.expts(1).data_ms(15).idvs.time(1,1) = 0;
m.expts(1).data_ms(15).idvs.val(1,1) = 0.042800;
m.expts(1).data_ms(15).idvs.std(1,1) = 0.001100;
m.expts(1).data_ms(15).idvs.val(2,1) = 0.473700;
m.expts(1).data_ms(15).idvs.std(2,1) = 0.004000;
m.expts(1).data_ms(15).idvs.val(3,1) = 0.483400;
m.expts(1).data_ms(15).idvs.std(3,1) = 0.003800;
m.expts(1).data_ms(16).idvs.id(1,1) = {'Phenylalanine308_0_0_[1,2-13C]glycerol'};
m.expts(1).data_ms(16).idvs.time(1,1) = 0;
m.expts(1).data_ms(16).idvs.val(1,1) = 0.002900;
m.expts(1).data_ms(16).idvs.std(1,1) = 0.001;
m.expts(1).data_ms(16).idvs.val(2,1) = 0.000100;
m.expts(1).data_ms(16).idvs.std(2,1) = 0.001;
m.expts(1).data_ms(16).idvs.val(3,1) = 0.005600;
m.expts(1).data_ms(16).idvs.std(3,1) = 0.001;
m.expts(1).data_ms(16).idvs.val(4,1) = 0.040500;
m.expts(1).data_ms(16).idvs.std(4,1) = 0.001900;
m.expts(1).data_ms(16).idvs.val(5,1) = 0.177200;
m.expts(1).data_ms(16).idvs.std(5,1) = 0.001600;
m.expts(1).data_ms(16).idvs.val(6,1) = 0.347200;
m.expts(1).data_ms(16).idvs.std(6,1) = 0.001500;
m.expts(1).data_ms(16).idvs.val(7,1) = 0.309800;
m.expts(1).data_ms(16).idvs.std(7,1) = 0.003200;
m.expts(1).data_ms(16).idvs.val(8,1) = 0.109200;
m.expts(1).data_ms(16).idvs.std(8,1) = 0.001;
m.expts(1).data_ms(16).idvs.val(9,1) = 0.007300;
m.expts(1).data_ms(16).idvs.std(9,1) = 0.001;
m.expts(1).data_ms(17).idvs.id(1,1) = {'Phenylalanine336_0_0_[1,2-13C]glycerol'};
m.expts(1).data_ms(17).idvs.time(1,1) = 0;
m.expts(1).data_ms(17).idvs.val(1,1) = 0.000400;
m.expts(1).data_ms(17).idvs.std(1,1) = 0.001;
m.expts(1).data_ms(17).idvs.val(2,1) = NaN;
m.expts(1).data_ms(17).idvs.std(2,1) = 0.001;
m.expts(1).data_ms(17).idvs.val(3,1) = 0.002700;
m.expts(1).data_ms(17).idvs.std(3,1) = 0.001;
m.expts(1).data_ms(17).idvs.val(4,1) = 0.017100;
m.expts(1).data_ms(17).idvs.std(4,1) = 0.001700;
m.expts(1).data_ms(17).idvs.val(5,1) = 0.082100;
m.expts(1).data_ms(17).idvs.std(5,1) = 0.002700;
m.expts(1).data_ms(17).idvs.val(6,1) = 0.263900;
m.expts(1).data_ms(17).idvs.std(6,1) = 0.002600;
m.expts(1).data_ms(17).idvs.val(7,1) = 0.374500;
m.expts(1).data_ms(17).idvs.std(7,1) = 0.005800;
m.expts(1).data_ms(17).idvs.val(8,1) = 0.217500;
m.expts(1).data_ms(17).idvs.std(8,1) = 0.002500;
m.expts(1).data_ms(17).idvs.val(9,1) = 0.039600;
m.expts(1).data_ms(17).idvs.std(9,1) = 0.003600;
m.expts(1).data_ms(17).idvs.val(10,1) = 0.002000;
m.expts(1).data_ms(17).idvs.std(10,1) = 0.001;
m.expts(1).data_ms(18).idvs.id(1,1) = {'Serine362_0_0_[1,2-13C]glycerol'};
m.expts(1).data_ms(18).idvs.time(1,1) = 0;
m.expts(1).data_ms(18).idvs.val(1,1) = 0.047400;
m.expts(1).data_ms(18).idvs.std(1,1) = 0.002700;
m.expts(1).data_ms(18).idvs.val(2,1) = 0.494900;
m.expts(1).data_ms(18).idvs.std(2,1) = 0.001900;
m.expts(1).data_ms(18).idvs.val(3,1) = 0.457700;
m.expts(1).data_ms(18).idvs.std(3,1) = 0.002700;
m.expts(1).data_ms(19).idvs.id(1,1) = {'Serine390_0_0_[1,2-13C]glycerol'};
m.expts(1).data_ms(19).idvs.time(1,1) = 0;
m.expts(1).data_ms(19).idvs.val(1,1) = 0.021700;
m.expts(1).data_ms(19).idvs.std(1,1) = 0.001300;
m.expts(1).data_ms(19).idvs.val(2,1) = 0.154000;
m.expts(1).data_ms(19).idvs.std(2,1) = 0.008600;
m.expts(1).data_ms(19).idvs.val(3,1) = 0.680900;
m.expts(1).data_ms(19).idvs.std(3,1) = 0.018600;
m.expts(1).data_ms(19).idvs.val(4,1) = 0.143400;
m.expts(1).data_ms(19).idvs.std(4,1) = 0.009300;
m.expts(1).data_ms(20).idvs.id(1,1) = {'Threonine376_0_0_[1,2-13C]glycerol'};
m.expts(1).data_ms(20).idvs.time(1,1) = 0;
m.expts(1).data_ms(20).idvs.val(1,1) = 0.034200;
m.expts(1).data_ms(20).idvs.std(1,1) = 0.001700;
m.expts(1).data_ms(20).idvs.val(2,1) = 0.232200;
m.expts(1).data_ms(20).idvs.std(2,1) = 0.002800;
m.expts(1).data_ms(20).idvs.val(3,1) = 0.492800;
m.expts(1).data_ms(20).idvs.std(3,1) = 0.004800;
m.expts(1).data_ms(20).idvs.val(4,1) = 0.240700;
m.expts(1).data_ms(20).idvs.std(4,1) = 0.006600;
m.expts(1).data_ms(21).idvs.id(1,1) = {'Threonine404_0_0_[1,2-13C]glycerol'};
m.expts(1).data_ms(21).idvs.time(1,1) = 0;
m.expts(1).data_ms(21).idvs.val(1,1) = 0.010000;
m.expts(1).data_ms(21).idvs.std(1,1) = 0.001;
m.expts(1).data_ms(21).idvs.val(2,1) = 0.077700;
m.expts(1).data_ms(21).idvs.std(2,1) = 0.001700;
m.expts(1).data_ms(21).idvs.val(3,1) = 0.344400;
m.expts(1).data_ms(21).idvs.std(3,1) = 0.002900;
m.expts(1).data_ms(21).idvs.val(4,1) = 0.440600;
m.expts(1).data_ms(21).idvs.std(4,1) = 0.004800;
m.expts(1).data_ms(21).idvs.val(5,1) = 0.127200;
m.expts(1).data_ms(21).idvs.std(5,1) = 0.002400;
m.expts(1).data_ms(22).idvs.id(1,1) = {'Valine260_0_0_[1,2-13C]glycerol'};
m.expts(1).data_ms(22).idvs.time(1,1) = 0;
m.expts(1).data_ms(22).idvs.val(1,1) = 0.004600;
m.expts(1).data_ms(22).idvs.std(1,1) = 0.001;
m.expts(1).data_ms(22).idvs.val(2,1) = 0.048800;
m.expts(1).data_ms(22).idvs.std(2,1) = 0.002200;
m.expts(1).data_ms(22).idvs.val(3,1) = 0.291800;
m.expts(1).data_ms(22).idvs.std(3,1) = 0.002100;
m.expts(1).data_ms(22).idvs.val(4,1) = 0.451900;
m.expts(1).data_ms(22).idvs.std(4,1) = 0.002500;
m.expts(1).data_ms(22).idvs.val(5,1) = 0.202900;
m.expts(1).data_ms(22).idvs.std(5,1) = 0.002400;
m.expts(1).data_ms(23).idvs.id(1,1) = {'Valine288_0_0_[1,2-13C]glycerol'};
m.expts(1).data_ms(23).idvs.time(1,1) = 0;
m.expts(1).data_ms(23).idvs.val(1,1) = 0.002900;
m.expts(1).data_ms(23).idvs.std(1,1) = 0.001;
m.expts(1).data_ms(23).idvs.val(2,1) = 0.016900;
m.expts(1).data_ms(23).idvs.std(2,1) = 0.001100;
m.expts(1).data_ms(23).idvs.val(3,1) = 0.107900;
m.expts(1).data_ms(23).idvs.std(3,1) = 0.004000;
m.expts(1).data_ms(23).idvs.val(4,1) = 0.430400;
m.expts(1).data_ms(23).idvs.std(4,1) = 0.002600;
m.expts(1).data_ms(23).idvs.val(5,1) = 0.389700;
m.expts(1).data_ms(23).idvs.std(5,1) = 0.004500;
m.expts(1).data_ms(23).idvs.val(6,1) = 0.052100;
m.expts(1).data_ms(23).idvs.std(6,1) = 0.002300;