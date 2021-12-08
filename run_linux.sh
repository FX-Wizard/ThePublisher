#!/bin/bash
source /mnt/resources/PIPELINE/RND/virtual-env-linux/bin/activate
export PYTHONPATH=$PYTHONPATH;/mnt/resources/PIPELINE/RND/thePublisherGUI
python ./publisher_main.py