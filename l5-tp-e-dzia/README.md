# L5 - 2019

## Scope
1. Kubernetes
2. K3s
3. Helm
4. Docker
5. Application deployment

## Tasks
1. **Infrastructure setup**

    - using your AWS account create at least 3 EC2 machines with Ubuntu 18.04 (or any other OS you are familiar with)
    - one machine will act as the Kubernetes master, the other ones will be worker nodes
    - choose appropriate machine flavours (at least 2 CPU and 2 GB RAM)

2. **K3s cluster installation**
    ```bash
    sudo apt-get update && sudo apt-get install -y apt-transport-https
    curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
    echo "deb https://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee -a /etc/apt/sources.list.d/kubernetes.list
    sudo apt-get update
    sudo apt-get install -y kubectl 
   ```

    - K3s is a lightweight version of Kubernetes, which is also easier to setup
    - read K3s' [documentation](https://rancher.com/docs/k3s/latest/en/quick-start/)
    - install all required software on the machines (including containerd and Docker)
    - following the guide, provision a K3s cluster with one master node and 2 worker nodes
    - remember to set appropriate firewall rules!
    - while installing the K3s agents make sure those will use Docker (see documentation)
    - obtain `kubeconfig` file and save it to your local machine (also install `kubectl`)
    - instead of manually installing K3s you can also use [k3sup](https://github.com/alexellis/k3sup)

    (https://rancher.com/blog/2019/k3s-kubeconfig-in-seconds)
    ```bash
    k3sup install --ip $MASTER --user ubuntu --ssh-key /home/edzia/.ssh/lsdp.pem
    k3sup join --ip $WORKER1 --server-ip $MASTER --user ubuntu --ssh-key /home/edzia/.ssh/lsdp.pem
    k3sup join --ip $WORKER2 --server-ip $MASTER --user ubuntu --ssh-key /home/edzia/.ssh/lsdp.pem
    export KUBECONFIG=/home/edzia/kubeconfig
    kubectl get node -o wide
    ```
   - uninstall (manually on nodes)
   ```bash
    /usr/local/bin/k3s-uninstall.sh  # master
    /usr/local/bin/k3s-agent-uninstall.sh  # workers
    ```

3. **Kubernetes objects & manifests**

    - [documentation](https://kubernetes.io/docs/concepts/)
    - what is the difference between a Docker container and a Kubernetes Pod?
        - "When you created a Deployment in Module 2, Kubernetes created a Pod to host your application instance. A Pod is a Kubernetes abstraction that represents a group of one or more application containers (such as Docker or rkt), and some shared resources for those containers. Those resources include:
            Shared storage, as Volumes
            Networking, as a unique cluster IP address
            Information about how to run each container, such as the container image version or specific ports to use"
            (https://kubernetes.io/docs/tutorials/kubernetes-basics/explore/explore-intro/)
    - what are the following Kubernetes objects and what are they used for?
        - deployment - "You describe a desired state in a Deployment, and the Deployment Controller changes the actual state to the desired state at a controlled rate. You can define Deployments to create new ReplicaSets, or to remove existing Deployments and adopt all their resources with new Deployments." (https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
        - service - "An abstract way to expose an application running on a set of Pods as a network service." (https://kubernetes.io/docs/concepts/services-networking/service/)
        - daemonset - "A DaemonSet ensures that all (or some) Nodes run a copy of a Pod." (https://kubernetes.io/docs/concepts/workloads/controllers/daemonset/)
        - statefulset - "StatefulSet is the workload API object used to manage stateful applications." (https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/)
        - configmap - "ConfigMaps allow you to decouple configuration artifacts from image content to keep containerized applications portable." (https://kubernetes.io/docs/tasks/configure-pod-container/configure-pod-configmap/)
        - secret - "Kubernetes secret objects let you store and manage sensitive information, such as passwords, OAuth tokens, and ssh keys." (https://kubernetes.io/docs/concepts/configuration/secret/)
        - persistentvolume(claim) - "A PersistentVolume (PV) is a piece of storage in the cluster that has been provisioned by an administrator or dynamically provisioned using Storage Classes."
        "A PersistentVolumeClaim (PVC) is a request for storage by a user." (https://kubernetes.io/docs/concepts/storage/persistent-volumes/)
    - how to deploy these objects to your Kubernetes cluster?
    ```bash
    kubectl create -f examples/plain_manifests/configmap.yaml
    kubectl create -f examples/plain_manifests/deployment.yaml
    kubectl create -f examples/plain_manifests/service.yaml
   
    kubectl get pods -o wide
    ```
   (https://kubernetes.io/docs/tutorials/kubernetes-basics/explore/explore-intro/)
    - deploy the provided sample manifests (`examples/plain_manifests`),
      check if they were correctly deployed (`kubectl get`),
      explain what these manifests do,
      eventually, delete them from your cluster

4. **Helm**
    
    - [documentation](https://helm.sh/docs/)
    - in practice, you don't write manifests with hardcoded values and don't deploy 
      them manually one after the other
    - Helm is a package manager for Kubernetes application deployments
    - it provides a template engine for Kubernetes manifests and manages deployments (rolling updates, rollbacks etc.)
    - install the Helm CLI
    ```bash
    curl https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 > get_helm.sh
    chmod 700 get_helm.sh
    ./get_helm.sh
    ```
    - deploy the provided sample Helm chart (`examples/helm`),
      check if application and all its components were deployed correctly,
      eventually, remove the application from your cluster
      ```bash
      helm install example examples/helm/nginx-example
      helm ls
      kubectl get pods # check if it works
      kubectl describe pod <pod>
      kubectl logs <pod>
      
      helm uninstall example
      ```
      (https://github.com/deislabs/helm-workshop)
    - explain how to use values defined in `values.yaml` inside your manifests
        - for example: `replicas: {{ .Values.replicaCount }}`
    - how to use 3rd party Helm charts in your chart?
        - in deployments:
        ```bash
          image: nginx
        ```
        - folder `charts`
    - you can find many existing charts in [Helm chart repository](https://github.com/helm/charts/tree/master/stable)

5. **Application chart**

    - prepare Docker images for our Reddit Scraper application - for all custom images (celery workers, scheduler etc.):
        - option A: push them as public images on your Docker Hub
        ```bash
        docker build -t lsdp-app .
        docker tag lsdp-app edzia/lsdp-app:latest
        docker push edzia/lsdp-app
        ```
        - option B: clone the repo to the K3s worker nodes and build the Dockerfiles there
    - create a Helm chart for our application
    ```bash
   helm create <name>  # creates Helm chart (mostly empty)
   kompose convert -c  # automatic tool to convert docker-compose into Helm chart 
   ```
    - decide which components ("services" in Docker-Compose) are already present as Helm charts and include them in our chart
    - for other components write appropriate Helm templates (deployments, services, etc.) 
    - make sure to handle volumes! (for simplicity you can use hostPaths, but in practice, you should use a Volume Provider, like EBS, Cinder, NFS etc.)
    - add appropriate liveness and readiness probes

6. **Application deployment**
    - deploy the prepared application chart to your Kubernetes cluster
    - check if everything works fine
        - if it doesn't, there is a nice tutorial of troubleshooting problems: 
        https://managedkube.com/kubernetes/pod/failure/crashloopbackoff/k8sbot/troubleshooting/2019/02/12/pod-failure-crashloopbackoff.html

    - make some change in the `values.yaml` file (e.g. increase the replicas of the text embedding worker) and perform a rolling update
    - rollback the change
    
    ```bash
    helm install lsdp docker-compose  # the last argument is a relative path
    helm upgrade lsdp docker-compose
    helm history lsdp
    helm rollback lsdp 1
    ```

7. **Application check**
    - make sure that everything is working correctly
        - data is collected
        - you can see changes on the Grafana dashboard
        - you can see changes on the Redash dashboard

