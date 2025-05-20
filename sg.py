import pulumi
import pulumi_aws as aws

def createSg(vpc):
    mainSg = aws.ec2.SecurityGroup(
        "main-sg",
        name="main-sg",
        description="SG for the EC2 instances",
        vpc_id=vpc.id,
        tags={"Name": "main-sg"}
    )

    k8sSg = aws.ec2.SecurityGroup(
        "k8s-sg",
        name="k8s-sg",
        description="SG for the k8s deployments on EC2",
        vpc_id=vpc.id,
        tags={"Name": "k8s-sg"}
    )

    webSg = aws.ec2.SecurityGroup(
        "web-sg",
        name="web-sg",
        description="SG for the standard web deployments on EC2",
        vpc_id=vpc.id,
        tags={"Name": "web-sg"}
    )

    mySsh = aws.vpc.SecurityGroupIngressRule(
        "my-ssh",
        security_group_id=mainSg.id,
        cidr_ipv4="your-ip-here",
        ip_protocol="tcp",
        from_port=22,
        to_port=22,
        description="SSH from my machine",
        tags={"Name": "my-ssh"}
    )

    httpIn = aws.vpc.SecurityGroupIngressRule(
        "http-in",
        security_group_id=webSg.id,
        cidr_ipv4="0.0.0.0/0",
        ip_protocol="tcp",
        from_port=80,
        to_port=80,
        description="HTTP Inbound",
        tags={"Name": "http-in"}
    )

    httpsIn = aws.vpc.SecurityGroupIngressRule(
        "https-in",
        security_group_id=webSg.id,
        cidr_ipv4="0.0.0.0/0",
        ip_protocol="tcp",
        from_port=443,
        to_port=443,
        description="HTTPS Inbound",
        tags={"Name": "https-in"}
    )

    k8sApi = aws.vpc.SecurityGroupIngressRule(
        "k8s-api",
        security_group_id=k8sSg.id,
        cidr_ipv4="16.0.1.14/32",
        ip_protocol="tcp",
        from_port=6443,
        to_port=6443,
        description="k8s API Inbound from Worker",
        tags={"Name": "k8s-api"}
    )

    kubeletApi = aws.vpc.SecurityGroupIngressRule(
        "kubelet-api",
        security_group_id=k8sSg.id,
        cidr_ipv4="16.0.1.200/32",
        ip_protocol="tcp",
        from_port=10250,
        to_port=10250,
        description="kubelet API Inbound from Master",
        tags={"Name": "kubelet-api"}
    )

    k8sNodeport = aws.vpc.SecurityGroupIngressRule(
        "k8s-nodeport",
        security_group_id=k8sSg.id,
        cidr_ipv4="0.0.0.0/0",
        ip_protocol="tcp",
        from_port=30000,
        to_port=32767,
        description="Nodeport Inbound from everywhere",
        tags={"Name": "k8s-nodeport"}
    )

    egressAll = aws.vpc.SecurityGroupEgressRule(
        "egress-all",
        security_group_id=mainSg.id,
        cidr_ipv4="0.0.0.0/0",
        ip_protocol="-1",
        description="Allow all outbound connections",
        tags={"Name": "egress-all"}
    )

    return mainSg, k8sSg, webSg
