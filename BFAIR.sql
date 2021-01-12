--
-- PostgreSQL database dump
--

-- Dumped from database version 12.3
-- Dumped by pg_dump version 12.3

-- Started on 2020-11-12 21:39:34

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

DROP DATABASE "BFAIROmics";
--
-- TOC entry 3446 (class 1262 OID 17434)
-- Name: BFAIROmics; Type: DATABASE; Schema: -; Owner: postgres
--

CREATE DATABASE "BFAIROmics" WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'German_Germany.1252' LC_CTYPE = 'German_Germany.1252';


ALTER DATABASE "BFAIROmics" OWNER TO postgres;

\connect "BFAIROmics"

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 203 (class 1259 OID 17437)
-- Name: ASSAY; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."ASSAY" (
    "Assay_ID" integer NOT NULL,
    "Assay_Identifier" text,
    "Assay_Measurement_Type" text,
    "Assay_Measurement_Type_Term_Accession_Number" text,
    "Assay_Measurement_Type_Term_Source_REF" text,
    "Assay_Technology_Type" text,
    "Assay_Technology_Type_Term_Accession_Number" text,
    "Assay_Technology_Type_Term_Source_REF" text,
    "Assay_Technology_Platform" text
);


ALTER TABLE public."ASSAY" OWNER TO postgres;

--
-- TOC entry 202 (class 1259 OID 17435)
-- Name: ASSAY_Assay_ID_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."ASSAY_Assay_ID_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."ASSAY_Assay_ID_seq" OWNER TO postgres;

--
-- TOC entry 3447 (class 0 OID 0)
-- Dependencies: 202
-- Name: ASSAY_Assay_ID_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."ASSAY_Assay_ID_seq" OWNED BY public."ASSAY"."Assay_ID";


--
-- TOC entry 221 (class 1259 OID 17579)
-- Name: A_TECHNOLOGY_MICROARRAY; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."A_TECHNOLOGY_MICROARRAY" (
    "Assay_ID" integer NOT NULL,
    "Sample_Name" text,
    "Extract_Name" text,
    "Labeled_Extract_Name" text,
    "Label" text,
    "Hybridization_Assay_Name" text,
    "Comment[ArrayExpress_Accession]" text,
    "Comment[ArrayExpress_Raw_Data_URL]" text,
    "Comment[ArrayExpress_Processed_Data_URL]" text,
    "Array_Design_REF" text,
    "Scan_Name" text,
    "Array_Data_File" text,
    "Data_Transformation_Name" text,
    "Derived_Array_Data_File" text,
    "Array_Data_Matrix_File" text,
    "Derived_Array_Data_Matrix_File" text,
    "Array_Design_File" text,
    "id" integer NOT NULL
);


ALTER TABLE public."A_TECHNOLOGY_MICROARRAY" OWNER TO postgres;

--
-- TOC entry 224 (class 1259 OID 18268)
-- Name: A_TECHNOLOGY_MICROARRAY_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."A_TECHNOLOGY_MICROARRAY_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."A_TECHNOLOGY_MICROARRAY_id_seq" OWNER TO postgres;

--
-- TOC entry 3448 (class 0 OID 0)
-- Dependencies: 224
-- Name: A_TECHNOLOGY_MICROARRAY_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."A_TECHNOLOGY_MICROARRAY_id_seq" OWNED BY public."A_TECHNOLOGY_MICROARRAY"."A_Technology_Microarray_ID";


--
-- TOC entry 222 (class 1259 OID 17587)
-- Name: A_TECHNOLOGY_MS; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."A_TECHNOLOGY_MS" (
    "Assay_ID" integer NOT NULL,
    "Sample_Name" text NOT NULL,
    "Extract_Name" text,
    "Labeled_Extract_Name" text,
    "Label" text,
    "MS_Assay_Name" text,
    "Raw_Spectral_Data_File" text,
    "Normalization_Name" text,
    "Protein_Assignment_File" text,
    "Peptide_Assignment_File" text,
    "Post_Translational_Modification_Assignment_File" text,
    "Data_Transformation_Name" text,
    "Derived_Spectral_Data_File" text,
    "id" integer NOT NULL
);


ALTER TABLE public."A_TECHNOLOGY_MS" OWNER TO postgres;

--
-- TOC entry 225 (class 1259 OID 18278)
-- Name: A_TECHNOLOGY_MS_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."A_TECHNOLOGY_MS_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."A_TECHNOLOGY_MS_A_Technology_MS_ID_seq" OWNER TO postgres;

--
-- TOC entry 3449 (class 0 OID 0)
-- Dependencies: 225
-- Name: A_TECHNOLOGY_MS_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."A_TECHNOLOGY_MS_id_seq" OWNED BY public."A_TECHNOLOGY_MS"."A_Technology_MS_ID";


--
-- TOC entry 223 (class 1259 OID 17595)
-- Name: A_TECHNOLOGY_NMR; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."A_TECHNOLOGY_NMR" (
    "Assay_ID" integer NOT NULL,
    "Sample_Name" text,
    "Extract_Name" text,
    "Labeled_Extract_Name" text,
    "Label" text,
    "NMR_Assay_Name" text,
    "Free_Induction_Decay_Data_File" text,
    "Acquisition_Parameter_Data_File" text,
    "Derived_Spectral_Data_File" text,
    "Normalization_Name" text,
    "Data_Transformation_Name" text,
    "Metabolite_Assignment_File" text,
    "id" integer NOT NULL
);


ALTER TABLE public."A_TECHNOLOGY_NMR" OWNER TO postgres;

--
-- TOC entry 226 (class 1259 OID 18289)
-- Name: A_TECHNOLOGY_NMR_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."A_TECHNOLOGY_NMR_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."A_TECHNOLOGY_NMR_A_Technology_NMR_ID_seq" OWNER TO postgres;

--
-- TOC entry 3450 (class 0 OID 0)
-- Dependencies: 226
-- Name: A_TECHNOLOGY_NMR_A_Technology_NMR_ID_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."A_TECHNOLOGY_NMR_A_Technology_NMR_ID_seq" OWNED BY public."A_TECHNOLOGY_NMR"."A_Technology_NMR_ID";


--
-- TOC entry 205 (class 1259 OID 17484)
-- Name: CONTACTS; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."CONTACTS" (
    "Contact_Person_ID" integer NOT NULL,
    "Person_Last_Name" text,
    "Person_First_Name" text,
    "Person_Mid_Initials" text,
    "Person_Email" text,
    "Person_Phone" text,
    "Person_Fax" text,
    "Person_Address" text,
    "Person_Affiliation" text,
    "Person_Roles" text,
    "Person_Roles_Term_Accession_Number" text,
    "Person_Roles_Term_Source_REF" text
);


ALTER TABLE public."CONTACTS" OWNER TO postgres;

--
-- TOC entry 204 (class 1259 OID 17482)
-- Name: CONTACTS_Contact_Person_ID_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."CONTACTS_Contact_Person_ID_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."CONTACTS_Contact_Person_ID_seq" OWNER TO postgres;

--
-- TOC entry 3451 (class 0 OID 0)
-- Dependencies: 204
-- Name: CONTACTS_Contact_Person_ID_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."CONTACTS_Contact_Person_ID_seq" OWNED BY public."CONTACTS"."Contact_Person_ID";


--
-- TOC entry 252 (class 1259 OID 18510)
-- Name: FeatureXML; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."FeatureXML" (
    "FeatureMap" xml NOT NULL,
    "Sample_Name" text NOT NULL,
    "Investigation_ID" integer NOT NULL,
    "Study_ID" integer NOT NULL,
    "Assay_ID" integer NOT NULL,
    id integer NOT NULL,
    "mzTab-ID" text NOT NULL
);


ALTER TABLE public."FeatureXML" OWNER TO postgres;

--
-- TOC entry 251 (class 1259 OID 18508)
-- Name: FeatureXML_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."FeatureXML_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."FeatureXML_id_seq" OWNER TO postgres;

--
-- TOC entry 3452 (class 0 OID 0)
-- Dependencies: 251
-- Name: FeatureXML_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."FeatureXML_id_seq" OWNED BY public."FeatureXML".id;


--
-- TOC entry 207 (class 1259 OID 17495)
-- Name: INVESTIGATION; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."INVESTIGATION" (
    "Investigation_ID" integer NOT NULL,
    "Investigation_Identifier" text NOT NULL,
    "Investigation_Title" text,
    "Investigation_Description" text,
    "Investigation_Submission_Date" date,
    "Investigation_Public_Release_Date" date,
    "Investigation_Contacts" integer,
    "Investigation_Publications" integer,
    "Investigation_Study_Identifier" text NOT NULL,
    id integer
);


ALTER TABLE public."INVESTIGATION" OWNER TO postgres;

--
-- TOC entry 206 (class 1259 OID 17493)
-- Name: INVESTIGATION_Investigation_ID_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."INVESTIGATION_Investigation_ID_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."INVESTIGATION_Investigation_ID_seq" OWNER TO postgres;

--
-- TOC entry 3453 (class 0 OID 0)
-- Dependencies: 206
-- Name: INVESTIGATION_Investigation_ID_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."INVESTIGATION_Investigation_ID_seq" OWNED BY public."INVESTIGATION"."Investigation_ID";


--
-- TOC entry 260 (class 1259 OID 18560)
-- Name: MFA_model_metabolites ; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."MFA_model_metabolites " (
    id integer NOT NULL,
    mapping_id text NOT NULL,
    met_id text NOT NULL,
    met_elements text[],
    met_atompositions integer[],
    met_symmetry_elements text[],
    met_symmetry_atompositions integer[],
    used boolean,
    comment text,
    met_mapping json,
    base_met_ids text[],
    base_met_elements json,
    base_met_atompositions json,
    base_met_symmetry_elements json,
    base_met_symmetry_atompositions json,
    base_met_indices integer[]
);


ALTER TABLE public."MFA_model_metabolites " OWNER TO postgres;

--
-- TOC entry 259 (class 1259 OID 18558)
-- Name: MFA_model_metabolites _id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."MFA_model_metabolites _id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."MFA_model_metabolites _id_seq" OWNER TO postgres;

--
-- TOC entry 3454 (class 0 OID 0)
-- Dependencies: 259
-- Name: MFA_model_metabolites _id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."MFA_model_metabolites _id_seq" OWNED BY public."MFA_model_metabolites ".id;


--
-- TOC entry 262 (class 1259 OID 18571)
-- Name: MFA_model_reactions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."MFA_model_reactions" (
    id integer NOT NULL,
    model_id text NOT NULL,
    rxn_id text NOT NULL,
    rxn_name text,
    equation text,
    subsystem text,
    gpr text,
    genes text[],
    reactants_stoichiometry double precision[],
    products_stoichiometry double precision[],
    reactants_ids text[],
    products_ids text[],
    lower_bound double precision,
    upper_bound double precision,
    objective_coefficient double precision,
    flux_units text,
    fixed boolean,
    free boolean,
    reversibility boolean,
    weight double precision,
    used boolean,
    comment text
);


ALTER TABLE public."MFA_model_reactions" OWNER TO postgres;

--
-- Name: MFA_model_reactions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."MFA_model_reactions_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."MFA_model_reactions_id_seq" OWNER TO postgres;

--
-- Name: MFA_model_reactions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."MFA_model_reactions_id_seq" OWNED BY public."MFA_model_reactions".id;


--
-- Name: MFA_model_reactions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."MFA_model_reactions" ALTER COLUMN id SET DEFAULT nextval('public."MFA_model_reactions_id_seq"'::regclass);


--
-- Name: MFA_model_reactions MFA_model_reactions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."MFA_model_reactions"
    ADD CONSTRAINT "MFA_model_reactions_pkey" PRIMARY KEY (id);


--
-- Name: MFA_model_reactions MFA_model_reactions_model_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."MFA_model_reactions"
    ADD CONSTRAINT "MFA_model_reactions_model_id_fkey" FOREIGN KEY (model_id) REFERENCES public.models(model_id) NOT VALID;


--
-- PostgreSQL database dump complete
--




--
-- TOC entry 236 (class 1259 OID 18377)
-- Name: MzTab_M_Metadata_metabolomics; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."MzTab_M_Metadata_metabolomics" (
    id integer NOT NULL,
    "mzTab_version" text NOT NULL,
    title text,
    description text,
    sample_processing_number integer,
    sample_processing text,
    "instrument_name_number" integer,
    "instrument_name" text,
    "instrument_source_number" integer,
    "instrument_source" text,
    instrument_number integer,
    analyzer_number integer,
    "instrument_analyzer" text,
    "instrument_detector_number" integer,
    "instrument_detector" text,
    software_number integer NOT NULL,
    software text NOT NULL,
    setting_number integer,
    "software_setting" text,
    publication_number integer,
    publication text,
    "contact_name_number" integer,
    "contact_name" text,
    "contact_affiliation_number" integer,
    "contact_affiliation" text,
    "contact_email_number" integer,
    "contact_email" text,
    uri_number integer,
    uri text,
    external_study_uri_number integer,
    external_study_uri text,
    quantification_method text NOT NULL,
    sample_number integer,
    sample text,
    species_number integer,
    "sample_species" text,
    tissue_number integer,
    "sample_tissue" text,
    cell_type_number integer,
    "sample_cell_type" text,
    disease_number integer,
    "sample_disease" text,
    "sample_description" text,
    custom_number integer,
    "sample_custom" text,
    ms_run integer NOT NULL,
    "ms_run_location" text NOT NULL,
    "ms_run_instrument_ref" integer,
    "ms_run_format" text,
    "ms_run_id_format" text,
    fragmentation_method_number integer,
    "ms_run_fragmentation_method" text,
    scan_polarity_number integer NOT NULL,
    "ms_run_scan_polarity" text NOT NULL,
    "ms_run_hash" text,
    "ms_run_hash_method" text,
    assay_number integer NOT NULL,
    assay text NOT NULL,
    "assay_custom" text,
    "assay_external_uri" text,
    "assay_sample_ref" text,
    "assay_ms_run_ref" text NOT NULL,
    study_variable_number integer NOT NULL,
    study_variable text NOT NULL,
    "study_variable_assay_refs" text NOT NULL,
    "study_variable_average_function" text,
    "study_variable_variation_function" text,
    "study_variable_description" text NOT NULL,
    "study_variable_factors" text,
    "study_custom" text,
    cv_number integer NOT NULL,
    "cv_label" text NOT NULL,
    "cv_full_name" text NOT NULL,
    "cv_version" text NOT NULL,
    "cv_uri" text NOT NULL,
    database_number integer NOT NULL,
    database text NOT NULL,
    "database_prefix" text NOT NULL,
    "database_version" text NOT NULL,
    "database_uri" text NOT NULL,
    derivatization_agent_number integer,
    derivatization_agent text,
    "small_molecule_quantification_unit" text,
    "small_molecule_identification_reliability" integer,
    id_confidence_measure_number integer NOT NULL,
    id_confidence_measure text NOT NULL,
    "colunit_small_molecule" text,
    "colunit_small_molecule_evidence" text,
    "mzTab_ID" text NOT NULL
);


ALTER TABLE public."MzTab_M_Metadata_metabolomics" OWNER TO postgres;

--
-- TOC entry 242 (class 1259 OID 18419)
-- Name: MzTab_M_Small_Molecule_Evidence_SME_Section; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."MzTab_M_Small_Molecule_Evidence_SME_Section" (
    "SME_ID" integer NOT NULL,
    evidence_input_id text,
    database_identifier text,
    chemical_formula text,
    smiles text,
    inchi text,
    chemical_name text,
    uri text,
    derivatized_form text,
    adduct_ion text,
    exp_mass_to_charge double precision,
    charge integer,
    theoretical_mass_to_charge double precision,
    ms_run integer,
    spectra_ref text,
    identification_method text,
    ms_level integer,
    id_confidence_measure_number integer,
    id_confidence_measure double precision,
    rank integer
);


ALTER TABLE public."MzTab_M_Small_Molecule_Evidence_SME_Section" OWNER TO postgres;

--
-- TOC entry 241 (class 1259 OID 18417)
-- Name: MzTab_M_Small_Molecule_Evidence_SME_Section_SME_ID_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."MzTab_M_Small_Molecule_Evidence_SME_Section_SME_ID_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."MzTab_M_Small_Molecule_Evidence_SME_Section_SME_ID_seq" OWNER TO postgres;

--
-- TOC entry 3456 (class 0 OID 0)
-- Dependencies: 241
-- Name: MzTab_M_Small_Molecule_Evidence_SME_Section_SME_ID_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."MzTab_M_Small_Molecule_Evidence_SME_Section_SME_ID_seq" OWNED BY public."MzTab_M_Small_Molecule_Evidence_SME_Section"."SME_ID";


