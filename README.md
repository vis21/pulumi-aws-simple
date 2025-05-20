# Pulumi AWS Python

A simple Pulumi project, which creates all the necessary AWS resources for EC2 instance (or instances) to be deployed.

The idea behind this project was to create something that can be easily/quickly pulled, ran, and be instantly ready to play around with. The intention is to use this for learning/testing/dev purposes only.

## Prerequisites

- An AWS account with relevant permissions.
- Authentication configured using `aws configure` or another method of your choice.
- Python 3.7 or later installed on your machine.
- Pulumi installed on your machine.

## Configuration

- **aws:region**: (Required) AWS region in which all the resources will be created.

## Resources Created

- **EC2 instance(s)** (`aws.ec2.Instance`): EC2 instances launched with Ubuntu as default OS.
- **KeyPair** (`aws.ec2.KeyPair`): Key Pair required to connect onto the servers.
- **Elastic IPs** (`aws.ec2.EipAssociation`): Public IPs created for each EC2 instance.
- **VPC** (`aws.ec2.Vpc`): /20 network for the EC2s.
- **Subnet** (`aws.ec2.Subnet`): /24 subnet for the EC2s.
- **Internet Gateway** (`aws.ec2.InternetGateway`): Internet Gateway for the created VPC.
- **Route Table** (`aws.ec2.RouteTable`): Route Table for traffic redirection.
- **Route Table Association** (`aws.ec2.RouteTableAssociation`): Linking route table to the internet gateway.
- **Security Groups** (`aws.ec2.SecurityGroup`): A few 'template' Security Groups.
- **Ingress Rules** (`aws.vpc.SecurityGroupIngressRule`): Standard ingress rules for https, http, ssh, k8s.
- **Egress Rules** (`aws.vpc.SecurityGroupEgressRule`): Standard egress to/for all.

## Outputs

- **Public IPs**: Public IP addresses of each EC2 instance created.

## Next Steps

- Specify number of instances you want to create (2 by default) in `__main__.py` within the `ec2_instances` variable.
- Update `public_key` in the `ec2.py` file to your own public key.
- Update `mySsh` variable in the `sg.py` file with your own IP address.
- (Optional) you can change the default OS, size of your EC2 instances or the images used all in the `ec2.py` using the variables at the top of the file (line 4-7).
