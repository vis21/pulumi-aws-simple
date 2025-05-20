import pulumi
import pulumi_aws as aws

size = "t3.small"
rockyImage = "ami-01af7acf3c778d87d"  # rocky 9
ubuntuImage = "ami-0745b7d4092315796"  # ubuntu 22.04
os_type = "ubuntu"  # can either be 'ubuntu' or 'rocky'

def createKp():
    customKp = aws.ec2.KeyPair(
        "custom-kp",
        key_name="custom-key",
        public_key="paste-your-public-key-here",
        tags={"Name": "custom-kp"}
    )

    return customKp


def createMultipleEc2(instances, subnet, mainSg, k8sSg, webSg, customKp, os_type):
    ec2_instances = []

    for i in range(instances):
        if os_type == "rocky":
            ami = rockyImage
        else:
            ami = ubuntuImage

        ec2Instances = aws.ec2.Instance(
            f"{os_type}-ec2-{i}",
            instance_type=size,
            ami=ami,
            subnet_id=subnet.id,
            vpc_security_group_ids=[mainSg.id, k8sSg.id, webSg.id],
            key_name=customKp.id,
            ebs_block_devices=[{
                "device_name": "/dev/sda1",
                "delete_on_termination": True,
                "encrypted": False,
                "iops": 3000,
                "tags": {
                    "Name": "main-ebs",
                },
                "throughput": 125,
                "volume_size": 20,
                "volume_type": "gp3",
            }],
            tags={"Name": f"{os_type}-ec2-{i}"}
        )

        ec2_instances.append(ec2Instances)

    return ec2_instances


def createEip(ec2_instances):
    eip_associations = []

    for i, instance in enumerate(ec2_instances):
        eip = aws.ec2.Eip(f"ec2-eip-{i}")

        eipAssociation = aws.ec2.EipAssociation(
            f"ec2-eip-association-{i}",
            instance_id=instance.id,
            allocation_id=eip.id
        )

        eip_associations.append(eipAssociation)

    return eip_associations