--
-- TOC entry 240 (class 1259 OID 18410)
-- Name: MzTab_M_Small_Molecule_Feature_SMF_Section; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."MzTab_M_Small_Molecule_Feature_SMF_Section" (
    "SMF_ID" integer NOT NULL,
    "SME_ID_REFS_number" integer,
    "SME_ID_REFS" integer,
    "SME_ID_REF_ambiguity_code" integer,
    adduct_ion text,
    isotopomer text,
    exp_mass_to_charge double precision NOT NULL,
    charge integer NOT NULL,
    retention_time_in_seconds double precision,
    retention_time_in_seconds_start double precision,
    retention_time_in_seconds_end double precision,
    abundance_assay_number integer,
    abundance_assay double precision
);


ALTER TABLE public."MzTab_M_Small_Molecule_Feature_SMF_Section" OWNER TO postgres;

--
-- TOC entry 239 (class 1259 OID 18408)
-- Name: MzTab_M_Small_Molecule_Feature_SMF_Section_SMF_ID_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."MzTab_M_Small_Molecule_Feature_SMF_Section_SMF_ID_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."MzTab_M_Small_Molecule_Feature_SMF_Section_SMF_ID_seq" OWNER TO postgres;

--
-- TOC entry 3457 (class 0 OID 0)
-- Dependencies: 239
-- Name: MzTab_M_Small_Molecule_Feature_SMF_Section_SMF_ID_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."MzTab_M_Small_Molecule_Feature_SMF_Section_SMF_ID_seq" OWNED BY public."MzTab_M_Small_Molecule_Feature_SMF_Section"."SMF_ID";


--
-- TOC entry 237 (class 1259 OID 18396)
-- Name: MzTab_M_small_molecule_section; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."MzTab_M_small_molecule_section" (
    "SML_ID" integer NOT NULL,
    "SMF_ID_REFS_number" integer,
    "SMF_ID_REFS" integer,
    database_identifier_number integer,
    database_identifier text,
    chemical_formula_number integer,
    chemical_formula text,
    smiles_number integer,
    smiles text,
    inchi_number integer,
    inchi text,
    chemical_name_number integer,
    chemical_name text,
    uri_number integer,
    uri text,
    theoretical_neutral_mass_number integer,
    theoretical_neutral_mass double precision,
    adduct_ions_number integer,
    adduct_ions text,
    reliability text,
    best_id_confidence_measure text,
    best_id_confidence_value double precision,
    abundance_assay_number integer,
    abundance_assay double precision,
    abundance_study_variable_number integer,
    abundance_study_variable double precision,
    abundance_variation_study_variable_number integer,
    abundance_variation_study_variable double precision,
    "mzTab_ID_REFS" text
);


ALTER TABLE public."MzTab_M_small_molecule_section" OWNER TO postgres;

--
-- TOC entry 238 (class 1259 OID 18399)
-- Name: MzTab_M_small_molecule_section_SML_ID_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."MzTab_M_small_molecule_section_SML_ID_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."MzTab_M_small_molecule_section_SML_ID_seq" OWNER TO postgres;

--
-- TOC entry 3458 (class 0 OID 0)
-- Dependencies: 238
-- Name: MzTab_M_small_molecule_section_SML_ID_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."MzTab_M_small_molecule_section_SML_ID_seq" OWNED BY public."MzTab_M_small_molecule_section"."SML_ID";


--
-- TOC entry 228 (class 1259 OID 18318)
-- Name: MzTab_Metadata_Proteomics; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."MzTab_Metadata_Proteomics" (
    "mzTab_version" text NOT NULL,
    "mzTab_mode" text NOT NULL,
    "mzTab_type" text NOT NULL,
    "mzTab_ID" text NOT NULL,
    title text,
    description text,
    sample_processing_number integer,
    sample_processing text,
    instrument_number integer,
    instrument text,
    "instrument_name" text,
    "instrument_source" text,
    analyzer_number integer,
    "instrument_analyzer" text,
    "instrument_detector" text,
    software_number integer NOT NULL,
    software text NOT NULL,
    setting_number integer,
    "software_setting" text,
    protein_search_engine_score_number integer,
    protein_search_engine_score double precision,
    peptide_search_engine_score_number integer,
    peptide_search_engine_score double precision,
    psm_search_engine_score_number integer,
    psm_search_engine_score double precision,
    smallmolecule_search_engine_score_number integer,
    smallmolecule_search_engine_score double precision,
    false_discovery_rate text[],
    publication_number integer,
    publication text,
    contact_number integer,
    "contact_name" text,
    "contact_affiliation" text,
    "contact_email" text,
    uri_number integer,
    uri text,
    fixed_mod_number integer,
    fixed_mod text,
    "fixed_mod_site" text,
    "fixed_mod_position" text,
    variable_mod_number integer,
    variable_mod text,
    "variable_mod_site" text,
    "variable_mod_position" text,
    quantification_method text NOT NULL,
    "protein_quantification_unit" text,
    "peptide_quantification_unit" text,
    "small_molecule_quantification_unit" text,
    ms_run_number integer NOT NULL,
    "ms_run_format" text,
    "ms_run_location" text NOT NULL,
    "ms_run_id_format" text,
    fragmentation_method_number integer NOT NULL,
    "ms_run_fragmentation_method" text NOT NULL,
    "ms_run_hash" text,
    "ms_run_hash_method" text,
    custom_number integer,
    custom text,
    sample_number integer,
    species_number integer,
    "sample_species" text,
    tissue_number integer,
    "sample_tissue" text,
    cell_type_number integer,
    "sample_cell_type" text,
    disease_number integer,
    "sample_disease" text,
    "sample_description" text,
    "sample_custom" text,
    assay_number integer NOT NULL,
    "assay_quantification_reagent" text,
    quantification_mod_number integer,
    "assay_quantification_mod" text,
    "assay_quantification_mod_site" text,
    "assay_quantification_mod_position" text,
    "assay_sample_ref " text,
    "assay_ms_run_ref" text,
    study_variable_number integer NOT NULL,
    "study_variable_assay_refs" text NOT NULL,
    "study_variable_sample_refs" text NOT NULL,
    "study_variable_description" text NOT NULL,
    cv_number integer NOT NULL,
    "cv_label" text NOT NULL,
    "cv_full_name" text NOT NULL,
    "cv_version" text NOT NULL,
    "cv_url" text NOT NULL,
    "colunit_protein" text,
    "colunit_peptide" text,
    "colunit_psm" text,
    "colunit_small_molecule" text,
    id integer NOT NULL
);


ALTER TABLE public."MzTab_Metadata_Proteomics" OWNER TO postgres;

--
-- TOC entry 227 (class 1259 OID 18316)
-- Name: MzTab_Metadata_Proteomics_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."MzTab_Metadata_Proteomics_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."MzTab_Metadata_Proteomics_id_seq" OWNER TO postgres;

--
-- TOC entry 3459 (class 0 OID 0)
-- Dependencies: 227
-- Name: MzTab_Metadata_Proteomics_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."MzTab_Metadata_Proteomics_id_seq" OWNED BY public."MzTab_Metadata_Proteomics".id;


--
-- TOC entry 230 (class 1259 OID 18329)
-- Name: MzTab_PSM_section; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."MzTab_PSM_section" (
    id integer NOT NULL,
    sequence text NOT NULL,
    "PSM_ID" integer NOT NULL,
    accession text NOT NULL,
    "unique" boolean NOT NULL,
    database text NOT NULL,
    database_version text NOT NULL,
    search_engine_number integer NOT NULL,
    search_engine text NOT NULL,
    search_engine_score_number integer NOT NULL,
    search_engine_score double precision NOT NULL,
    reliability integer NOT NULL,
    modifications text NOT NULL,
    retention_time double precision[] NOT NULL,
    charge integer NOT NULL,
    exp_mass_to_charge double precision NOT NULL,
    calc_mass_to_charge double precision NOT NULL,
    uri text NOT NULL,
    spectra_ref text NOT NULL,
    pre text NOT NULL,
    post text NOT NULL,
    start integer NOT NULL,
    "end" integer NOT NULL
);


ALTER TABLE public."MzTab_PSM_section" OWNER TO postgres;

--
-- TOC entry 229 (class 1259 OID 18327)
-- Name: MzTab_PSM section_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."MzTab_PSM section_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."MzTab_PSM section_id_seq" OWNER TO postgres;

--
-- TOC entry 3460 (class 0 OID 0)
-- Dependencies: 229
-- Name: MzTab_PSM section_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."MzTab_PSM section_id_seq" OWNED BY public."MzTab_PSM_section".id;


--
-- TOC entry 234 (class 1259 OID 18351)
-- Name: MzTab_Peptide_section; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."MzTab_Peptide_section" (
    id integer NOT NULL,
    sequence text NOT NULL,
    accession text NOT NULL,
    "unique" boolean NOT NULL,
    database text NOT NULL,
    database_version text NOT NULL,
    search_engine_number integer NOT NULL,
    search_engine text NOT NULL,
    best_search_engine_score_number integer NOT NULL,
    best_search_engine_score double precision NOT NULL,
    search_engine_score_number integer NOT NULL,
    search_engine_score double precision NOT NULL,
    ms_run integer NOT NULL,
    search_engine_score_ms_run double precision NOT NULL,
    reliability integer NOT NULL,
    modifications text NOT NULL,
    retention_time double precision[] NOT NULL,
    retention_time_window double precision[] NOT NULL,
    charge integer NOT NULL,
    mass_to_charge double precision NOT NULL,
    uri text NOT NULL,
    spectra_ref text NOT NULL,
    peptide_abundance_assay_number integer NOT NULL,
    peptide_abundance_assay double precision NOT NULL,
    peptide_abundance_study_variable_number integer NOT NULL,
    peptide_abundance_study_variable double precision NOT NULL,
    peptide_abundance_stdev_study_variable_number integer NOT NULL,
    peptide_abundance_stdev_study_variable double precision NOT NULL,
    peptide_abundance_std_error_study_variable_number integer NOT NULL,
    peptide_abundance_std_error_study_variable double precision NOT NULL
);


ALTER TABLE public."MzTab_Peptide_section" OWNER TO postgres;

--
-- TOC entry 233 (class 1259 OID 18349)
-- Name: MzTab_Peptide section_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."MzTab_Peptide section_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."MzTab_Peptide section_id_seq" OWNER TO postgres;

--
-- TOC entry 3461 (class 0 OID 0)
-- Dependencies: 233
-- Name: MzTab_Peptide section_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."MzTab_Peptide section_id_seq" OWNED BY public."MzTab_Peptide_section".id;


--
-- TOC entry 232 (class 1259 OID 18340)
-- Name: MzTab_Protein_section; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."MzTab_Protein_section" (
    id integer NOT NULL,
    accession text NOT NULL,
    description text NOT NULL,
    taxid integer NOT NULL,
    species text NOT NULL,
    database text NOT NULL,
    database_version text NOT NULL,
    search_engine_number integer NOT NULL,
    search_engine text NOT NULL,
    best_search_engine_score_number integer NOT NULL,
    best_search_engine_score double precision NOT NULL,
    search_engine_score_number integer NOT NULL,
    search_engine_score double precision NOT NULL,
    ms_run integer NOT NULL,
    reliability integer NOT NULL,
    num_psms_ms_run integer NOT NULL,
    num_peptides_distinct_ms_run integer NOT NULL,
    num_peptides_unique_ms_run integer NOT NULL,
    ambiguity_members text[] NOT NULL,
    modifications text NOT NULL,
    uri text NOT NULL,
    go_terms text[] NOT NULL,
    protein_coverage double precision NOT NULL,
    protein_abundance_assay_number integer NOT NULL,
    protein_abundance_assay double precision NOT NULL,
    protein_abundance_study_variable_number integer NOT NULL,
    protein_abundance_study_variable double precision NOT NULL,
    protein_abundance_stdev_study_variable_number integer NOT NULL,
    protein_abundance_stdev_study_variable double precision NOT NULL,
    protein_abundance_std_error_study_variable_number integer NOT NULL,
    protein_abundance_std_error_study_variable double precision NOT NULL,
    "mzTab_ID_REFS" text NOT NULL
);


ALTER TABLE public."MzTab_Protein_section" OWNER TO postgres;

--
-- TOC entry 231 (class 1259 OID 18338)
-- Name: MzTab_Protein section_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."MzTab_Protein section_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."MzTab_Protein section_id_seq" OWNER TO postgres;

--
-- TOC entry 3462 (class 0 OID 0)
-- Dependencies: 231
-- Name: MzTab_Protein section_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."MzTab_Protein section_id_seq" OWNED BY public."MzTab_Protein_section".id;


--
-- TOC entry 209 (class 1259 OID 17506)
-- Name: ONTOLOGY_SOURCE_REFERENCE; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."ONTOLOGY_SOURCE_REFERENCE" (
    "Ontology_Source_REF_ID" integer NOT NULL,
    "Term_Source_Name" text NOT NULL,
    "Term_Source_File" text NOT NULL,
    "Term_Source_Version" text NOT NULL,
    "Term_Source_Description" text NOT NULL,
    "Ontology_REF_Investigation_Identifier" text NOT NULL
);


ALTER TABLE public."ONTOLOGY_SOURCE_REFERENCE" OWNER TO postgres;

--
-- TOC entry 208 (class 1259 OID 17504)
-- Name: ONTOLOGY_SOURCE_REFERENCE_Ontology_Source_REF_ID_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."ONTOLOGY_SOURCE_REFERENCE_Ontology_Source_REF_ID_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."ONTOLOGY_SOURCE_REFERENCE_Ontology_Source_REF_ID_seq" OWNER TO postgres;

--
-- TOC entry 3463 (class 0 OID 0)
-- Dependencies: 208
-- Name: ONTOLOGY_SOURCE_REFERENCE_Ontology_Source_REF_ID_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."ONTOLOGY_SOURCE_REFERENCE_Ontology_Source_REF_ID_seq" OWNED BY public."ONTOLOGY_SOURCE_REFERENCE"."Ontology_Source_REF_ID";


--
-- TOC entry 244 (class 1259 OID 18465)
-- Name: PQP_compound; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."PQP_compound" (
    id integer NOT NULL,
    "COMPOUND_ID" integer NOT NULL,
    "COMPOUND_NAME" text,
    "SUM_FORMULA" text,
    "SMILES" text,
    "ADDUCTS" text,
    "DECOY" integer
);


ALTER TABLE public."PQP_compound" OWNER TO postgres;

--
-- TOC entry 243 (class 1259 OID 18463)
-- Name: PQP_compound_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."PQP_compound_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."PQP_compound_id_seq" OWNER TO postgres;

--
-- TOC entry 3464 (class 0 OID 0)
-- Dependencies: 243
-- Name: PQP_compound_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."PQP_compound_id_seq" OWNED BY public."PQP_compound".id;


--
-- TOC entry 246 (class 1259 OID 18476)
-- Name: PQP_gene; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."PQP_gene" (
    id integer NOT NULL,
    "GENE_ID" integer NOT NULL,
    "GENE_NAME" text,
    "DECOY" integer
);


ALTER TABLE public."PQP_gene" OWNER TO postgres;

--
-- TOC entry 245 (class 1259 OID 18474)
-- Name: PQP_gene_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."PQP_gene_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."PQP_gene_id_seq" OWNER TO postgres;

--
-- TOC entry 3465 (class 0 OID 0)
-- Dependencies: 245
-- Name: PQP_gene_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."PQP_gene_id_seq" OWNED BY public."PQP_gene".id;


--
-- TOC entry 248 (class 1259 OID 18488)
-- Name: PQP_peptide; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."PQP_peptide" (
    id integer NOT NULL,
    "PEPTIDE_ID" integer NOT NULL,
    "UNMODIFIED_SEQUENCE" text,
    "MODIFIED_SEQUENCE" text,
    "DECOY" integer
);


ALTER TABLE public."PQP_peptide" OWNER TO postgres;

--
-- TOC entry 247 (class 1259 OID 18486)
-- Name: PQP_peptide_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."PQP_peptide_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."PQP_peptide_id_seq" OWNER TO postgres;

--
-- TOC entry 3466 (class 0 OID 0)
-- Dependencies: 247
-- Name: PQP_peptide_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."PQP_peptide_id_seq" OWNED BY public."PQP_peptide".id;


--
-- TOC entry 250 (class 1259 OID 18499)
-- Name: PQP_protein; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."PQP_protein" (
    id integer NOT NULL,
    "PROTEIN_ID" integer NOT NULL,
    "PROTEIN_ACCESSION" text,
    "DECOY" integer
);


ALTER TABLE public."PQP_protein" OWNER TO postgres;

--
-- TOC entry 249 (class 1259 OID 18497)
-- Name: PQP_protein_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."PQP_protein_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."PQP_protein_id_seq" OWNER TO postgres;

--
-- TOC entry 3467 (class 0 OID 0)
-- Dependencies: 249
-- Name: PQP_protein_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."PQP_protein_id_seq" OWNED BY public."PQP_protein".id;


--
-- TOC entry 211 (class 1259 OID 17517)
-- Name: PROTOCOLS; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."PROTOCOLS" (
    "Protocol_ID" integer NOT NULL,
    "Protocol_Name" text,
    "Protocol_Type" text,
    "Protocol_Type_Term_Accession_Number" text,
    "Protocol_Type_Term_Source_REF" text,
    "Protocol_Description" text,
    "Protocol_URI" text,
    "Protocol_Version" text,
    "Protocol_Parameters_Name" text,
    "Protocol_Parameter_Name_Term_Accession_Number" text,
    "Protocol_Parameter_Name_Term_Source_REF" text,
    "Protocol_Components_Name" text,
    "Protocol_Components_Type" text,
    "Protocol_Components_Type_Term_Accession_Number" text,
    "Protocol_Components_Type_Term_Source_REF" text
);


