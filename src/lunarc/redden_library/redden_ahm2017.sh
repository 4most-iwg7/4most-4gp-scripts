#!/bin/sh
# requesting the number of nodes needed
#
# job time, change for what your job requires
#SBATCH -t 24:00:00
#SBATCH --exclusive
#
# job name and output file names
#SBATCH -J redden_ahm2017
#SBATCH -o stdout_redden_ahm2017_%j.out
#SBATCH -e stderr_redden_ahm2017_%j.out
cat $0

# Add the software packages which 4GP depends upon
module add GCC/4.9.3-binutils-2.25  OpenMPI/1.8.8 CFITSIO/3.38  GCCcore/6.4.0 SQLite/3.20.1 Anaconda3

# Activate the conda python environment

# This line used to work up until Feb 2019...
source activate myenv

# ... but since it's stopped working, this line makes sure we use the right python ...
export PATH="/home/dominic/.conda/envs/myenv/bin:$PATH"

# Rsync the spectrum libraries that we're going to run through the reddening code onto a local
# disk on the worker node. This is necessary as aurora tends to go into
# spin-lock reading data from the astro3 disk.
cd /projects/astro3/nobackup/dominic/iwg7_pipeline/4most-4gp-scripts/src/scripts/degrade_spectra/
echo Starting rsync: `date`
echo Temporary directory: ${TMPDIR}/workspace
mkdir ${TMPDIR}/workspace
rsync -a ../../../workspace/turbospec_ahm2017_perturbed ${TMPDIR}/workspace/
echo Rsync done: `date`
echo Running reddening script: `date`

# Now we actually run the reddening code
python3 redden_library.py --input-library turbospec_ahm2017_perturbed \
                          --workspace "${TMPDIR}/workspace" \
                          --output-library reddened_ahm2017_perturbed

# Once the code is done, we rsync the results from local storage back onto a shared disk
echo Starting rsync: `date`
rsync -a ${TMPDIR}/workspace/reddened_* ../../../workspace
echo Rsync done: `date`

