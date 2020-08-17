from python:3.7

copy requirements.txt ./

# install the requirements, don't store the cache in the container
run pip3 install --no-cache-dir -r requirements.txt

# run /bin/bash first to let users develop inside
cmd /bin/bash