ALTER TABLE public."PROTOCOLS" OWNER TO postgres;

--
-- TOC entry 210 (class 1259 OID 17515)
-- Name: PROTOCOLS_Protocol_ID_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."PROTOCOLS_Protocol_ID_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."PROTOCOLS_Protocol_ID_seq" OWNER TO postgres;

--
-- TOC entry 3468 (class 0 OID 0)
-- Dependencies: 210
-- Name: PROTOCOLS_Protocol_ID_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."PROTOCOLS_Protocol_ID_seq" OWNED BY public."PROTOCOLS"."Protocol_ID";


--
-- TOC entry 213 (class 1259 OID 17528)
-- Name: PUBLICATIONS; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."PUBLICATIONS" (
    "Publication_ID" integer NOT NULL,
    "PubMed_ID" text,
    "Publication_DOI" text,
    "Publication_Author_List" text,
    "Publication_Title" text,
    "Publication_Status" text,
    "Publication_Status_Term_Accession_Number" text,
    "Publication_Status_Term_Source_REF" text
);


ALTER TABLE public."PUBLICATIONS" OWNER TO postgres;

--
-- TOC entry 212 (class 1259 OID 17526)
-- Name: PUBLICATIONS_Publication_ID_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."PUBLICATIONS_Publication_ID_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."PUBLICATIONS_Publication_ID_seq" OWNER TO postgres;

--
-- TOC entry 3469 (class 0 OID 0)
-- Dependencies: 212
-- Name: PUBLICATIONS_Publication_ID_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."PUBLICATIONS_Publication_ID_seq" OWNED BY public."PUBLICATIONS"."Publication_ID";


--
-- TOC entry 254 (class 1259 OID 18521)
-- Name: SOPs; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."SOPs" (
    sop_title text NOT NULL,
    sop_authors text NOT NULL,
    sop_version text NOT NULL,
    sop_description text NOT NULL,
    sop_purpose text NOT NULL,
    sop_history_of_changes text NOT NULL,
    sop_scope text NOT NULL,
    sop_safety text NOT NULL,
    sop_equipment_and_labware text NOT NULL,
    sop_reagents text NOT NULL,
    sop_procedure text NOT NULL,
    sop_referencs text NOT NULL,
    sop_appendix text NOT NULL,
    sop_timeline text NOT NULL,
    sop_deviations_from_procedure text NOT NULL,
    "sop_ID" integer NOT NULL
);


ALTER TABLE public."SOPs" OWNER TO postgres;

--
-- TOC entry 253 (class 1259 OID 18519)
-- Name: SOPs_sop_ID_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."SOPs_sop_ID_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."SOPs_sop_ID_seq" OWNER TO postgres;

--
-- TOC entry 3470 (class 0 OID 0)
-- Dependencies: 253
-- Name: SOPs_sop_ID_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."SOPs_sop_ID_seq" OWNED BY public."SOPs"."sop_ID";


--
-- TOC entry 215 (class 1259 OID 17540)
-- Name: STUDY; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."STUDY" (
    "Study_ID" integer NOT NULL,
    "Study_Identifier" text NOT NULL,
    "Study_Title" text,
    "Study_Description" text,
    "Study_Submission_Date" date,
    "Study_Public_Release_Date" date,
    "Study_File_Name" text,
    "Study_Assays" integer,
    "Study_Contact" integer,
    "Study_Design_Descriptors" integer,
    "Study_Factors" integer,
    "Study_Protocols" integer,
    "Study_Publications" integer
);


ALTER TABLE public."STUDY" OWNER TO postgres;

--
-- TOC entry 217 (class 1259 OID 17551)
-- Name: STUDY_DESIGN_DESCRIPTORS; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."STUDY_DESIGN_DESCRIPTORS" (
    "Design_Descriptors_ID" integer NOT NULL,
    "Design_Type" text,
    "Design_Type_Term_Accession_Number" text,
    "Design_Type_Term_Source_REF" text
);


ALTER TABLE public."STUDY_DESIGN_DESCRIPTORS" OWNER TO postgres;

--
-- TOC entry 216 (class 1259 OID 17549)
-- Name: STUDY_DESIGN_DESCRIPTORS_Design_Descriptors_ID_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."STUDY_DESIGN_DESCRIPTORS_Design_Descriptors_ID_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."STUDY_DESIGN_DESCRIPTORS_Design_Descriptors_ID_seq" OWNER TO postgres;

--
-- TOC entry 3471 (class 0 OID 0)
-- Dependencies: 216
-- Name: STUDY_DESIGN_DESCRIPTORS_Design_Descriptors_ID_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."STUDY_DESIGN_DESCRIPTORS_Design_Descriptors_ID_seq" OWNED BY public."STUDY_DESIGN_DESCRIPTORS"."Design_Descriptors_ID";


--
-- TOC entry 219 (class 1259 OID 17562)
-- Name: STUDY_FACTORS; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."STUDY_FACTORS" (
    "Study_Factors_ID" integer NOT NULL,
    "Factor_Name" text,
    "Factor_Type" text,
    "Factor_Type_Term_Accession_Number" text,
    "Factor_Type_Term_Source_REF" text
);


ALTER TABLE public."STUDY_FACTORS" OWNER TO postgres;

--
-- TOC entry 218 (class 1259 OID 17560)
-- Name: STUDY_FACTORS_Study_Factors_ID_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."STUDY_FACTORS_Study_Factors_ID_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."STUDY_FACTORS_Study_Factors_ID_seq" OWNER TO postgres;

--
-- TOC entry 3472 (class 0 OID 0)
-- Dependencies: 218
-- Name: STUDY_FACTORS_Study_Factors_ID_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."STUDY_FACTORS_Study_Factors_ID_seq" OWNED BY public."STUDY_FACTORS"."Study_Factors_ID";


--
-- TOC entry 220 (class 1259 OID 17571)
-- Name: STUDY_SAMPLES; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."STUDY_SAMPLES" (
    "Study_ID" integer NOT NULL,
    "Sample_Name" text NOT NULL,
    "Characteristics" text,
    "Material_Type" text,
    "Protocol_REF" text,
    "Term_Accession_Number" text,
    "Term_Source_REF" text,
    "Comment" text,
    "Provider" text,
    "Description" text
);


ALTER TABLE public."STUDY_SAMPLES" OWNER TO postgres;

--
-- TOC entry 214 (class 1259 OID 17538)
-- Name: STUDY_Study_ID_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."STUDY_Study_ID_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."STUDY_Study_ID_seq" OWNER TO postgres;

--
-- TOC entry 3473 (class 0 OID 0)
-- Dependencies: 214
-- Name: STUDY_Study_ID_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."STUDY_Study_ID_seq" OWNED BY public."STUDY"."Study_ID";


--
-- TOC entry 255 (class 1259 OID 18530)
-- Name: TraML; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."TraML" (
    "GeneName" text,
    "ProteinName" text,
    "PeptideSequence" text,
    "FullPeptideName" text,
    transition_group_id text,
    transition_name text,
    "Annotation" text,
    "PrecursorMz" double precision,
    "MS1_Res" text,
    "ProductMz" double precision,
    "MS2_Res" text,
    "Dwell" integer,
    "Fragmentor" integer,
    "CollisionEnergy" double precision,
    "CellAcceleratorVoltage" integer,
    "LibraryIntensity" double precision,
    decoy integer,
    "LabelType" text,
    "PrecursorCharge" integer,
    "FragmentCharge" integer,
    "FragmentType" text,
    "FragmentSeriesNumber" integer,
    quantifying_transition integer,
    identifying_transition integer,
    detecting_transition integer,
    "Tr_recalibrated" double precision,
    "RetentionTime" double precision,
    "PeptideGroupLabel" text,
    "UniprotId" text,
    "CompoundName" text,
    "SMILES" text,
    "SumFormula" text,
    "mzTab_ID" text NOT NULL,
    id integer NOT NULL
);


ALTER TABLE public."TraML" OWNER TO postgres;

--
-- TOC entry 256 (class 1259 OID 18536)
-- Name: TraML_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."TraML_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."TraML_id_seq" OWNER TO postgres;

--
-- TOC entry 3474 (class 0 OID 0)
-- Dependencies: 256
-- Name: TraML_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."TraML_id_seq" OWNED BY public."TraML".id;


--
-- TOC entry 264 (class 1259 OID 18582)
-- Name: atomMappingMetabolites; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."atomMappingMetabolites" (
    id integer NOT NULL,
    mapping_id text,
    met_id text,
    met_elements text[],
    met_atompositions integer[],
    met_symmetry_elements text[],
    met_symmetry_atompositions integer[],
    used boolean,
    comment text,
    met_mapping json,
    base_met_ids text[],
    base_met_elements json,
    base_met_atompositions json,
    base_met_symmetry_elements json,
    base_met_symmetry_atompositions json,
    base_met_indices integer[]
);


ALTER TABLE public."atomMappingMetabolites" OWNER TO postgres;

--
-- Name: atomMappingMetabolites_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."atomMappingMetabolites_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."atomMappingMetabolites_id_seq" OWNER TO postgres;

--
-- Name: atomMappingMetabolites_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."atomMappingMetabolites_id_seq" OWNED BY public."atomMappingMetabolites".id;


--
-- Name: atomMappingMetabolites id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."atomMappingMetabolites" ALTER COLUMN id SET DEFAULT nextval('public."atomMappingMetabolites_id_seq"'::regclass);


--
-- Name: atomMappingMetabolites atomMappingMetabolites_mapping_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."atomMappingMetabolites"
    ADD CONSTRAINT "atomMappingMetabolites_mapping_id_key" UNIQUE (mapping_id);


--
-- Name: atomMappingMetabolites atomMappingMetabolites_met_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."atomMappingMetabolites"
    ADD CONSTRAINT "atomMappingMetabolites_met_id_key" UNIQUE (met_id);


--
-- Name: atomMappingMetabolites atomMappingMetabolites_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."atomMappingMetabolites"
    ADD CONSTRAINT "atomMappingMetabolites_pkey" PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--



--
-- TOC entry 266 (class 1259 OID 18594)
-- Name: atomMappingReactions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."atomMappingReactions" (
    id integer NOT NULL,
    mapping_id text NOT NULL,
    rxn_id text,
    rxn_description text,
    reactants_stoichiometry_tracked double precision[],
    products_stoichiometry_tracked double precision[],
    reactants_ids_tracked text[],
    products_id_tracked text[],
    reactants_mapping text[],
    products_mapping text[],
    rxn_equation text,
    used boolean,
    comment text,
    reactants_elements_tracked json,
    products_elements_tracked json,
    reactants_positions_tracked json,
    products_positions_tracked json
);


ALTER TABLE public."atomMappingReactions" OWNER TO postgres;

--
-- Name: atomMappingReactions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."atomMappingReactions_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."atomMappingReactions_id_seq" OWNER TO postgres;

--
-- Name: atomMappingReactions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."atomMappingReactions_id_seq" OWNED BY public."atomMappingReactions".id;


--
-- Name: atomMappingReactions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."atomMappingReactions" ALTER COLUMN id SET DEFAULT nextval('public."atomMappingReactions_id_seq"'::regclass);


--
-- Name: atomMappingReactions atomMappingReactions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."atomMappingReactions"
    ADD CONSTRAINT "atomMappingReactions_pkey" PRIMARY KEY (id);


--
-- Name: atomMappingReactions atomMappingReactions_mapping_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."atomMappingReactions"
    ADD CONSTRAINT "atomMappingReactions_mapping_id_fkey" FOREIGN KEY (mapping_id) REFERENCES public."atomMappingMetabolites"(mapping_id) NOT VALID;


--
-- PostgreSQL database dump complete
--


--
-- TOC entry 268 (class 1259 OID 18605)
-- Name: calcFluxes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."calcFluxes" (
    id integer NOT NULL,
    experiment_id text NOT NULL,
    model_id text NOT NULL,
    mapping_id text NOT NULL,
    sample_name_abbreviation text NOT NULL,
    time_point text NOT NULL,
    rxn_id text NOT NULL,
    flux_average double precision,
    flux_stdev double precision,
    flux_lb double precision,
    flux_ub double precision,
    flux_units text,
    used boolean,
    comment text
);


ALTER TABLE public."calcFluxes" OWNER TO postgres;

--
-- Name: calcFluxes_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."calcFluxes_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."calcFluxes_id_seq" OWNER TO postgres;

--
-- Name: calcFluxes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."calcFluxes_id_seq" OWNED BY public."calcFluxes".id;


--
-- Name: calcFluxes id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."calcFluxes" ALTER COLUMN id SET DEFAULT nextval('public."calcFluxes_id_seq"'::regclass);


--
-- Name: calcFluxes calcFluxes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."calcFluxes"
    ADD CONSTRAINT "calcFluxes_pkey" PRIMARY KEY (id);


--
-- Name: calcFluxes calcFluxes_mapping_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."calcFluxes"
    ADD CONSTRAINT "calcFluxes_mapping_id_fkey" FOREIGN KEY (mapping_id) REFERENCES public."atomMappingMetabolites"(mapping_id) NOT VALID;


--
-- Name: calcFluxes calcFluxes_rxn_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."calcFluxes"
    ADD CONSTRAINT "calcFluxes_rxn_id_fkey" FOREIGN KEY (rxn_id) REFERENCES public."fittedFluxes"(rxn_id) NOT VALID;


--
-- PostgreSQL database dump complete
--




--
-- TOC entry 270 (class 1259 OID 18616)
-- Name: calcFragments; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."calcFragments" (
    id integer NOT NULL,
    experiment_id text,
    model_id text,
    mapping_id text,
    sample_name_abbreviation text,
    time_point text,
    met_id text,
    fragment_name text,
    fragment_formula text,
    idv_average double precision,
    idv_stdev double precision,
    idv_units text,
    used boolean,
    comment text
);


ALTER TABLE public."calcFragments" OWNER TO postgres;

--
-- Name: calcFragments_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."calcFragments_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."calcFragments_id_seq" OWNER TO postgres;

--
-- Name: calcFragments_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."calcFragments_id_seq" OWNED BY public."calcFragments".id;


--
-- Name: calcFragments id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."calcFragments" ALTER COLUMN id SET DEFAULT nextval('public."calcFragments_id_seq"'::regclass);


--
-- Name: calcFragments calcFragments_experiment_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."calcFragments"
    ADD CONSTRAINT "calcFragments_experiment_id_key" UNIQUE (experiment_id);


--
-- Name: calcFragments calcFragments_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."calcFragments"
    ADD CONSTRAINT "calcFragments_pkey" PRIMARY KEY (id);


--
-- Name: calcFragments calcFragments_mapping_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."calcFragments"
    ADD CONSTRAINT "calcFragments_mapping_id_fkey" FOREIGN KEY (mapping_id) REFERENCES public."atomMappingMetabolites"(mapping_id) NOT VALID;


--
-- PostgreSQL database dump complete
--

--
-- TOC entry 272 (class 1259 OID 18627)
-- Name: fittedData; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."fittedData" (
    id integer NOT NULL,
    simulation_id text,
    "simulation_dateAndTime" timestamp(6) with time zone[],
    fitted_echi2 double precision[],
    fitted_alf double precision,
    fitted_chi2 double precision,
    fitted_dof integer,
    used boolean,
    comment text,
    original_filename text
);


ALTER TABLE public."fittedData" OWNER TO postgres;

--
-- Name: fittedData_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."fittedData_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."fittedData_id_seq" OWNER TO postgres;

--
-- Name: fittedData_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."fittedData_id_seq" OWNED BY public."fittedData".id;


--
-- Name: fittedData id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."fittedData" ALTER COLUMN id SET DEFAULT nextval('public."fittedData_id_seq"'::regclass);


--
-- Name: fittedData fittedData_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."fittedData"
    ADD CONSTRAINT "fittedData_pkey" PRIMARY KEY (id);


--
-- Name: fittedData fittedData_simulation_id_simulation_dateAndTime_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."fittedData"
    ADD CONSTRAINT "fittedData_simulation_id_simulation_dateAndTime_key" UNIQUE (simulation_id, "simulation_dateAndTime");


--
-- Name: fittedData fittedData_simulation_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."fittedData"
    ADD CONSTRAINT "fittedData_simulation_id_fkey" FOREIGN KEY (simulation_id) REFERENCES public.simulation(simulation_id) NOT VALID;


--
-- PostgreSQL database dump complete
--




--
-- TOC entry 274 (class 1259 OID 18640)
-- Name: fittedExchangeFluxStatistics; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."fittedExchangeFluxStatistics" (
    id integer NOT NULL,
    simulation_id text,
    "simulation_dateAndTime" timestamp(6) without time zone,
    n_fluxes integer,
    "n_observableFluxes" integer,
    total_precision double precision,
    "total_observablePrecision" double precision,
    "relative_nObservableFluxes" double precision,
    "average_observableFluxPrecision" double precision,
    "average_fluxPrecision" double precision,
    flux_units text,
    used boolean,
    comment text
);


