module load HDF5/1.10.1-intel-2018a git FFTW CMake GSL Boost/1.68.0-intel-2018a-Python-3.6.4 Doxygen/1.8.14-GCCcore-6.4.0

export CC=mpiicc
export CXX=mpiicpc
export FC=mpiifort
export FFTW3_ROOT=/apps/leuven/skylake/2018a/software/FFTW/3.3.8-intel-2018a

#mkdir build_debug
#cd build_debug
#cp ../myconfig.hpp .
mkdir build
cd build

python -m venv mdenv
source mdenv/bin/activate
pip install --upgrade pip
pip install tidynamics matplotlib numpy h5py scipy
pip install --upgrade cython

cmake ..

make -j 12
