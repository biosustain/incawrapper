clear functions %#ok<*CLFUNC> 

% define reactions
r = reaction({... 
'glu_DASH_L_c (hijkl) + pyr_c (efg) + succoa_c (mnop) + atp_c + asp_DASH_L_c (abcd) + 2.0 nadph_c -> 26dap_DASH_M_c (abcdgfe) + succ_c (mnop) + akg_c (hijkl) ';...
'cit_c (abcdef) -> icit_c (abcdef) ';...
'icit_c (abcdef) -> cit_c (abcdef) ';...
'akg_c (abcde) -> nadh_c + succoa_c (bcde) + co2_c (a) ';...
'glu_DASH_L_c (defgh) + pyr_c (abc) -> akg_c (defgh) + ala_DASH_L_c (abc) ';...
'glu_DASH_L_c (abcde) + gln_DASH_L_c (ghijk) + co2_c (f) + 5.0 atp_c + nadph_c + accoa_c (pq) + asp_DASH_L_c (lmno) -> ac_c (pq) + arg_DASH_L_c (abcdef) + akg_c (ghijk) + fum_c (lmno) ';...
'2.0 atp_c + asp_DASH_L_c (abcd) + nh4_c -> asn_DASH_L_c (abcd) ';...
'glu_DASH_L_c (efghi) + oaa_c (abcd) -> akg_c (efghi) + asp_DASH_L_c (abcd) ';...
'atp_c -> atp_c.ext ';...
'oaa_c (abcd) + accoa_c (ef) -> cit_c (dcbfea) ';...
'26dap_DASH_M_c (abcdefg) -> lys_DASH_L_c (abcdef) + co2_c (g) ';...
'0.176 phe_DASH_L_c + 0.443 mlthf_c + 0.34 oaa_c + 0.326 lys_DASH_L_c + 33.247 atp_c + 0.205 ser_DASH_L_c + 0.129 g3p_c + 0.131 tyr_DASH_L_c + 0.051 pep_c + 0.146 met_DASH_L_c + 0.205 g6p_c + 0.087 akg_c + 0.25 glu_DASH_L_c + 0.25 gln_DASH_L_c + 0.754*r5p_c + 0.071 f6p_c + 0.083 pyr_c + 0.582 gly_c + 0.241 thr_DASH_L_c + 0.229 asp_DASH_L_c + 5.363 nadph_c + 0.087 cys_DASH_L_c + 0.619 3pg_c + 0.402 val_DASH_L_c + 0.488 ala_DASH_L_c + 0.276 ile_DASH_L_c + 0.229 asn_DASH_L_c + 0.09 his_DASH_L_c + 0.428 leu_DASH_L_c + 2.51 accoa_c + 0.281 arg_DASH_L_c + 0.21 pro_DASH_L_c + 0.054 trp_DASH_L_c -> 1.455 nadh_c + 39.68 Biomass_c ';...
'2ddg6p_c (abcdef) -> pyr_c (abc) + g3p_c (def) ';...
'6pgc_c (abcdef) -> 2ddg6p_c (abcdef) ';...
'ac_c (ab) -> ac_c.ext (ab) ';...
'co2_c (a) -> co2_c.ext (a) ';...
'co2_c.unlabeled (a) + co2_c (b) -> co2_c.out (b) + co2_c (a) ';...
'glc_DASH_D_e.ext (abcdef) -> glc_DASH_D_e (abcdef) ';...
'nh4_c.ext -> nh4_c ';...
'o2_c.ext -> o2_c ';...
'so4_c.ext -> so4_c ';...
'fadh2_c + 0.5 o2_c -> atp_c ';...
'fdp_c (abcdef) -> dhap_c (cba) + g3p_c (def) ';...
'dhap_c (cba) + g3p_c (def) -> fdp_c (abcdef) ';...
'fum_c (abcd) -> mal_DASH_L_c (abcd) ';...
'mal_DASH_L_c (abcd) -> fum_c (abcd) ';...
'g6p_c (abcdef) -> 6pgc_c (abcdef) + nadph_c ';...
'g3p_c (abc) -> nadh_c + atp_c + 3pg_c (abc) ';...
'nadh_c + atp_c + 3pg_c (abc) -> g3p_c (abc) ';...
'ser_DASH_L_c (abc) -> gly_c (ab) + mlthf_c (c) ';...
'gly_c (ab) + mlthf_c (c) -> ser_DASH_L_c (abc) ';...
'pep_c (ghi) + glc_DASH_D_e (abcdef) -> pyr_c (ghi) + g6p_c (abcdef) ';...
'glc_DASH_D_e (abcdef) -> glc_DASH_D_c (abcdef) ';...
'glu_DASH_L_c (abcde) + atp_c + nh4_c -> gln_DASH_L_c (abcde) ';...
'akg_c (abcde) + nh4_c + nadph_c -> glu_DASH_L_c (abcde) ';...
'6pgc_c (abcdef) -> ru5p_DASH_D_c (bcdef) + co2_c (a) + nadph_c ';...
'glc_DASH_D_c (abcdef) + atp_c -> g6p_c (abcdef) ';...
'10fthf_c (f) + prpp_c (abcde) + gln_DASH_L_c (ghijk) + 4.0 atp_c + asp_DASH_L_c (lmno) -> 2.0 nadh_c + his_DASH_L_c (edcbaf) + akg_c (ghijk) + fum_c (lmno) ';...
'icit_c (abcdef) -> akg_c (abcde) + nadph_c + co2_c (f) ';...
'akg_c (abcde) + nadph_c + co2_c (f) -> icit_c (abcdef) ';...
'icit_c (abcdef) -> succ_c (edcf) + glx_c (ab) ';...
'glu_DASH_L_c (hijkl) + pyr_c (efg) + nadph_c + thr_DASH_L_c (abcd) -> ile_DASH_L_c (abfcdg) + co2_c (e) + akg_c (hijkl) + nh4_c ';...
'glu_DASH_L_c (ijklm) + pyr_c (cde) + pyr_c (fgh) + nadph_c + accoa_c (ab) -> nadh_c + leu_DASH_L_c (abdghe) + co2_c (c) + co2_c (f) + akg_c (ijklm) ';...
'glx_c (ab) + accoa_c (cd) -> mal_DASH_L_c (abdc) ';...
'mal_DASH_L_c (abcd) -> oaa_c (abcd) + nadh_c ';...
'oaa_c (abcd) + nadh_c -> mal_DASH_L_c (abcd) ';...
'mal_DASH_L_c (abcd) -> pyr_c (abc) + co2_c (d) + nadph_c ';...
'mal_DASH_L_c (abcd) -> pyr_c (abc) + nadh_c + co2_c (d) ';...
'succoa_c (ijkl) + atp_c + methf_c (e) + asp_DASH_L_c (abcd) + 2.0 nadph_c + cys_DASH_L_c (fgh) -> pyr_c (fgh) + succ_c (ijkl) + met_DASH_L_c (abcde) + nh4_c ';...
'gly_c (ab) -> nadh_c + co2_c (a) + mlthf_c (b) + nh4_c ';...
'nadh_c + co2_c (a) + mlthf_c (b) + nh4_c -> gly_c (ab) ';...
'mlthf_c (a) -> 10fthf_c (a) + nadph_c ';...
'nadh_c + mlthf_c (a) -> methf_c (a) ';...
'nadh_c + 0.5 o2_c -> 2.0 atp_c ';...
'nadh_c -> nadph_c ';...
'nadph_c -> nadh_c ';...
'pyr_c (abc) -> nadh_c + accoa_c (bc) + co2_c (a) ';...
'f6p_c (abcdef) + atp_c -> fdp_c (abcdef) ';...
'g6p_c (abcdef) -> f6p_c (abcdef) ';...
'f6p_c (abcdef) -> g6p_c (abcdef) ';...
'3pg_c (abc) -> pep_c (abc) ';...
'pep_c (abc) -> 3pg_c (abc) ';...
'e4p_c (ghij) + glu_DASH_L_c (klmno) + nadph_c + atp_c + pep_c (abc) + pep_c (def) -> phe_DASH_L_c (abcefghij) + co2_c (d) + akg_c (klmno) ';...
'pep_c (abc) + co2_c (d) -> oaa_c (abcd) ';...
'oaa_c (abcd) + atp_c -> pep_c (abc) + co2_c (d) ';...
'glu_DASH_L_c (abcde) + atp_c + 2.0 nadph_c -> pro_DASH_L_c (abcde) ';...
'r5p_c (abcde) + atp_c -> prpp_c (abcde) ';...
'accoa_c (ab) -> atp_c + ac_c (ab) ';...
'atp_c + ac_c (ab) -> accoa_c (ab) ';...
'pep_c (abc) -> pyr_c (abc) + atp_c ';...
'ru5p_DASH_D_c (abcde) -> xu5p_DASH_D_c (abcde) ';...
'xu5p_DASH_D_c (abcde) -> ru5p_DASH_D_c (abcde) ';...
'ru5p_DASH_D_c (abcde) -> r5p_c (abcde) ';...
'r5p_c (abcde) -> ru5p_DASH_D_c (abcde) ';...
'3.0 atp_c + ser_DASH_L_c (abc) + so4_c + accoa_c (de) + 4.0 nadph_c -> ac_c (de) + cys_DASH_L_c (abc) ';...
'glu_DASH_L_c (defgh) + 3pg_c (abc) -> akg_c (defgh) + nadh_c + ser_DASH_L_c (abc) ';...
'succoa_c (abcd) -> succ_c (abcd) + atp_c ';...
'succ_c (abcd) + atp_c -> succoa_c (abcd) ';...
'succ_c (abcd) -> fadh2_c + fum_c (abcd) ';...
'fadh2_c + fum_c (abcd) -> succ_c (abcd) ';...
's7p_c (abcdefg) -> e4p_c (defg) + TA_C3_c (abc) ';...
'e4p_c (defg) + TA_C3_c (abc) -> s7p_c (abcdefg) ';...
'thr_DASH_L_c (abcd) -> nadh_c + gly_c (ab) + accoa_c (cd) ';...
'2.0 atp_c + asp_DASH_L_c (abcd) + 2.0 nadph_c -> thr_DASH_L_c (abcd) ';...
's7p_c (abcdefg) -> TK_C2_c (ab) + r5p_c (cdefg) ';...
'TK_C2_c (ab) + r5p_c (cdefg) -> s7p_c (abcdefg) ';...
'f6p_c (abcdef) -> TA_C3_c (abc) + g3p_c (def) ';...
'TA_C3_c (abc) + g3p_c (def) -> f6p_c (abcdef) ';...
'xu5p_DASH_D_c (abcde) -> TK_C2_c (ab) + g3p_c (cde) ';...
'TK_C2_c (ab) + g3p_c (cde) -> xu5p_DASH_D_c (abcde) ';...
'f6p_c (abcdef) -> e4p_c (cdef) + TK_C2_c (ab) ';...
'e4p_c (cdef) + TK_C2_c (ab) -> f6p_c (abcdef) ';...
'dhap_c (abc) -> g3p_c (abc) ';...
'g3p_c (abc) -> dhap_c (abc) ';...
'e4p_c (lmno) + gln_DASH_L_c (stuvw) + nadph_c + r5p_c (defgh) + 3.0 atp_c + ser_DASH_L_c (abc) + pep_c (ijk) + pep_c (pqr) -> pyr_c (pqr) + glu_DASH_L_c (stuvw) + g3p_c (fgh) + co2_c (i) + trp_DASH_L_c (abcedklmnoj) ';...
'e4p_c (ghij) + glu_DASH_L_c (klmno) + nadph_c + atp_c + pep_c (abc) + pep_c (def) -> nadh_c + tyr_DASH_L_c (abcefghij) + co2_c (d) + akg_c (klmno) ';...
'glu_DASH_L_c (ghijk) + pyr_c (abc) + pyr_c (def) + nadph_c -> co2_c (d) + akg_c (ghijk) + val_DASH_L_c (abcef) ';...
});