ALTER TABLE public."fittedExchangeFluxStatistics" OWNER TO postgres;

--
-- Name: fittedExchangeFluxStatistics_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."fittedExchangeFluxStatistics_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."fittedExchangeFluxStatistics_id_seq" OWNER TO postgres;

--
-- Name: fittedExchangeFluxStatistics_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."fittedExchangeFluxStatistics_id_seq" OWNED BY public."fittedExchangeFluxStatistics".id;


--
-- Name: fittedExchangeFluxStatistics id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."fittedExchangeFluxStatistics" ALTER COLUMN id SET DEFAULT nextval('public."fittedExchangeFluxStatistics_id_seq"'::regclass);


--
-- Name: fittedExchangeFluxStatistics fittedExchangeFluxStatistics_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."fittedExchangeFluxStatistics"
    ADD CONSTRAINT "fittedExchangeFluxStatistics_pkey" PRIMARY KEY (id);


--
-- Name: fittedExchangeFluxStatistics fittedExchangeFluxStatistics_simulation_id_simulation_dateA_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."fittedExchangeFluxStatistics"
    ADD CONSTRAINT "fittedExchangeFluxStatistics_simulation_id_simulation_dateA_key" UNIQUE (simulation_id, "simulation_dateAndTime", flux_units);


--
-- Name: fittedExchangeFluxStatistics fittedExchangeFluxStatistics_simulation_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."fittedExchangeFluxStatistics"
    ADD CONSTRAINT "fittedExchangeFluxStatistics_simulation_id_fkey" FOREIGN KEY (simulation_id) REFERENCES public.simulation(simulation_id) NOT VALID;


--
-- PostgreSQL database dump complete
--



--
-- TOC entry 276 (class 1259 OID 18653)
-- Name: fittedExchangeFluxes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."fittedExchangeFluxes" (
    id integer NOT NULL,
    simulation_id text,
    "simulation_dateAndTime" timestamp(6) without time zone,
    rxn_id text,
    flux_exchange double precision,
    flux_exchange_stdev double precision,
    flux_exchange_lb double precision,
    flux_exchange_ub double precision,
    flux_exchange_units text,
    flux_exchange_normalized double precision,
    flux_exchange_normalized_stdev double precision,
    flux_exchange_normalized_lb double precision,
    flux_exchange_normalized_ub double precision,
    flux_exchange_normalized_units text,
    used boolean,
    comment text
);


ALTER TABLE public."fittedExchangeFluxes" OWNER TO postgres;

--
-- Name: fittedExchangeFluxes_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."fittedExchangeFluxes_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."fittedExchangeFluxes_id_seq" OWNER TO postgres;

--
-- Name: fittedExchangeFluxes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."fittedExchangeFluxes_id_seq" OWNED BY public."fittedExchangeFluxes".id;


--
-- Name: fittedExchangeFluxes id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."fittedExchangeFluxes" ALTER COLUMN id SET DEFAULT nextval('public."fittedExchangeFluxes_id_seq"'::regclass);


--
-- Name: fittedExchangeFluxes fittedExchangeFluxes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."fittedExchangeFluxes"
    ADD CONSTRAINT "fittedExchangeFluxes_pkey" PRIMARY KEY (id);


--
-- Name: fittedExchangeFluxes fittedExchangeFluxes_simulation_id_simulation_dateAndTime_r_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."fittedExchangeFluxes"
    ADD CONSTRAINT "fittedExchangeFluxes_simulation_id_simulation_dateAndTime_r_key" UNIQUE (simulation_id, "simulation_dateAndTime", rxn_id, flux_exchange_units);


--
-- Name: fittedExchangeFluxes fittedExchangeFluxes_simulation_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."fittedExchangeFluxes"
    ADD CONSTRAINT "fittedExchangeFluxes_simulation_id_fkey" FOREIGN KEY (simulation_id) REFERENCES public.simulation(simulation_id) NOT VALID;


--
-- PostgreSQL database dump complete
--




--
-- TOC entry 278 (class 1259 OID 18666)
-- Name: fittedFluxStatistics; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."fittedFluxStatistics" (
    id integer NOT NULL,
    simulation_id text,
    "simulation_dateAndtime" timestamp(6) without time zone,
    n_fluxes integer,
    "n_observableFluxes" integer,
    total_precision double precision,
    "total_observablePrecision" double precision,
    "relative_nObservableFluxes" double precision,
    "average_observableFluxPrecision" double precision,
    "average_fluxPrecision" double precision,
    flux_units text,
    used boolean,
    comment text
);


ALTER TABLE public."fittedFluxStatistics" OWNER TO postgres;

--
-- Name: fittedFluxStatistics_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."fittedFluxStatistics_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."fittedFluxStatistics_id_seq" OWNER TO postgres;

--
-- Name: fittedFluxStatistics_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."fittedFluxStatistics_id_seq" OWNED BY public."fittedFluxStatistics".id;


--
-- Name: fittedFluxStatistics id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."fittedFluxStatistics" ALTER COLUMN id SET DEFAULT nextval('public."fittedFluxStatistics_id_seq"'::regclass);


--
-- Name: fittedFluxStatistics fittedFluxStatistics_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."fittedFluxStatistics"
    ADD CONSTRAINT "fittedFluxStatistics_pkey" PRIMARY KEY (id);


--
-- Name: fittedFluxStatistics fittedFluxStatistics_simulation_id_simulation_dateAndtime_f_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."fittedFluxStatistics"
    ADD CONSTRAINT "fittedFluxStatistics_simulation_id_simulation_dateAndtime_f_key" UNIQUE (simulation_id, "simulation_dateAndtime", flux_units);


--
-- Name: fittedFluxStatistics fittedFluxStatistics_simulation_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."fittedFluxStatistics"
    ADD CONSTRAINT "fittedFluxStatistics_simulation_id_fkey" FOREIGN KEY (simulation_id) REFERENCES public.simulation(simulation_id) NOT VALID;


--
-- PostgreSQL database dump complete
--


--
-- TOC entry 280 (class 1259 OID 18679)
-- Name: fittedFluxes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."fittedFluxes" (
    id integer NOT NULL,
    simulation_id text,
    "simulation_dateAndTime" timestamp(6) without time zone,
    rxn_id text,
    flux double precision,
    flux_stdev double precision,
    flux_lb double precision,
    flux_ub double precision,
    flux_units text,
    fit_alf double precision,
    fit_chi2s double precision[],
    fit_cor double precision[],
    fit_cov double precision[],
    free boolean,
    used boolean,
    comment text
);


ALTER TABLE public."fittedFluxes" OWNER TO postgres;

--
-- Name: fittedFluxes_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."fittedFluxes_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."fittedFluxes_id_seq" OWNER TO postgres;

--
-- Name: fittedFluxes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."fittedFluxes_id_seq" OWNED BY public."fittedFluxes".id;


--
-- Name: fittedFluxes id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."fittedFluxes" ALTER COLUMN id SET DEFAULT nextval('public."fittedFluxes_id_seq"'::regclass);


--
-- Name: fittedFluxes fittedFluxes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."fittedFluxes"
    ADD CONSTRAINT "fittedFluxes_pkey" PRIMARY KEY (id);


--
-- Name: fittedFluxes fittedFluxes_rxn_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."fittedFluxes"
    ADD CONSTRAINT "fittedFluxes_rxn_id_key" UNIQUE (rxn_id);


--
-- Name: fittedFluxes fittedFluxes_simulation_id_simulation_dateAndTime_rxn_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."fittedFluxes"
    ADD CONSTRAINT "fittedFluxes_simulation_id_simulation_dateAndTime_rxn_id_key" UNIQUE (simulation_id, "simulation_dateAndTime", rxn_id);


--
-- Name: fittedFluxes fittedFluxes_simulation_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."fittedFluxes"
    ADD CONSTRAINT "fittedFluxes_simulation_id_fkey" FOREIGN KEY (simulation_id) REFERENCES public.simulation(simulation_id) NOT VALID;


--
-- PostgreSQL database dump complete
--



--
-- TOC entry 282 (class 1259 OID 18694)
-- Name: fittedFragments; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."fittedFragments" (
    id integer NOT NULL,
    simulation_id text,
    "simulation_dateAndTime" timestamp(6) without time zone,
    experiment_id text,
    sample_name_abbreviation text,
    time_point text,
    fragment_id text,
    fragment_mass integer,
    fit_val double precision,
    fit_stdev double precision,
    fit_units text,
    fit_alf double precision,
    fit_cor double precision[],
    fit_cov double precision[],
    free boolean,
    used boolean,
    comment text
);


ALTER TABLE public."fittedFragments" OWNER TO postgres;

--
-- Name: fittedFragments_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."fittedFragments_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."fittedFragments_id_seq" OWNER TO postgres;

--
-- Name: fittedFragments_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."fittedFragments_id_seq" OWNED BY public."fittedFragments".id;


--
-- Name: fittedFragments id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."fittedFragments" ALTER COLUMN id SET DEFAULT nextval('public."fittedFragments_id_seq"'::regclass);


--
-- Name: fittedFragments fittedFragments_fragment_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."fittedFragments"
    ADD CONSTRAINT "fittedFragments_fragment_id_key" UNIQUE (fragment_id);


--
-- Name: fittedFragments fittedFragments_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."fittedFragments"
    ADD CONSTRAINT "fittedFragments_pkey" PRIMARY KEY (id);


--
-- Name: fittedFragments fittedFragments_simulation_id_simulation_dateAndTime_time_p_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."fittedFragments"
    ADD CONSTRAINT "fittedFragments_simulation_id_simulation_dateAndTime_time_p_key" UNIQUE (simulation_id, "simulation_dateAndTime", time_point, fragment_id, fragment_mass);


--
-- Name: fittedFragments fittedFragments_experiment_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."fittedFragments"
    ADD CONSTRAINT "fittedFragments_experiment_id_fkey" FOREIGN KEY (experiment_id) REFERENCES public."calcFragments"(experiment_id) NOT VALID;


--
-- Name: fittedFragments fittedFragments_simulation_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."fittedFragments"
    ADD CONSTRAINT "fittedFragments_simulation_id_fkey" FOREIGN KEY (simulation_id) REFERENCES public.simulation(simulation_id) NOT VALID;


--
-- PostgreSQL database dump complete
--


--
-- TOC entry 284 (class 1259 OID 18707)
-- Name: fittedMeasuredFluxResiduals; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."fittedMeasuredFluxResiduals" (
    id integer NOT NULL,
    simulation_id text,
    "simulation_dateAndTime" timestamp(6) without time zone,
    experiment_id text,
    sample_name_abbreviation text,
    time_point text,
    rxn_id text,
    res_data double precision,
    res_esens double precision,
    res_fit double precision,
    res_msens double precision,
    res_peak text,
    res_stdev double precision,
    res_val double precision,
    used boolean,
    comment text
);


ALTER TABLE public."fittedMeasuredFluxResiduals" OWNER TO postgres;

--
-- Name: fittedMeasuredFluxResiduals_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."fittedMeasuredFluxResiduals_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."fittedMeasuredFluxResiduals_id_seq" OWNER TO postgres;

--
-- Name: fittedMeasuredFluxResiduals_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."fittedMeasuredFluxResiduals_id_seq" OWNED BY public."fittedMeasuredFluxResiduals".id;


--
-- Name: fittedMeasuredFluxResiduals id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."fittedMeasuredFluxResiduals" ALTER COLUMN id SET DEFAULT nextval('public."fittedMeasuredFluxResiduals_id_seq"'::regclass);


--
-- Name: fittedMeasuredFluxResiduals fittedMeasuredFluxResiduals_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."fittedMeasuredFluxResiduals"
    ADD CONSTRAINT "fittedMeasuredFluxResiduals_pkey" PRIMARY KEY (id);


--
-- Name: fittedMeasuredFluxResiduals s; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."fittedMeasuredFluxResiduals"
    ADD CONSTRAINT s UNIQUE (simulation_id, "simulation_dateAndTime", time_point, rxn_id);


--
-- Name: fittedMeasuredFluxResiduals fittedMeasuredFluxResiduals_simulation_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."fittedMeasuredFluxResiduals"
    ADD CONSTRAINT "fittedMeasuredFluxResiduals_simulation_id_fkey" FOREIGN KEY (simulation_id) REFERENCES public.simulation(simulation_id) NOT VALID;


--
-- PostgreSQL database dump complete
--


--
-- TOC entry 286 (class 1259 OID 18720)
-- Name: fittedMeasuredFluxes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."fittedMeasuredFluxes" (
    id integer NOT NULL,
    simulation_id text,
    "simulation_dateAndTime" timestamp(6) without time zone,
    experiment_id text,
    sample_name_abbreviation text,
    rxn_id text,
    fitted_sres double precision,
    used boolean,
    comment text
);


ALTER TABLE public."fittedMeasuredFluxes" OWNER TO postgres;

--
-- Name: fittedMeasuredFluxes_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."fittedMeasuredFluxes_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."fittedMeasuredFluxes_id_seq" OWNER TO postgres;

--
-- Name: fittedMeasuredFluxes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."fittedMeasuredFluxes_id_seq" OWNED BY public."fittedMeasuredFluxes".id;


--
-- Name: fittedMeasuredFluxes id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."fittedMeasuredFluxes" ALTER COLUMN id SET DEFAULT nextval('public."fittedMeasuredFluxes_id_seq"'::regclass);


--
-- Name: fittedMeasuredFluxes fittedMeasuredFluxes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."fittedMeasuredFluxes"
    ADD CONSTRAINT "fittedMeasuredFluxes_pkey" PRIMARY KEY (id);


--
-- Name: fittedMeasuredFluxes fittedMeasuredFluxes_simulation_id_simulation_dateAndTime_r_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."fittedMeasuredFluxes"
    ADD CONSTRAINT "fittedMeasuredFluxes_simulation_id_simulation_dateAndTime_r_key" UNIQUE (simulation_id, "simulation_dateAndTime", rxn_id);


--
-- Name: fittedMeasuredFluxes fittedMeasuredFluxes_simulation_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."fittedMeasuredFluxes"
    ADD CONSTRAINT "fittedMeasuredFluxes_simulation_id_fkey" FOREIGN KEY (simulation_id) REFERENCES public.simulation(simulation_id) NOT VALID;


--
-- PostgreSQL database dump complete
--

--
-- TOC entry 288 (class 1259 OID 18734)
-- Name: fittedMeasuredFragmentResiduals; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."fittedMeasuredFragmentResiduals" (
    id integer NOT NULL,
    simulation_id text,
    "simulation_dateAndTime" timestamp(6) without time zone,
    experiment_id text,
    sample_name_abbreviation text,
    time_point text,
    fragment_id text,
    fragment_mass integer,
    res_data double precision,
    res_esens double precision,
    res_fit double precision,
    res_msens double precision,
    res_peak text,
    res_stdev double precision,
    res_val double precision,
    used boolean,
    comment text
);


ALTER TABLE public."fittedMeasuredFragmentResiduals" OWNER TO postgres;

--
-- Name: fittedMeasuredFragmentResiduals_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."fittedMeasuredFragmentResiduals_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."fittedMeasuredFragmentResiduals_id_seq" OWNER TO postgres;

--
-- Name: fittedMeasuredFragmentResiduals_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."fittedMeasuredFragmentResiduals_id_seq" OWNED BY public."fittedMeasuredFragmentResiduals".id;


--
-- Name: fittedMeasuredFragmentResiduals id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."fittedMeasuredFragmentResiduals" ALTER COLUMN id SET DEFAULT nextval('public."fittedMeasuredFragmentResiduals_id_seq"'::regclass);


--
-- Name: fittedMeasuredFragmentResiduals fittedMeasuredFragmentResidua_simulation_id_simulation_date_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."fittedMeasuredFragmentResiduals"
    ADD CONSTRAINT "fittedMeasuredFragmentResidua_simulation_id_simulation_date_key" UNIQUE (simulation_id, "simulation_dateAndTime", time_point, fragment_id, fragment_mass);


--
-- Name: fittedMeasuredFragmentResiduals fittedMeasuredFragmentResiduals_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."fittedMeasuredFragmentResiduals"
    ADD CONSTRAINT "fittedMeasuredFragmentResiduals_pkey" PRIMARY KEY (id);


--
-- Name: fittedMeasuredFragmentResiduals fittedMeasuredFragmentResiduals_simulation_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."fittedMeasuredFragmentResiduals"
    ADD CONSTRAINT "fittedMeasuredFragmentResiduals_simulation_id_fkey" FOREIGN KEY (simulation_id) REFERENCES public.simulation(simulation_id) NOT VALID;


--
-- PostgreSQL database dump complete
--




