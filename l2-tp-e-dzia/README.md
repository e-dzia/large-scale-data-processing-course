# L2 - 2019

## Scope

1. Docker - Dockerfile, docker-compose, containers in general
2. Python - pip, requirements
3. Celery
4. Task queue


## Tasks

1. Investigate existing codebase:
    - why we use a broker
      - to send messages
    - why there is no broker URL defined in code
      - it is defined in docker-compose (?): `CELERY_BROKER_URL=amqp://guest:guest@rabbitmq:5672`
    - how the broker URL is build (what is guest etc.)
      - https://www.rabbitmq.com/uri-spec.html
      - `amqp://` - Advanced Message Queuing Protocol (AMQP)
      - `guest:guest` - username:password
      - `rabbitmq:5672` - host:port
    - change RabitMQ logs to appropriate severity (warning)
      - docker-compose:
      ```
      environment: 
         RABBITMQ_SERVER_ADDITIONAL_ERL_ARGS=-rabbit log [{console,[{level,warning}]}]
      ```
    - do tasks need to return results?
      - No, if we don't want to know the results.
      With return:
      ![return](return.png)
      No return:
      ![no-return](no-return.png)
    - can we schedule periodical tasks?
      - Yes. Sample code:
        ```python
        from celery import Celery
        from celery.schedules import crontab
        
        app = Celery()
        
        @app.on_after_configure.connect
        def setup_periodic_tasks(sender, **kwargs):
            # Calls test('hello') every 10 seconds.
            sender.add_periodic_task(10.0, test.s('hello'), name='add every 10')
            
            # Calls test('world') every 30 seconds
            sender.add_periodic_task(30.0, test.s('world'), expires=10)
            
            # Executes every Monday morning at 7:30 a.m.
            sender.add_periodic_task(
                crontab(hour=7, minute=30, day_of_week=1),
                test.s('Happy Mondays!'),
            )
        
        @app.task
        def test(arg):
            print(arg)
        ```
    - why the worker is logging twice? can we fix that?
      - https://stackoverflow.com/questions/45340837/prevent-duplicate-celery-logging
      - >The logging system is basically a tree of logginig.Logger objects with main logging.Logger in the root of the tree (you get the root with call logging.getLogger() without parameters).
        >
        >When you call logging.getLogger("child") you get reference to the logging.Logger processing the "child" logs. The problem is when you call logging.getLogger("child").info() the info message is delivered to the "child" but also to the parent of the "child" and to its parent until it arrives to the root.
        >
        >To avoid sending logs to the parent you have to setup the `logging.getLogger("child").propagate = False`.
    - why we can see celery errors at the beginning?
      - Because the RabbitMQ server didn't start yet.
    - what is the context of docker image building process defined in docker-compose file?
      - current dir (.)
    - can we somehow exclude some files from docker image building context?
      - .dockerignore file
2. Decide if you are using an API approach or scrapping based approach. Create fine-grained tasks for everything.
    - Scrapping approach
        1. Implement Reddit submission URL provider that will create appropriate tasks
        2. Implement submission scrapper that utilizes the provided URL and fetch submission data:
             - check further tasks to know what date you will need
    - API approach
        1. Get credentials
        2. Select client lib
        3. Create code that will create tasks required for submission fetching
        4. Create code that will consume tasks and fetch submissions
3. Take care of new submissions fetching. Add appropriate task scheduling, that will fetch new submissions. (How to check if the submission is new? Utilize current time, submission creation time, schedule interval)
4. Add process monitoring:
    - Utilize Prometheus or InfluxDB (add them to docker-compose, remember about volumes for data persistency)
    - Publish some metrics about the data fetching process (submission counts, lengths, properties distributions, timings etc.) at least:
        - submission fetch times (avg, histogram)
          - `submission_fetch_time_sum/submission_fetch_time_count`
        - 2 counters 
        - 2 distributions (histogram)
    - publish general celery metrics (you can use a library)
    - Visualize metrics using Grafana (add it to docker-compose, remember about volume for dashboard persistency)



##### Notes

Prometheus server: http://0.0.0.0:9090/

Useful page to test if endpoints are working: http://0.0.0.0:9090/targets

Grafana server: http://localhost:3000/
 
In Grafana, set Data Source and add HTTP URL http://0.0.0.0:9090 and name Prometheus.
Then add new dashboard and add query as in Prometheus main page.
