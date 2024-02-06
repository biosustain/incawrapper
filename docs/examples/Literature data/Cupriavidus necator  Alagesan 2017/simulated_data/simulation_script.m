clear functions

% REACTION BLOCK
% Create reactions
r = [...
reaction('FRU.ext (abcdef) -> F6P (abcdef)', 'id', 'ex_1'),...
reaction('GLY.ext (abc) -> GLY (abc)', 'id', 'ex_2'),...
reaction('GLY (abc) -> DHAP (abc)', 'id', 'R1'),...
reaction('F6P (abcdef) <-> G6P (abcdef)', 'id', 'R2'),...
reaction('F16P (abcdef) -> F6P (abcdef)', 'id', 'R4'),...
reaction('F16P (abcdef) <-> DHAP (cba) + G3P (def)', 'id', 'R5'),...
reaction('DHAP (abc) <-> G3P (abc)', 'id', 'R7'),...
reaction('G3P (abc) <-> 3PG (abc)', 'id', 'R9'),...
reaction('3PG (abc) <-> PEP (abc)', 'id', 'R11'),...
reaction('PEP (abc) <-> PYR (abc)', 'id', 'R13'),...
reaction('PYR (abc) -> ACCOA (bc) + CO2 (a)', 'id', 'R15'),...
reaction('OAA (abcd) + ACCOA (ef) -> CIT (dcbfea)', 'id', 'R16'),...
reaction('CIT (abcdef) <-> ISCIT (abcdef)', 'id', 'R17'),...
reaction('ISCIT (abcdef) -> AKG (abcde) + CO2 (f)', 'id', 'R19'),...
reaction('AKG (abcde) -> 0.5*SUCOA (bcde) + 0.5*SUCOA (edcb) + CO2 (a)', 'id', 'R20'),...
reaction('SUCOA (abcd) -> 0.5*SUC (abcd) + 0.5*SUC (dcba)', 'id', 'R21'),...
reaction('SUC (abcd) <-> MAL (abcd)', 'id', 'R22'),...
reaction('MAL (abcd) <-> OAA (abcd)', 'id', 'R24'),...
reaction('G6P (abcdef) -> 6PG (abcdef)', 'id', 'R26'),...
reaction('6PG (abcdef) -> PYR (abc) + G3P (def)', 'id', 'R27'),...
reaction('ISCIT (abcdef) -> GLYOXY (ab) + 0.5*SUC (edcf) + 0.5*SUC (fcde)', 'id', 'R28'),...
reaction('GLYOXY (ab) + ACCOA (cd) -> MAL (abdc)', 'id', 'R29'),...
reaction('MAL (abcd) -> PYR (abc) + CO2 (d)', 'id', 'R30'),...
reaction('PEP (abc) + CO2 (d) <-> OAA (abcd)', 'id', 'R31'),...
reaction('OAA (abcd) -> PYR (abc) + CO2 (d)', 'id', 'R33'),...
reaction('RU5P (abcde) <-> R5P (abcde)', 'id', 'R34'),...
reaction('RU5P (abcde) <-> X5P (abcde)', 'id', 'R36'),...
reaction('X5P (abcde) + R5P (fghij) <-> G3P (cde) + S7P (abfghij)', 'id', 'R38'),...
reaction('S7P (abcdefg) + G3P (hij) <-> E4P (defg) + F6P (abchij)', 'id', 'R40'),...
reaction('E4P (fghi) + X5P (abcde) <-> F6P (abfghi) + G3P (cde)', 'id', 'R42'),...
reaction('DHAP (efg) + E4P (abcd) -> S7P (gfeabcd)', 'id', 'R44'),...
reaction('RU5P (abcde) -> RUBP (abcde)', 'id', 'R45'),...
reaction('RUBP (abcde)  + CO2 (f) -> 3PG (fba) + 3PG (cde)', 'id', 'R46'),...
reaction('AKG (abcde) -> GLU (abcde)', 'id', 'R47'),...
reaction('AKG (abcde) -> PRO (abcde)', 'id', 'R48'),...
reaction('AKG (abcde) + CO2 (f) -> ARG (abcdef)', 'id', 'R49'),...
reaction('OAA (abcd) -> ASP (abcd)', 'id', 'R50'),...
reaction('PYR (abc) -> ALA (abc)', 'id', 'R51'),...
reaction('3PG (abc) -> SER (abc)', 'id', 'R52'),...
reaction('3PG (abc) -> CYS (abc)', 'id', 'R53'),...
reaction('3PG (abc) -> GL (ab) + MTHF (c)   ', 'id', 'R54'),...
reaction('OAA (abcd) -> GL (ab) + ACCOA (cd)', 'id', 'R55'),...
reaction('OAA (abcd) -> THR (abcd)', 'id', 'R56'),...
reaction('OAA (abcd) + MTHF (e) -> MET (abcde)', 'id', 'R57'),...
reaction('OAA (abcd) + PYR (efg) -> LYS (bcdgfe)  + CO2 (a)', 'id', 'R58'),...
reaction('PYR (abc) + PYR (def) -> VAL (abcef) + CO2 (d)', 'id', 'R59'),...
reaction('PYR (abc) + PYR (def) -> ISV (abefc) + CO2 (d)', 'id', 'R60'),...
reaction('ISV (abcde) + ACCOA (fg) -> LEU (fgbcde) + CO2 (a)', 'id', 'R61'),...
reaction('OAA (abcd) + PYR (efg) -> ILE (abfcdg)  + CO2 (e)', 'id', 'R62'),...
reaction('E4P (abcd) + PEP (efg) -> SHKM (efgabcd)', 'id', 'R63'),...
reaction('SHKM (abcdefg) + PEP (hij) -> CHRM (abcdefghij)', 'id', 'R64'),...
reaction('CHRM (abcdefghij) -> PHE (hijbcdefg) + CO2 (a)', 'id', 'R65'),...
reaction('CHRM (abcdefghij) -> TYR (hijbcdefg) + CO2 (a)', 'id', 'R66'),...
reaction('CHRM (abcdefghij) -> ANTHR (abcdefg) + G3P (hij)', 'id', 'R67'),...
reaction('ANTHR (abcdefg) + R5P (hijkl) -> CPADR5P (abcdefghijkl)', 'id', 'R68'),...
reaction('CPADR5P (abcdefghijkl) -> INDG (abcdfghijkl) + CO2 (e)', 'id', 'R69'),...
reaction('INDG (abcdfghijkl) -> TRP (abcdfghijkl) ', 'id', 'R70'),...
reaction('R5P (abcde) + MTHF (f)-> HIS (edcbaf)', 'id', 'R71'),...
reaction('ACCOA -> PHB_B', 'id', 'R72'),...
];