--
-- TOC entry 290 (class 1259 OID 18758)
-- Name: fittedMeasuredFragments; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."fittedMeasuredFragments" (
    id integer NOT NULL,
    simulation_id text,
    "simulation_dateAndTime" timestamp(6) without time zone,
    experiment_id text,
    sample_name_abbreviation text,
    fragment_id text,
    fitted_sres double precision,
    used boolean,
    comment text
);


ALTER TABLE public."fittedMeasuredFragments" OWNER TO postgres;

--
-- Name: fittedMeasuredFragments_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."fittedMeasuredFragments_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."fittedMeasuredFragments_id_seq" OWNER TO postgres;

--
-- Name: fittedMeasuredFragments_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."fittedMeasuredFragments_id_seq" OWNED BY public."fittedMeasuredFragments".id;


--
-- Name: fittedMeasuredFragments id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."fittedMeasuredFragments" ALTER COLUMN id SET DEFAULT nextval('public."fittedMeasuredFragments_id_seq"'::regclass);


--
-- Name: fittedMeasuredFragments fittedMeasuredFragments_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."fittedMeasuredFragments"
    ADD CONSTRAINT "fittedMeasuredFragments_pkey" PRIMARY KEY (id);


--
-- Name: fittedMeasuredFragments fittedMeasuredFragments_simulation_id_simulation_dateAndTim_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."fittedMeasuredFragments"
    ADD CONSTRAINT "fittedMeasuredFragments_simulation_id_simulation_dateAndTim_key" UNIQUE (simulation_id, "simulation_dateAndTime", fragment_id);


--
-- Name: fittedMeasuredFragments fittedMeasuredFragments_simulation_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."fittedMeasuredFragments"
    ADD CONSTRAINT "fittedMeasuredFragments_simulation_id_fkey" FOREIGN KEY (simulation_id) REFERENCES public.simulation(simulation_id) NOT VALID;


--
-- PostgreSQL database dump complete
--




--
-- TOC entry 292 (class 1259 OID 18771)
-- Name: fittedNetFluxStatistics; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."fittedNetFluxStatistics" (
    id integer NOT NULL,
    simulation_id text,
    "simulation_dateAndTime" timestamp(6) without time zone,
    n_fluxes integer,
    "n_observableFluxes" integer,
    total_precision double precision,
    "total_observablePrecision" double precision,
    "relative_nObservableFluxes" double precision,
    "average_observableFluxPrecision" double precision,
    "average_fluxPrecision" double precision,
    flux_units text,
    used boolean,
    comment text
);


ALTER TABLE public."fittedNetFluxStatistics" OWNER TO postgres;

--
-- Name: fittedNetFluxStatistics_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."fittedNetFluxStatistics_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."fittedNetFluxStatistics_id_seq" OWNER TO postgres;

--
-- Name: fittedNetFluxStatistics_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."fittedNetFluxStatistics_id_seq" OWNED BY public."fittedNetFluxStatistics".id;


--
-- Name: fittedNetFluxStatistics id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."fittedNetFluxStatistics" ALTER COLUMN id SET DEFAULT nextval('public."fittedNetFluxStatistics_id_seq"'::regclass);


--
-- Name: fittedNetFluxStatistics fittedNetFluxStatistics_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."fittedNetFluxStatistics"
    ADD CONSTRAINT "fittedNetFluxStatistics_pkey" PRIMARY KEY (id);


--
-- Name: fittedNetFluxStatistics fittedNetFluxStatistics_simulation_id_simulation_dateAndTim_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."fittedNetFluxStatistics"
    ADD CONSTRAINT "fittedNetFluxStatistics_simulation_id_simulation_dateAndTim_key" UNIQUE (simulation_id, "simulation_dateAndTime", flux_units);


--
-- Name: fittedNetFluxStatistics fittedNetFluxStatistics_simulation_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."fittedNetFluxStatistics"
    ADD CONSTRAINT "fittedNetFluxStatistics_simulation_id_fkey" FOREIGN KEY (simulation_id) REFERENCES public.simulation(simulation_id) NOT VALID;


--
-- PostgreSQL database dump complete
--



--
-- TOC entry 294 (class 1259 OID 18784)
-- Name: fittedNetFluxes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."fittedNetFluxes" (
    id integer NOT NULL,
    simulation_id text,
    "simulation_dateAndTime" timestamp(6) without time zone,
    rxn_id text,
    flux double precision,
    flux_stdev double precision,
    flux_lb double precision,
    flux_ub double precision,
    flux_units text,
    used boolean,
    comment text
);


ALTER TABLE public."fittedNetFluxes" OWNER TO postgres;

--
-- Name: fittedNetFluxes_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."fittedNetFluxes_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."fittedNetFluxes_id_seq" OWNER TO postgres;

--
-- Name: fittedNetFluxes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."fittedNetFluxes_id_seq" OWNED BY public."fittedNetFluxes".id;


--
-- Name: fittedNetFluxes id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."fittedNetFluxes" ALTER COLUMN id SET DEFAULT nextval('public."fittedNetFluxes_id_seq"'::regclass);


--
-- Name: fittedNetFluxes fittedNetFluxes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."fittedNetFluxes"
    ADD CONSTRAINT "fittedNetFluxes_pkey" PRIMARY KEY (id);


--
-- Name: fittedNetFluxes fittedNetFluxes_simulation_id_simulation_dateAndTime_rxn_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."fittedNetFluxes"
    ADD CONSTRAINT "fittedNetFluxes_simulation_id_simulation_dateAndTime_rxn_id_key" UNIQUE (simulation_id, "simulation_dateAndTime", rxn_id, flux_units);


--
-- Name: fittedNetFluxes fittedNetFluxes_simulation_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."fittedNetFluxes"
    ADD CONSTRAINT "fittedNetFluxes_simulation_id_fkey" FOREIGN KEY (simulation_id) REFERENCES public.simulation(simulation_id) NOT VALID;


--
-- PostgreSQL database dump complete
--



--
-- TOC entry 296 (class 1259 OID 18797)
-- Name: measuredFluxes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."measuredFluxes" (
    id integer NOT NULL,
    experiment_id text NOT NULL,
    model_id text,
    sample_name_abbreviation text,
    rxn_id text,
    flux_average double precision,
    flux_stdev double precision,
    flux_lb double precision,
    flux_ub double precision,
    flux_units text,
    used boolean,
    comment text
);


ALTER TABLE public."measuredFluxes" OWNER TO postgres;

--
-- Name: measuredFluxes_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."measuredFluxes_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."measuredFluxes_id_seq" OWNER TO postgres;

--
-- Name: measuredFluxes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."measuredFluxes_id_seq" OWNED BY public."measuredFluxes".id;


--
-- Name: measuredFluxes id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."measuredFluxes" ALTER COLUMN id SET DEFAULT nextval('public."measuredFluxes_id_seq"'::regclass);


--
-- Name: measuredFluxes measuredFluxes_experiment_id_model_id_sample_name_abbreviat_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."measuredFluxes"
    ADD CONSTRAINT "measuredFluxes_experiment_id_model_id_sample_name_abbreviat_key" UNIQUE (experiment_id, model_id, sample_name_abbreviation, rxn_id);


--
-- Name: measuredFluxes measuredFluxes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."measuredFluxes"
    ADD CONSTRAINT "measuredFluxes_pkey" PRIMARY KEY (id);


--
-- Name: measuredFluxes measuredFluxes_rxn_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."measuredFluxes"
    ADD CONSTRAINT "measuredFluxes_rxn_id_fkey" FOREIGN KEY (rxn_id) REFERENCES public."fittedFluxes"(rxn_id) NOT VALID;


--
-- PostgreSQL database dump complete
--


--
-- TOC entry 298 (class 1259 OID 18810)
-- Name: measuredFragments; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."measuredFragments" (
    id integer NOT NULL,
    experiment_id text,
    sample_name_abbreviation text,
    time_point text,
    met_id text,
    fragment_id text,
    fragment_formula text,
    intensity_normalized_average double precision[],
    intensity_normalized_cv double precision[],
    intensity_normalized_stdev double precision[],
    intensity_normalized_units text,
    scan_type text,
    met_element text[],
    met_atompositions integer[],
    used boolean,
    comment text
);


ALTER TABLE public."measuredFragments" OWNER TO postgres;

--
-- Name: measuredFragments_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."measuredFragments_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."measuredFragments_id_seq" OWNER TO postgres;

--
-- Name: measuredFragments_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."measuredFragments_id_seq" OWNED BY public."measuredFragments".id;


--
-- Name: measuredFragments id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."measuredFragments" ALTER COLUMN id SET DEFAULT nextval('public."measuredFragments_id_seq"'::regclass);


--
-- Name: measuredFragments measuredFragments_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."measuredFragments"
    ADD CONSTRAINT "measuredFragments_pkey" PRIMARY KEY (id);


--
-- Name: measuredFragments measuredFragments_fragment_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."measuredFragments"
    ADD CONSTRAINT "measuredFragments_fragment_id_fkey" FOREIGN KEY (fragment_id) REFERENCES public."fittedFragments"(fragment_id) NOT VALID;


--
-- PostgreSQL database dump complete
--


--
-- TOC entry 300 (class 1259 OID 18821)
-- Name: measuredPools; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."measuredPools" (
    id integer NOT NULL,
    experiment_id text,
    model_id text,
    sample_name_abbreviation text,
    time_point text,
    met_id text,
    pool_size double precision,
    concentration_average double precision,
    concentration_var double precision,
    concentration_lb double precision,
    concentration_ub double precision,
    concentration_units text,
    used boolean,
    comment text
);


ALTER TABLE public."measuredPools" OWNER TO postgres;

--
-- Name: measuredPools_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."measuredPools_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."measuredPools_id_seq" OWNER TO postgres;

--
-- Name: measuredPools_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."measuredPools_id_seq" OWNED BY public."measuredPools".id;


--
-- Name: measuredPools id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."measuredPools" ALTER COLUMN id SET DEFAULT nextval('public."measuredPools_id_seq"'::regclass);


--
-- Name: measuredPools measuredPools_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."measuredPools"
    ADD CONSTRAINT "measuredPools_pkey" PRIMARY KEY (id);


--
-- Name: measuredPools measuredPools_met_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."measuredPools"
    ADD CONSTRAINT "measuredPools_met_id_fkey" FOREIGN KEY (met_id) REFERENCES public."atomMappingMetabolites"(met_id) NOT VALID;


--
-- PostgreSQL database dump complete
--




--
-- TOC entry 302 (class 1259 OID 18832)
-- Name: modelMetabolites; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."modelMetabolites" (
    id integer NOT NULL,
    model_id text,
    met_name text,
    met_id text,
    formula text,
    charge integer,
    compartment text,
    bound double precision,
    constraint_sense text,
    used boolean,
    comment text,
    lower_bound double precision,
    upper_bound double precision,
    balanced boolean,
    fixed boolean
);


ALTER TABLE public."modelMetabolites" OWNER TO postgres;

--
-- Name: modelMetabolites_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."modelMetabolites_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."modelMetabolites_id_seq" OWNER TO postgres;

--
-- Name: modelMetabolites_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."modelMetabolites_id_seq" OWNED BY public."modelMetabolites".id;


--
-- Name: modelMetabolites id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."modelMetabolites" ALTER COLUMN id SET DEFAULT nextval('public."modelMetabolites_id_seq"'::regclass);


--
-- Name: modelMetabolites modelMetabolites_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."modelMetabolites"
    ADD CONSTRAINT "modelMetabolites_pkey" PRIMARY KEY (id);


--
-- Name: modelMetabolites modelMetabolites_model_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."modelMetabolites"
    ADD CONSTRAINT "modelMetabolites_model_id_fkey" FOREIGN KEY (model_id) REFERENCES public.models(model_id) NOT VALID;


--
-- PostgreSQL database dump complete
--




--
-- TOC entry 304 (class 1259 OID 18843)
-- Name: modelPathways; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."modelPathways" (
    id integer NOT NULL,
    model_id text NOT NULL,
    pathway_id text NOT NULL,
    reactions text[],
    stoichiometry double precision[],
    used boolean,
    comment text
);


ALTER TABLE public."modelPathways" OWNER TO postgres;

--
-- Name: modelPathways_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."modelPathways_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."modelPathways_id_seq" OWNER TO postgres;

--
-- Name: modelPathways_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."modelPathways_id_seq" OWNED BY public."modelPathways".id;


--
-- Name: modelPathways id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."modelPathways" ALTER COLUMN id SET DEFAULT nextval('public."modelPathways_id_seq"'::regclass);


--
-- Name: modelPathways modelPathways_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."modelPathways"
    ADD CONSTRAINT "modelPathways_pkey" PRIMARY KEY (id, model_id, pathway_id);


--
-- Name: modelPathways modelPathways_model_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."modelPathways"
    ADD CONSTRAINT "modelPathways_model_id_fkey" FOREIGN KEY (model_id) REFERENCES public.models(model_id) NOT VALID;


--
-- PostgreSQL database dump complete
--


--
-- TOC entry 306 (class 1259 OID 18854)
-- Name: modelReactions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."modelReactions" (
    id integer NOT NULL,
    model_id text NOT NULL,
    rxn_id text NOT NULL,
    rxn_name text,
    equation text,
    subsystem text,
    gpr text,
    genes text[],
    reactants_stoichiometry double precision[],
    products_stoichiometry double precision[],
    reactants_ids text[],
    products_ids text[],
    lower_bound double precision,
    upper_bound double precision,
    objective_coefficient double precision,
    flux_units text,
    fixed boolean,
    free boolean,
    reversibility boolean,
    weight double precision,
    used boolean,
    comment text
);


ALTER TABLE public."modelReactions" OWNER TO postgres;

--
-- Name: modelReactions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."modelReactions_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."modelReactions_id_seq" OWNER TO postgres;

--
-- Name: modelReactions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."modelReactions_id_seq" OWNED BY public."modelReactions".id;


--
-- Name: modelReactions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."modelReactions" ALTER COLUMN id SET DEFAULT nextval('public."modelReactions_id_seq"'::regclass);


--
-- Name: modelReactions modelReactions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."modelReactions"
    ADD CONSTRAINT "modelReactions_pkey" PRIMARY KEY (id);


--
-- Name: modelReactions modelReactions_model_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."modelReactions"
    ADD CONSTRAINT "modelReactions_model_id_fkey" FOREIGN KEY (model_id) REFERENCES public.models(model_id) NOT VALID;


--
-- PostgreSQL database dump complete
--


--
-- TOC entry 308 (class 1259 OID 18865)
-- Name: models; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.models (
    id integer NOT NULL,
    model_id text,
    model_name text,
    model_description text,
    model_file text,
    date timestamp(6) without time zone,
    file_type text
);


ALTER TABLE public.models OWNER TO postgres;

--
-- Name: models_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.models_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.models_id_seq OWNER TO postgres;

--
-- Name: models_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.models_id_seq OWNED BY public.models.id;


--
-- Name: models id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.models ALTER COLUMN id SET DEFAULT nextval('public.models_id_seq'::regclass);


--
-- Name: models models_model_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.models
    ADD CONSTRAINT models_model_id_key UNIQUE (model_id);


--
-- Name: models models_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.models
    ADD CONSTRAINT models_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--




--
-- TOC entry 235 (class 1259 OID 18375)
-- Name: mzTab_M_Metadata_metabolomics_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."mzTab_M_Metadata_metabolomics_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."mzTab_M_Metadata_metabolomics_id_seq" OWNER TO postgres;

--
-- TOC entry 3498 (class 0 OID 0)
-- Dependencies: 235
-- Name: mzTab_M_Metadata_metabolomics_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."mzTab_M_Metadata_metabolomics_id_seq" OWNED BY public."MzTab_M_Metadata_metabolomics".id;


--
-- TOC entry 310 (class 1259 OID 18876)
-- Name: simulation; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.simulation (
    id integer NOT NULL,
    experiment_id text,
    model_id text,
    mapping_id text,
    sample_name_abbreviation text,
    time_point text,
    used boolean,
    comment text,
    simulation_id text
);


ALTER TABLE public.simulation OWNER TO postgres;

--
-- Name: simulation_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.simulation_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.simulation_id_seq OWNER TO postgres;

--
-- Name: simulation_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.simulation_id_seq OWNED BY public.simulation.id;


--
-- Name: simulation id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.simulation ALTER COLUMN id SET DEFAULT nextval('public.simulation_id_seq'::regclass);


--
-- Name: simulation simulation_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.simulation
    ADD CONSTRAINT simulation_pkey PRIMARY KEY (id);


--
-- Name: simulation simulation_simulation_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.simulation
    ADD CONSTRAINT simulation_simulation_id_key UNIQUE (simulation_id);


--
-- PostgreSQL database dump complete
--

--
-- TOC entry 312 (class 1259 OID 18887)
-- Name: simulationParameters; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."simulationParameters" (
    id integer NOT NULL,
    simulation_id text,
    "simulation_dateAndTime" timestamp(6) without time zone,
    cont_alpha double precision,
    cont_reltol double precision,
    cont_steps double precision,
    fit_nudge double precision,
    fit_reinit boolean,
    fit_reltol double precision,
    fit_starts double precision,
    fit_tau double precision,
    hpc_mcr text,
    hpc_on boolean,
    hpc_serve text,
    int_maxstep double precision,
    int_reltol double precision,
    int_senstol double precision,
    int_timeout double precision,
    int_tspan double precision,
    ms_correct boolean,
    oed_crit text,
    oed_reinit boolean,
    oed_tolf double precision,
    oed_tolx double precision,
    sim_more boolean,
    sim_na boolean,
    sim_sens boolean,
    sim_ss boolean,
    sim_tunit text,
    original_filename text
);


