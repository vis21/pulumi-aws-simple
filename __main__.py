import pulumi
from ec2 import createKp, createMultipleEc2, os_type, createEip
from vpc import createNetwork
from sg import createSg

# Create VPC and components
vpc, subnet = createNetwork()

# Create SG and rules
mainSg, k8sSg, webSg = createSg(vpc)

# Launch EC2 instance
keyPair = createKp()
ec2_instances = createMultipleEc2(2, subnet, mainSg, k8sSg, webSg, keyPair, os_type)
eip_associations = createEip(ec2_instances)

# Extract public IP addresses
public_ips = [ec2.public_ip for ec2 in eip_associations]

# Export required values
pulumi.export("Public IPs", public_ips)