% TRACERS BLOCK
% define tracers used in fructose
t_fructose = tracer({...
'D-[1-13C]fructose: FRU.ext @ 1',...
});
t_fructose.frac = [1.0 ];
t_fructose.atoms.it(:,1) = [0.01,0.99];


% FLUXES BLOCK


% MS_FRAGMENTS BLOCK

% define mass spectrometry measurements for experiment fructose
ms_fructose = [...
msdata('Alanine232: ALA @ 2 3', 'more', 'C8H26ONSi2'),...
msdata('Alanine260: ALA @ 1 2 3', 'more', 'C8H26O2NSi2'),...
msdata('Asparticacid302: ASP @ 1 2', 'more', 'C12H32O2NSi2'),...
msdata('Asparticacid390: ASP @ 2 3 4', 'more', 'C14H40O3NSi3'),...
msdata('Asparticacid418: ASP @ 1 2 3 4', 'more', 'C14H40O4NSi3'),...
msdata('Glutamicacid330: GLU @ 2 3 4 5', 'more', 'C12H36O2NSi2'),...
msdata('Glutamicacid432: GLU @ 1 2 3 4 5', 'more', 'C14H42O4NSi3'),...
msdata('Glycine218: GL @ 2', 'more', 'C8H24ONSi2'),...
msdata('Glycine246: GL @ 1 2', 'more', 'C8H24O2NSi2'),...
msdata('Histidine338: HIS @ 2 3 4 5 6', 'more', 'C12H36N3Si2'),...
msdata('Histidine440: HIS @ 1 2 3 4 5 6', 'more', 'C14H42O2N3Si3'),...
msdata('Isoleucine274: ILE @ 2 3 4 5 6', 'more', 'C8H32ONSi2'),...
msdata('Leucine274: LEU @ 2 3 4 5 6', 'more', 'C8H32ONSi2'),...
msdata('Methionine320: MET @ 2 3 4 5', 'more', 'C6H24NSiS'),...
msdata('Phenylalanine302: PHE @ 1 2', 'more', 'C12H32O2NSi2'),...
msdata('Phenylalanine308: PHE @ 2 3 4 5 6 7 8 9', 'more', 'C8H30ONSi2'),...
msdata('Phenylalanine336: PHE @ 1 2 3 4 5 6 7 8 9', 'more', 'C8H30O2NSi2'),...
msdata('Serine362: SER @ 2 3', 'more', 'C14H40O2NSi3'),...
msdata('Serine390: SER @ 1 2 3', 'more', 'C14H40O3NSi3'),...
msdata('Threonine376: THR @ 2 3 4', 'more', 'C14H42O2NSi3'),...
msdata('Threonine404: THR @ 1 2 3 4', 'more', 'C14H42O3NSi3'),...
msdata('Valine260: VAL @ 2 3 4 5', 'more', 'C8H30ONSi2'),...
msdata('Valine288: VAL @ 1 2 3 4 5', 'more', 'C8H30O2NSi2'),...
];

