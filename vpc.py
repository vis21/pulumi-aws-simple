import pulumi
import pulumi_aws as aws


def createNetwork():
    vpc = aws.ec2.Vpc(
        "my-vpc",
        cidr_block="16.0.0.0/20",
        tags={"Name": "my-vpc"}
    )

    subnet = aws.ec2.Subnet(
        "pub-subnet-1",
        vpc_id=vpc.id,
        cidr_block="16.0.1.0/24",
        availability_zone="eu-central-1a",
        tags={"Name": "pub-subnet-1"}
    )

    igw = aws.ec2.InternetGateway(
        "my-igw",
        vpc_id=vpc.id
    )

    routeTable = aws.ec2.RouteTable(
        "my-rt1",
        vpc_id=vpc.id,
        routes=[
            {
                "cidr_block": "0.0.0.0/0",
                "gateway_id": igw.id
            }
        ],
        tags={"Name": "my-rt1"}
    )

    rtLink = aws.ec2.RouteTableAssociation(
        "rtLink",
        subnet_id=subnet.id,
        route_table_id=routeTable.id
    )

    return vpc, subnet