ALTER TABLE public."simulationParameters" OWNER TO postgres;

--
-- Name: simulationParameters_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."simulationParameters_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."simulationParameters_id_seq" OWNER TO postgres;

--
-- Name: simulationParameters_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."simulationParameters_id_seq" OWNED BY public."simulationParameters".id;


--
-- Name: simulationParameters id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."simulationParameters" ALTER COLUMN id SET DEFAULT nextval('public."simulationParameters_id_seq"'::regclass);


--
-- Name: simulationParameters simulationParameters_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."simulationParameters"
    ADD CONSTRAINT "simulationParameters_pkey" PRIMARY KEY (id);


--
-- Name: simulationParameters simulationParameters_simulation_id_simulation_dateAndTime_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."simulationParameters"
    ADD CONSTRAINT "simulationParameters_simulation_id_simulation_dateAndTime_key" UNIQUE (simulation_id, "simulation_dateAndTime");


--
-- Name: simulationParameters simulationParameters_simulation_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."simulationParameters"
    ADD CONSTRAINT "simulationParameters_simulation_id_fkey" FOREIGN KEY (simulation_id) REFERENCES public.simulation(simulation_id) NOT VALID;


--
-- PostgreSQL database dump complete
--




--
-- TOC entry 314 (class 1259 OID 18901)
-- Name: tracers; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tracers (
    met_id text NOT NULL,
    id integer NOT NULL,
    met_name text,
    isotopomer_formula text[],
    met_elements text[],
    met_atompositions integer[],
    ratio double precision,
    supplier text,
    supplier_reference text,
    purity double precision,
    comment text
);


ALTER TABLE public.tracers OWNER TO postgres;

--
-- TOC entry 313 (class 1259 OID 18899)
-- Name: tracers_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tracers_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tracers_id_seq OWNER TO postgres;

--
-- TOC entry 3158 (class 0 OID 0)
-- Dependencies: 313
-- Name: tracers_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tracers_id_seq OWNED BY public.tracers.id;


--
-- TOC entry 3021 (class 2604 OID 18904)
-- Name: tracers id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tracers ALTER COLUMN id SET DEFAULT nextval('public.tracers_id_seq'::regclass);


--
-- TOC entry 3023 (class 2606 OID 18911)
-- Name: tracers tracers_met_id_met_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tracers
    ADD CONSTRAINT tracers_met_id_met_name_key UNIQUE (met_id, met_name);


--
-- TOC entry 3025 (class 2606 OID 18909)
-- Name: tracers tracers_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tracers
    ADD CONSTRAINT tracers_pkey PRIMARY KEY (id);


--
-- TOC entry 3026 (class 2606 OID 19027)
-- Name: tracers tracers_met_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tracers
    ADD CONSTRAINT tracers_met_id_fkey FOREIGN KEY (met_id) REFERENCES public."atomMappingMetabolites"(met_id) NOT VALID;


-- Completed on 2021-01-05 14:23:01

--
-- PostgreSQL database dump complete
--



--
-- TOC entry 258 (class 1259 OID 18549)
-- Name: xxxxx_MDVFragments; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."xxxxx_MDVFragments" (
    met_id text NOT NULL,
    formula text NOT NULL,
    id integer NOT NULL,
    elements text[] NOT NULL,
    positions integer[] NOT NULL
);


ALTER TABLE public."xxxxx_MDVFragments" OWNER TO postgres;

--
-- TOC entry 257 (class 1259 OID 18547)
-- Name: xxxxx_MDVFragments_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."xxxxx_MDVFragments_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."xxxxx_MDVFragments_id_seq" OWNER TO postgres;

--
-- TOC entry 3502 (class 0 OID 0)
-- Dependencies: 257
-- Name: xxxxx_MDVFragments_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."xxxxx_MDVFragments_id_seq" OWNED BY public."xxxxx_MDVFragments".id;


--
-- TOC entry 3078 (class 2604 OID 17440)
-- Name: ASSAY Assay_ID; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."ASSAY" ALTER COLUMN "Assay_ID" SET DEFAULT nextval('public."ASSAY_Assay_ID_seq"'::regclass);


--
-- TOC entry 3087 (class 2604 OID 18270)
-- Name: A_TECHNOLOGY_MICROARRAY id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."A_TECHNOLOGY_MICROARRAY" ALTER COLUMN "id" SET DEFAULT nextval('public."A_TECHNOLOGY_MICROARRAY_id_seq"'::regclass);


--
-- TOC entry 3088 (class 2604 OID 18280)
-- Name: A_TECHNOLOGY_MS id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."A_TECHNOLOGY_MS" ALTER COLUMN "id" SET DEFAULT nextval('public."A_TECHNOLOGY_MS_id_seq"'::regclass);


--
-- TOC entry 3089 (class 2604 OID 18291)
-- Name: A_TECHNOLOGY_NMR id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."A_TECHNOLOGY_NMR" ALTER COLUMN "id" SET DEFAULT nextval('public."A_TECHNOLOGY_NMR_id_seq"'::regclass);


--
-- TOC entry 3079 (class 2604 OID 17487)
-- Name: CONTACTS Contact_Person_ID; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."CONTACTS" ALTER COLUMN "Contact_Person_ID" SET DEFAULT nextval('public."CONTACTS_Contact_Person_ID_seq"'::regclass);


--
-- TOC entry 3102 (class 2604 OID 18513)
-- Name: FeatureXML id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."FeatureXML" ALTER COLUMN id SET DEFAULT nextval('public."FeatureXML_id_seq"'::regclass);


--
-- TOC entry 3080 (class 2604 OID 17498)
-- Name: INVESTIGATION Investigation_ID; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."INVESTIGATION" ALTER COLUMN "Investigation_ID" SET DEFAULT nextval('public."INVESTIGATION_Investigation_ID_seq"'::regclass);


--
-- TOC entry 3106 (class 2604 OID 18563)
-- Name: MFA_model_metabolites  id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."MFA_model_metabolites " ALTER COLUMN id SET DEFAULT nextval('public."MFA_model_metabolites _id_seq"'::regclass);


--
-- TOC entry 3107 (class 2604 OID 18574)
-- Name: MFA_model_reactions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."MFA_model_reactions" ALTER COLUMN id SET DEFAULT nextval('public."MFA_model_reactions_id_seq"'::regclass);


--
-- TOC entry 3094 (class 2604 OID 18380)
-- Name: MzTab_M_Metadata_metabolomics id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."MzTab_M_Metadata_metabolomics" ALTER COLUMN id SET DEFAULT nextval('public."mzTab_M_Metadata_metabolomics_id_seq"'::regclass);


--
-- TOC entry 3097 (class 2604 OID 18422)
-- Name: MzTab_M_Small_Molecule_Evidence_SME_Section SME_ID; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."MzTab_M_Small_Molecule_Evidence_SME_Section" ALTER COLUMN "SME_ID" SET DEFAULT nextval('public."MzTab_M_Small_Molecule_Evidence_SME_Section_SME_ID_seq"'::regclass);


--
-- TOC entry 3096 (class 2604 OID 18413)
-- Name: MzTab_M_Small_Molecule_Feature_SMF_Section SMF_ID; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."MzTab_M_Small_Molecule_Feature_SMF_Section" ALTER COLUMN "SMF_ID" SET DEFAULT nextval('public."MzTab_M_Small_Molecule_Feature_SMF_Section_SMF_ID_seq"'::regclass);


--
-- TOC entry 3095 (class 2604 OID 18401)
-- Name: MzTab_M_small_molecule_section SML_ID; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."MzTab_M_small_molecule_section" ALTER COLUMN "SML_ID" SET DEFAULT nextval('public."MzTab_M_small_molecule_section_SML_ID_seq"'::regclass);


--
-- TOC entry 3090 (class 2604 OID 18321)
-- Name: MzTab_Metadata_Proteomics id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."MzTab_Metadata_Proteomics" ALTER COLUMN id SET DEFAULT nextval('public."MzTab_Metadata_Proteomics_id_seq"'::regclass);


--
-- TOC entry 3091 (class 2604 OID 18332)
-- Name: MzTab_PSM_section id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."MzTab_PSM_section" ALTER COLUMN id SET DEFAULT nextval('public."MzTab_PSM section_id_seq"'::regclass);


--
-- TOC entry 3093 (class 2604 OID 18354)
-- Name: MzTab_Peptide_section id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."MzTab_Peptide_section" ALTER COLUMN id SET DEFAULT nextval('public."MzTab_Peptide section_id_seq"'::regclass);


--
-- TOC entry 3092 (class 2604 OID 18343)
-- Name: MzTab_Protein_section id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."MzTab_Protein_section" ALTER COLUMN id SET DEFAULT nextval('public."MzTab_Protein section_id_seq"'::regclass);


--
-- TOC entry 3081 (class 2604 OID 17509)
-- Name: ONTOLOGY_SOURCE_REFERENCE Ontology_Source_REF_ID; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."ONTOLOGY_SOURCE_REFERENCE" ALTER COLUMN "Ontology_Source_REF_ID" SET DEFAULT nextval('public."ONTOLOGY_SOURCE_REFERENCE_Ontology_Source_REF_ID_seq"'::regclass);


--
-- TOC entry 3098 (class 2604 OID 18468)
-- Name: PQP_compound id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."PQP_compound" ALTER COLUMN id SET DEFAULT nextval('public."PQP_compound_id_seq"'::regclass);


--
-- TOC entry 3099 (class 2604 OID 18479)
-- Name: PQP_gene id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."PQP_gene" ALTER COLUMN id SET DEFAULT nextval('public."PQP_gene_id_seq"'::regclass);


--
-- TOC entry 3100 (class 2604 OID 18491)
-- Name: PQP_peptide id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."PQP_peptide" ALTER COLUMN id SET DEFAULT nextval('public."PQP_peptide_id_seq"'::regclass);


--
-- TOC entry 3101 (class 2604 OID 18502)
-- Name: PQP_protein id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."PQP_protein" ALTER COLUMN id SET DEFAULT nextval('public."PQP_protein_id_seq"'::regclass);


--
-- TOC entry 3082 (class 2604 OID 17520)
-- Name: PROTOCOLS Protocol_ID; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."PROTOCOLS" ALTER COLUMN "Protocol_ID" SET DEFAULT nextval('public."PROTOCOLS_Protocol_ID_seq"'::regclass);


--
-- TOC entry 3083 (class 2604 OID 17531)
-- Name: PUBLICATIONS Publication_ID; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."PUBLICATIONS" ALTER COLUMN "Publication_ID" SET DEFAULT nextval('public."PUBLICATIONS_Publication_ID_seq"'::regclass);


--
-- TOC entry 3103 (class 2604 OID 18524)
-- Name: SOPs sop_ID; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."SOPs" ALTER COLUMN "sop_ID" SET DEFAULT nextval('public."SOPs_sop_ID_seq"'::regclass);


--
-- TOC entry 3084 (class 2604 OID 17543)
-- Name: STUDY Study_ID; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."STUDY" ALTER COLUMN "Study_ID" SET DEFAULT nextval('public."STUDY_Study_ID_seq"'::regclass);


--
-- TOC entry 3085 (class 2604 OID 17554)
-- Name: STUDY_DESIGN_DESCRIPTORS Design_Descriptors_ID; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."STUDY_DESIGN_DESCRIPTORS" ALTER COLUMN "Design_Descriptors_ID" SET DEFAULT nextval('public."STUDY_DESIGN_DESCRIPTORS_Design_Descriptors_ID_seq"'::regclass);


--
-- TOC entry 3086 (class 2604 OID 17565)
-- Name: STUDY_FACTORS Study_Factors_ID; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."STUDY_FACTORS" ALTER COLUMN "Study_Factors_ID" SET DEFAULT nextval('public."STUDY_FACTORS_Study_Factors_ID_seq"'::regclass);


--
-- TOC entry 3104 (class 2604 OID 18538)
-- Name: TraML id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."TraML" ALTER COLUMN id SET DEFAULT nextval('public."TraML_id_seq"'::regclass);


--
-- TOC entry 3108 (class 2604 OID 18585)
-- Name: atomMappingMetabolites id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."atomMappingMetabolites" ALTER COLUMN id SET DEFAULT nextval('public."atomMappingMetabolites_id_seq"'::regclass);


--
-- TOC entry 3109 (class 2604 OID 18597)
-- Name: atomMappingReactions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."atomMappingReactions" ALTER COLUMN id SET DEFAULT nextval('public."atomMappingReactions_id_seq"'::regclass);


--
-- TOC entry 3110 (class 2604 OID 18608)
-- Name: calcFluxes id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."calcFluxes" ALTER COLUMN id SET DEFAULT nextval('public."calcFluxes_id_seq"'::regclass);


--
-- TOC entry 3111 (class 2604 OID 18619)
-- Name: calcFragments id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."calcFragments" ALTER COLUMN id SET DEFAULT nextval('public."calcFragments_id_seq"'::regclass);


--
-- TOC entry 3112 (class 2604 OID 18630)
-- Name: fittedData id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."fittedData" ALTER COLUMN id SET DEFAULT nextval('public."fittedData_id_seq"'::regclass);


--
-- TOC entry 3113 (class 2604 OID 18643)
-- Name: fittedExchangeFluxStatistics id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."fittedExchangeFluxStatistics" ALTER COLUMN id SET DEFAULT nextval('public."fittedExchangeFluxStatistics_id_seq"'::regclass);


--
-- TOC entry 3114 (class 2604 OID 18656)
-- Name: fittedExchangeFluxes id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."fittedExchangeFluxes" ALTER COLUMN id SET DEFAULT nextval('public."fittedExchangeFluxes_id_seq"'::regclass);


--
-- TOC entry 3115 (class 2604 OID 18669)
-- Name: fittedFluxStatistics id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."fittedFluxStatistics" ALTER COLUMN id SET DEFAULT nextval('public."fittedFluxStatistics_id_seq"'::regclass);


--
-- TOC entry 3116 (class 2604 OID 18682)
-- Name: fittedFluxes id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."fittedFluxes" ALTER COLUMN id SET DEFAULT nextval('public."fittedFluxes_id_seq"'::regclass);


--
-- TOC entry 3117 (class 2604 OID 18697)
-- Name: fittedFragments id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."fittedFragments" ALTER COLUMN id SET DEFAULT nextval('public."fittedFragments_id_seq"'::regclass);


--
-- TOC entry 3118 (class 2604 OID 18710)
-- Name: fittedMeasuredFluxResiduals id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."fittedMeasuredFluxResiduals" ALTER COLUMN id SET DEFAULT nextval('public."fittedMeasuredFluxResiduals_id_seq"'::regclass);


--
-- TOC entry 3119 (class 2604 OID 18723)
-- Name: fittedMeasuredFluxes id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."fittedMeasuredFluxes" ALTER COLUMN id SET DEFAULT nextval('public."fittedMeasuredFluxes_id_seq"'::regclass);


--
-- TOC entry 3120 (class 2604 OID 18737)
-- Name: fittedMeasuredFragmentResiduals id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."fittedMeasuredFragmentResiduals" ALTER COLUMN id SET DEFAULT nextval('public."fittedMeasuredFragmentResiduals_id_seq"'::regclass);


--
-- TOC entry 3121 (class 2604 OID 18761)
-- Name: fittedMeasuredFragments id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."fittedMeasuredFragments" ALTER COLUMN id SET DEFAULT nextval('public."fittedMeasuredFragments_id_seq"'::regclass);


--
-- TOC entry 3122 (class 2604 OID 18774)
-- Name: fittedNetFluxStatistics id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."fittedNetFluxStatistics" ALTER COLUMN id SET DEFAULT nextval('public."fittedNetFluxStatistics_id_seq"'::regclass);


--
-- TOC entry 3123 (class 2604 OID 18787)
-- Name: fittedNetFluxes id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."fittedNetFluxes" ALTER COLUMN id SET DEFAULT nextval('public."fittedNetFluxes_id_seq"'::regclass);


--
-- TOC entry 3124 (class 2604 OID 18800)
-- Name: measuredFluxes id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."measuredFluxes" ALTER COLUMN id SET DEFAULT nextval('public."measuredFluxes_id_seq"'::regclass);


--
-- TOC entry 3125 (class 2604 OID 18813)
-- Name: measuredFragments id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."measuredFragments" ALTER COLUMN id SET DEFAULT nextval('public."measuredFragments_id_seq"'::regclass);


--
-- TOC entry 3126 (class 2604 OID 18824)
-- Name: measuredPools id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."measuredPools" ALTER COLUMN id SET DEFAULT nextval('public."measuredPools_id_seq"'::regclass);


