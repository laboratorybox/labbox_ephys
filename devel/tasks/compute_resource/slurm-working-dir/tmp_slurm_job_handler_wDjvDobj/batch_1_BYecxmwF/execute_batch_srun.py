#!/usr/bin/env python

import sys
import os
import time
import json
import random
import traceback
import kachery as ka
from hither2 import FileLock
from hither2 import _deserialize_job, _serialize_item

working_dir = 'slurm-working-dir/tmp_slurm_job_handler_wDjvDobj/batch_1_BYecxmwF'
num_workers = 4
running_fname = 'slurm-working-dir/tmp_slurm_job_handler_wDjvDobj/batch_1_BYecxmwF/running.txt'

kachery_config = json.loads('{"to": {"url": null, "channel": null, "password": null}, "fr": {"url": null, "channel": null, "password": null}, "from_remote_only": false, "to_remote_only": false, "algorithm": "sha1", "verbose": false}')
try:
    import kachery as ka
    ka.set_config(**kachery_config)
except:
    pass

slurm_started_fname = working_dir + '/slurm_started.txt'
with FileLock(slurm_started_fname + '.lock', exclusive=True):
    with open(slurm_started_fname, 'w') as f:
        f.write('slurm is running.')

# Let's claim a place and determine which worker number we are
worker_num = None
# wait a random amount of time before starting
time.sleep(random.uniform(0, 0.1))
for i in range(num_workers):
    fname = working_dir + '/worker_{}_claimed.txt'.format(i)
    if not os.path.exists(fname):
        with FileLock(fname + '.lock', exclusive=True):
            if not os.path.exists(fname):
                with open(fname, 'w') as f:
                    f.write('claimed')
                worker_num = i
                break
if worker_num is None:
    raise Exception('Unable to claim worker file.')

job_fname = working_dir + '/worker_{}_job.json'.format(worker_num)
result_fname = working_dir + '/worker_{}_result.json'.format(worker_num)

try:  # We are going to catch any exceptions and report them back to the parent process
    num_found = 0
    num_exceptions = 0
    while True:
        # Check whether running file exists
        try:
            with FileLock(running_fname + '.lock', exclusive=False):
                if not os.path.exists(running_fname):
                    print('Stopping worker.')
                    break
        except:
            if not os.path.exists(working_dir):
                print('Working directory does not exist. Stopping worker.')
                break
            traceback.print_exc()
            print('WARNING: Unexpected problem checking for running file in worker. Trying to continue.')
            num_exceptions = num_exceptions + 1
            if num_exceptions >= 5:
                raise Exception('Problem checking for running file in worker. Too many exceptions. Aborting')
            time.sleep(3)

        # Check to see if we have a job to do
        job_serialized = None
        try:
            with FileLock(job_fname + '.lock', exclusive=False):
                if (os.path.exists(job_fname)) and not (os.path.exists(result_fname)):
                    num_found = num_found + 1
                    with open(job_fname, 'r') as f:
                        job_serialized = json.load(f)
        except:
            traceback.print_exc()
            print('WARNING: Unexpected problem loading job object file in worker. Trying to continue.')
            num_exceptions = num_exceptions + 1
            if num_exceptions >= 5:
                raise Exception('Problem loading job object file in worker. Too many exceptions. Aborting')
            time.sleep(3)
                        
        # If we have a job to do, then let's do it
        if job_serialized:
            job = _deserialize_job(job_serialized)
            job._execute()
            result = dict(
                result=job._result,
                status=job._status,
                exception=job._exception,
                runtime_info=job._runtime_info
            )
            result_serialized = _serialize_item(result)
            with FileLock(result_fname + '.lock', exclusive=True):
                with open(result_fname, 'w') as f:
                    # Write the result
                    json.dump(result_serialized, f)
        time.sleep(0.2)
except:
    # report the exception back to the parent process by writing a _result.json.error file
    with FileLock(result_fname + '.lock', exclusive=True):
        with open(result_fname + ".error", 'w') as f:
            f.write(traceback.format_exc())
            