% define mass spectrometry measurements for experiment fructose
ms_fructose{'Alanine232'}.idvs = idv([[NaN;NaN;NaN]], 'id', {'fructose_Alanine232_inf_1'}, 'std', [[NaN;NaN;NaN]], 'time', [inf])
ms_fructose{'Alanine260'}.idvs = idv([[NaN;NaN;NaN;NaN]], 'id', {'fructose_Alanine260_inf_1'}, 'std', [[NaN;NaN;NaN;NaN]], 'time', [inf])
ms_fructose{'Asparticacid302'}.idvs = idv([[NaN;NaN;NaN]], 'id', {'fructose_Asparticacid302_inf_1'}, 'std', [[NaN;NaN;NaN]], 'time', [inf])
ms_fructose{'Asparticacid390'}.idvs = idv([[NaN;NaN;NaN;NaN]], 'id', {'fructose_Asparticacid390_inf_1'}, 'std', [[NaN;NaN;NaN;NaN]], 'time', [inf])
ms_fructose{'Asparticacid418'}.idvs = idv([[NaN;NaN;NaN;NaN;NaN]], 'id', {'fructose_Asparticacid418_inf_1'}, 'std', [[NaN;NaN;NaN;NaN;NaN]], 'time', [inf])
ms_fructose{'Glutamicacid330'}.idvs = idv([[NaN;NaN;NaN;NaN;NaN]], 'id', {'fructose_Glutamicacid330_inf_1'}, 'std', [[NaN;NaN;NaN;NaN;NaN]], 'time', [inf])
ms_fructose{'Glutamicacid432'}.idvs = idv([[NaN;NaN;NaN;NaN;NaN]], 'id', {'fructose_Glutamicacid432_inf_1'}, 'std', [[NaN;NaN;NaN;NaN;NaN]], 'time', [inf])
ms_fructose{'Glycine218'}.idvs = idv([[NaN;NaN]], 'id', {'fructose_Glycine218_inf_1'}, 'std', [[NaN;NaN]], 'time', [inf])
ms_fructose{'Glycine246'}.idvs = idv([[NaN;NaN;NaN]], 'id', {'fructose_Glycine246_inf_1'}, 'std', [[NaN;NaN;NaN]], 'time', [inf])
ms_fructose{'Histidine338'}.idvs = idv([[NaN;NaN;NaN;NaN;NaN;NaN]], 'id', {'fructose_Histidine338_inf_1'}, 'std', [[NaN;NaN;NaN;NaN;NaN;NaN]], 'time', [inf])
ms_fructose{'Histidine440'}.idvs = idv([[NaN;NaN;NaN;NaN]], 'id', {'fructose_Histidine440_inf_1'}, 'std', [[NaN;NaN;NaN;NaN]], 'time', [inf])
ms_fructose{'Isoleucine274'}.idvs = idv([[NaN;NaN;NaN;NaN]], 'id', {'fructose_Isoleucine274_inf_1'}, 'std', [[NaN;NaN;NaN;NaN]], 'time', [inf])
ms_fructose{'Leucine274'}.idvs = idv([[NaN;NaN;NaN;NaN;NaN]], 'id', {'fructose_Leucine274_inf_1'}, 'std', [[NaN;NaN;NaN;NaN;NaN]], 'time', [inf])
ms_fructose{'Methionine320'}.idvs = idv([[NaN;NaN;NaN;NaN]], 'id', {'fructose_Methionine320_inf_1'}, 'std', [[NaN;NaN;NaN;NaN]], 'time', [inf])
ms_fructose{'Phenylalanine302'}.idvs = idv([[NaN;NaN;NaN]], 'id', {'fructose_Phenylalanine302_inf_1'}, 'std', [[NaN;NaN;NaN]], 'time', [inf])
ms_fructose{'Phenylalanine308'}.idvs = idv([[NaN;NaN;NaN;NaN;NaN]], 'id', {'fructose_Phenylalanine308_inf_1'}, 'std', [[NaN;NaN;NaN;NaN;NaN]], 'time', [inf])
ms_fructose{'Phenylalanine336'}.idvs = idv([[NaN;NaN;NaN;NaN]], 'id', {'fructose_Phenylalanine336_inf_1'}, 'std', [[NaN;NaN;NaN;NaN]], 'time', [inf])
ms_fructose{'Serine362'}.idvs = idv([[NaN;NaN;NaN]], 'id', {'fructose_Serine362_inf_1'}, 'std', [[NaN;NaN;NaN]], 'time', [inf])
ms_fructose{'Serine390'}.idvs = idv([[NaN;NaN;NaN]], 'id', {'fructose_Serine390_inf_1'}, 'std', [[NaN;NaN;NaN]], 'time', [inf])
ms_fructose{'Threonine376'}.idvs = idv([[NaN;NaN;NaN]], 'id', {'fructose_Threonine376_inf_1'}, 'std', [[NaN;NaN;NaN]], 'time', [inf])
ms_fructose{'Threonine404'}.idvs = idv([[NaN;NaN;NaN;NaN]], 'id', {'fructose_Threonine404_inf_1'}, 'std', [[NaN;NaN;NaN;NaN]], 'time', [inf])
ms_fructose{'Valine260'}.idvs = idv([[NaN;NaN;NaN;NaN;NaN]], 'id', {'fructose_Valine260_inf_1'}, 'std', [[NaN;NaN;NaN;NaN;NaN]], 'time', [inf])
ms_fructose{'Valine288'}.idvs = idv([[NaN;NaN;NaN;NaN;NaN;NaN]], 'id', {'fructose_Valine288_inf_1'}, 'std', [[NaN;NaN;NaN;NaN;NaN;NaN]], 'time', [inf])


% POOL_SIZES BLOCK


% EXPERIMENTAL_DATA BLOCK
e_fructose = experiment(t_fructose, 'id', 'fructose', 'data_ms', ms_fructose);


% MODEL BLOCK
m = model(r, 'expts', [e_fructose]);


% MODEL MODIFICATIONS BLOCK

m.rates.flx.val = [100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100 100];
m.rates(1).flx.fix = true; % fix the value so it not change when finding the nearest feasible flux distribution
index_CO2 = find(strcmp(m.states.id, 'CO2'));
m.states.bal(index_CO2) = false;
% Find nearest feasible flux solution
m.rates.flx.val = transpose(mod2stoich(m));


% OPTIONS BLOCK
m.options = option('sim_more', true, 'sim_na', true, 'sim_ss', true)

mod2stoich(m); % make sure the fluxes are feasible

% RUNNER BLOCK
s=simulate(m);
filename = '/Users/s143838/projects/AutoFlow-OmicsDataHandling/docs/examples/Literature data/Cupriavidus necator  Alagesan 2017/c_necator_simulation.mat';
save(filename, 's', 'm');