% define tracers used in the experiments
t = tracer({...
'1-13C_D-Glucose: glc_DASH_D_e.EX @ 1';...
'U-13C_D-Glucose: glc_DASH_D_e.EX @ 1 2 3 4 5 6';...
});

% define fractions of tracers used
t.frac = [0.8,0.2];

% flux measurements
% define experiments for fit data
f = data(' Ec_Biomass_INCA EX_ac_LPAREN_e_RPAREN_ EX_glc_LPAREN_e_RPAREN_ ');
% add fit values
f.val = [...
0.7040000000000001,...
2.13,...
7.4,...
];

% add fit stds
f.std = [...
0.008,...
0.5,...
0.2,...
];

% define which fragments of molecules were measured in which experiment
d = msdata({...
'3pg_c_C3H6O7P_MRM: 3pg_c @ 1 2 3';
'6pgc_c_C6H12O10P_MRM: 6pgc_c @ 1 2 3 4 5 6';
'akg_c_C4H5O3_MRM: akg_c @ 1 2 3 4';
'akg_c_C5H5O5_MRM: akg_c @ 1 2 3 4 5';
'asp_DASH_L_c_C3H6NO2_MRM: asp_DASH_L_c @ 2 3 4';
'asp_DASH_L_c_C4H6NO4_MRM: asp_DASH_L_c @ 1 2 3 4';
'dhap_c_C3H6O6P_MRM: dhap_c @ 1 2 3';
'fdp_c_C6H13O12P2_MRM: fdp_c @ 1 2 3 4 5 6';
'g6p_c_C6H12O9P_MRM: g6p_c @ 1 2 3 4 5 6';
'glc_DASH_D_c_C2H3O2_MRM: glc_DASH_D_c @ 5 6';
'glc_DASH_D_c_C6H11O6_MRM: glc_DASH_D_c @ 1 2 3 4 5 6';
'glu_DASH_L_c_C5H6NO3_MRM: glu_DASH_L_c @ 1 2 3 4 5';
'glu_DASH_L_c_C5H8NO4_MRM: glu_DASH_L_c @ 1 2 3 4 5';
'icit_c_C5H3O3_MRM: icit_c @ 1 2 3 4 5';
'icit_c_C6H7O7_MRM: icit_c @ 1 2 3 4 5 6';
'mal_DASH_L_c_C4H3O4_MRM: mal_DASH_L_c @ 1 2 3 4';
'mal_DASH_L_c_C4H5O5_MRM: mal_DASH_L_c @ 1 2 3 4';
'met_DASH_L_c_C5H10NO2S_MRM: met_DASH_L_c @ 1 2 3 4 5';
'met_DASH_L_c_CH3S_MRM: met_DASH_L_c @ 5C';
'pep_c_C3H4O6P_MRM: pep_c @ 1 2 3';
'phe_DASH_L_c_C9H10NO2_MRM: phe_DASH_L_c @ 1 2 3 4 5 6 7 8 9';
'phe_DASH_L_c_C9H7O2_MRM: phe_DASH_L_c @ 1 2 3 4 5 6 7 8 9';
'prpp_c_C5H12O14P3_MRM: prpp_c @ 1 2 3 4 5';
'pyr_c_C3H3O3_MRM: pyr_c @ 1 2 3';
's7p_c_C7H14O10P_MRM: s7p_c @ 1 2 3 4 5 6 7';
'succ_c_C4H3O3_MRM: succ_c @ 1 2 3 4';
'succ_c_C4H5O4_MRM: succ_c @ 1 2 3 4';
'thr_DASH_L_c_C2H4NO2_MRM: thr_DASH_L_c @ 1 2';
'thr_DASH_L_c_C4H8NO3_MRM: thr_DASH_L_c @ 1 2 3 4';
});