--
-- TOC entry 3127 (class 2604 OID 18835)
-- Name: modelMetabolites id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."modelMetabolites" ALTER COLUMN id SET DEFAULT nextval('public."modelMetabolites_id_seq"'::regclass);


--
-- TOC entry 3128 (class 2604 OID 18846)
-- Name: modelPathways id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."modelPathways" ALTER COLUMN id SET DEFAULT nextval('public."modelPathways_id_seq"'::regclass);


--
-- TOC entry 3129 (class 2604 OID 18857)
-- Name: modelReactions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."modelReactions" ALTER COLUMN id SET DEFAULT nextval('public."modelReactions_id_seq"'::regclass);


--
-- TOC entry 3130 (class 2604 OID 18868)
-- Name: models id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.models ALTER COLUMN id SET DEFAULT nextval('public.models_id_seq'::regclass);


--
-- TOC entry 3131 (class 2604 OID 18879)
-- Name: simulation id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.simulation ALTER COLUMN id SET DEFAULT nextval('public.simulation_id_seq'::regclass);


--
-- TOC entry 3132 (class 2604 OID 18890)
-- Name: simulationParameters id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."simulationParameters" ALTER COLUMN id SET DEFAULT nextval('public."simulationParameters_id_seq"'::regclass);


--
-- TOC entry 3133 (class 2604 OID 18904)
-- Name: tracers id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tracers ALTER COLUMN id SET DEFAULT nextval('public.tracers_id_seq'::regclass);


--
-- TOC entry 3105 (class 2604 OID 18552)
-- Name: xxxxx_MDVFragments id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."xxxxx_MDVFragments" ALTER COLUMN id SET DEFAULT nextval('public."xxxxx_MDVFragments_id_seq"'::regclass);


--
-- TOC entry 3135 (class 2606 OID 17445)
-- Name: ASSAY ASSAY_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."ASSAY"
    ADD CONSTRAINT "ASSAY_pkey" PRIMARY KEY ("Assay_ID");


--
-- TOC entry 3165 (class 2606 OID 17586)
-- Name: A_TECHNOLOGY_MICROARRAY A_TECHNOLOGY_MICROARRAY_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."A_TECHNOLOGY_MICROARRAY"
    ADD CONSTRAINT "A_TECHNOLOGY_MICROARRAY_pkey" PRIMARY KEY ("Assay_ID");


--
-- TOC entry 3167 (class 2606 OID 17594)
-- Name: A_TECHNOLOGY_MS A_TECHNOLOGY_MS_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."A_TECHNOLOGY_MS"
    ADD CONSTRAINT "A_TECHNOLOGY_MS_pkey" PRIMARY KEY ("Assay_ID");


--
-- TOC entry 3169 (class 2606 OID 17602)
-- Name: A_TECHNOLOGY_NMR A_TECHNOLOGY_NMR_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."A_TECHNOLOGY_NMR"
    ADD CONSTRAINT "A_TECHNOLOGY_NMR_pkey" PRIMARY KEY ("Assay_ID");


--
-- TOC entry 3137 (class 2606 OID 17492)
-- Name: CONTACTS CONTACTS_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."CONTACTS"
    ADD CONSTRAINT "CONTACTS_pkey" PRIMARY KEY ("Contact_Person_ID");


--
-- TOC entry 3201 (class 2606 OID 18518)
-- Name: FeatureXML FeatureXML_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."FeatureXML"
    ADD CONSTRAINT "FeatureXML_pkey" PRIMARY KEY ("mzTab-ID");


--
-- TOC entry 3139 (class 2606 OID 17679)
-- Name: INVESTIGATION INVESTIGATION_Investigation_Identifier_External_ID_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."INVESTIGATION"
    ADD CONSTRAINT "INVESTIGATION_Investigation_Identifier_External_ID_key" UNIQUE ("Investigation_Identifier") INCLUDE (id);


--
-- TOC entry 3141 (class 2606 OID 17503)
-- Name: INVESTIGATION INVESTIGATION_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."INVESTIGATION"
    ADD CONSTRAINT "INVESTIGATION_pkey" PRIMARY KEY ("Investigation_ID");


--
-- TOC entry 3209 (class 2606 OID 18568)
-- Name: MFA_model_metabolites  MFA_model_metabolites _pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."MFA_model_metabolites "
    ADD CONSTRAINT "MFA_model_metabolites _pkey" PRIMARY KEY (id);


--
-- TOC entry 3211 (class 2606 OID 18579)
-- Name: MFA_model_reactions MFA_model_reactions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."MFA_model_reactions"
    ADD CONSTRAINT "MFA_model_reactions_pkey" PRIMARY KEY (id);


--
-- TOC entry 3179 (class 2606 OID 18433)
-- Name: MzTab_M_Metadata_metabolomics MzTab_M_Metadata_metabolomics_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."MzTab_M_Metadata_metabolomics"
    ADD CONSTRAINT "MzTab_M_Metadata_metabolomics_id_key" UNIQUE (id);


--
-- TOC entry 3181 (class 2606 OID 18386)
-- Name: MzTab_M_Metadata_metabolomics MzTab_M_Metadata_metabolomics_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."MzTab_M_Metadata_metabolomics"
    ADD CONSTRAINT "MzTab_M_Metadata_metabolomics_pkey" PRIMARY KEY ("mzTab_ID");


--
-- TOC entry 3191 (class 2606 OID 18431)
-- Name: MzTab_M_Small_Molecule_Evidence_SME_Section MzTab_M_Small_Molecule_Evidence_SME_Section_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."MzTab_M_Small_Molecule_Evidence_SME_Section"
    ADD CONSTRAINT "MzTab_M_Small_Molecule_Evidence_SME_Section_pkey" PRIMARY KEY ("SME_ID");


--
-- TOC entry 3187 (class 2606 OID 18457)
-- Name: MzTab_M_Small_Molecule_Feature_SMF_Section MzTab_M_Small_Molecule_Feature_SMF_Section_SME_ID_REFS_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."MzTab_M_Small_Molecule_Feature_SMF_Section"
    ADD CONSTRAINT "MzTab_M_Small_Molecule_Feature_SMF_Section_SME_ID_REFS_key" UNIQUE ("SME_ID_REFS");


--
-- TOC entry 3189 (class 2606 OID 18429)
-- Name: MzTab_M_Small_Molecule_Feature_SMF_Section MzTab_M_Small_Molecule_Feature_SMF_Section_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."MzTab_M_Small_Molecule_Feature_SMF_Section"
    ADD CONSTRAINT "MzTab_M_Small_Molecule_Feature_SMF_Section_pkey" PRIMARY KEY ("SMF_ID");


--
-- TOC entry 3183 (class 2606 OID 18450)
-- Name: MzTab_M_small_molecule_section MzTab_M_small_molecule_section_SMF_ID_REFS_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."MzTab_M_small_molecule_section"
    ADD CONSTRAINT "MzTab_M_small_molecule_section_SMF_ID_REFS_key" UNIQUE ("SMF_ID_REFS");


--
-- TOC entry 3185 (class 2606 OID 18427)
-- Name: MzTab_M_small_molecule_section MzTab_M_small_molecule_section_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."MzTab_M_small_molecule_section"
    ADD CONSTRAINT "MzTab_M_small_molecule_section_pkey" PRIMARY KEY ("SML_ID");


--
-- TOC entry 3171 (class 2606 OID 18326)
-- Name: MzTab_Metadata_Proteomics MzTab_Metadata_Proteomics_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."MzTab_Metadata_Proteomics"
    ADD CONSTRAINT "MzTab_Metadata_Proteomics_pkey" PRIMARY KEY ("mzTab-ID");


--
-- TOC entry 3173 (class 2606 OID 18337)
-- Name: MzTab_PSM_section MzTab_PSM section_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."MzTab_PSM_section"
    ADD CONSTRAINT "MzTab_PSM section_pkey" PRIMARY KEY ("PSM_ID");


--
-- TOC entry 3177 (class 2606 OID 18359)
-- Name: MzTab_Peptide_section MzTab_Peptide section_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."MzTab_Peptide_section"
    ADD CONSTRAINT "MzTab_Peptide section_pkey" PRIMARY KEY (accession);


--
-- TOC entry 3175 (class 2606 OID 18348)
-- Name: MzTab_Protein_section MzTab_Protein section_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."MzTab_Protein_section"
    ADD CONSTRAINT "MzTab_Protein section_pkey" PRIMARY KEY (accession);


--
-- TOC entry 3143 (class 2606 OID 17688)
-- Name: ONTOLOGY_SOURCE_REFERENCE ONTOLOGY_SOURCE_REFERENCE_Ontology_REF_Investigation_Identi_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."ONTOLOGY_SOURCE_REFERENCE"
    ADD CONSTRAINT "ONTOLOGY_SOURCE_REFERENCE_Ontology_REF_Investigation_Identi_key" UNIQUE ("Ontology_REF_Investigation_Identifier");


--
-- TOC entry 3145 (class 2606 OID 18300)
-- Name: ONTOLOGY_SOURCE_REFERENCE ONTOLOGY_SOURCE_REFERENCE_Term_Source_Name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."ONTOLOGY_SOURCE_REFERENCE"
    ADD CONSTRAINT "ONTOLOGY_SOURCE_REFERENCE_Term_Source_Name_key" UNIQUE ("Term_Source_Name");


--
-- TOC entry 3147 (class 2606 OID 17514)
-- Name: ONTOLOGY_SOURCE_REFERENCE ONTOLOGY_SOURCE_REFERENCE_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."ONTOLOGY_SOURCE_REFERENCE"
    ADD CONSTRAINT "ONTOLOGY_SOURCE_REFERENCE_pkey" PRIMARY KEY ("Ontology_Source_REF_ID");


--
-- TOC entry 3193 (class 2606 OID 18473)
-- Name: PQP_compound PQP_compound_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."PQP_compound"
    ADD CONSTRAINT "PQP_compound_pkey" PRIMARY KEY ("COMPOUND_ID");


--
-- TOC entry 3195 (class 2606 OID 18484)
-- Name: PQP_gene PQP_gene_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."PQP_gene"
    ADD CONSTRAINT "PQP_gene_pkey" PRIMARY KEY ("GENE_ID");


--
-- TOC entry 3197 (class 2606 OID 18496)
-- Name: PQP_peptide PQP_peptide_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."PQP_peptide"
    ADD CONSTRAINT "PQP_peptide_pkey" PRIMARY KEY ("PEPTIDE_ID");


--
-- TOC entry 3199 (class 2606 OID 18507)
-- Name: PQP_protein PQP_protein_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."PQP_protein"
    ADD CONSTRAINT "PQP_protein_pkey" PRIMARY KEY ("PROTEIN_ID");


--
-- TOC entry 3149 (class 2606 OID 17525)
-- Name: PROTOCOLS PROTOCOLS_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."PROTOCOLS"
    ADD CONSTRAINT "PROTOCOLS_pkey" PRIMARY KEY ("Protocol_ID");


--
-- TOC entry 3151 (class 2606 OID 17536)
-- Name: PUBLICATIONS PUBLICATIONS_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."PUBLICATIONS"
    ADD CONSTRAINT "PUBLICATIONS_pkey" PRIMARY KEY ("Publication_ID");


--
-- TOC entry 3203 (class 2606 OID 18529)
-- Name: SOPs SOPs_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."SOPs"
    ADD CONSTRAINT "SOPs_pkey" PRIMARY KEY ("sop_ID");


--
-- TOC entry 3157 (class 2606 OID 17559)
-- Name: STUDY_DESIGN_DESCRIPTORS STUDY_DESIGN_DESCRIPTORS_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."STUDY_DESIGN_DESCRIPTORS"
    ADD CONSTRAINT "STUDY_DESIGN_DESCRIPTORS_pkey" PRIMARY KEY ("Design_Descriptors_ID");


--
-- TOC entry 3159 (class 2606 OID 17570)
-- Name: STUDY_FACTORS STUDY_FACTORS_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."STUDY_FACTORS"
    ADD CONSTRAINT "STUDY_FACTORS_pkey" PRIMARY KEY ("Study_Factors_ID");


--
-- TOC entry 3161 (class 2606 OID 18267)
-- Name: STUDY_SAMPLES STUDY_SAMPLES_Sample_Name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."STUDY_SAMPLES"
    ADD CONSTRAINT "STUDY_SAMPLES_Sample_Name_key" UNIQUE ("Sample_Name");


--
-- TOC entry 3163 (class 2606 OID 17578)
-- Name: STUDY_SAMPLES STUDY_SAMPLES_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."STUDY_SAMPLES"
    ADD CONSTRAINT "STUDY_SAMPLES_pkey" PRIMARY KEY ("Sample_Name");


--
-- TOC entry 3153 (class 2606 OID 17681)
-- Name: STUDY STUDY_Study_Identifier_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."STUDY"
    ADD CONSTRAINT "STUDY_Study_Identifier_key" UNIQUE ("Study_Identifier");


--
-- TOC entry 3155 (class 2606 OID 17548)
-- Name: STUDY STUDY_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."STUDY"
    ADD CONSTRAINT "STUDY_pkey" PRIMARY KEY ("Study_ID");


--
-- TOC entry 3205 (class 2606 OID 18546)
-- Name: TraML TraML_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."TraML"
    ADD CONSTRAINT "TraML_pkey" PRIMARY KEY ("mzTab-ID");


--
-- TOC entry 3213 (class 2606 OID 18590)
-- Name: atomMappingMetabolites atomMappingMetabolites_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."atomMappingMetabolites"
    ADD CONSTRAINT "atomMappingMetabolites_pkey" PRIMARY KEY (id);


--
-- TOC entry 3215 (class 2606 OID 18602)
-- Name: atomMappingReactions atomMappingReactions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."atomMappingReactions"
    ADD CONSTRAINT "atomMappingReactions_pkey" PRIMARY KEY (id);


--
-- TOC entry 3217 (class 2606 OID 18613)
-- Name: calcFluxes calcFluxes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."calcFluxes"
    ADD CONSTRAINT "calcFluxes_pkey" PRIMARY KEY (id);


--
-- TOC entry 3219 (class 2606 OID 18624)
-- Name: calcFragments calcFragments_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."calcFragments"
    ADD CONSTRAINT "calcFragments_pkey" PRIMARY KEY (id);


--
-- TOC entry 3221 (class 2606 OID 18635)
-- Name: fittedData fittedData_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."fittedData"
    ADD CONSTRAINT "fittedData_pkey" PRIMARY KEY (id);


--
-- TOC entry 3223 (class 2606 OID 18637)
-- Name: fittedData fittedData_simulation_id_simulation_dateAndTime_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."fittedData"
    ADD CONSTRAINT "fittedData_simulation_id_simulation_dateAndTime_key" UNIQUE (simulation_id, "simulation_dateAndTime");


--
-- TOC entry 3225 (class 2606 OID 18648)
-- Name: fittedExchangeFluxStatistics fittedExchangeFluxStatistics_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."fittedExchangeFluxStatistics"
    ADD CONSTRAINT "fittedExchangeFluxStatistics_pkey" PRIMARY KEY (id);


--
-- TOC entry 3227 (class 2606 OID 18650)
-- Name: fittedExchangeFluxStatistics fittedExchangeFluxStatistics_simulation_id_simulation_dateA_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."fittedExchangeFluxStatistics"
    ADD CONSTRAINT "fittedExchangeFluxStatistics_simulation_id_simulation_dateA_key" UNIQUE (simulation_id, "simulation_dateAndTime", flux_units);


--
-- TOC entry 3229 (class 2606 OID 18661)
-- Name: fittedExchangeFluxes fittedExchangeFluxes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."fittedExchangeFluxes"
    ADD CONSTRAINT "fittedExchangeFluxes_pkey" PRIMARY KEY (id);


--
-- TOC entry 3231 (class 2606 OID 18663)
-- Name: fittedExchangeFluxes fittedExchangeFluxes_simulation_id_simulation_dateAndTime_r_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."fittedExchangeFluxes"
    ADD CONSTRAINT "fittedExchangeFluxes_simulation_id_simulation_dateAndTime_r_key" UNIQUE (simulation_id, "simulation_dateAndTime", rxn_id, flux_exchange_units);


--
-- TOC entry 3233 (class 2606 OID 18674)
-- Name: fittedFluxStatistics fittedFluxStatistics_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."fittedFluxStatistics"
    ADD CONSTRAINT "fittedFluxStatistics_pkey" PRIMARY KEY (id);


--
-- TOC entry 3235 (class 2606 OID 18676)
-- Name: fittedFluxStatistics fittedFluxStatistics_simulation_id_simulation_dateAndtime_f_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."fittedFluxStatistics"
    ADD CONSTRAINT "fittedFluxStatistics_simulation_id_simulation_dateAndtime_f_key" UNIQUE (simulation_id, "simulation_dateAndtime", flux_units);


--
-- TOC entry 3237 (class 2606 OID 18687)
-- Name: fittedFluxes fittedFluxes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."fittedFluxes"
    ADD CONSTRAINT "fittedFluxes_pkey" PRIMARY KEY (id);


