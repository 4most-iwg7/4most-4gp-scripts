#!/bin/sh
# requesting the number of nodes needed
#
# job time, change for what your job requires
#SBATCH -t 48:00:00
#
# job name and output file names
#SBATCH -J 4fs_ahm2017_perturbed
#SBATCH -o stdout_4fs_ahm2017_perturbed_%j.out
#SBATCH -e stderr_4fs_ahm2017_perturbed_%j.out
cat $0

# NOTE THAT THE 4FS EXPOSURE TIME CALCULATOR RUNS *HORRENDOUSLY* SLOWLY ON
# LUNARC. It does lots of file accesses, which the filing system on Aurora
# is not optimised for. It will probably run much faster on your laptop.

# Add the software packages which 4FS depends upon
module add GCC/4.9.3-binutils-2.25  OpenMPI/1.8.8 CFITSIO/3.38  GCCcore/6.4.0 SQLite/3.20.1 Anaconda3

# This line used to work up until Feb 2019...
source activate myenv

# ... but since it's stopped working, this line makes sure we use the right python ...
export PATH="/home/dominic/.conda/envs/myenv/bin:$PATH"

# Rsync the spectrum libraries that we're going to run through 4FS onto a local
# disk on the worker node. This is necessary as aurora tends to go into
# spin-lock reading data from the astro3 disk.
cd /projects/astro3/nobackup/dominic/iwg7_pipeline/4most-4gp-scripts/src/scripts/degrade_spectra/
echo Starting rsync: `date`
echo Temporary directory: ${TMPDIR}/workspace
mkdir ${TMPDIR}/workspace
rsync -a ../../../workspace/turbospec_ahm2017_perturbed ${TMPDIR}/workspace/
echo Rsync done: `date`
echo Running 4fs script: `date`

# Now we actually run 4FS
python3 degrade_library_with_4fs.py --input-library turbospec_ahm2017_perturbed \
                                    --workspace "${TMPDIR}/workspace" \
                                    --snr-list "10,12,14,16,18,20,23,26,30,35,40,45,50,80,100,130,180,250" \
                                    --output-library-lrs 4fs_ahm2017_perturbed_lrs \
                                    --output-library-hrs 4fs_ahm2017_perturbed_hrs

# Once 4FS is done, we rsync the results from local storage back onto a shared disk
echo Starting rsync: `date`
rsync -a ${TMPDIR}/workspace/4fs_* ../../../workspace
echo Rsync done: `date`