% create default IDVs, which will be replaced by measured IDVs later.
d.idvs = idv; 

% initialize experiment with t and add f and d
x = experiment(t);
x.data_flx = f;
x.data_ms = d;
% assigning all the previous values to a specific experiment
m.expts = x;

m = model(r); % set up model (unnecessary) 

% take care of symmetrical metabolites
m.mets{'succ_c'}.sym = list('rotate180', atommap('1:4 2:3 3:2 4:1'));
m.mets{'fum_c'}.sym = list('rotate180', atommap('1:4 2:3 3:2 4:1'));

% input of MS measurements
nmts = 8;                               % number of total measurements
samp = 8/60/60;                         % spacing between measurements in hours
m.options.int_tspan = 0:samp:(samp*nmts);   % time points in hours
m.options.sim_tunit = 'h';              % hours are unit of time
m.options.fit_reinit = true;
m.options.sim_ss = false;
m.options.sim_sens = true;

% define unbalanced reactions
% m.states('gly')
% define lower bounds
m.rates.flx.lb = zeros(1, 97);
m.rates.flx.lb([12 15 18]) = [ 0.6336 1.9169999999999998 6.66 ];

% set upper bounds
m.rates.flx.ub = 1000 * ones(1, 97); % default to 1000
m.rates.flx.ub([12 15 18]) = [ 0.7744 2.343 8.14 ];

% set flux values
m.rates.flx.val = zeros(1, 97);
m.rates.flx.val([12 15 18]) = [ 0.7040000000000001 2.13 7.4 ];

% include/exclude reactions
m.rates.on = ones(1, 97);
excluded_reaction_indexes = [  ]; % Enter reaction indexes to be excluded, separated by a space
% e.g. to exclude reaction 5, 15 and 77 write `[5 15 77]`
m.rates.on(excluded_reaction_indexes) = zeros(1, length(excluded_reaction_indexes));

% define reaction ids
m.rates.id = {...
'26dap_DASH_MSYN',...
'ACONTa_ACONTb',...
'ACONTa_ACONTb_reverse',...
'AKGDH',...
'ALATA_L',...
'ArgSYN',...
'ASNN',...
'ASPTA',...
'ATPM',...
'CS',...
'DAPDC',...
'Ec_Biomass_INCA',...
'EDA',...
'EDD',...
'EX_ac_LPAREN_e_RPAREN_',...
'EX_co2_LPAREN_e_RPAREN_',...
'EX_co2_LPAREN_e_RPAREN__unlabeled',...
'EX_glc_LPAREN_e_RPAREN_',...
'EX_nh4_LPAREN_e_RPAREN_',...
'EX_o2_LPAREN_e_RPAREN_',...
'EX_so4_LPAREN_e_RPAREN_',...
'FADR_NADH_CYTBD_HYD_ATPS4r',...
'FBA',...
'FBA_reverse',...
'FUM',...
'FUM_reverse',...
'G6PDH2r_PGL',...
'GAPD_PGK',...
'GAPD_PGK_reverse',...
'GHMT2r',...
'GHMT2r_reverse',...
'GLCptspp',...
'GLCt2pp',...
'GLNS',...
'GluSYN',...
'GND',...
'HEX1',...
'HisSYN',...
'ICDHyr',...
'ICDHyr_reverse',...
'ICL',...
'IleSYN',...
'LeuSYN',...
'MALS',...
'MDH',...
'MDH_reverse',...
'ME1',...
'ME2',...
'MetSYN',...
'MlthfSYN',...
'MlthfSYN_reverse',...
'MTHFC',...
'MTHFD',...
'NADH_CYTBD_HYD_ATPS4r',...
'NADTRHD_THD2pp',...
'NADTRHD_THD2pp_reverse',...
'PDH',...
'PFK',...
'PGI',...
'PGI_reverse',...
'PGM',...
'PGM_reverse',...
'PheSYN',...
'PPC',...
'PPCK',...
'ProSYN',...
'PRPPS',...
'PTAr_ACKr_ACS',...
'PTAr_ACKr_ACS_reverse',...
'PYK',...
'RPE',...
'RPE_reverse',...
'RPI',...
'RPI_reverse',...
'SERAT_CYSS',...
'SerSYN',...
'SUCCOAS',...
'SUCCOAS_reverse',...
'SUCDi',...
'SUCDi_reverse',...
'TALA',...
'TALA_reverse',...
'THRD_GLYAT',...
'ThrSYN',...
'TKT1a',...
'TKT1a_reverse',...
'TKT1b',...
'TKT1b_reverse',...
'TKT2a',...
'TKT2a_reverse',...
'TKT2b',...
'TKT2b_reverse',...
'TPI',...
'TPI_reverse',...
'TrpSYN',...
'TyrSYN',...
'ValSYN',...
};

