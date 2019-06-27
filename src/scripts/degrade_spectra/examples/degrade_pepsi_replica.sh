#!/bin/bash

# A little bit of scripting magic so that whatever directory this script is
# run from, we always find the python scripts and data we need.
cd "$(dirname "$0")"
cwd=`pwd`/..
cd ${cwd}

# Activate python virtual environment
source ../../../../virtualenv/bin/activate

# Now do some work
python3 degrade_library_with_4fs.py --input-library turbospec_turbo_pepsi_replica_3label \
                                    --snr-list "10000" \
                                    --output-library-lrs turbospec_turbo_pepsi_replica_3label_lrs \
                                    --output-library-hrs turbospec_turbo_pepsi_replica_3label_hrs


python3 degrade_library_with_4fs.py --input-library turbospec_turbo_pepsi_replica_4label \
                                    --snr-list "10000" \
                                    --output-library-lrs turbospec_turbo_pepsi_replica_4label_lrs \
                                    --output-library-hrs turbospec_turbo_pepsi_replica_4label_hrs

