# L1 - 2019

## Task 3
Write your own Dockerfile and create a script which builds and publishes it on: [https://hub.docker.com/](https://hub.docker.com/). Use following keywords in your Dockerfile:
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

#### Notes

docker build -t test --build-arg varname=value .

docker run --env key=value [env-name]
