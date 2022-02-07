# Setup Environment 

The following code blocks execute the creation of the required resources for the demo. 
Basically the biggest resource is a GKE cluster, but it is also a preparation needed for that in Argolis.

## Prepare

```
gcloud config set project greenops-demo-env

export PROJECT_ID=$(gcloud config list --format 'value(core.project)')
export PROJECT_NUMBER=$(gcloud projects list \
    --filter=${PROJECT_ID} --format="value(PROJECT_NUMBER)")

export REGION=europe-north1
export ZONE=a
export SUBNET_RANGE=10.128.0.0/20 
```

##  Network Creation

```
gcloud compute networks create k8s-vpc \
--project=$PROJECT_ID \
--subnet-mode=custom \
--mtu=1460 \
--bgp-routing-mode=regional

gcloud compute networks subnets create k8s-subnet \
--project=$PROJECT_ID \
--range=$SUBNET_RANGE \
--network=k8s-vpc \
--region=$REGION
```


##  Adapt Policy
This needs to be executed with the admin user that has Policy Admin role:

```
gcloud org-policies set-policy policies/os_login.yaml 
gcloud org-policies set-policy policies/shieldedVm.yaml 
gcloud org-policies set-policy policies/vmCanIpForward.yaml
gcloud org-policies set-policy policies/vmExternalIpAccess.yaml
gcloud org-policies set-policy policies/restrictVpcPeering.yaml
```


##  Create BQ Dataset
``` 
bq --location=${REGION} mk \
--dataset \
${PROJECT_ID}:k8s_resource_data
``` 

##  Provision GKE Cluster
``` 
gcloud beta container --project "greenops-demo-env" clusters create "greenops-sanboxing" \
--zone "europe-north1-a" --node-locations "europe-north1-a" \
--no-enable-basic-auth --cluster-version "1.21.6-gke.1500" --release-channel "regular" \
--machine-type "e2-medium" --image-type "COS_CONTAINERD" --disk-type "pd-standard" --disk-size "100" \
--min-cpu 2 --max-cpu 6 --min-memory 8 --max-memory 24 \
--scopes "https://www.googleapis.com/auth/devstorage.read_only","https://www.googleapis.com/auth/logging.write","https://www.googleapis.com/auth/monitoring","https://www.googleapis.com/auth/servicecontrol","https://www.googleapis.com/auth/service.management.readonly","https://www.googleapis.com/auth/trace.append" \
 --enable-autoscaling --num-nodes "3" --min-nodes "0" --max-nodes "3"  \
--enable-private-nodes --master-ipv4-cidr "10.124.10.0/28" --enable-ip-alias \
--network "projects/$PROJECT_ID/global/networks/k8s-vpc" \
--subnetwork "projects/$PROJECT_ID/regions/$REGION/subnetworks/k8s-subnet" \
--no-enable-master-authorized-networks \
--no-enable-intra-node-visibility --default-max-pods-per-node "110" --max-pods-per-node "110"  \
--logging=SYSTEM,WORKLOAD --monitoring=SYSTEM \
--addons HorizontalPodAutoscaling,HttpLoadBalancing,GcePersistentDiskCsiDriver \
--metadata disable-legacy-endpoints=true  --enable-autoupgrade --enable-autorepair --max-surge-upgrade 1 --max-unavailable-upgrade 0 \
--enable-autoprovisioning --autoprovisioning-scopes=https://www.googleapis.com/auth/logging.write,https://www.googleapis.com/auth/monitoring --enable-autoprovisioning-autorepair --enable-autoprovisioning-autoupgrade \
--autoprovisioning-max-surge-upgrade 1 --autoprovisioning-max-unavailable-upgrade 0 --autoscaling-profile optimize-utilization --enable-vertical-pod-autoscaling \
--resource-usage-bigquery-dataset "k8s_resource_data" --enable-network-egress-metering --enable-resource-consumption-metering \
--workload-pool "greenops-demo-env.svc.id.goog" --enable-shielded-nodes --shielded-secure-boot 
``` 