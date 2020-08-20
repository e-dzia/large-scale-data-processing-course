# L1 - 2019

## Scope

1. Linux - bash, ssh, scp, tmux, htop, kill, killall, pipe operator, ls, sed, vim, cat
2. Docker - Dockerfile, docker-compose, containers in general
3. Python - pip, virtualenv, requirements, tox
4. Parallelize computation in Python

## Tasks

1. Write shell (Bash) scripts, which:
    - copies certain files from one machine to another
    ```bash
    $ ./copy.sh <user@source-machine-IP:/path/to/files> <user@target-machine-IP:/path/to/files> <file-1> <file-2> ... <file-N>
    ```
    - runs an infinite command in background and kills the command (use: `&`, `kill/killall/pidof`)
    ```bash
    $ ./run-backgroud.sh <command-to-run>
    $ ./kill.sh <command-to-run>
    ```
    - filters an random data stream (use: `/dev/urandom`.  `sed/tr`)
    ```bash
    $ ./filter.sh
    ```
    
2. Proof that you can use Vim:
    - find an expression
    - jump to line
    - substitute a single character
    - substitute a whole expression
    - save changes
    - exit Vim (2 ways)

3. Write your own Dockerfile and create a script which builds and publishes it on: [https://hub.docker.com/](https://hub.docker.com/). Use following keywords in your Dockerfile:
    - `FROM`
    - `RUN`
    - `ADD`
    - `ENV`
    - `ARG`
    - `ENTRYPOINT`
    - `CMD`
    ```bash
    $ ./publish.sh </path/to/Dockerfile>
    ```

4. Create a docker-compose manifest with 2 containers, which communicate with each other.
   For example use a `nginx` docker for hosting some content and another `curl` container, 
   which checks if the resource is available. Use docker-compose version 3 and following 
   service attributes:
    - `links`
    - `restarts`
    - `resources`
    ```bash
    $ docker-compose up
    ```

5. Parallelization of computations in Python. Use the prepared code from directory `task_5/`
   to implement a linear regression model:
    - Implement an artificial dataset generator.
    ```bash
    $ python3 scripts/data-generator.py --num-samples <num-samples> --out-dir </path/to/datasets>
    ```
    - Implement linear regression models using:
        - Sequential computations (baseline)
        - Numpy
        - Threaded computation parallelization
        - Process-based computation parallelization
    - Generate plots, which show the execution times of the above models with respect to the size of the dataset
    ```bash
    $ PYTHONPATH=. python3 scripts/run-experiments.py --datasets-dir </path/to/datasets>
    ```
    - Ensure the code passes all tests and is well written using `tox`
    ```bash
    $ tox -v
    ```