m.rates.flx.val = mod2stoich(m); % make sure the fluxes are feasible
m.options.fit_starts = 10; % 10 restarts during the estimation procedure

m.expts = x;

m.expts.id = {'WTEColi_113C80_U13C20_01'};

% add experimental data for annotated fragments 
% (fragments are represented by (1,1) / (2,1) / (3,1) etc)
m.expts.data_ms(1).idvs.id(1,1) = {'3pg_c_C3H6O7P_MRM_0_0_WTEColi_113C80_U13C20_01'};
m.expts.data_ms(1).idvs.time(1,1) = 0;
m.expts.data_ms(1).idvs.val(1,1) = 0.434465;
m.expts.data_ms(1).idvs.std(1,1) = 0.016856;
m.expts.data_ms(1).idvs.val(2,1) = 0.355111;
m.expts.data_ms(1).idvs.std(2,1) = 0.016396;
m.expts.data_ms(1).idvs.val(3,1) = 0.029010;
m.expts.data_ms(1).idvs.std(3,1) = 0.001;
m.expts.data_ms(1).idvs.val(4,1) = 0.181414;
m.expts.data_ms(1).idvs.std(4,1) = 0.010082;
m.expts.data_ms(2).idvs.id(1,1) = {'6pgc_c_C6H12O10P_MRM_0_0_WTEColi_113C80_U13C20_01'};
m.expts.data_ms(2).idvs.time(1,1) = 0;
m.expts.data_ms(2).idvs.val(1,1) = 0.095200;
m.expts.data_ms(2).idvs.std(1,1) = 0.028053;
m.expts.data_ms(2).idvs.val(2,1) = 0.579040;
m.expts.data_ms(2).idvs.std(2,1) = 0.044410;
m.expts.data_ms(2).idvs.val(3,1) = 0.078848;
m.expts.data_ms(2).idvs.std(3,1) = 0.002324;
m.expts.data_ms(2).idvs.val(4,1) = 0.052890;
m.expts.data_ms(2).idvs.std(4,1) = 0.018948;
m.expts.data_ms(2).idvs.val(5,1) = 0.034830;
m.expts.data_ms(2).idvs.std(5,1) = 0.004691;
m.expts.data_ms(2).idvs.val(6,1) = 0.028073;
m.expts.data_ms(2).idvs.std(6,1) = 0.007793;
m.expts.data_ms(2).idvs.val(7,1) = 0.131119;
m.expts.data_ms(2).idvs.std(7,1) = 0.009860;
m.expts.data_ms(3).idvs.id(1,1) = {'akg_c_C4H5O3_MRM_0_0_WTEColi_113C80_U13C20_01'};
m.expts.data_ms(3).idvs.time(1,1) = 0;
m.expts.data_ms(3).idvs.val(1,1) = 0.013934;
m.expts.data_ms(3).idvs.std(1,1) = 0.001558;
m.expts.data_ms(3).idvs.val(2,1) = 0.428172;
m.expts.data_ms(3).idvs.std(2,1) = 0.024559;
m.expts.data_ms(3).idvs.val(3,1) = 0.352685;
m.expts.data_ms(3).idvs.std(3,1) = 0.015731;
m.expts.data_ms(3).idvs.val(4,1) = 0.164231;
m.expts.data_ms(3).idvs.std(4,1) = 0.008213;
m.expts.data_ms(3).idvs.val(5,1) = 0.045623;
m.expts.data_ms(3).idvs.std(5,1) = 0.013708;
m.expts.data_ms(4).idvs.id(1,1) = {'akg_c_C5H5O5_MRM_0_0_WTEColi_113C80_U13C20_01'};
m.expts.data_ms(4).idvs.time(1,1) = 0;
m.expts.data_ms(4).idvs.val(1,1) = NaN;
m.expts.data_ms(4).idvs.std(1,1) = 0.05;
m.expts.data_ms(4).idvs.val(2,1) = 0.353333;
m.expts.data_ms(4).idvs.std(2,1) = 0.017717;
m.expts.data_ms(4).idvs.val(3,1) = 0.332789;
m.expts.data_ms(4).idvs.std(3,1) = 0.015585;
m.expts.data_ms(4).idvs.val(4,1) = 0.216495;
m.expts.data_ms(4).idvs.std(4,1) = 0.013032;
m.expts.data_ms(4).idvs.val(5,1) = 0.073872;
m.expts.data_ms(4).idvs.std(5,1) = 0.010747;
m.expts.data_ms(4).idvs.val(6,1) = 0.023512;
m.expts.data_ms(4).idvs.std(6,1) = 0.003334;
m.expts.data_ms(5).idvs.id(1,1) = {'asp_DASH_L_c_C3H6NO2_MRM_0_0_WTEColi_113C80_U13C20_01'};
m.expts.data_ms(5).idvs.time(1,1) = 0;
m.expts.data_ms(5).idvs.val(1,1) = 0.362688;
m.expts.data_ms(5).idvs.std(1,1) = 0.012540;
m.expts.data_ms(5).idvs.val(2,1) = 0.371120;
m.expts.data_ms(5).idvs.std(2,1) = 0.018407;
m.expts.data_ms(5).idvs.val(3,1) = 0.156202;
m.expts.data_ms(5).idvs.std(3,1) = 0.006683;
m.expts.data_ms(5).idvs.val(4,1) = 0.109989;
m.expts.data_ms(5).idvs.std(4,1) = 0.009069;
m.expts.data_ms(6).idvs.id(1,1) = {'asp_DASH_L_c_C4H6NO4_MRM_0_0_WTEColi_113C80_U13C20_01'};
m.expts.data_ms(6).idvs.time(1,1) = 0;
m.expts.data_ms(6).idvs.val(1,1) = 0.326136;
m.expts.data_ms(6).idvs.std(1,1) = 0.015887;
m.expts.data_ms(6).idvs.val(2,1) = 0.351614;
m.expts.data_ms(6).idvs.std(2,1) = 0.018870;
m.expts.data_ms(6).idvs.val(3,1) = 0.148690;
m.expts.data_ms(6).idvs.std(3,1) = 0.007521;
m.expts.data_ms(6).idvs.val(4,1) = 0.149127;
m.expts.data_ms(6).idvs.std(4,1) = 0.013360;
m.expts.data_ms(6).idvs.val(5,1) = 0.024432;
m.expts.data_ms(6).idvs.std(5,1) = 0.002726;
m.expts.data_ms(7).idvs.id(1,1) = {'dhap_c_C3H6O6P_MRM_0_0_WTEColi_113C80_U13C20_01'};
m.expts.data_ms(7).idvs.time(1,1) = 0;
m.expts.data_ms(7).idvs.val(1,1) = 0.285900;
m.expts.data_ms(7).idvs.std(1,1) = 0.032310;
m.expts.data_ms(7).idvs.val(2,1) = 0.483533;
m.expts.data_ms(7).idvs.std(2,1) = 0.025295;
m.expts.data_ms(7).idvs.val(3,1) = NaN;
m.expts.data_ms(7).idvs.std(3,1) = 0.05;
m.expts.data_ms(7).idvs.val(4,1) = 0.230567;
m.expts.data_ms(7).idvs.std(4,1) = 0.022203;
m.expts.data_ms(8).idvs.id(1,1) = {'fdp_c_C6H13O12P2_MRM_0_0_WTEColi_113C80_U13C20_01'};
m.expts.data_ms(8).idvs.time(1,1) = 0;
m.expts.data_ms(8).idvs.val(1,1) = 0.041052;
m.expts.data_ms(8).idvs.std(1,1) = 0.004040;
m.expts.data_ms(8).idvs.val(2,1) = 0.461428;
m.expts.data_ms(8).idvs.std(2,1) = 0.023609;
m.expts.data_ms(8).idvs.val(3,1) = 0.158614;
m.expts.data_ms(8).idvs.std(3,1) = 0.005668;
m.expts.data_ms(8).idvs.val(4,1) = 0.118388;
m.expts.data_ms(8).idvs.std(4,1) = 0.011194;
m.expts.data_ms(8).idvs.val(5,1) = 0.107184;
m.expts.data_ms(8).idvs.std(5,1) = 0.014787;
m.expts.data_ms(8).idvs.val(6,1) = 0.018744;
m.expts.data_ms(8).idvs.std(6,1) = 0.004603;
m.expts.data_ms(8).idvs.val(7,1) = 0.094590;
m.expts.data_ms(8).idvs.std(7,1) = 0.011793;
m.expts.data_ms(9).idvs.id(1,1) = {'g6p_c_C6H12O9P_MRM_0_0_WTEColi_113C80_U13C20_01'};
m.expts.data_ms(9).idvs.time(1,1) = 0;
m.expts.data_ms(9).idvs.val(1,1) = 0.062617;
m.expts.data_ms(9).idvs.std(1,1) = 0.023661;
m.expts.data_ms(9).idvs.val(2,1) = 0.751292;
m.expts.data_ms(9).idvs.std(2,1) = 0.026106;
m.expts.data_ms(9).idvs.val(3,1) = NaN;
m.expts.data_ms(9).idvs.std(3,1) = 0.05;
m.expts.data_ms(9).idvs.val(4,1) = NaN;
m.expts.data_ms(9).idvs.std(4,1) = 0.05;
m.expts.data_ms(9).idvs.val(5,1) = NaN;
m.expts.data_ms(9).idvs.std(5,1) = 0.05;
m.expts.data_ms(9).idvs.val(6,1) = NaN;
m.expts.data_ms(9).idvs.std(6,1) = 0.05;
m.expts.data_ms(9).idvs.val(7,1) = 0.186092;
m.expts.data_ms(9).idvs.std(7,1) = 0.016314;
m.expts.data_ms(10).idvs.id(1,1) = {'glc_DASH_D_c_C2H3O2_MRM_0_0_WTEColi_113C80_U13C20_01'};
m.expts.data_ms(10).idvs.time(1,1) = 0;
m.expts.data_ms(10).idvs.val(1,1) = 0.624427;
m.expts.data_ms(10).idvs.std(1,1) = 0.016085;
m.expts.data_ms(10).idvs.val(2,1) = 0.148057;
m.expts.data_ms(10).idvs.std(2,1) = 0.008542;
m.expts.data_ms(10).idvs.val(3,1) = 0.227517;
m.expts.data_ms(10).idvs.std(3,1) = 0.017151;
m.expts.data_ms(11).idvs.id(1,1) = {'glc_DASH_D_c_C6H11O6_MRM_0_0_WTEColi_113C80_U13C20_01'};
m.expts.data_ms(11).idvs.time(1,1) = 0;
m.expts.data_ms(11).idvs.val(1,1) = 0.006993;
m.expts.data_ms(11).idvs.std(1,1) = 0.001303;
m.expts.data_ms(11).idvs.val(2,1) = 0.733836;
m.expts.data_ms(11).idvs.std(2,1) = 0.018927;
m.expts.data_ms(11).idvs.val(3,1) = 0.024066;
m.expts.data_ms(11).idvs.std(3,1) = 0.001442;
m.expts.data_ms(11).idvs.val(4,1) = 0.009327;
m.expts.data_ms(11).idvs.std(4,1) = 0.001;
m.expts.data_ms(11).idvs.val(5,1) = 0.001631;
m.expts.data_ms(11).idvs.std(5,1) = 0.001;
m.expts.data_ms(11).idvs.val(6,1) = 0.013691;
m.expts.data_ms(11).idvs.std(6,1) = 0.001;
m.expts.data_ms(11).idvs.val(7,1) = 0.212787;
m.expts.data_ms(11).idvs.std(7,1) = 0.017021;
m.expts.data_ms(12).idvs.id(1,1) = {'glu_DASH_L_c_C5H6NO3_MRM_0_0_WTEColi_113C80_U13C20_01'};
m.expts.data_ms(12).idvs.time(1,1) = 0;
m.expts.data_ms(12).idvs.val(1,1) = 0.134416;
m.expts.data_ms(12).idvs.std(1,1) = 0.005110;
m.expts.data_ms(12).idvs.val(2,1) = 0.282379;
m.expts.data_ms(12).idvs.std(2,1) = 0.018534;
m.expts.data_ms(12).idvs.val(3,1) = 0.294520;
m.expts.data_ms(12).idvs.std(3,1) = 0.015667;
m.expts.data_ms(12).idvs.val(4,1) = 0.194677;
m.expts.data_ms(12).idvs.std(4,1) = 0.007157;
m.expts.data_ms(12).idvs.val(5,1) = 0.076754;
m.expts.data_ms(12).idvs.std(5,1) = 0.004422;
m.expts.data_ms(12).idvs.val(6,1) = 0.017254;
m.expts.data_ms(12).idvs.std(6,1) = 0.001;
m.expts.data_ms(13).idvs.id(1,1) = {'glu_DASH_L_c_C5H8NO4_MRM_0_0_WTEColi_113C80_U13C20_01'};
m.expts.data_ms(13).idvs.time(1,1) = 0;
m.expts.data_ms(13).idvs.val(1,1) = 0.134416;
m.expts.data_ms(13).idvs.std(1,1) = 0.005110;
m.expts.data_ms(13).idvs.val(2,1) = 0.282379;
m.expts.data_ms(13).idvs.std(2,1) = 0.018534;
m.expts.data_ms(13).idvs.val(3,1) = 0.294520;
m.expts.data_ms(13).idvs.std(3,1) = 0.015667;
m.expts.data_ms(13).idvs.val(4,1) = 0.194677;
m.expts.data_ms(13).idvs.std(4,1) = 0.007157;
m.expts.data_ms(13).idvs.val(5,1) = 0.076754;
m.expts.data_ms(13).idvs.std(5,1) = 0.004422;
m.expts.data_ms(13).idvs.val(6,1) = 0.017254;
m.expts.data_ms(13).idvs.std(6,1) = 0.001;
m.expts.data_ms(14).idvs.id(1,1) = {'icit_c_C5H3O3_MRM_0_0_WTEColi_113C80_U13C20_01'};
m.expts.data_ms(14).idvs.time(1,1) = 0;
m.expts.data_ms(14).idvs.val(1,1) = 0.271897;
m.expts.data_ms(14).idvs.std(1,1) = 0.076534;
m.expts.data_ms(14).idvs.val(2,1) = 0.258801;
m.expts.data_ms(14).idvs.std(2,1) = 0.017047;
m.expts.data_ms(14).idvs.val(3,1) = 0.237092;
m.expts.data_ms(14).idvs.std(3,1) = 0.029387;
m.expts.data_ms(14).idvs.val(4,1) = 0.148028;
m.expts.data_ms(14).idvs.std(4,1) = 0.021229;
m.expts.data_ms(14).idvs.val(5,1) = 0.068104;
m.expts.data_ms(14).idvs.std(5,1) = 0.010874;
m.expts.data_ms(14).idvs.val(6,1) = 0.016077;
m.expts.data_ms(14).idvs.std(6,1) = 0.003853;
m.expts.data_ms(15).idvs.id(1,1) = {'icit_c_C6H7O7_MRM_0_0_WTEColi_113C80_U13C20_01'};
m.expts.data_ms(15).idvs.time(1,1) = 0;
m.expts.data_ms(15).idvs.val(1,1) = 0.255439;
m.expts.data_ms(15).idvs.std(1,1) = 0.078364;
m.expts.data_ms(15).idvs.val(2,1) = 0.225579;
m.expts.data_ms(15).idvs.std(2,1) = 0.014389;
m.expts.data_ms(15).idvs.val(3,1) = 0.224783;
m.expts.data_ms(15).idvs.std(3,1) = 0.032035;
m.expts.data_ms(15).idvs.val(4,1) = 0.169475;
m.expts.data_ms(15).idvs.std(4,1) = 0.020443;
m.expts.data_ms(15).idvs.val(5,1) = 0.086903;
m.expts.data_ms(15).idvs.std(5,1) = 0.015603;
m.expts.data_ms(15).idvs.val(6,1) = 0.032236;
m.expts.data_ms(15).idvs.std(6,1) = 0.006167;
m.expts.data_ms(15).idvs.val(7,1) = 0.005586;
m.expts.data_ms(15).idvs.std(7,1) = 0.001350;
m.expts.data_ms(16).idvs.id(1,1) = {'mal_DASH_L_c_C4H3O4_MRM_0_0_WTEColi_113C80_U13C20_01'};
m.expts.data_ms(16).idvs.time(1,1) = 0;
m.expts.data_ms(16).idvs.val(1,1) = 0.324639;
m.expts.data_ms(16).idvs.std(1,1) = 0.010540;
m.expts.data_ms(16).idvs.val(2,1) = 0.336361;
m.expts.data_ms(16).idvs.std(2,1) = 0.006635;
m.expts.data_ms(16).idvs.val(3,1) = 0.162212;
m.expts.data_ms(16).idvs.std(3,1) = 0.009092;
m.expts.data_ms(16).idvs.val(4,1) = 0.151846;
m.expts.data_ms(16).idvs.std(4,1) = 0.008262;
m.expts.data_ms(16).idvs.val(5,1) = 0.024941;
m.expts.data_ms(16).idvs.std(5,1) = 0.001721;
m.expts.data_ms(17).idvs.id(1,1) = {'mal_DASH_L_c_C4H5O5_MRM_0_0_WTEColi_113C80_U13C20_01'};
m.expts.data_ms(17).idvs.time(1,1) = 0;
m.expts.data_ms(17).idvs.val(1,1) = 0.324639;
m.expts.data_ms(17).idvs.std(1,1) = 0.010540;
m.expts.data_ms(17).idvs.val(2,1) = 0.336361;
m.expts.data_ms(17).idvs.std(2,1) = 0.006635;
m.expts.data_ms(17).idvs.val(3,1) = 0.162212;
m.expts.data_ms(17).idvs.std(3,1) = 0.009092;
m.expts.data_ms(17).idvs.val(4,1) = 0.151846;
m.expts.data_ms(17).idvs.std(4,1) = 0.008262;
m.expts.data_ms(17).idvs.val(5,1) = 0.024941;
m.expts.data_ms(17).idvs.std(5,1) = 0.001721;
m.expts.data_ms(18).idvs.id(1,1) = {'met_DASH_L_c_C5H10NO2S_MRM_0_0_WTEColi_113C80_U13C20_01'};
m.expts.data_ms(18).idvs.time(1,1) = 0;
m.expts.data_ms(18).idvs.val(1,1) = 0.116097;
m.expts.data_ms(18).idvs.std(1,1) = 0.025444;
m.expts.data_ms(18).idvs.val(2,1) = 0.288208;
m.expts.data_ms(18).idvs.std(2,1) = 0.012455;
m.expts.data_ms(18).idvs.val(3,1) = 0.275276;
m.expts.data_ms(18).idvs.std(3,1) = 0.023369;
m.expts.data_ms(18).idvs.val(4,1) = 0.189532;
m.expts.data_ms(18).idvs.std(4,1) = 0.006959;
m.expts.data_ms(18).idvs.val(5,1) = 0.099766;
m.expts.data_ms(18).idvs.std(5,1) = 0.013654;
m.expts.data_ms(18).idvs.val(6,1) = 0.031122;
m.expts.data_ms(18).idvs.std(6,1) = 0.004254;
m.expts.data_ms(19).idvs.id(1,1) = {'met_DASH_L_c_CH3S_MRM_0_0_WTEColi_113C80_U13C20_01'};
m.expts.data_ms(19).idvs.time(1,1) = 0;
m.expts.data_ms(19).idvs.val(1,1) = 0.473937;
m.expts.data_ms(19).idvs.std(1,1) = 0.029731;
m.expts.data_ms(19).idvs.val(2,1) = 0.526063;
m.expts.data_ms(19).idvs.std(2,1) = 0.029731;
m.expts.data_ms(20).idvs.id(1,1) = {'pep_c_C3H4O6P_MRM_0_0_WTEColi_113C80_U13C20_01'};
m.expts.data_ms(20).idvs.time(1,1) = 0;
m.expts.data_ms(20).idvs.val(1,1) = 0.439365;
m.expts.data_ms(20).idvs.std(1,1) = 0.020835;
m.expts.data_ms(20).idvs.val(2,1) = 0.360178;
m.expts.data_ms(20).idvs.std(2,1) = 0.019004;
m.expts.data_ms(20).idvs.val(3,1) = 0.034129;
m.expts.data_ms(20).idvs.std(3,1) = 0.002554;
m.expts.data_ms(20).idvs.val(4,1) = 0.166329;
m.expts.data_ms(20).idvs.std(4,1) = 0.018437;
m.expts.data_ms(21).idvs.id(1,1) = {'phe_DASH_L_c_C9H10NO2_MRM_0_0_WTEColi_113C80_U13C20_01'};
m.expts.data_ms(21).idvs.time(1,1) = 0;
m.expts.data_ms(21).idvs.val(1,1) = NaN;
m.expts.data_ms(21).idvs.std(1,1) = 0.05;
m.expts.data_ms(21).idvs.val(2,1) = 0.250992;
m.expts.data_ms(21).idvs.std(2,1) = 0.037377;
m.expts.data_ms(21).idvs.val(3,1) = 0.230747;
m.expts.data_ms(21).idvs.std(3,1) = 0.030177;
m.expts.data_ms(21).idvs.val(4,1) = 0.208668;
m.expts.data_ms(21).idvs.std(4,1) = 0.041008;
m.expts.data_ms(21).idvs.val(5,1) = 0.142391;
m.expts.data_ms(21).idvs.std(5,1) = 0.027538;
m.expts.data_ms(21).idvs.val(6,1) = 0.087717;
m.expts.data_ms(21).idvs.std(6,1) = 0.018462;
m.expts.data_ms(21).idvs.val(7,1) = 0.040323;
m.expts.data_ms(21).idvs.std(7,1) = 0.016610;
m.expts.data_ms(21).idvs.val(8,1) = 0.024409;
m.expts.data_ms(21).idvs.std(8,1) = 0.007441;
m.expts.data_ms(21).idvs.val(9,1) = 0.017703;
m.expts.data_ms(21).idvs.std(9,1) = 0.006475;
m.expts.data_ms(21).idvs.val(10,1) = NaN;
m.expts.data_ms(21).idvs.std(10,1) = 0.05;
m.expts.data_ms(22).idvs.id(1,1) = {'phe_DASH_L_c_C9H7O2_MRM_0_0_WTEColi_113C80_U13C20_01'};
m.expts.data_ms(22).idvs.time(1,1) = 0;
m.expts.data_ms(22).idvs.val(1,1) = NaN;
m.expts.data_ms(22).idvs.std(1,1) = 0.05;
m.expts.data_ms(22).idvs.val(2,1) = 0.250992;
m.expts.data_ms(22).idvs.std(2,1) = 0.037377;
m.expts.data_ms(22).idvs.val(3,1) = 0.230747;
m.expts.data_ms(22).idvs.std(3,1) = 0.030177;
m.expts.data_ms(22).idvs.val(4,1) = 0.208668;
m.expts.data_ms(22).idvs.std(4,1) = 0.041008;
m.expts.data_ms(22).idvs.val(5,1) = 0.142391;
m.expts.data_ms(22).idvs.std(5,1) = 0.027538;
m.expts.data_ms(22).idvs.val(6,1) = 0.087717;
m.expts.data_ms(22).idvs.std(6,1) = 0.018462;
m.expts.data_ms(22).idvs.val(7,1) = 0.040323;
m.expts.data_ms(22).idvs.std(7,1) = 0.016610;
m.expts.data_ms(22).idvs.val(8,1) = 0.024409;
m.expts.data_ms(22).idvs.std(8,1) = 0.007441;
m.expts.data_ms(22).idvs.val(9,1) = 0.017703;
m.expts.data_ms(22).idvs.std(9,1) = 0.006475;
m.expts.data_ms(22).idvs.val(10,1) = NaN;
m.expts.data_ms(22).idvs.std(10,1) = 0.05;
m.expts.data_ms(23).idvs.id(1,1) = {'prpp_c_C5H12O14P3_MRM_0_0_WTEColi_113C80_U13C20_01'};
m.expts.data_ms(23).idvs.time(1,1) = 0;
m.expts.data_ms(23).idvs.val(1,1) = 0.266659;
m.expts.data_ms(23).idvs.std(1,1) = 0.014429;
m.expts.data_ms(23).idvs.val(2,1) = 0.278395;
m.expts.data_ms(23).idvs.std(2,1) = 0.042145;
m.expts.data_ms(23).idvs.val(3,1) = 0.153679;
m.expts.data_ms(23).idvs.std(3,1) = 0.015803;
m.expts.data_ms(23).idvs.val(4,1) = 0.168375;
m.expts.data_ms(23).idvs.std(4,1) = 0.019471;
m.expts.data_ms(23).idvs.val(5,1) = 0.050496;
m.expts.data_ms(23).idvs.std(5,1) = 0.018131;
m.expts.data_ms(23).idvs.val(6,1) = 0.082396;
m.expts.data_ms(23).idvs.std(6,1) = 0.031270;
m.expts.data_ms(24).idvs.id(1,1) = {'pyr_c_C3H3O3_MRM_0_0_WTEColi_113C80_U13C20_01'};
m.expts.data_ms(24).idvs.time(1,1) = 0;
m.expts.data_ms(24).idvs.val(1,1) = 0.424906;
m.expts.data_ms(24).idvs.std(1,1) = 0.009673;
m.expts.data_ms(24).idvs.val(2,1) = 0.348525;
m.expts.data_ms(24).idvs.std(2,1) = 0.016715;
m.expts.data_ms(24).idvs.val(3,1) = 0.062996;
m.expts.data_ms(24).idvs.std(3,1) = 0.008472;
m.expts.data_ms(24).idvs.val(4,1) = 0.163573;
m.expts.data_ms(24).idvs.std(4,1) = 0.017494;
m.expts.data_ms(25).idvs.id(1,1) = {'s7p_c_C7H14O10P_MRM_0_0_WTEColi_113C80_U13C20_01'};
m.expts.data_ms(25).idvs.time(1,1) = 0;
m.expts.data_ms(25).idvs.val(1,1) = 0.210187;
m.expts.data_ms(25).idvs.std(1,1) = 0.026767;
m.expts.data_ms(25).idvs.val(2,1) = 0.286272;
m.expts.data_ms(25).idvs.std(2,1) = 0.014999;
m.expts.data_ms(25).idvs.val(3,1) = 0.196354;
m.expts.data_ms(25).idvs.std(3,1) = 0.025616;
m.expts.data_ms(25).idvs.val(4,1) = 0.149359;
m.expts.data_ms(25).idvs.std(4,1) = 0.015062;
m.expts.data_ms(25).idvs.val(5,1) = NaN;
m.expts.data_ms(25).idvs.std(5,1) = 0.05;
m.expts.data_ms(25).idvs.val(6,1) = 0.088349;
m.expts.data_ms(25).idvs.std(6,1) = 0.019838;
m.expts.data_ms(25).idvs.val(7,1) = 0.034132;
m.expts.data_ms(25).idvs.std(7,1) = 0.015539;
m.expts.data_ms(25).idvs.val(8,1) = 0.035348;
m.expts.data_ms(25).idvs.std(8,1) = 0.007067;
m.expts.data_ms(26).idvs.id(1,1) = {'succ_c_C4H3O3_MRM_0_0_WTEColi_113C80_U13C20_01'};
m.expts.data_ms(26).idvs.time(1,1) = 0;
m.expts.data_ms(26).idvs.val(1,1) = 0.217845;
m.expts.data_ms(26).idvs.std(1,1) = 0.014353;
m.expts.data_ms(26).idvs.val(2,1) = 0.307375;
m.expts.data_ms(26).idvs.std(2,1) = 0.018162;
m.expts.data_ms(26).idvs.val(3,1) = 0.287934;
m.expts.data_ms(26).idvs.std(3,1) = 0.008495;
m.expts.data_ms(26).idvs.val(4,1) = 0.143579;
m.expts.data_ms(26).idvs.std(4,1) = 0.014728;
m.expts.data_ms(26).idvs.val(5,1) = 0.043266;
m.expts.data_ms(26).idvs.std(5,1) = 0.008765;
m.expts.data_ms(27).idvs.id(1,1) = {'succ_c_C4H5O4_MRM_0_0_WTEColi_113C80_U13C20_01'};
m.expts.data_ms(27).idvs.time(1,1) = 0;
m.expts.data_ms(27).idvs.val(1,1) = 0.217845;
m.expts.data_ms(27).idvs.std(1,1) = 0.014353;
m.expts.data_ms(27).idvs.val(2,1) = 0.307375;
m.expts.data_ms(27).idvs.std(2,1) = 0.018162;
m.expts.data_ms(27).idvs.val(3,1) = 0.287934;
m.expts.data_ms(27).idvs.std(3,1) = 0.008495;
m.expts.data_ms(27).idvs.val(4,1) = 0.143579;
m.expts.data_ms(27).idvs.std(4,1) = 0.014728;
m.expts.data_ms(27).idvs.val(5,1) = 0.043266;
m.expts.data_ms(27).idvs.std(5,1) = 0.008765;
m.expts.data_ms(28).idvs.id(1,1) = {'thr_DASH_L_c_C2H4NO2_MRM_0_0_WTEColi_113C80_U13C20_01'};
m.expts.data_ms(28).idvs.time(1,1) = 0;
m.expts.data_ms(28).idvs.val(1,1) = 0.501832;
m.expts.data_ms(28).idvs.std(1,1) = 0.077235;
m.expts.data_ms(28).idvs.val(2,1) = 0.337914;
m.expts.data_ms(28).idvs.std(2,1) = 0.093654;
m.expts.data_ms(28).idvs.val(3,1) = 0.160254;
m.expts.data_ms(28).idvs.std(3,1) = 0.018596;
m.expts.data_ms(29).idvs.id(1,1) = {'thr_DASH_L_c_C4H8NO3_MRM_0_0_WTEColi_113C80_U13C20_01'};
m.expts.data_ms(29).idvs.time(1,1) = 0;
m.expts.data_ms(29).idvs.val(1,1) = 0.262139;
m.expts.data_ms(29).idvs.std(1,1) = 0.056147;
m.expts.data_ms(29).idvs.val(2,1) = 0.391915;
m.expts.data_ms(29).idvs.std(2,1) = 0.112472;
m.expts.data_ms(29).idvs.val(3,1) = 0.172558;
m.expts.data_ms(29).idvs.std(3,1) = 0.034926;
m.expts.data_ms(29).idvs.val(4,1) = 0.126749;
m.expts.data_ms(29).idvs.std(4,1) = 0.022886;
m.expts.data_ms(29).idvs.val(5,1) = 0.046639;
m.expts.data_ms(29).idvs.std(5,1) = 0.007105;

% estimates parameters of the partially specified ARIMA(p,D,q) model m
% given the observed univariate time series y using maximum likelihood. 
% f is the corresponding fully specified ARIMA model that stores the parameter estimates
% f = simulate(m);
f=estimate(m,10);

f=continuate(f,m);

%filename = 'TestFile.mat';
%save(filename,'f','m')