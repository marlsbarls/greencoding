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

```
gcloud org-policies set-policy policies/os_login.yaml 
gcloud org-policies set-policy policies/shieldedVm.yaml 
gcloud org-policies set-policy policies/vmCanIpForward.yaml
gcloud org-policies set-policy policies/vmExternalIpAccess.yaml
gcloud org-policies set-policy policies/restrictVpcPeering.yaml
```