
/* Generic features */
//#define PARTIAL_PERIODIC
//#define EXTERNAL_FORCES
//#define MASS
//#define EXCLUSIONS
//#define BOND_CONSTRAINT
//#define LANGEVIN_PER_PARTICLE
//#define COLLISION_DETECTION
//#define METADYNAMICS
//#define NPT
//#define SWIMMER_REACTIONS
//#define ENGINE
//#define PARTICLE_ANISOTROPY
//#define LEES_EDWARDS

/* Rotation */
//#define ROTATION
//#define ROTATIONAL_INERTIA

/* Electrostatics */
//#define ELECTROSTATICS
//#define INTER_RF
//#define MMM1D_GPU
//#define EWALD_GPU
//#define _P3M_GPU_FLOAT


/* Magnetostatics */
//#define DIPOLES


/* Virtual sites features */
//#define VIRTUAL_SITES
//#define VIRTUAL_SITES_RELATIVE

//#define VIRTUAL_SITES_INERTIALESS_TRACERS

/* DPD features */
#define DPD
#define LEES_EDWARDS

/* Lattice-Boltzmann features */
//#define LB
//#define LB_GPU
//#define LB_BOUNDARIES
//#define LB_BOUNDARIES_GPU
//#define LB_ELECTROHYDRODYNAMICS
//#define ELECTROKINETICS
//#define EK_BOUNDARIES
//#define EK_ELECTROSTATIC_COUPLING
//#define EK_DEBUG
//#define EK_DOUBLE_PREC
//#define SHANCHEN


/* Interaction features */
//#define TABULATED
//#define LENNARD_JONES
//#define WCA
//#define LJ_WARN_WHEN_CLOSE
//#define LENNARD_JONES_GENERIC
//#define LJCOS
//#define LJCOS2
//#define LJGEN_SOFTCORE
//#define COS2
//#define GAY_BERNE
//#define SMOOTH_STEP
//#define HERTZIAN
//#define GAUSSIAN
//#define BMHTF_NACL
//#define MORSE
//#define BUCKINGHAM
//#define SOFT_SPHERE
#define HAT
//#define UMBRELLA
//#define OVERLAPPED
//#define THOLE

/* Fluid-Structure Interactions (object in fluid) */
//#define OIF_LOCAL_FORCES
//#define OIF_GLOBAL_FORCES
//#define AFFINITY
//#define MEMBRANE_COLLISION

//#define BOND_ANGLE

/* Immersed-Boundary Bayreuth version */
//#define IMMERSED_BOUNDARY
//#define SCAFACOS_DIPOLES

//#define EXPERIMENTAL_FEATURES

// Shape of the noise in the (Langevin) thermostat
//#define FLATNOISE
//#define GAUSSRANDOM
//#define GAUSSRANDOMCUT


/* Strange features. Use only if you know what you are doing! */
/* activate the old dihedral form */
//#define OLD_DIHEDRAL
/* turn off certain nonbonded interactions within molecules */
//#define NO_INTRA_NB


/* Debugging */
//#define ADDITIONAL_CHECKS

//#define ESIF_DEBUG
//#define COMM_DEBUG
//#define EVENT_DEBUG
//#define INTEG_DEBUG
//#define CELL_DEBUG
//#define GHOST_DEBUG
//#define LATTICE_DEBUG
//#define HALO_DEBUG
//#define GRID_DEBUG
//#define VERLET_DEBUG
//#define PARTICLE_DEBUG
//#define P3M_DEBUG
//#define FFT_DEBUG
//#define RANDOM_DEBUG
//#define FORCE_DEBUG
//#define THERMO_DEBUG
//#define LE_DEBUG
//#define LJ_DEBUG
//#define MORSE_DEBUG
//#define ESR_DEBUG
//#define ESK_DEBUG
//#define FENE_DEBUG
//#define GHOST_FORCE_DEBUG
//#define STAT_DEBUG
//#define POLY_DEBUG
//#define PTENSOR_DEBUG
//#define MAGGS_DEBUG
//#define LB_DEBUG
//#define VIRTUAL_SITES_DEBUG
//#define CUDA_DEBUG
//#define H5MD_DEBUG
//#define ICC_DEBUG


/* Single particle debugging */
//#define ONEPART_DEBUG
// which particle id to debug
//#define ONEPART_DEBUG_ID 13