--
-- TOC entry 3239 (class 2606 OID 18689)
-- Name: fittedFluxes fittedFluxes_simulation_id_simulation_dateAndTime_rxn_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."fittedFluxes"
    ADD CONSTRAINT "fittedFluxes_simulation_id_simulation_dateAndTime_rxn_id_key" UNIQUE (simulation_id, "simulation_dateAndTime", rxn_id);


--
-- TOC entry 3241 (class 2606 OID 18702)
-- Name: fittedFragments fittedFragments_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."fittedFragments"
    ADD CONSTRAINT "fittedFragments_pkey" PRIMARY KEY (id);


--
-- TOC entry 3243 (class 2606 OID 18704)
-- Name: fittedFragments fittedFragments_simulation_id_simulation_dateAndTime_time_p_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."fittedFragments"
    ADD CONSTRAINT "fittedFragments_simulation_id_simulation_dateAndTime_time_p_key" UNIQUE (simulation_id, "simulation_dateAndTime", time_point, fragment_id, fragment_mass);


--
-- TOC entry 3245 (class 2606 OID 18715)
-- Name: fittedMeasuredFluxResiduals fittedMeasuredFluxResiduals_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."fittedMeasuredFluxResiduals"
    ADD CONSTRAINT "fittedMeasuredFluxResiduals_pkey" PRIMARY KEY (id);


--
-- TOC entry 3249 (class 2606 OID 18728)
-- Name: fittedMeasuredFluxes fittedMeasuredFluxes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."fittedMeasuredFluxes"
    ADD CONSTRAINT "fittedMeasuredFluxes_pkey" PRIMARY KEY (id);


--
-- TOC entry 3251 (class 2606 OID 18730)
-- Name: fittedMeasuredFluxes fittedMeasuredFluxes_simulation_id_simulation_dateAndTime_r_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."fittedMeasuredFluxes"
    ADD CONSTRAINT "fittedMeasuredFluxes_simulation_id_simulation_dateAndTime_r_key" UNIQUE (simulation_id, "simulation_dateAndTime", rxn_id);


--
-- TOC entry 3253 (class 2606 OID 18744)
-- Name: fittedMeasuredFragmentResiduals fittedMeasuredFragmentResidua_simulation_id_simulation_date_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."fittedMeasuredFragmentResiduals"
    ADD CONSTRAINT "fittedMeasuredFragmentResidua_simulation_id_simulation_date_key" UNIQUE (simulation_id, "simulation_dateAndTime", time_point, fragment_id, fragment_mass);


--
-- TOC entry 3255 (class 2606 OID 18742)
-- Name: fittedMeasuredFragmentResiduals fittedMeasuredFragmentResiduals_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."fittedMeasuredFragmentResiduals"
    ADD CONSTRAINT "fittedMeasuredFragmentResiduals_pkey" PRIMARY KEY (id);


--
-- TOC entry 3257 (class 2606 OID 18766)
-- Name: fittedMeasuredFragments fittedMeasuredFragments_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."fittedMeasuredFragments"
    ADD CONSTRAINT "fittedMeasuredFragments_pkey" PRIMARY KEY (id);


--
-- TOC entry 3259 (class 2606 OID 18768)
-- Name: fittedMeasuredFragments fittedMeasuredFragments_simulation_id_simulation_dateAndTim_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."fittedMeasuredFragments"
    ADD CONSTRAINT "fittedMeasuredFragments_simulation_id_simulation_dateAndTim_key" UNIQUE (simulation_id, "simulation_dateAndTime", fragment_id);


--
-- TOC entry 3261 (class 2606 OID 18779)
-- Name: fittedNetFluxStatistics fittedNetFluxStatistics_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."fittedNetFluxStatistics"
    ADD CONSTRAINT "fittedNetFluxStatistics_pkey" PRIMARY KEY (id);


--
-- TOC entry 3263 (class 2606 OID 18781)
-- Name: fittedNetFluxStatistics fittedNetFluxStatistics_simulation_id_simulation_dateAndTim_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."fittedNetFluxStatistics"
    ADD CONSTRAINT "fittedNetFluxStatistics_simulation_id_simulation_dateAndTim_key" UNIQUE (simulation_id, "simulation_dateAndTime", flux_units);


--
-- TOC entry 3265 (class 2606 OID 18792)
-- Name: fittedNetFluxes fittedNetFluxes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."fittedNetFluxes"
    ADD CONSTRAINT "fittedNetFluxes_pkey" PRIMARY KEY (id);


--
-- TOC entry 3267 (class 2606 OID 18794)
-- Name: fittedNetFluxes fittedNetFluxes_simulation_id_simulation_dateAndTime_rxn_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."fittedNetFluxes"
    ADD CONSTRAINT "fittedNetFluxes_simulation_id_simulation_dateAndTime_rxn_id_key" UNIQUE (simulation_id, "simulation_dateAndTime", rxn_id, flux_units);


--
-- TOC entry 3269 (class 2606 OID 18807)
-- Name: measuredFluxes measuredFluxes_experiment_id_model_id_sample_name_abbreviat_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."measuredFluxes"
    ADD CONSTRAINT "measuredFluxes_experiment_id_model_id_sample_name_abbreviat_key" UNIQUE (experiment_id, model_id, sample_name_abbreviation, rxn_id);


--
-- TOC entry 3271 (class 2606 OID 18805)
-- Name: measuredFluxes measuredFluxes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."measuredFluxes"
    ADD CONSTRAINT "measuredFluxes_pkey" PRIMARY KEY (id);


--
-- TOC entry 3273 (class 2606 OID 18818)
-- Name: measuredFragments measuredFragments_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."measuredFragments"
    ADD CONSTRAINT "measuredFragments_pkey" PRIMARY KEY (id);


--
-- TOC entry 3275 (class 2606 OID 18829)
-- Name: measuredPools measuredPools_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."measuredPools"
    ADD CONSTRAINT "measuredPools_pkey" PRIMARY KEY (id);


--
-- TOC entry 3277 (class 2606 OID 18840)
-- Name: modelMetabolites modelMetabolites_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."modelMetabolites"
    ADD CONSTRAINT "modelMetabolites_pkey" PRIMARY KEY (id);


--
-- TOC entry 3279 (class 2606 OID 18851)
-- Name: modelPathways modelPathways_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."modelPathways"
    ADD CONSTRAINT "modelPathways_pkey" PRIMARY KEY (id, model_id, pathway_id);


--
-- TOC entry 3281 (class 2606 OID 18862)
-- Name: modelReactions modelReactions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."modelReactions"
    ADD CONSTRAINT "modelReactions_pkey" PRIMARY KEY (id);


--
-- TOC entry 3283 (class 2606 OID 18873)
-- Name: models models_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.models
    ADD CONSTRAINT models_pkey PRIMARY KEY (id);


--
-- TOC entry 3247 (class 2606 OID 18717)
-- Name: fittedMeasuredFluxResiduals s; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."fittedMeasuredFluxResiduals"
    ADD CONSTRAINT s UNIQUE (simulation_id, "simulation_dateAndTime", time_point, rxn_id);


--
-- TOC entry 3287 (class 2606 OID 18895)
-- Name: simulationParameters simulationParameters_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."simulationParameters"
    ADD CONSTRAINT "simulationParameters_pkey" PRIMARY KEY (id);


--
-- TOC entry 3289 (class 2606 OID 18897)
-- Name: simulationParameters simulationParameters_simulation_id_simulation_dateAndTime_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."simulationParameters"
    ADD CONSTRAINT "simulationParameters_simulation_id_simulation_dateAndTime_key" UNIQUE (simulation_id, "simulation_dateAndTime");


--
-- TOC entry 3285 (class 2606 OID 18884)
-- Name: simulation simulation_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.simulation
    ADD CONSTRAINT simulation_pkey PRIMARY KEY (id);


--
-- TOC entry 3291 (class 2606 OID 18911)
-- Name: tracers tracers_met_id_met_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tracers
    ADD CONSTRAINT tracers_met_id_met_name_key UNIQUE (met_id, met_name);


--
-- TOC entry 3293 (class 2606 OID 18909)
-- Name: tracers tracers_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tracers
    ADD CONSTRAINT tracers_pkey PRIMARY KEY (id);


--
-- TOC entry 3207 (class 2606 OID 18557)
-- Name: xxxxx_MDVFragments xxxxx_MDVFragments_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."xxxxx_MDVFragments"
    ADD CONSTRAINT "xxxxx_MDVFragments_pkey" PRIMARY KEY (met_id);


--
-- TOC entry 3304 (class 2606 OID 18301)
-- Name: A_TECHNOLOGY_MICROARRAY id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."A_TECHNOLOGY_MICROARRAY"
    ADD CONSTRAINT "A_TECHNOLOGY_MICROARRAY_Assay_ID_fkey" FOREIGN KEY ("Assay_ID") REFERENCES public."ASSAY"("Assay_ID") NOT VALID;


--
-- TOC entry 3303 (class 2606 OID 17603)
-- Name: A_TECHNOLOGY_MICROARRAY A_TECHNOLOGY_MICROARRAY_Sample_Name_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."A_TECHNOLOGY_MICROARRAY"
    ADD CONSTRAINT "A_TECHNOLOGY_MICROARRAY_Sample_Name_fkey" FOREIGN KEY ("Sample_Name") REFERENCES public."STUDY_SAMPLES"("Sample_Name") NOT VALID;


--
-- TOC entry 3306 (class 2606 OID 18306)
-- Name: A_TECHNOLOGY_MS id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."A_TECHNOLOGY_MS"
    ADD CONSTRAINT "A_TECHNOLOGY_MS_Assay_ID_fkey" FOREIGN KEY ("Assay_ID") REFERENCES public."ASSAY"("Assay_ID") NOT VALID;


--
-- TOC entry 3305 (class 2606 OID 17608)
-- Name: A_TECHNOLOGY_MS A_TECHNOLOGY_MS_Sample_Name_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."A_TECHNOLOGY_MS"
    ADD CONSTRAINT "A_TECHNOLOGY_MS_Sample_Name_fkey" FOREIGN KEY ("Sample_Name") REFERENCES public."STUDY_SAMPLES"("Sample_Name") NOT VALID;


--
-- TOC entry 3308 (class 2606 OID 18311)
-- Name: A_TECHNOLOGY_NMR id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."A_TECHNOLOGY_NMR"
    ADD CONSTRAINT "A_TECHNOLOGY_NMR_Assay_ID_fkey" FOREIGN KEY ("Assay_ID") REFERENCES public."ASSAY"("Assay_ID") NOT VALID;


--
-- TOC entry 3307 (class 2606 OID 17613)
-- Name: A_TECHNOLOGY_NMR A_TECHNOLOGY_NMR_Sample_Name_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."A_TECHNOLOGY_NMR"
    ADD CONSTRAINT "A_TECHNOLOGY_NMR_Sample_Name_fkey" FOREIGN KEY ("Sample_Name") REFERENCES public."STUDY_SAMPLES"("Sample_Name") NOT VALID;


--
-- TOC entry 3295 (class 2606 OID 17689)
-- Name: INVESTIGATION INVESTIGATION_Investigation_Identifier_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."INVESTIGATION"
    ADD CONSTRAINT "INVESTIGATION_Investigation_Identifier_fkey" FOREIGN KEY ("Investigation_Identifier") REFERENCES public."ONTOLOGY_SOURCE_REFERENCE"("Ontology_REF_Investigation_Identifier") NOT VALID;


--
-- TOC entry 3294 (class 2606 OID 17682)
-- Name: INVESTIGATION INVESTIGATION_Investigation_Study_Identifier_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."INVESTIGATION"
    ADD CONSTRAINT "INVESTIGATION_Investigation_Study_Identifier_fkey" FOREIGN KEY ("Investigation_Study_Identifier") REFERENCES public."STUDY"("Study_Identifier") NOT VALID;


--
-- TOC entry 3314 (class 2606 OID 18458)
-- Name: MzTab_M_Small_Molecule_Evidence_SME_Section MzTab_M_Small_Molecule_Evidence_SME_Section_SME_ID_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."MzTab_M_Small_Molecule_Evidence_SME_Section"
    ADD CONSTRAINT "MzTab_M_Small_Molecule_Evidence_SME_Section_SME_ID_fkey" FOREIGN KEY ("SME_ID") REFERENCES public."MzTab_M_Small_Molecule_Feature_SMF_Section"("SME_ID_REFS") NOT VALID;


--
-- TOC entry 3313 (class 2606 OID 18451)
-- Name: MzTab_M_Small_Molecule_Feature_SMF_Section MzTab_M_Small_Molecule_Feature_SMF_Section_SMF_ID_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."MzTab_M_Small_Molecule_Feature_SMF_Section"
    ADD CONSTRAINT "MzTab_M_Small_Molecule_Feature_SMF_Section_SMF_ID_fkey" FOREIGN KEY ("SMF_ID") REFERENCES public."MzTab_M_small_molecule_section"("SMF_ID_REFS") NOT VALID;


--
-- TOC entry 3312 (class 2606 OID 18444)
-- Name: MzTab_M_small_molecule_section MzTab_M_small_molecule_section_mzTab_ID_REFS_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."MzTab_M_small_molecule_section"
    ADD CONSTRAINT "MzTab_M_small_molecule_section_mzTab_ID_REFS_fkey" FOREIGN KEY ("mzTab_ID_REFS") REFERENCES public."MzTab_M_Metadata_metabolomics"("mzTab_ID") NOT VALID;


--
-- TOC entry 3309 (class 2606 OID 18370)
-- Name: MzTab_PSM_section MzTab_PSM section_accession_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."MzTab_PSM_section"
    ADD CONSTRAINT "MzTab_PSM section_accession_fkey" FOREIGN KEY (accession) REFERENCES public."MzTab_Peptide_section"(accession) NOT VALID;


--
-- TOC entry 3311 (class 2606 OID 18365)
-- Name: MzTab_Peptide_section MzTab_Peptide section_accession_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."MzTab_Peptide_section"
    ADD CONSTRAINT "MzTab_Peptide section_accession_fkey" FOREIGN KEY (accession) REFERENCES public."MzTab_Protein_section"(accession) NOT VALID;


--
-- TOC entry 3310 (class 2606 OID 18360)
-- Name: MzTab_Protein_section MzTab_Protein section_mzTab_ID_REFS_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."MzTab_Protein_section"
    ADD CONSTRAINT "MzTab_Protein section_mzTab-ID_REFS_fkey" FOREIGN KEY ("mzTab_ID_REFS") REFERENCES public."MzTab_Metadata_Proteomics"("mzTab-ID") NOT VALID;


--
-- TOC entry 3302 (class 2606 OID 17658)
-- Name: STUDY_SAMPLES STUDY_SAMPLES_Study_ID_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."STUDY_SAMPLES"
    ADD CONSTRAINT "STUDY_SAMPLES_Study_ID_fkey" FOREIGN KEY ("Study_ID") REFERENCES public."STUDY"("Study_ID") NOT VALID;


--
-- TOC entry 3296 (class 2606 OID 17628)
-- Name: STUDY STUDY_Study_Assays_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."STUDY"
    ADD CONSTRAINT "STUDY_Study_Assays_fkey" FOREIGN KEY ("Study_Assays") REFERENCES public."ASSAY"("Assay_ID") NOT VALID;


--
-- TOC entry 3297 (class 2606 OID 17633)
-- Name: STUDY STUDY_Study_Contact_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."STUDY"
    ADD CONSTRAINT "STUDY_Study_Contact_fkey" FOREIGN KEY ("Study_Contact") REFERENCES public."CONTACTS"("Contact_Person_ID") NOT VALID;


--
-- TOC entry 3298 (class 2606 OID 17638)
-- Name: STUDY STUDY_Study_Design_Descriptors_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."STUDY"
    ADD CONSTRAINT "STUDY_Study_Design_Descriptors_fkey" FOREIGN KEY ("Study_Design_Descriptors") REFERENCES public."STUDY_DESIGN_DESCRIPTORS"("Design_Descriptors_ID") NOT VALID;


--
-- TOC entry 3299 (class 2606 OID 17643)
-- Name: STUDY STUDY_Study_Factors_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."STUDY"
    ADD CONSTRAINT "STUDY_Study_Factors_fkey" FOREIGN KEY ("Study_Factors") REFERENCES public."STUDY_FACTORS"("Study_Factors_ID") NOT VALID;


--
-- TOC entry 3300 (class 2606 OID 17648)
-- Name: STUDY STUDY_Study_ID_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."STUDY"
    ADD CONSTRAINT "STUDY_Study_ID_fkey" FOREIGN KEY ("Study_ID") REFERENCES public."PROTOCOLS"("Protocol_ID") NOT VALID;


--
-- TOC entry 3301 (class 2606 OID 17653)
-- Name: STUDY STUDY_Study_Publications_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."STUDY"
    ADD CONSTRAINT "STUDY_Study_Publications_fkey" FOREIGN KEY ("Study_Publications") REFERENCES public."PUBLICATIONS"("Publication_ID") NOT VALID;


-- Completed on 2020-11-12 21:39:34

--
-- PostgreSQL database dump complete
--
