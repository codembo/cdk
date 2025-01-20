# Network Builders



The `network` package contains builders for setting up networking and networking security.



## Vpc Builder

Most projects need a Virtual Private Cloud to provide security by means of
network partitioning. This is achieved by creating an instance of
`VpcBuilder`:

```python
from packages.network.vpc_builder import VpcBuilder
from aws_cdk import Stack, aws_ec2 as ec2

stack = Stack()

vpc_builder = VpcBuilder("VPC_NAME", stack)
vpc_builder.ip_addresses("10.64.32.0/20")
vpc_builder.availability_zones(["us-east-1a", "us-east-1b", "us-east-1c"])
vpc_builder.subnet_configuration([
            ec2.SubnetConfiguration(name="Public", subnet_type=ec2.SubnetType.PUBLIC, cidr_mask=27),
            ec2.SubnetConfiguration(name="Database", subnet_type=ec2.SubnetType.PRIVATE_ISOLATED),
            ec2.SubnetConfiguration(name="Private", subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS)
        ])

vpc = vpc_builder.build() # Build the aws-cdk vpc instance

```
### Subnet Types

A VPC consists of one or more subnets that instances can be placed into. CDK
distinguishes three different subnet types:

* **Public (`SubnetType.PUBLIC`)** - public subnets connect directly to the Internet using an
  Internet Gateway. If you want your instances to have a public IP address
  and be directly reachable from the Internet, you must place them in a
  public subnet.
* **Private with Internet Access (`SubnetType.PRIVATE_WITH_EGRESS`)** - instances in private subnets are not directly routable from the
  Internet, and you must provide a way to connect out to the Internet.
  By default, a NAT gateway is created in every public subnet for maximum availability. Be
  aware that you will be charged for NAT gateways.
  Alternatively you can set `natGateways:0` and provide your own egress configuration (i.e through Transit Gateway)
* **Isolated (`SubnetType.PRIVATE_ISOLATED`)** - isolated subnets do not route from or to the Internet, and
  as such do not require NAT gateways. They can only connect to or be
  connected to from other instances in the same VPC. A default VPC configuration
  will not include isolated subnets,

A default VPC configuration will create **public** and **private** subnets. However, if
`natGateways:0` **and** `subnetConfiguration` is undefined, default VPC configuration
will create public and **isolated** subnets. See [*Advanced Subnet Configuration*](#advanced-subnet-configuration)
below for information on how to change the default subnet configuration.

Constructs using the VPC will "launch instances" (or more accurately, create
Elastic Network Interfaces) into one or more of the subnets. They all accept
a property called `subnetSelection` (sometimes called `vpcSubnets`) to allow
you to select in what subnet to place the ENIs, usually defaulting to
*private* subnets if the property is omitted.

If you would like to save on the cost of NAT gateways, you can use
*isolated* subnets instead of *private* subnets (as described in Advanced
*Subnet Configuration*). If you need private instances to have
internet connectivity, another option is to reduce the number of NAT gateways
created by setting the `natGateways` property to a lower value (the default
is one NAT gateway per availability zone). Be aware that this may have
availability implications for your application.

[Read more about
subnets](https://docs.aws.amazon.com/AmazonVPC/latest/UserGuide/VPC_Subnets.html).

### Restricting access to the VPC default security group

AWS Security best practices recommend that the [VPC default security group should
not allow inbound and outbound
traffic](https://docs.aws.amazon.com/securityhub/latest/userguide/ec2-controls.html#ec2-2).
When the `VpcBuilder:restrict_default_security_group` feature flag is set to
`True` this will be enabled by default. The `restrict_default_security_group` default value is `True`.

```python
vpc_builder.restrict_default_security_group(True) # Default value is True
```

If you use the property default value `True` and then later set it to `False`
the default ingress/egress will be restored on the default security group.

## Security Group Builder

```python 
from packages.network.security_group_builder import SecurityGroupBuilder, IngressRule

stack = Stack()
vpc = # use the VpcBuilder to create a new vpc instance

security_group_builder = SecurityGroupBuilder("SecurityGroup", stack, vpc)
security_group_builder.security_group_name("<your-company> security group")
security_group_builder.description("Example of security group")
security_group_builder.ingress_rules([
    IngressRule(peer=ec2.Peer.ipv4("10.64.32.0/20"),
                description="Allow all traffic from VPC CIDR",
                connection=ec2.Port.all_traffic())
])

security_group = security_group_builder.build() # Build the aws-cdk security group instance
```

[//]: # (## END)

[//]: # ()
[//]: # ()
[//]: # ()
[//]: # (### Control over availability zones)

[//]: # ()
[//]: # (By default, a VPC will spread over at most 3 Availability Zones available to)

[//]: # (it. To change the number of Availability Zones that the VPC will spread over,)

[//]: # (specify the `maxAzs` property when defining it.)

[//]: # ()
[//]: # (The number of Availability Zones that are available depends on the *region*)

[//]: # (and *account* of the Stack containing the VPC. If the [region and account are)

[//]: # (specified]&#40;https://docs.aws.amazon.com/cdk/latest/guide/environments.html&#41; on)

[//]: # (the Stack, the CLI will [look up the existing Availability)

[//]: # (Zones]&#40;https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-regions-availability-zones.html#using-regions-availability-zones-describe&#41;)

[//]: # (and get an accurate count. The result of this operation will be written to a file)

[//]: # (called `cdk.context.json`. You must commit this file to source control so)

[//]: # (that the lookup values are available in non-privileged environments such)

[//]: # (as CI build steps, and to ensure your template builds are repeatable.)

[//]: # ()
[//]: # ()
[//]: # (If region and account are not specified, the stack)

[//]: # (could be deployed anywhere and it will have to make a safe choice, limiting)

[//]: # (itself to 2 Availability Zones.)

[//]: # ()
[//]: # (Therefore, to get the VPC to spread over 3 or more availability zones, you)

[//]: # (must specify the environment where the stack will be deployed.)

[//]: # ()
[//]: # (You can gain full control over the availability zones selection strategy by overriding the Stack's [`get availabilityZones&#40;&#41;`]&#40;https://github.com/aws/aws-cdk/blob/main/packages/@aws-cdk/core/lib/stack.ts&#41; method:)

[//]: # ()
[//]: # (```text)

[//]: # (// This example is only available in TypeScript)

[//]: # ()
[//]: # (class MyStack extends Stack {)

[//]: # ()
[//]: # (  constructor&#40;scope: Construct, id: string, props?: StackProps&#41; {)

[//]: # (    super&#40;scope, id, props&#41;;)

[//]: # ()
[//]: # (    // ...)

[//]: # (  })

[//]: # ()
[//]: # (  get availabilityZones&#40;&#41;: string[] {)

[//]: # (    return ['us-west-2a', 'us-west-2b'];)

[//]: # (  })

[//]: # ()
[//]: # (})

[//]: # (```)

[//]: # ()
[//]: # (Note that overriding the `get availabilityZones&#40;&#41;` method will override the default behavior for all constructs defined within the Stack.)

[//]: # ()
[//]: # (### Choosing subnets for resources)

[//]: # ()
[//]: # (When creating resources that create Elastic Network Interfaces &#40;such as)

[//]: # (databases or instances&#41;, there is an option to choose which subnets to place)

[//]: # (them in. For example, a VPC endpoint by default is placed into a subnet in)

[//]: # (every availability zone, but you can override which subnets to use. The property)

[//]: # (is typically called one of `subnets`, `vpcSubnets` or `subnetSelection`.)

[//]: # ()
[//]: # (The example below will place the endpoint into two AZs &#40;`us-east-1a` and `us-east-1c`&#41;,)

[//]: # (in Isolated subnets:)

[//]: # ()
[//]: # (```ts)

[//]: # (declare const vpc: ec2.Vpc;)

[//]: # ()
[//]: # (new ec2.InterfaceVpcEndpoint&#40;this, 'VPC Endpoint', {)

[//]: # (  vpc,)

[//]: # (  service: new ec2.InterfaceVpcEndpointService&#40;'com.amazonaws.vpce.us-east-1.vpce-svc-uuddlrlrbastrtsvc', 443&#41;,)

[//]: # (  subnets: {)

[//]: # (    subnetType: ec2.SubnetType.PRIVATE_ISOLATED,)

[//]: # (    availabilityZones: ['us-east-1a', 'us-east-1c'])

[//]: # (  })

[//]: # (}&#41;;)

[//]: # (```)

[//]: # ()
[//]: # (You can also specify specific subnet objects for granular control:)

[//]: # ()
[//]: # (```ts)

[//]: # (declare const vpc: ec2.Vpc;)

[//]: # (declare const subnet1: ec2.Subnet;)

[//]: # (declare const subnet2: ec2.Subnet;)

[//]: # ()
[//]: # (new ec2.InterfaceVpcEndpoint&#40;this, 'VPC Endpoint', {)

[//]: # (  vpc,)

[//]: # (  service: new ec2.InterfaceVpcEndpointService&#40;'com.amazonaws.vpce.us-east-1.vpce-svc-uuddlrlrbastrtsvc', 443&#41;,)

[//]: # (  subnets: {)

[//]: # (    subnets: [subnet1, subnet2])

[//]: # (  })

[//]: # (}&#41;;)

[//]: # (```)

[//]: # ()
[//]: # (Which subnets are selected is evaluated as follows:)

[//]: # ()
[//]: # (* `subnets`: if specific subnet objects are supplied, these are selected, and no other)

[//]: # (  logic is used.)

[//]: # (* `subnetType`/`subnetGroupName`: otherwise, a set of subnets is selected by)

[//]: # (  supplying either type or name:)

[//]: # (  * `subnetType` will select all subnets of the given type.)

[//]: # (  * `subnetGroupName` should be used to distinguish between multiple groups of subnets of)

[//]: # (    the same type &#40;for example, you may want to separate your application instances and your)

[//]: # (    RDS instances into two distinct groups of Isolated subnets&#41;.)

[//]: # (  * If neither are given, the first available subnet group of a given type that)

[//]: # (    exists in the VPC will be used, in this order: Private, then Isolated, then Public.)

[//]: # (    In short: by default ENIs will preferentially be placed in subnets not connected to)

[//]: # (    the Internet.)

[//]: # (* `availabilityZones`/`onePerAz`: finally, some availability-zone based filtering may be done.)

[//]: # (  This filtering by availability zones will only be possible if the VPC has been created or)

[//]: # (  looked up in a non-environment agnostic stack &#40;so account and region have been set and)

[//]: # (  availability zones have been looked up&#41;.)

[//]: # (  * `availabilityZones`: only the specific subnets from the selected subnet groups that are)

[//]: # (    in the given availability zones will be returned.)

[//]: # (  * `onePerAz`: per availability zone, a maximum of one subnet will be returned &#40;Useful for resource)

[//]: # (    types that do not allow creating two ENIs in the same availability zone&#41;.)

[//]: # (* `subnetFilters`: additional filtering on subnets using any number of user-provided filters which)

[//]: # (  extend `SubnetFilter`.  The following methods on the `SubnetFilter` class can be used to create)

[//]: # (  a filter:)

[//]: # (  * `byIds`: chooses subnets from a list of ids)

[//]: # (  * `availabilityZones`: chooses subnets in the provided list of availability zones)

[//]: # (  * `onePerAz`: chooses at most one subnet per availability zone)

[//]: # (  * `containsIpAddresses`: chooses a subnet which contains *any* of the listed ip addresses)

[//]: # (  * `byCidrMask`: chooses subnets that have the provided CIDR netmask)

[//]: # (  * `byCidrRanges`: chooses subnets which are inside any of the specified CIDR ranges)

[//]: # ()
[//]: # (### Using NAT instances)

[//]: # ()
[//]: # (By default, the `Vpc` construct will create NAT *gateways* for you, which)

[//]: # (are managed by AWS. If you would prefer to use your own managed NAT)

[//]: # (*instances* instead, specify a different value for the `natGatewayProvider`)

[//]: # (property, as follows:)

[//]: # ()
[//]: # (The construct will automatically selects the latest version of Amazon Linux 2023.)

[//]: # (If you prefer to use a custom AMI, use `machineImage:)

[//]: # (MachineImage.genericLinux&#40;{ ... }&#41;` and configure the right AMI ID for the)

[//]: # (regions you want to deploy to.)

[//]: # ()
[//]: # (> **Warning**)

[//]: # (> The NAT instances created using this method will be **unmonitored**.)

[//]: # (> They are not part of an Auto Scaling Group,)

[//]: # (> and if they become unavailable or are terminated for any reason,)

[//]: # (> will not be restarted or replaced.)

[//]: # ()
[//]: # (By default, the NAT instances will route all traffic. To control what traffic)

[//]: # (gets routed, pass a custom value for `defaultAllowedTraffic` and access the)

[//]: # (`NatInstanceProvider.connections` member after having passed the NAT provider to)

[//]: # (the VPC:)

[//]: # ()
[//]: # (```ts)

[//]: # (declare const instanceType: ec2.InstanceType;)

[//]: # ()
[//]: # (const provider = ec2.NatProvider.instanceV2&#40;{)

[//]: # (  instanceType,)

[//]: # (  defaultAllowedTraffic: ec2.NatTrafficDirection.OUTBOUND_ONLY,)

[//]: # (}&#41;;)

[//]: # (new ec2.Vpc&#40;this, 'TheVPC', {)

[//]: # (  natGatewayProvider: provider,)

[//]: # (}&#41;;)

[//]: # (provider.connections.allowFrom&#40;ec2.Peer.ipv4&#40;'1.2.3.4/8'&#41;, ec2.Port.HTTP&#41;;)

[//]: # (```)

[//]: # ()
[//]: # (You can also customize the characteristics of your NAT instances, including their security group,)

[//]: # (as well as their initialization scripts:)

[//]: # ()
[//]: # (```ts)

[//]: # (declare const bucket: s3.Bucket;)

[//]: # ()
[//]: # (const userData = ec2.UserData.forLinux&#40;&#41;;)

[//]: # (userData.addCommands&#40;)

[//]: # (  ...ec2.NatInstanceProviderV2.DEFAULT_USER_DATA_COMMANDS,)

[//]: # (  'echo "hello world!" > hello.txt',)

[//]: # (  `aws s3 cp hello.txt s3://${bucket.bucketName}`,)

[//]: # (&#41;;)

[//]: # ()
[//]: # (const provider = ec2.NatProvider.instanceV2&#40;{)

[//]: # (  instanceType: new ec2.InstanceType&#40;'t3.small'&#41;,)

[//]: # (  creditSpecification: ec2.CpuCredits.UNLIMITED,)

[//]: # (  defaultAllowedTraffic: ec2.NatTrafficDirection.NONE,)

[//]: # (}&#41;;)

[//]: # ()
[//]: # (const vpc = new ec2.Vpc&#40;this, 'TheVPC', {)

[//]: # (  natGatewayProvider: provider,)

[//]: # (  natGateways: 2,)

[//]: # (}&#41;;)

[//]: # ()
[//]: # (const securityGroup = new ec2.SecurityGroup&#40;this, 'SecurityGroup', { vpc }&#41;;)

[//]: # (    securityGroup.addEgressRule&#40;ec2.Peer.anyIpv4&#40;&#41;, ec2.Port.tcp&#40;443&#41;&#41;;)

[//]: # (for &#40;const gateway of provider.gatewayInstances&#41; {)

[//]: # (  bucket.grantWrite&#40;gateway&#41;;)

[//]: # (  gateway.addSecurityGroup&#40;securityGroup&#41;;)

[//]: # (})

[//]: # (```)

[//]: # ()
[//]: # ([using NAT instances]&#40;test/integ.nat-instances.lit.ts&#41; [Deprecated])

[//]: # ()
[//]: # (The V1 `NatProvider.instance` construct will use the AWS official NAT instance AMI, which has already)

[//]: # (reached EOL on Dec 31, 2023. For more information, see the following blog post:)

[//]: # ([Amazon Linux AMI end of life]&#40;https://aws.amazon.com/blogs/aws/update-on-amazon-linux-ami-end-of-life/&#41;.)

[//]: # ()
[//]: # (```ts)

[//]: # (declare const instanceType: ec2.InstanceType;)

[//]: # ()
[//]: # (const provider = ec2.NatProvider.instance&#40;{)

[//]: # (  instanceType,)

[//]: # (  defaultAllowedTraffic: ec2.NatTrafficDirection.OUTBOUND_ONLY,)

[//]: # (}&#41;;)

[//]: # (new ec2.Vpc&#40;this, 'TheVPC', {)

[//]: # (  natGatewayProvider: provider,)

[//]: # (}&#41;;)

[//]: # (provider.connections.allowFrom&#40;ec2.Peer.ipv4&#40;'1.2.3.4/8'&#41;, ec2.Port.HTTP&#41;;)

[//]: # (```)

[//]: # ()
[//]: # (### Ip Address Management)

[//]: # ()
[//]: # (The VPC spans a supernet IP range, which contains the non-overlapping IPs of its contained subnets. Possible sources for this IP range are:)

[//]: # ()
[//]: # (* You specify an IP range directly by specifying a CIDR)

[//]: # (* You allocate an IP range of a given size automatically from AWS IPAM)

[//]: # ()
[//]: # (By default the Vpc will allocate the `10.0.0.0/16` address range which will be exhaustively spread across all subnets in the subnet configuration. This behavior can be changed by passing an object that implements `IIpAddresses` to the `ipAddress` property of a Vpc. See the subsequent sections for the options.)

[//]: # ()
[//]: # (Be aware that if you don't explicitly reserve subnet groups in `subnetConfiguration`, the address space will be fully allocated! If you predict you may need to add more subnet groups later, add them early on and set `reserved: true` &#40;see the "Advanced Subnet Configuration" section for more information&#41;.)

[//]: # ()
[//]: # (#### Specifying a CIDR directly)

[//]: # ()
[//]: # (Use `IpAddresses.cidr` to define a Cidr range for your Vpc directly in code:)

[//]: # ()
[//]: # (```ts)

[//]: # (import { IpAddresses } from 'aws-cdk-lib/aws-ec2';)

[//]: # ()
[//]: # (new ec2.Vpc&#40;this, 'TheVPC', {)

[//]: # (  ipAddresses: IpAddresses.cidr&#40;'10.0.1.0/20'&#41;)

[//]: # (}&#41;;)

[//]: # (```)

[//]: # ()
[//]: # (Space will be allocated to subnets in the following order:)

[//]: # ()
[//]: # (* First, spaces is allocated for all subnets groups that explicitly have a `cidrMask` set as part of their configuration &#40;including reserved subnets&#41;.)

[//]: # (* Afterwards, any remaining space is divided evenly between the rest of the subnets &#40;if any&#41;.)

[//]: # ()
[//]: # (The argument to `IpAddresses.cidr` may not be a token, and concrete Cidr values are generated in the synthesized CloudFormation template.)

[//]: # ()
[//]: # (#### Allocating an IP range from AWS IPAM)

[//]: # ()
[//]: # (Amazon VPC IP Address Manager &#40;IPAM&#41; manages a large IP space, from which chunks can be allocated for use in the Vpc. For information on Amazon VPC IP Address Manager please see the [official documentation]&#40;https://docs.aws.amazon.com/vpc/latest/ipam/what-it-is-ipam.html&#41;. An example of allocating from AWS IPAM looks like this:)

[//]: # ()
[//]: # (```ts)

[//]: # (import { IpAddresses } from 'aws-cdk-lib/aws-ec2';)

[//]: # ()
[//]: # (declare const pool: ec2.CfnIPAMPool;)

[//]: # ()
[//]: # (new ec2.Vpc&#40;this, 'TheVPC', {)

[//]: # (  ipAddresses: IpAddresses.awsIpamAllocation&#40;{)

[//]: # (    ipv4IpamPoolId: pool.ref,)

[//]: # (    ipv4NetmaskLength: 18,)

[//]: # (    defaultSubnetIpv4NetmaskLength: 24)

[//]: # (  }&#41;)

[//]: # (}&#41;;)

[//]: # (```)

[//]: # ()
[//]: # (`IpAddresses.awsIpamAllocation` requires the following:)

[//]: # ()
[//]: # (* `ipv4IpamPoolId`, the id of an IPAM Pool from which the VPC range should be allocated.)

[//]: # (* `ipv4NetmaskLength`, the size of the IP range that will be requested from the Pool at deploy time.)

[//]: # (* `defaultSubnetIpv4NetmaskLength`, the size of subnets in groups that don't have `cidrMask` set.)

[//]: # ()
[//]: # (With this method of IP address management, no attempt is made to guess at subnet group sizes or to exhaustively allocate the IP range. All subnet groups must have an explicit `cidrMask` set as part of their subnet configuration, or `defaultSubnetIpv4NetmaskLength` must be set for a default size. If not, synthesis will fail and you must provide one or the other.)

[//]: # ()
[//]: # (### Dual Stack configuration)

[//]: # ()
[//]: # (To allocate both IPv4 and IPv6 addresses in your VPC, you can configure your VPC to have a dual stack protocol.)

[//]: # ()
[//]: # (```ts)

[//]: # (new ec2.Vpc&#40;this, 'DualStackVpc', {)

[//]: # (  ipProtocol: ec2.IpProtocol.DUAL_STACK,)

[//]: # (}&#41;)

[//]: # (```)

[//]: # ()
[//]: # (By default, a dual stack VPC will create an Amazon provided IPv6 /56 CIDR block associated to the VPC. It will then assign /64 portions of the block to each subnet. For each subnet, auto-assigning an IPv6 address will be enabled, and auto-asigning a public IPv4 address will be disabled. An egress only internet gateway will be created for `PRIVATE_WITH_EGRESS` subnets, and IPv6 routes will be added for IGWs and EIGWs.)

[//]: # ()
[//]: # (Disabling the auto-assigning of a public IPv4 address by default can avoid the cost of public IPv4 addresses starting 2/1/2024. For use cases that need an IPv4 address, the `mapPublicIpOnLaunch` property in `subnetConfiguration` can be set to auto-assign the IPv4 address. Note that private IPv4 address allocation will not be changed.)

[//]: # ()
[//]: # (See [Advanced Subnet Configuration]&#40;#advanced-subnet-configuration&#41; for all IPv6 specific properties.)

[//]: # ()
[//]: # (### Reserving availability zones)

[//]: # ()
[//]: # (There are situations where the IP space for availability zones will)

[//]: # (need to be reserved. This is useful in situations where availability)

[//]: # (zones would need to be added after the vpc is originally deployed,)

[//]: # (without causing IP renumbering for availability zones subnets. The IP)

[//]: # (space for reserving `n` availability zones can be done by setting the)

[//]: # (`reservedAzs` to `n` in vpc props, as shown below:)

[//]: # ()
[//]: # (```ts)

[//]: # (const vpc = new ec2.Vpc&#40;this, 'TheVPC', {)

[//]: # (  cidr: '10.0.0.0/21',)

[//]: # (  maxAzs: 3,)

[//]: # (  reservedAzs: 1,)

[//]: # (}&#41;;)

[//]: # (```)

[//]: # ()
[//]: # (In the example above, the subnets for reserved availability zones is not)

[//]: # (actually provisioned but its IP space is still reserved. If, in the future,)

[//]: # (new availability zones needs to be provisioned, then we would decrement)

[//]: # (the value of `reservedAzs` and increment the `maxAzs` or `availabilityZones`)

[//]: # (accordingly. This action would not cause the IP address of subnets to get)

[//]: # (renumbered, but rather the IP space that was previously reserved will be)

[//]: # (used for the new availability zones subnets.)

[//]: # ()
[//]: # (### Advanced Subnet Configuration)

[//]: # ()
[//]: # (If the default VPC configuration &#40;public and private subnets spanning the)

[//]: # (size of the VPC&#41; don't suffice for you, you can configure what subnets to)

[//]: # (create by specifying the `subnetConfiguration` property. It allows you)

[//]: # (to configure the number and size of all subnets. Specifying an advanced)

[//]: # (subnet configuration could look like this:)

[//]: # ()
[//]: # (```ts)

[//]: # (const vpc = new ec2.Vpc&#40;this, 'TheVPC', {)

[//]: # (  // 'IpAddresses' configures the IP range and size of the entire VPC.)

[//]: # (  // The IP space will be divided based on configuration for the subnets.)

[//]: # (  ipAddresses: ec2.IpAddresses.cidr&#40;'10.0.0.0/21'&#41;,)

[//]: # ()
[//]: # (  // 'maxAzs' configures the maximum number of availability zones to use.)

[//]: # (  // If you want to specify the exact availability zones you want the VPC)

[//]: # (  // to use, use `availabilityZones` instead.)

[//]: # (  maxAzs: 3,)

[//]: # ()
[//]: # (  // 'subnetConfiguration' specifies the "subnet groups" to create.)

[//]: # (  // Every subnet group will have a subnet for each AZ, so this)

[//]: # (  // configuration will create `3 groups × 3 AZs = 9` subnets.)

[//]: # (  subnetConfiguration: [)

[//]: # (    {)

[//]: # (      // 'subnetType' controls Internet access, as described above.)

[//]: # (      subnetType: ec2.SubnetType.PUBLIC,)

[//]: # ()
[//]: # (      // 'name' is used to name this particular subnet group. You will have to)

[//]: # (      // use the name for subnet selection if you have more than one subnet)

[//]: # (      // group of the same type.)

[//]: # (      name: 'Ingress',)

[//]: # ()
[//]: # (      // 'cidrMask' specifies the IP addresses in the range of of individual)

[//]: # (      // subnets in the group. Each of the subnets in this group will contain)

[//]: # (      // `2^&#40;32 address bits - 24 subnet bits&#41; - 2 reserved addresses = 254`)

[//]: # (      // usable IP addresses.)

[//]: # (      //)

[//]: # (      // If 'cidrMask' is left out the available address space is evenly)

[//]: # (      // divided across the remaining subnet groups.)

[//]: # (      cidrMask: 24,)

[//]: # (    },)

[//]: # (    {)

[//]: # (      cidrMask: 24,)

[//]: # (      name: 'Application',)

[//]: # (      subnetType: ec2.SubnetType.PRIVATE_WITH_EGRESS,)

[//]: # (    },)

[//]: # (    {)

[//]: # (      cidrMask: 28,)

[//]: # (      name: 'Database',)

[//]: # (      subnetType: ec2.SubnetType.PRIVATE_ISOLATED,)

[//]: # ()
[//]: # (      // 'reserved' can be used to reserve IP address space. No resources will)

[//]: # (      // be created for this subnet, but the IP range will be kept available for)

[//]: # (      // future creation of this subnet, or even for future subdivision.)

[//]: # (      reserved: true)

[//]: # (    })

[//]: # (  ],)

[//]: # (}&#41;;)

[//]: # (```)

[//]: # ()
[//]: # (The example above is one possible configuration, but the user can use the)

[//]: # (constructs above to implement many other network configurations.)

[//]: # ()
[//]: # (The `Vpc` from the above configuration in a Region with three)

[//]: # (availability zones will be the following:)

[//]: # ()
[//]: # (Subnet Name       |Type      |IP Block      |AZ|Features)

[//]: # (------------------|----------|--------------|--|--------)

[//]: # (IngressSubnet1    |`PUBLIC`  |`10.0.0.0/24` |#1|NAT Gateway)

[//]: # (IngressSubnet2    |`PUBLIC`  |`10.0.1.0/24` |#2|NAT Gateway)

[//]: # (IngressSubnet3    |`PUBLIC`  |`10.0.2.0/24` |#3|NAT Gateway)

[//]: # (ApplicationSubnet1|`PRIVATE` |`10.0.3.0/24` |#1|Route to NAT in IngressSubnet1)

[//]: # (ApplicationSubnet2|`PRIVATE` |`10.0.4.0/24` |#2|Route to NAT in IngressSubnet2)

[//]: # (ApplicationSubnet3|`PRIVATE` |`10.0.5.0/24` |#3|Route to NAT in IngressSubnet3)

[//]: # (DatabaseSubnet1   |`ISOLATED`|`10.0.6.0/28` |#1|Only routes within the VPC)

[//]: # (DatabaseSubnet2   |`ISOLATED`|`10.0.6.16/28`|#2|Only routes within the VPC)

[//]: # (DatabaseSubnet3   |`ISOLATED`|`10.0.6.32/28`|#3|Only routes within the VPC)

[//]: # ()
[//]: # (#### Dual Stack Configurations)

[//]: # ()
[//]: # (Here is a break down of IPv4 and IPv6 specifc `subnetConfiguration` properties in a dual stack VPC:)

[//]: # ()
[//]: # (```ts)

[//]: # (const vpc = new ec2.Vpc&#40;this, 'TheVPC', {)

[//]: # (  ipProtocol: ec2.IpProtocol.DUAL_STACK,)

[//]: # ()
[//]: # (  subnetConfiguration: [)

[//]: # (    {)

[//]: # (      // general properties)

[//]: # (      name: 'Public',)

[//]: # (      subnetType: ec2.SubnetType.PUBLIC,)

[//]: # (      reserved: false,)

[//]: # ()
[//]: # (      // IPv4 specific properties)

[//]: # (      mapPublicIpOnLaunch: true,)

[//]: # (      cidrMask: 24,)

[//]: # ()
[//]: # (      // new IPv6 specific property)

[//]: # (      ipv6AssignAddressOnCreation: true,)

[//]: # (    },)

[//]: # (  ],)

[//]: # (}&#41;;)

[//]: # (```)

[//]: # ()
[//]: # (The property `mapPublicIpOnLaunch` controls if a public IPv4 address will be assigned. This defaults to `false` for dual stack VPCs to avoid inadvertant costs of having the public address. However, a public IP must be enabled &#40;or otherwise configured with BYOIP or IPAM&#41; in order for services that rely on the address to function.)

[//]: # ()
[//]: # (The `ipv6AssignAddressOnCreation` property controls the same behavior for the IPv6 address. It defaults to true.)

[//]: # ()
[//]: # (Using IPv6 specific properties in an IPv4 only VPC will result in errors.)

[//]: # ()
[//]: # (### Accessing the Internet Gateway)

[//]: # ()
[//]: # (If you need access to the internet gateway, you can get its ID like so:)

[//]: # ()
[//]: # (```ts)

[//]: # (declare const vpc: ec2.Vpc;)

[//]: # ()
[//]: # (const igwId = vpc.internetGatewayId;)

[//]: # (```)

[//]: # ()
[//]: # (For a VPC with only `ISOLATED` subnets, this value will be undefined.)

[//]: # ()
[//]: # (This is only supported for VPCs created in the stack - currently you're)

[//]: # (unable to get the ID for imported VPCs. To do that you'd have to specifically)

[//]: # (look up the Internet Gateway by name, which would require knowing the name)

[//]: # (beforehand.)

[//]: # ()
[//]: # (This can be useful for configuring routing using a combination of gateways:)

[//]: # (for more information see [Routing]&#40;#routing&#41; below.)

[//]: # ()
[//]: # (### Disabling the creation of the default internet gateway)

[//]: # ()
[//]: # (If you need to control the creation of the internet gateway explicitly,)

[//]: # (you can disable the creation of the default one using the `createInternetGateway`)

[//]: # (property:)

[//]: # ()
[//]: # (```ts)

[//]: # (const vpc = new ec2.Vpc&#40;this, "VPC", {)

[//]: # (  createInternetGateway: false,)

[//]: # (  subnetConfiguration: [{)

[//]: # (      subnetType: ec2.SubnetType.PUBLIC,)

[//]: # (      name: 'Public',)

[//]: # (    }])

[//]: # (}&#41;;)

[//]: # (```)

[//]: # ()
[//]: # (#### Routing)

[//]: # ()
[//]: # (It's possible to add routes to any subnets using the `addRoute&#40;&#41;` method. If for)

[//]: # (example you want an isolated subnet to have a static route via the default)

[//]: # (Internet Gateway created for the public subnet - perhaps for routing a VPN)

[//]: # (connection - you can do so like this:)

[//]: # ()
[//]: # (```ts)

[//]: # (const vpc = new ec2.Vpc&#40;this, "VPC", {)

[//]: # (  subnetConfiguration: [{)

[//]: # (      subnetType: ec2.SubnetType.PUBLIC,)

[//]: # (      name: 'Public',)

[//]: # (    },{)

[//]: # (      subnetType: ec2.SubnetType.PRIVATE_ISOLATED,)

[//]: # (      name: 'Isolated',)

[//]: # (    }])

[//]: # (}&#41;;)

[//]: # ()
[//]: # (&#40;vpc.isolatedSubnets[0] as ec2.Subnet&#41;.addRoute&#40;"StaticRoute", {)

[//]: # (    routerId: vpc.internetGatewayId!,)

[//]: # (    routerType: ec2.RouterType.GATEWAY,)

[//]: # (    destinationCidrBlock: "8.8.8.8/32",)

[//]: # (}&#41;)

[//]: # (```)

[//]: # ()
[//]: # (*Note that we cast to `Subnet` here because the list of subnets only returns an)

[//]: # (`ISubnet`.*)

[//]: # ()
[//]: # (### Reserving subnet IP space)

[//]: # ()
[//]: # (There are situations where the IP space for a subnet or number of subnets)

[//]: # (will need to be reserved. This is useful in situations where subnets would)

[//]: # (need to be added after the vpc is originally deployed, without causing IP)

[//]: # (renumbering for existing subnets. The IP space for a subnet may be reserved)

[//]: # (by setting the `reserved` subnetConfiguration property to true, as shown)

[//]: # (below:)

[//]: # ()
[//]: # (```ts)

[//]: # (const vpc = new ec2.Vpc&#40;this, 'TheVPC', {)

[//]: # (  natGateways: 1,)

[//]: # (  subnetConfiguration: [)

[//]: # (    {)

[//]: # (      cidrMask: 26,)

[//]: # (      name: 'Public',)

[//]: # (      subnetType: ec2.SubnetType.PUBLIC,)

[//]: # (    },)

[//]: # (    {)

[//]: # (      cidrMask: 26,)

[//]: # (      name: 'Application1',)

[//]: # (      subnetType: ec2.SubnetType.PRIVATE_WITH_EGRESS,)

[//]: # (    },)

[//]: # (    {)

[//]: # (      cidrMask: 26,)

[//]: # (      name: 'Application2',)

[//]: # (      subnetType: ec2.SubnetType.PRIVATE_WITH_EGRESS,)

[//]: # (      reserved: true,   // <---- This subnet group is reserved)

[//]: # (    },)

[//]: # (    {)

[//]: # (      cidrMask: 27,)

[//]: # (      name: 'Database',)

[//]: # (      subnetType: ec2.SubnetType.PRIVATE_ISOLATED,)

[//]: # (    })

[//]: # (  ],)

[//]: # (}&#41;;)

[//]: # (```)

[//]: # ()
[//]: # (In the example above, the subnet for Application2 is not actually provisioned)

[//]: # (but its IP space is still reserved. If in the future this subnet needs to be)

[//]: # (provisioned, then the `reserved: true` property should be removed. Reserving)

[//]: # (parts of the IP space prevents the other subnets from getting renumbered.)

[//]: # ()
[//]: # (### Sharing VPCs between stacks)

[//]: # ()
[//]: # (If you are creating multiple `Stack`s inside the same CDK application, you)

[//]: # (can reuse a VPC defined in one Stack in another by simply passing the VPC)

[//]: # (instance around:)

[//]: # ()
[//]: # ([sharing VPCs between stacks]&#40;test/integ.share-vpcs.lit.ts&#41;)

[//]: # ()
[//]: # (### Importing an existing VPC)

[//]: # ()
[//]: # (If your VPC is created outside your CDK app, you can use `Vpc.fromLookup&#40;&#41;`.)

[//]: # (The CDK CLI will search for the specified VPC in the the stack's region and)

[//]: # (account, and import the subnet configuration. Looking up can be done by VPC)

[//]: # (ID, but more flexibly by searching for a specific tag on the VPC.)

[//]: # ()
[//]: # (Subnet types will be determined from the `aws-cdk:subnet-type` tag on the)

[//]: # (subnet if it exists, or the presence of a route to an Internet Gateway)

[//]: # (otherwise. Subnet names will be determined from the `aws-cdk:subnet-name` tag)

[//]: # (on the subnet if it exists, or will mirror the subnet type otherwise &#40;i.e.)

[//]: # (a public subnet will have the name `"Public"`&#41;.)

[//]: # ()
[//]: # (The result of the `Vpc.fromLookup&#40;&#41;` operation will be written to a file)

[//]: # (called `cdk.context.json`. You must commit this file to source control so)

[//]: # (that the lookup values are available in non-privileged environments such)

[//]: # (as CI build steps, and to ensure your template builds are repeatable.)

[//]: # ()
[//]: # (Here's how `Vpc.fromLookup&#40;&#41;` can be used:)

[//]: # ()
[//]: # ([importing existing VPCs]&#40;test/integ.import-default-vpc.lit.ts&#41;)

[//]: # ()
[//]: # (`Vpc.fromLookup` is the recommended way to import VPCs. If for whatever)

[//]: # (reason you do not want to use the context mechanism to look up a VPC at)

[//]: # (synthesis time, you can also use `Vpc.fromVpcAttributes`. This has the)

[//]: # (following limitations:)

[//]: # ()
[//]: # (* Every subnet group in the VPC must have a subnet in each availability zone)

[//]: # (  &#40;for example, each AZ must have both a public and private subnet&#41;. Asymmetric)

[//]: # (  VPCs are not supported.)

[//]: # (* All VpcId, SubnetId, RouteTableId, ... parameters must either be known at)

[//]: # (  synthesis time, or they must come from deploy-time list parameters whose)

[//]: # (  deploy-time lengths are known at synthesis time.)

[//]: # ()
[//]: # (Using `Vpc.fromVpcAttributes&#40;&#41;` looks like this:)

[//]: # ()
[//]: # (```ts)

[//]: # (const vpc = ec2.Vpc.fromVpcAttributes&#40;this, 'VPC', {)

[//]: # (  vpcId: 'vpc-1234',)

[//]: # (  availabilityZones: ['us-east-1a', 'us-east-1b'],)

[//]: # ()
[//]: # (  // Either pass literals for all IDs)

[//]: # (  publicSubnetIds: ['s-12345', 's-67890'],)

[//]: # ()
[//]: # (  // OR: import a list of known length)

[//]: # (  privateSubnetIds: Fn.importListValue&#40;'PrivateSubnetIds', 2&#41;,)

[//]: # ()
[//]: # (  // OR: split an imported string to a list of known length)

[//]: # (  isolatedSubnetIds: Fn.split&#40;',', ssm.StringParameter.valueForStringParameter&#40;this, `MyParameter`&#41;, 2&#41;,)

[//]: # (}&#41;;)

[//]: # (```)

[//]: # ()
[//]: # (For each subnet group the import function accepts optional parameters for subnet)

[//]: # (names, route table ids and IPv4 CIDR blocks. When supplied, the length of these)

[//]: # (lists are required to match the length of the list of subnet ids, allowing the)

[//]: # (lists to be zipped together to form `ISubnet` instances.)

[//]: # ()
[//]: # (Public subnet group example &#40;for private or isolated subnet groups, use the properties with the respective prefix&#41;:)

[//]: # ()
[//]: # (```ts)

[//]: # (const vpc = ec2.Vpc.fromVpcAttributes&#40;this, 'VPC', {)

[//]: # (  vpcId: 'vpc-1234',)

[//]: # (  availabilityZones: ['us-east-1a', 'us-east-1b', 'us-east-1c'],)

[//]: # (  publicSubnetIds: ['s-12345', 's-34567', 's-56789'],)

[//]: # (  publicSubnetNames: ['Subnet A', 'Subnet B', 'Subnet C'],)

[//]: # (  publicSubnetRouteTableIds: ['rt-12345', 'rt-34567', 'rt-56789'],)

[//]: # (  publicSubnetIpv4CidrBlocks: ['10.0.0.0/24', '10.0.1.0/24', '10.0.2.0/24'],)

[//]: # (}&#41;;)

[//]: # (```)

[//]: # ()
[//]: # (The above example will create an `IVpc` instance with three public subnets:)

[//]: # ()
[//]: # (| Subnet id | Availability zone | Subnet name | Route table id | IPv4 CIDR   |)

[//]: # (| --------- | ----------------- | ----------- | -------------- | ----------- |)

[//]: # (| s-12345   | us-east-1a        | Subnet A    | rt-12345       | 10.0.0.0/24 |)

[//]: # (| s-34567   | us-east-1b        | Subnet B    | rt-34567       | 10.0.1.0/24 |)

[//]: # (| s-56789   | us-east-1c        | Subnet B    | rt-56789       | 10.0.2.0/24 |)

[//]: # ()
[//]: # (### Restricting access to the VPC default security group)

[//]: # ()
[//]: # (AWS Security best practices recommend that the [VPC default security group should)

[//]: # (not allow inbound and outbound)

[//]: # (traffic]&#40;https://docs.aws.amazon.com/securityhub/latest/userguide/ec2-controls.html#ec2-2&#41;.)

[//]: # (When the `@aws-cdk/aws-ec2:restrictDefaultSecurityGroup` feature flag is set to)

[//]: # (`true` &#40;default for new projects&#41; this will be enabled by default. If you do not)

[//]: # (have this feature flag set you can either set the feature flag _or_ you can set)

[//]: # (the `restrictDefaultSecurityGroup` property to `true`.)

[//]: # ()
[//]: # (```ts)

[//]: # (new ec2.Vpc&#40;this, 'VPC', {)

[//]: # (  restrictDefaultSecurityGroup: true,)

[//]: # (}&#41;;)

[//]: # (```)

[//]: # ()
[//]: # (If you set this property to `true` and then later remove it or set it to `false`)

[//]: # (the default ingress/egress will be restored on the default security group.)

[//]: # ()
[//]: # (## Allowing Connections)

[//]: # ()
[//]: # (In AWS, all network traffic in and out of **Elastic Network Interfaces** &#40;ENIs&#41;)

[//]: # (is controlled by **Security Groups**. You can think of Security Groups as a)

[//]: # (firewall with a set of rules. By default, Security Groups allow no incoming)

[//]: # (&#40;ingress&#41; traffic and all outgoing &#40;egress&#41; traffic. You can add ingress rules)

[//]: # (to them to allow incoming traffic streams. To exert fine-grained control over)

[//]: # (egress traffic, set `allowAllOutbound: false` on the `SecurityGroup`, after)

[//]: # (which you can add egress traffic rules.)

[//]: # ()
[//]: # (You can manipulate Security Groups directly:)

[//]: # ()
[//]: # (```ts fixture=with-vpc)

[//]: # (const mySecurityGroup = new ec2.SecurityGroup&#40;this, 'SecurityGroup', {)

[//]: # (  vpc,)

[//]: # (  description: 'Allow ssh access to ec2 instances',)

[//]: # (  allowAllOutbound: true   // Can be set to false)

[//]: # (}&#41;;)

[//]: # (mySecurityGroup.addIngressRule&#40;ec2.Peer.anyIpv4&#40;&#41;, ec2.Port.tcp&#40;22&#41;, 'allow ssh access from the world'&#41;;)

[//]: # (```)

[//]: # ()
[//]: # (All constructs that create ENIs on your behalf &#40;typically constructs that create)

[//]: # (EC2 instances or other VPC-connected resources&#41; will all have security groups)

[//]: # (automatically assigned. Those constructs have an attribute called)

[//]: # (**connections**, which is an object that makes it convenient to update the)

[//]: # (security groups. If you want to allow connections between two constructs that)

[//]: # (have security groups, you have to add an **Egress** rule to one Security Group,)

[//]: # (and an **Ingress** rule to the other. The connections object will automatically)

[//]: # (take care of this for you:)

[//]: # ()
[//]: # (```ts)

[//]: # (declare const loadBalancer: elbv2.ApplicationLoadBalancer;)

[//]: # (declare const appFleet: autoscaling.AutoScalingGroup;)

[//]: # (declare const dbFleet: autoscaling.AutoScalingGroup;)

[//]: # ()
[//]: # (// Allow connections from anywhere)

[//]: # (loadBalancer.connections.allowFromAnyIpv4&#40;ec2.Port.HTTPS, 'Allow inbound HTTPS'&#41;;)

[//]: # ()
[//]: # (// The same, but an explicit IP address)

[//]: # (loadBalancer.connections.allowFrom&#40;ec2.Peer.ipv4&#40;'1.2.3.4/32'&#41;, ec2.Port.HTTPS, 'Allow inbound HTTPS'&#41;;)

[//]: # ()
[//]: # (// Allow connection between AutoScalingGroups)

[//]: # (appFleet.connections.allowTo&#40;dbFleet, ec2.Port.HTTPS, 'App can call database'&#41;;)

[//]: # (```)

[//]: # ()
[//]: # (### Connection Peers)

[//]: # ()
[//]: # (There are various classes that implement the connection peer part:)

[//]: # ()
[//]: # (```ts)

[//]: # (declare const appFleet: autoscaling.AutoScalingGroup;)

[//]: # (declare const dbFleet: autoscaling.AutoScalingGroup;)

[//]: # ()
[//]: # (// Simple connection peers)

[//]: # (let peer = ec2.Peer.ipv4&#40;'10.0.0.0/16'&#41;;)

[//]: # (peer = ec2.Peer.anyIpv4&#40;&#41;;)

[//]: # (peer = ec2.Peer.ipv6&#40;'::0/0'&#41;;)

[//]: # (peer = ec2.Peer.anyIpv6&#40;&#41;;)

[//]: # (peer = ec2.Peer.prefixList&#40;'pl-12345'&#41;;)

[//]: # (appFleet.connections.allowTo&#40;peer, ec2.Port.HTTPS, 'Allow outbound HTTPS'&#41;;)

[//]: # (```)

[//]: # ()
[//]: # (Any object that has a security group can itself be used as a connection peer:)

[//]: # ()
[//]: # (```ts)

[//]: # (declare const fleet1: autoscaling.AutoScalingGroup;)

[//]: # (declare const fleet2: autoscaling.AutoScalingGroup;)

[//]: # (declare const appFleet: autoscaling.AutoScalingGroup;)

[//]: # ()
[//]: # (// These automatically create appropriate ingress and egress rules in both security groups)

[//]: # (fleet1.connections.allowTo&#40;fleet2, ec2.Port.HTTP, 'Allow between fleets'&#41;;)

[//]: # ()
[//]: # (appFleet.connections.allowFromAnyIpv4&#40;ec2.Port.HTTP, 'Allow from load balancer'&#41;;)

[//]: # (```)

[//]: # ()
[//]: # (### Port Ranges)

[//]: # ()
[//]: # (The connections that are allowed are specified by port ranges. A number of classes provide)

[//]: # (the connection specifier:)

[//]: # ()
[//]: # (```ts)

[//]: # (ec2.Port.tcp&#40;80&#41;)

[//]: # (ec2.Port.HTTPS)

[//]: # (ec2.Port.tcpRange&#40;60000, 65535&#41;)

[//]: # (ec2.Port.allTcp&#40;&#41;)

[//]: # (ec2.Port.allIcmp&#40;&#41;)

[//]: # (ec2.Port.allIcmpV6&#40;&#41;)

[//]: # (ec2.Port.allTraffic&#40;&#41;)

[//]: # (```)

[//]: # ()
[//]: # (> NOTE: Not all protocols have corresponding helper methods. In the absence of a helper method,)

[//]: # (> you can instantiate `Port` yourself with your own settings. You are also welcome to contribute)

[//]: # (> new helper methods.)

[//]: # ()
[//]: # (### Default Ports)

[//]: # ()
[//]: # (Some Constructs have default ports associated with them. For example, the)

[//]: # (listener of a load balancer does &#40;it's the public port&#41;, or instances of an)

[//]: # (RDS database &#40;it's the port the database is accepting connections on&#41;.)

[//]: # ()
[//]: # (If the object you're calling the peering method on has a default port associated with it, you can call)

[//]: # (`allowDefaultPortFrom&#40;&#41;` and omit the port specifier. If the argument has an associated default port, call)

[//]: # (`allowDefaultPortTo&#40;&#41;`.)

[//]: # ()
[//]: # (For example:)

[//]: # ()
[//]: # (```ts)

[//]: # (declare const listener: elbv2.ApplicationListener;)

[//]: # (declare const appFleet: autoscaling.AutoScalingGroup;)

[//]: # (declare const rdsDatabase: rds.DatabaseCluster;)

[//]: # ()
[//]: # (// Port implicit in listener)

[//]: # (listener.connections.allowDefaultPortFromAnyIpv4&#40;'Allow public'&#41;;)

[//]: # ()
[//]: # (// Port implicit in peer)

[//]: # (appFleet.connections.allowDefaultPortTo&#40;rdsDatabase, 'Fleet can access database'&#41;;)

[//]: # (```)

[//]: # ()
[//]: # (### Security group rules)

[//]: # ()
[//]: # (By default, security group wills be added inline to the security group in the output cloud formation)

[//]: # (template, if applicable.  This includes any static rules by ip address and port range.  This)

[//]: # (optimization helps to minimize the size of the template.)

[//]: # ()
[//]: # (In some environments this is not desirable, for example if your security group access is controlled)

[//]: # (via tags. You can disable inline rules per security group or globally via the context key)

[//]: # (`@aws-cdk/aws-ec2.securityGroupDisableInlineRules`.)

[//]: # ()
[//]: # (```ts fixture=with-vpc)

[//]: # (const mySecurityGroupWithoutInlineRules = new ec2.SecurityGroup&#40;this, 'SecurityGroup', {)

[//]: # (  vpc,)

[//]: # (  description: 'Allow ssh access to ec2 instances',)

[//]: # (  allowAllOutbound: true,)

[//]: # (  disableInlineRules: true)

[//]: # (}&#41;;)

[//]: # (//This will add the rule as an external cloud formation construct)

[//]: # (mySecurityGroupWithoutInlineRules.addIngressRule&#40;ec2.Peer.anyIpv4&#40;&#41;, ec2.Port.SSH, 'allow ssh access from the world'&#41;;)

[//]: # (```)

[//]: # ()
[//]: # (### Importing an existing security group)

[//]: # ()
[//]: # (If you know the ID and the configuration of the security group to import, you can use `SecurityGroup.fromSecurityGroupId`:)

[//]: # ()
[//]: # (```ts)

[//]: # (const sg = ec2.SecurityGroup.fromSecurityGroupId&#40;this, 'SecurityGroupImport', 'sg-1234', {)

[//]: # (  allowAllOutbound: true,)

[//]: # (}&#41;;)

[//]: # (```)

[//]: # ()
[//]: # (Alternatively, use lookup methods to import security groups if you do not know the ID or the configuration details. Method `SecurityGroup.fromLookupByName` looks up a security group if the security group ID is unknown.)

[//]: # ()
[//]: # (```ts fixture=with-vpc)

[//]: # (const sg = ec2.SecurityGroup.fromLookupByName&#40;this, 'SecurityGroupLookup', 'security-group-name', vpc&#41;;)

[//]: # (```)

[//]: # ()
[//]: # (If the security group ID is known and configuration details are unknown, use method `SecurityGroup.fromLookupById` instead. This method will lookup property `allowAllOutbound` from the current configuration of the security group.)

[//]: # ()
[//]: # (```ts)

[//]: # (const sg = ec2.SecurityGroup.fromLookupById&#40;this, 'SecurityGroupLookup', 'sg-1234'&#41;;)

[//]: # (```)

[//]: # ()
[//]: # (The result of `SecurityGroup.fromLookupByName` and `SecurityGroup.fromLookupById` operations will be written to a file called `cdk.context.json`. You must commit this file to source control so that the lookup values are available in non-privileged environments such as CI build steps, and to ensure your template builds are repeatable.)

[//]: # ()
[//]: # (### Cross Stack Connections)

[//]: # ()
[//]: # (If you are attempting to add a connection from a peer in one stack to a peer in a different stack, sometimes it is necessary to ensure that you are making the connection in)

[//]: # (a specific stack in order to avoid a cyclic reference. If there are no other dependencies between stacks then it will not matter in which stack you make)

[//]: # (the connection, but if there are existing dependencies &#40;i.e. stack1 already depends on stack2&#41;, then it is important to make the connection in the dependent stack &#40;i.e. stack1&#41;.)

[//]: # ()
[//]: # (Whenever you make a `connections` function call, the ingress and egress security group rules will be added to the stack that the calling object exists in.)

[//]: # (So if you are doing something like `peer1.connections.allowFrom&#40;peer2&#41;`, then the security group rules &#40;both ingress and egress&#41; will be created in `peer1`'s Stack.)

[//]: # ()
[//]: # (As an example, if we wanted to allow a connection from a security group in one stack &#40;egress&#41; to a security group in a different stack &#40;ingress&#41;,)

[//]: # (we would make the connection like:)

[//]: # ()
[//]: # (**If Stack1 depends on Stack2**)

[//]: # ()
[//]: # (```ts fixture=with-vpc)

[//]: # (// Stack 1)

[//]: # (declare const stack1: Stack;)

[//]: # (declare const stack2: Stack;)

[//]: # ()
[//]: # (const sg1 = new ec2.SecurityGroup&#40;stack1, 'SG1', {)

[//]: # (  allowAllOutbound: false, // if this is `true` then no egress rule will be created)

[//]: # (  vpc,)

[//]: # (}&#41;;)

[//]: # ()
[//]: # (// Stack 2)

[//]: # (const sg2 = new ec2.SecurityGroup&#40;stack2, 'SG2', {)

[//]: # (  allowAllOutbound: false, // if this is `true` then no egress rule will be created)

[//]: # (  vpc,)

[//]: # (}&#41;;)

[//]: # ()
[//]: # ()
[//]: # (// `connections.allowTo` on `sg1` since we want the)

[//]: # (// rules to be created in Stack1)

[//]: # (sg1.connections.allowTo&#40;sg2, ec2.Port.tcp&#40;3333&#41;&#41;;)

[//]: # (```)

[//]: # ()
[//]: # (In this case both the Ingress Rule for `sg2` and the Egress Rule for `sg1` will both be created)

[//]: # (in `Stack 1` which avoids the cyclic reference.)

[//]: # ()
[//]: # ()
[//]: # (**If Stack2 depends on Stack1**)

[//]: # ()
[//]: # (```ts fixture=with-vpc)

[//]: # (// Stack 1)

[//]: # (declare const stack1: Stack;)

[//]: # (declare const stack2: Stack;)

[//]: # ()
[//]: # (const sg1 = new ec2.SecurityGroup&#40;stack1, 'SG1', {)

[//]: # (  allowAllOutbound: false, // if this is `true` then no egress rule will be created)

[//]: # (  vpc,)

[//]: # (}&#41;;)

[//]: # ()
[//]: # (// Stack 2)

[//]: # (const sg2 = new ec2.SecurityGroup&#40;stack2, 'SG2', {)

[//]: # (  allowAllOutbound: false, // if this is `true` then no egress rule will be created)

[//]: # (  vpc,)

[//]: # (}&#41;;)

[//]: # ()
[//]: # ()
[//]: # (// `connections.allowFrom` on `sg2` since we want the)

[//]: # (// rules to be created in Stack2)

[//]: # (sg2.connections.allowFrom&#40;sg1, ec2.Port.tcp&#40;3333&#41;&#41;;)

[//]: # (```)

[//]: # ()
[//]: # (In this case both the Ingress Rule for `sg2` and the Egress Rule for `sg1` will both be created)

[//]: # (in `Stack 2` which avoids the cyclic reference.)

[//]: # ()
[//]: # (## Machine Images &#40;AMIs&#41;)

[//]: # ()
[//]: # (AMIs control the OS that gets launched when you start your EC2 instance. The EC2)

[//]: # (library contains constructs to select the AMI you want to use.)

[//]: # ()
[//]: # (Depending on the type of AMI, you select it a different way. Here are some)

[//]: # (examples of images you might want to use:)

[//]: # ()
[//]: # ([example of creating images]&#40;test/example.images.lit.ts&#41;)

[//]: # ()
[//]: # (> NOTE: The AMIs selected by `MachineImage.lookup&#40;&#41;` will be cached in)

[//]: # (> `cdk.context.json`, so that your AutoScalingGroup instances aren't replaced while)

[//]: # (> you are making unrelated changes to your CDK app.)

[//]: # (>)

[//]: # (> To query for the latest AMI again, remove the relevant cache entry from)

[//]: # (> `cdk.context.json`, or use the `cdk context` command. For more information, see)

[//]: # (> [Runtime Context]&#40;https://docs.aws.amazon.com/cdk/latest/guide/context.html&#41; in the CDK)

[//]: # (> developer guide.)

[//]: # (>)

[//]: # (> `MachineImage.genericLinux&#40;&#41;`, `MachineImage.genericWindows&#40;&#41;` will use `CfnMapping` in)

[//]: # (> an agnostic stack.)

[//]: # ()
[//]: # (## Special VPC configurations)

[//]: # ()
[//]: # (### VPN connections to a VPC)

[//]: # ()
[//]: # (Create your VPC with VPN connections by specifying the `vpnConnections` props &#40;keys are construct `id`s&#41;:)

[//]: # ()
[//]: # (```ts)

[//]: # (import { SecretValue } from 'aws-cdk-lib/core';)

[//]: # ()
[//]: # (const vpc = new ec2.Vpc&#40;this, 'MyVpc', {)

[//]: # (  vpnConnections: {)

[//]: # (    dynamic: { // Dynamic routing &#40;BGP&#41;)

[//]: # (      ip: '1.2.3.4',)

[//]: # (      tunnelOptions: [)

[//]: # (        {)

[//]: # (          preSharedKeySecret: SecretValue.unsafePlainText&#40;'secretkey1234'&#41;,)

[//]: # (        },)

[//]: # (        {)

[//]: # (          preSharedKeySecret: SecretValue.unsafePlainText&#40;'secretkey5678'&#41;,)

[//]: # (        },)

[//]: # (      ],)

[//]: # (    },)

[//]: # (    static: { // Static routing)

[//]: # (      ip: '4.5.6.7',)

[//]: # (      staticRoutes: [)

[//]: # (        '192.168.10.0/24',)

[//]: # (        '192.168.20.0/24')

[//]: # (      ])

[//]: # (    })

[//]: # (  })

[//]: # (}&#41;;)

[//]: # (```)

[//]: # ()
[//]: # (To create a VPC that can accept VPN connections, set `vpnGateway` to `true`:)

[//]: # ()
[//]: # (```ts)

[//]: # (const vpc = new ec2.Vpc&#40;this, 'MyVpc', {)

[//]: # (  vpnGateway: true)

[//]: # (}&#41;;)

[//]: # (```)

[//]: # ()
[//]: # (VPN connections can then be added:)

[//]: # ()
[//]: # (```ts fixture=with-vpc)

[//]: # (vpc.addVpnConnection&#40;'Dynamic', {)

[//]: # (  ip: '1.2.3.4')

[//]: # (}&#41;;)

[//]: # (```)

[//]: # ()
[//]: # (By default, routes will be propagated on the route tables associated with the private subnets. If no)

[//]: # (private subnets exist, isolated subnets are used. If no isolated subnets exist, public subnets are)

[//]: # (used. Use the `Vpc` property `vpnRoutePropagation` to customize this behavior.)

[//]: # ()
[//]: # (VPN connections expose [metrics &#40;cloudwatch.Metric&#41;]&#40;https://github.com/aws/aws-cdk/blob/main/packages/aws-cdk-lib/aws-cloudwatch/README.md&#41; across all tunnels in the account/region and per connection:)

[//]: # ()
[//]: # (```ts fixture=with-vpc)

[//]: # (// Across all tunnels in the account/region)

[//]: # (const allDataOut = ec2.VpnConnection.metricAllTunnelDataOut&#40;&#41;;)

[//]: # ()
[//]: # (// For a specific vpn connection)

[//]: # (const vpnConnection = vpc.addVpnConnection&#40;'Dynamic', {)

[//]: # (  ip: '1.2.3.4')

[//]: # (}&#41;;)

[//]: # (const state = vpnConnection.metricTunnelState&#40;&#41;;)

[//]: # (```)

[//]: # ()
[//]: # (### VPC endpoints)

[//]: # ()
[//]: # (A VPC endpoint enables you to privately connect your VPC to supported AWS services and VPC endpoint services powered by PrivateLink without requiring an internet gateway, NAT device, VPN connection, or AWS Direct Connect connection. Instances in your VPC do not require public IP addresses to communicate with resources in the service. Traffic between your VPC and the other service does not leave the Amazon network.)

[//]: # ()
[//]: # (Endpoints are virtual devices. They are horizontally scaled, redundant, and highly available VPC components that allow communication between instances in your VPC and services without imposing availability risks or bandwidth constraints on your network traffic.)

[//]: # ()
[//]: # ([example of setting up VPC endpoints]&#40;test/integ.vpc-endpoint.lit.ts&#41;)

[//]: # ()
[//]: # (By default, CDK will place a VPC endpoint in one subnet per AZ. If you wish to override the AZs CDK places the VPC endpoint in,)

[//]: # (use the `subnets` parameter as follows:)

[//]: # ()
[//]: # (```ts)

[//]: # (declare const vpc: ec2.Vpc;)

[//]: # ()
[//]: # (new ec2.InterfaceVpcEndpoint&#40;this, 'VPC Endpoint', {)

[//]: # (  vpc,)

[//]: # (  service: new ec2.InterfaceVpcEndpointService&#40;'com.amazonaws.vpce.us-east-1.vpce-svc-uuddlrlrbastrtsvc', 443&#41;,)

[//]: # (  // Choose which availability zones to place the VPC endpoint in, based on)

[//]: # (  // available AZs)

[//]: # (  subnets: {)

[//]: # (    availabilityZones: ['us-east-1a', 'us-east-1c'])

[//]: # (  })

[//]: # (}&#41;;)

[//]: # (```)

[//]: # ()
[//]: # (Per the [AWS documentation]&#40;https://aws.amazon.com/premiumsupport/knowledge-center/interface-endpoint-availability-zone/&#41;, not all)

[//]: # (VPC endpoint services are available in all AZs. If you specify the parameter `lookupSupportedAzs`, CDK attempts to discover which)

[//]: # (AZs an endpoint service is available in, and will ensure the VPC endpoint is not placed in a subnet that doesn't match those AZs.)

[//]: # (These AZs will be stored in cdk.context.json.)

[//]: # ()
[//]: # (```ts)

[//]: # (declare const vpc: ec2.Vpc;)

[//]: # ()
[//]: # (new ec2.InterfaceVpcEndpoint&#40;this, 'VPC Endpoint', {)

[//]: # (  vpc,)

[//]: # (  service: new ec2.InterfaceVpcEndpointService&#40;'com.amazonaws.vpce.us-east-1.vpce-svc-uuddlrlrbastrtsvc', 443&#41;,)

[//]: # (  // Choose which availability zones to place the VPC endpoint in, based on)

[//]: # (  // available AZs)

[//]: # (  lookupSupportedAzs: true)

[//]: # (}&#41;;)

[//]: # (```)

[//]: # ()
[//]: # (Pre-defined AWS services are defined in the [InterfaceVpcEndpointAwsService]&#40;lib/vpc-endpoint.ts&#41; class, and can be used to)

[//]: # (create VPC endpoints without having to configure name, ports, etc. For example, a Keyspaces endpoint can be created for)

[//]: # (use in your VPC:)

[//]: # ()
[//]: # (``` ts)

[//]: # (declare const vpc: ec2.Vpc;)

[//]: # ()
[//]: # (new ec2.InterfaceVpcEndpoint&#40;this, 'VPC Endpoint', {)

[//]: # (  vpc,)

[//]: # (  service: ec2.InterfaceVpcEndpointAwsService.KEYSPACES,)

[//]: # (}&#41;;)

[//]: # (```)

[//]: # ()
[//]: # (#### Security groups for interface VPC endpoints)

[//]: # ()
[//]: # (By default, interface VPC endpoints create a new security group and all traffic to the endpoint from within the VPC will be automatically allowed.)

[//]: # ()
[//]: # (Use the `connections` object to allow other traffic to flow to the endpoint:)

[//]: # ()
[//]: # (```ts)

[//]: # (declare const myEndpoint: ec2.InterfaceVpcEndpoint;)

[//]: # ()
[//]: # (myEndpoint.connections.allowDefaultPortFromAnyIpv4&#40;&#41;;)

[//]: # (```)

[//]: # ()
[//]: # (Alternatively, existing security groups can be used by specifying the `securityGroups` prop.)

[//]: # ()
[//]: # (### VPC endpoint services)

[//]: # ()
[//]: # (A VPC endpoint service enables you to expose a Network Load Balancer&#40;s&#41; as a provider service to consumers, who connect to your service over a VPC endpoint. You can restrict access to your service via allowed principals &#40;anything that extends ArnPrincipal&#41;, and require that new connections be manually accepted. You can also enable Contributor Insight rules.)

[//]: # ()
[//]: # (```ts)

[//]: # (declare const networkLoadBalancer1: elbv2.NetworkLoadBalancer;)

[//]: # (declare const networkLoadBalancer2: elbv2.NetworkLoadBalancer;)

[//]: # ()
[//]: # (new ec2.VpcEndpointService&#40;this, 'EndpointService', {)

[//]: # (  vpcEndpointServiceLoadBalancers: [networkLoadBalancer1, networkLoadBalancer2],)

[//]: # (  acceptanceRequired: true,)

[//]: # (  allowedPrincipals: [new iam.ArnPrincipal&#40;'arn:aws:iam::123456789012:root'&#41;],)

[//]: # (  contributorInsights: true)

[//]: # (}&#41;;)

[//]: # (```)

[//]: # ()
[//]: # (You can also include a service principal in the `allowedPrincipals` property by specifying it as a parameter to the  `ArnPrincipal` constructor.)

[//]: # (The resulting VPC endpoint will have an allowlisted principal of type `Service`, instead of `Arn` for that item in the list.)

[//]: # (```ts)

[//]: # (declare const networkLoadBalancer: elbv2.NetworkLoadBalancer;)

[//]: # ()
[//]: # (new ec2.VpcEndpointService&#40;this, 'EndpointService', {)

[//]: # (  vpcEndpointServiceLoadBalancers: [networkLoadBalancer],)

[//]: # (  allowedPrincipals: [new iam.ArnPrincipal&#40;'ec2.amazonaws.com'&#41;],)

[//]: # (}&#41;;)

[//]: # (```)

[//]: # ()
[//]: # (Endpoint services support private DNS, which makes it easier for clients to connect to your service by automatically setting up DNS in their VPC.)

[//]: # (You can enable private DNS on an endpoint service like so:)

[//]: # ()
[//]: # (```ts)

[//]: # (import { PublicHostedZone, VpcEndpointServiceDomainName } from 'aws-cdk-lib/aws-route53';)

[//]: # (declare const zone: PublicHostedZone;)

[//]: # (declare const vpces: ec2.VpcEndpointService;)

[//]: # ()
[//]: # (new VpcEndpointServiceDomainName&#40;this, 'EndpointDomain', {)

[//]: # (  endpointService: vpces,)

[//]: # (  domainName: 'my-stuff.aws-cdk.dev',)

[//]: # (  publicHostedZone: zone,)

[//]: # (}&#41;;)

[//]: # (```)

[//]: # ()
[//]: # (Note: The domain name must be owned &#40;registered through Route53&#41; by the account the endpoint service is in, or delegated to the account.)

[//]: # (The VpcEndpointServiceDomainName will handle the AWS side of domain verification, the process for which can be found)

[//]: # ([here]&#40;https://docs.aws.amazon.com/vpc/latest/userguide/endpoint-services-dns-validation.html&#41;)

[//]: # ()
[//]: # (### Client VPN endpoint)

[//]: # ()
[//]: # (AWS Client VPN is a managed client-based VPN service that enables you to securely access your AWS)

[//]: # (resources and resources in your on-premises network. With Client VPN, you can access your resources)

[//]: # (from any location using an OpenVPN-based VPN client.)

[//]: # ()
[//]: # (Use the `addClientVpnEndpoint&#40;&#41;` method to add a client VPN endpoint to a VPC:)

[//]: # ()
[//]: # (```ts fixture=client-vpn)

[//]: # (vpc.addClientVpnEndpoint&#40;'Endpoint', {)

[//]: # (  cidr: '10.100.0.0/16',)

[//]: # (  serverCertificateArn: 'arn:aws:acm:us-east-1:123456789012:certificate/server-certificate-id',)

[//]: # (  // Mutual authentication)

[//]: # (  clientCertificateArn: 'arn:aws:acm:us-east-1:123456789012:certificate/client-certificate-id',)

[//]: # (  // User-based authentication)

[//]: # (  userBasedAuthentication: ec2.ClientVpnUserBasedAuthentication.federated&#40;samlProvider&#41;,)

[//]: # (}&#41;;)

[//]: # (```)

[//]: # ()
[//]: # (The endpoint must use at least one [authentication method]&#40;https://docs.aws.amazon.com/vpn/latest/clientvpn-admin/client-authentication.html&#41;:)

[//]: # ()
[//]: # (* Mutual authentication with a client certificate)

[//]: # (* User-based authentication &#40;directory or federated&#41;)

[//]: # ()
[//]: # (If user-based authentication is used, the [self-service portal URL]&#40;https://docs.aws.amazon.com/vpn/latest/clientvpn-user/self-service-portal.html&#41;)

[//]: # (is made available via a CloudFormation output.)

[//]: # ()
[//]: # (By default, a new security group is created, and logging is enabled. Moreover, a rule to)

[//]: # (authorize all users to the VPC CIDR is created.)

[//]: # ()
[//]: # (To customize authorization rules, set the `authorizeAllUsersToVpcCidr` prop to `false`)

[//]: # (and use `addAuthorizationRule&#40;&#41;`:)

[//]: # ()
[//]: # (```ts fixture=client-vpn)

[//]: # (const endpoint = vpc.addClientVpnEndpoint&#40;'Endpoint', {)

[//]: # (  cidr: '10.100.0.0/16',)

[//]: # (  serverCertificateArn: 'arn:aws:acm:us-east-1:123456789012:certificate/server-certificate-id',)

[//]: # (  userBasedAuthentication: ec2.ClientVpnUserBasedAuthentication.federated&#40;samlProvider&#41;,)

[//]: # (  authorizeAllUsersToVpcCidr: false,)

[//]: # (}&#41;;)

[//]: # ()
[//]: # (endpoint.addAuthorizationRule&#40;'Rule', {)

[//]: # (  cidr: '10.0.10.0/32',)

[//]: # (  groupId: 'group-id',)

[//]: # (}&#41;;)

[//]: # (```)

[//]: # ()
[//]: # (Use `addRoute&#40;&#41;` to configure network routes:)

[//]: # ()
[//]: # (```ts fixture=client-vpn)

[//]: # (const endpoint = vpc.addClientVpnEndpoint&#40;'Endpoint', {)

[//]: # (  cidr: '10.100.0.0/16',)

[//]: # (  serverCertificateArn: 'arn:aws:acm:us-east-1:123456789012:certificate/server-certificate-id',)

[//]: # (  userBasedAuthentication: ec2.ClientVpnUserBasedAuthentication.federated&#40;samlProvider&#41;,)

[//]: # (}&#41;;)

[//]: # ()
[//]: # (// Client-to-client access)

[//]: # (endpoint.addRoute&#40;'Route', {)

[//]: # (  cidr: '10.100.0.0/16',)

[//]: # (  target: ec2.ClientVpnRouteTarget.local&#40;&#41;,)

[//]: # (}&#41;;)

[//]: # (```)

[//]: # ()
[//]: # (Use the `connections` object of the endpoint to allow traffic to other security groups.)

[//]: # ()
[//]: # (## Instances)

[//]: # ()
[//]: # (You can use the `Instance` class to start up a single EC2 instance. For production setups, we recommend)

[//]: # (you use an `AutoScalingGroup` from the `aws-autoscaling` module instead, as AutoScalingGroups will take)

[//]: # (care of restarting your instance if it ever fails.)

[//]: # ()
[//]: # (```ts)

[//]: # (declare const vpc: ec2.Vpc;)

[//]: # (declare const instanceType: ec2.InstanceType;)

[//]: # ()
[//]: # (// Amazon Linux 2)

[//]: # (new ec2.Instance&#40;this, 'Instance2', {)

[//]: # (  vpc,)

[//]: # (  instanceType,)

[//]: # (  machineImage: ec2.MachineImage.latestAmazonLinux2&#40;&#41;,)

[//]: # (}&#41;;)

[//]: # ()
[//]: # (// Amazon Linux 2 with kernel 5.x)

[//]: # (new ec2.Instance&#40;this, 'Instance3', {)

[//]: # (  vpc,)

[//]: # (  instanceType,)

[//]: # (  machineImage: ec2.MachineImage.latestAmazonLinux2&#40;{)

[//]: # (    kernel: ec2.AmazonLinux2Kernel.KERNEL_5_10,)

[//]: # (  }&#41;,)

[//]: # (}&#41;;)

[//]: # ()
[//]: # (// Amazon Linux 2023)

[//]: # (new ec2.Instance&#40;this, 'Instance4', {)

[//]: # (  vpc,)

[//]: # (  instanceType,)

[//]: # (  machineImage: ec2.MachineImage.latestAmazonLinux2023&#40;&#41;,)

[//]: # (}&#41;;)

[//]: # ()
[//]: # (// Graviton 3 Processor)

[//]: # (new ec2.Instance&#40;this, 'Instance5', {)

[//]: # (  vpc,)

[//]: # (  instanceType: ec2.InstanceType.of&#40;ec2.InstanceClass.C7G, ec2.InstanceSize.LARGE&#41;,)

[//]: # (  machineImage: ec2.MachineImage.latestAmazonLinux2023&#40;{)

[//]: # (    cpuType: ec2.AmazonLinuxCpuType.ARM_64,)

[//]: # (  }&#41;,)

[//]: # (}&#41;;)

[//]: # (```)

[//]: # ()
[//]: # (### Latest Amazon Linux Images)

[//]: # ()
[//]: # (Rather than specifying a specific AMI ID to use, it is possible to specify a SSM)

[//]: # (Parameter that contains the AMI ID. AWS publishes a set of [public parameters]&#40;https://docs.aws.amazon.com/systems-manager/latest/userguide/parameter-store-public-parameters-ami.html&#41;)

[//]: # (that contain the latest Amazon Linux AMIs. To make it easier to query a)

[//]: # (particular image parameter, the CDK provides a couple of constructs `AmazonLinux2ImageSsmParameter`,)

[//]: # (`AmazonLinux2022ImageSsmParameter`, & `AmazonLinux2023SsmParameter`. For example)

[//]: # (to use the latest `al2023` image:)

[//]: # ()
[//]: # (```ts)

[//]: # (declare const vpc: ec2.Vpc;)

[//]: # ()
[//]: # (new ec2.Instance&#40;this, 'LatestAl2023', {)

[//]: # (  vpc,)

[//]: # (  instanceType: ec2.InstanceType.of&#40;ec2.InstanceClass.C7G, ec2.InstanceSize.LARGE&#41;,)

[//]: # (  machineImage: ec2.MachineImage.latestAmazonLinux2023&#40;&#41;,)

[//]: # (}&#41;;)

[//]: # (```)

[//]: # ()
[//]: # (> **Warning**)

[//]: # (> Since this retrieves the value from an SSM parameter at deployment time, the)

[//]: # (> value will be resolved each time the stack is deployed. This means that if)

[//]: # (> the parameter contains a different value on your next deployment, the instance)

[//]: # (> will be replaced.)

[//]: # ()
[//]: # (It is also possible to perform the lookup once at synthesis time and then cache)

[//]: # (the value in CDK context. This way the value will not change on future)

[//]: # (deployments unless you manually refresh the context.)

[//]: # ()
[//]: # (```ts)

[//]: # (declare const vpc: ec2.Vpc;)

[//]: # ()
[//]: # (new ec2.Instance&#40;this, 'LatestAl2023', {)

[//]: # (  vpc,)

[//]: # (  instanceType: ec2.InstanceType.of&#40;ec2.InstanceClass.C7G, ec2.InstanceSize.LARGE&#41;,)

[//]: # (  machineImage: ec2.MachineImage.latestAmazonLinux2023&#40;{)

[//]: # (    cachedInContext: true, // default is false)

[//]: # (  }&#41;,)

[//]: # (}&#41;;)

[//]: # ()
[//]: # (// or)

[//]: # (new ec2.Instance&#40;this, 'LatestAl2023', {)

[//]: # (  vpc,)

[//]: # (  instanceType: ec2.InstanceType.of&#40;ec2.InstanceClass.C7G, ec2.InstanceSize.LARGE&#41;,)

[//]: # (  // context cache is turned on by default)

[//]: # (  machineImage: new ec2.AmazonLinux2023ImageSsmParameter&#40;&#41;,)

[//]: # (}&#41;;)

[//]: # (```)

[//]: # ()
[//]: # (#### Kernel Versions)

[//]: # ()
[//]: # (Each Amazon Linux AMI uses a specific kernel version. Most Amazon Linux)

[//]: # (generations come with an AMI using the "default" kernel and then 1 or more)

[//]: # (AMIs using a specific kernel version, which may or may not be different from the)

[//]: # (default kernel version.)

[//]: # ()
[//]: # (For example, Amazon Linux 2 has two different AMIs available from the SSM)

[//]: # (parameters.)

[//]: # ()
[//]: # (- `/aws/service/ami-amazon-linux-latest/amzn2-ami-hvm-x86_64-ebs`)

[//]: # (  - This is the "default" kernel which uses `kernel-4.14`)

[//]: # (- `/aws/service/ami-amazon-linux-latest/amzn2-ami-kernel-5.10-hvm-x86_64-ebs`)

[//]: # ()
[//]: # (If a new Amazon Linux generation AMI is published with a new kernel version,)

[//]: # (then a new SSM parameter will be created with the new version)

[//]: # (&#40;e.g. `/aws/service/ami-amazon-linux-latest/amzn2-ami-kernel-5.15-hvm-x86_64-ebs`&#41;,)

[//]: # (but the "default" AMI may or may not be updated.)

[//]: # ()
[//]: # (If you would like to make sure you always have the latest kernel version, then)

[//]: # (either specify the specific latest kernel version or opt-in to using the CDK)

[//]: # (latest kernel version.)

[//]: # ()
[//]: # (```ts)

[//]: # (declare const vpc: ec2.Vpc;)

[//]: # ()
[//]: # (new ec2.Instance&#40;this, 'LatestAl2023', {)

[//]: # (  vpc,)

[//]: # (  instanceType: ec2.InstanceType.of&#40;ec2.InstanceClass.C7G, ec2.InstanceSize.LARGE&#41;,)

[//]: # (  // context cache is turned on by default)

[//]: # (  machineImage: new ec2.AmazonLinux2023ImageSsmParameter&#40;{)

[//]: # (    kernel: ec2.AmazonLinux2023Kernel.KERNEL_6_1,)

[//]: # (  }&#41;,)

[//]: # (}&#41;;)

[//]: # (```)

[//]: # (_CDK managed latest_)

[//]: # ()
[//]: # (```ts)

[//]: # (declare const vpc: ec2.Vpc;)

[//]: # ()
[//]: # (new ec2.Instance&#40;this, 'LatestAl2023', {)

[//]: # (  vpc,)

[//]: # (  instanceType: ec2.InstanceType.of&#40;ec2.InstanceClass.C7G, ec2.InstanceSize.LARGE&#41;,)

[//]: # (  // context cache is turned on by default)

[//]: # (  machineImage: new ec2.AmazonLinux2023ImageSsmParameter&#40;{)

[//]: # (    kernel: ec2.AmazonLinux2023Kernel.CDK_LATEST,)

[//]: # (  }&#41;,)

[//]: # (}&#41;;)

[//]: # ()
[//]: # (// or)

[//]: # ()
[//]: # (new ec2.Instance&#40;this, 'LatestAl2023', {)

[//]: # (  vpc,)

[//]: # (  instanceType: ec2.InstanceType.of&#40;ec2.InstanceClass.C7G, ec2.InstanceSize.LARGE&#41;,)

[//]: # (  machineImage: ec2.MachineImage.latestAmazonLinux2023&#40;&#41;, // always uses latest kernel version)

[//]: # (}&#41;;)

[//]: # (```)

[//]: # ()
[//]: # (When using the CDK managed latest version, when a new kernel version is made)

[//]: # (available the `LATEST` will be updated to point to the new kernel version. You)

[//]: # (then would be required to update the newest CDK version for it to take effect.)

[//]: # ()
[//]: # (### Configuring Instances using CloudFormation Init &#40;cfn-init&#41;)

[//]: # ()
[//]: # (CloudFormation Init allows you to configure your instances by writing files to them, installing software)

[//]: # (packages, starting services and running arbitrary commands. By default, if any of the instance setup)

[//]: # (commands throw an error; the deployment will fail and roll back to the previously known good state.)

[//]: # (The following documentation also applies to `AutoScalingGroup`s.)

[//]: # ()
[//]: # (For the full set of capabilities of this system, see the documentation for)

[//]: # ([`AWS::CloudFormation::Init`]&#40;https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-init.html&#41;.)

[//]: # (Here is an example of applying some configuration to an instance:)

[//]: # ()
[//]: # (```ts)

[//]: # (declare const vpc: ec2.Vpc;)

[//]: # (declare const instanceType: ec2.InstanceType;)

[//]: # (declare const machineImage: ec2.IMachineImage;)

[//]: # ()
[//]: # (new ec2.Instance&#40;this, 'Instance', {)

[//]: # (  vpc,)

[//]: # (  instanceType,)

[//]: # (  machineImage,)

[//]: # ()
[//]: # (  // Showing the most complex setup, if you have simpler requirements)

[//]: # (  // you can use `CloudFormationInit.fromElements&#40;&#41;`.)

[//]: # (  init: ec2.CloudFormationInit.fromConfigSets&#40;{)

[//]: # (    configSets: {)

[//]: # (      // Applies the configs below in this order)

[//]: # (      default: ['yumPreinstall', 'config'],)

[//]: # (    },)

[//]: # (    configs: {)

[//]: # (      yumPreinstall: new ec2.InitConfig&#40;[)

[//]: # (        // Install an Amazon Linux package using yum)

[//]: # (        ec2.InitPackage.yum&#40;'git'&#41;,)

[//]: # (      ]&#41;,)

[//]: # (      config: new ec2.InitConfig&#40;[)

[//]: # (        // Create a JSON file from tokens &#40;can also create other files&#41;)

[//]: # (        ec2.InitFile.fromObject&#40;'/etc/stack.json', {)

[//]: # (          stackId: Stack.of&#40;this&#41;.stackId,)

[//]: # (          stackName: Stack.of&#40;this&#41;.stackName,)

[//]: # (          region: Stack.of&#40;this&#41;.region,)

[//]: # (        }&#41;,)

[//]: # ()
[//]: # (        // Create a group and user)

[//]: # (        ec2.InitGroup.fromName&#40;'my-group'&#41;,)

[//]: # (        ec2.InitUser.fromName&#40;'my-user'&#41;,)

[//]: # ()
[//]: # (        // Install an RPM from the internet)

[//]: # (        ec2.InitPackage.rpm&#40;'http://mirrors.ukfast.co.uk/sites/dl.fedoraproject.org/pub/epel/8/Everything/x86_64/Packages/r/rubygem-git-1.5.0-2.el8.noarch.rpm'&#41;,)

[//]: # (      ]&#41;,)

[//]: # (    },)

[//]: # (  }&#41;,)

[//]: # (  initOptions: {)

[//]: # (    // Optional, which configsets to activate &#40;['default'] by default&#41;)

[//]: # (    configSets: ['default'],)

[//]: # ()
[//]: # (    // Optional, how long the installation is expected to take &#40;5 minutes by default&#41;)

[//]: # (    timeout: Duration.minutes&#40;30&#41;,)

[//]: # ()
[//]: # (    // Optional, whether to include the --url argument when running cfn-init and cfn-signal commands &#40;false by default&#41;)

[//]: # (    includeUrl: true,)

[//]: # ()
[//]: # (    // Optional, whether to include the --role argument when running cfn-init and cfn-signal commands &#40;false by default&#41;)

[//]: # (    includeRole: true,)

[//]: # (  },)

[//]: # (}&#41;;)

[//]: # (```)

[//]: # ()
[//]: # (`InitCommand` can not be used to start long-running processes. At deploy time,)

[//]: # (`cfn-init` will always wait for the process to exit before continuing, causing)

[//]: # (the CloudFormation deployment to fail because the signal hasn't been received)

[//]: # (within the expected timeout.)

[//]: # ()
[//]: # (Instead, you should install a service configuration file onto your machine `InitFile`,)

[//]: # (and then use `InitService` to start it.)

[//]: # ()
[//]: # (If your Linux OS is using SystemD &#40;like Amazon Linux 2 or higher&#41;, the CDK has)

[//]: # (helpers to create a long-running service using CFN Init. You can create a)

[//]: # (SystemD-compatible config file using `InitService.systemdConfigFile&#40;&#41;`, and)

[//]: # (start it immediately. The following examples shows how to start a trivial Python)

[//]: # (3 web server:)

[//]: # ()
[//]: # (```ts)

[//]: # (declare const vpc: ec2.Vpc;)

[//]: # (declare const instanceType: ec2.InstanceType;)

[//]: # ()
[//]: # (new ec2.Instance&#40;this, 'Instance', {)

[//]: # (  vpc,)

[//]: # (  instanceType,)

[//]: # (  machineImage: ec2.MachineImage.latestAmazonLinux2023&#40;&#41;,)

[//]: # ()
[//]: # (  init: ec2.CloudFormationInit.fromElements&#40;)

[//]: # (    // Create a simple config file that runs a Python web server)

[//]: # (    ec2.InitService.systemdConfigFile&#40;'simpleserver', {)

[//]: # (      command: '/usr/bin/python3 -m http.server 8080',)

[//]: # (      cwd: '/var/www/html',)

[//]: # (    }&#41;,)

[//]: # (    // Start the server using SystemD)

[//]: # (    ec2.InitService.enable&#40;'simpleserver', {)

[//]: # (      serviceManager: ec2.ServiceManager.SYSTEMD,)

[//]: # (    }&#41;,)

[//]: # (    // Drop an example file to show the web server working)

[//]: # (    ec2.InitFile.fromString&#40;'/var/www/html/index.html', 'Hello! It\'s working!'&#41;,)

[//]: # (  &#41;,)

[//]: # (}&#41;;)

[//]: # (```)

[//]: # ()
[//]: # (You can have services restarted after the init process has made changes to the system.)

[//]: # (To do that, instantiate an `InitServiceRestartHandle` and pass it to the config elements)

[//]: # (that need to trigger the restart and the service itself. For example, the following)

[//]: # (config writes a config file for nginx, extracts an archive to the root directory, and then)

[//]: # (restarts nginx so that it picks up the new config and files:)

[//]: # ()
[//]: # (```ts)

[//]: # (declare const myBucket: s3.Bucket;)

[//]: # ()
[//]: # (const handle = new ec2.InitServiceRestartHandle&#40;&#41;;)

[//]: # ()
[//]: # (ec2.CloudFormationInit.fromElements&#40;)

[//]: # (  ec2.InitFile.fromString&#40;'/etc/nginx/nginx.conf', '...', { serviceRestartHandles: [handle] }&#41;,)

[//]: # (  ec2.InitSource.fromS3Object&#40;'/var/www/html', myBucket, 'html.zip', { serviceRestartHandles: [handle] }&#41;,)

[//]: # (  ec2.InitService.enable&#40;'nginx', {)

[//]: # (    serviceRestartHandle: handle,)

[//]: # (  }&#41;)

[//]: # (&#41;;)

[//]: # (```)

[//]: # ()
[//]: # (You can use the `environmentVariables` or `environmentFiles` parameters to specify environment variables)

[//]: # (for your services:)

[//]: # ()
[//]: # (```ts)

[//]: # (new ec2.InitConfig&#40;[)

[//]: # (  ec2.InitFile.fromString&#40;'/myvars.env', 'VAR_FROM_FILE="VAR_FROM_FILE"'&#41;,)

[//]: # (  ec2.InitService.systemdConfigFile&#40;'myapp', {)

[//]: # (    command: '/usr/bin/python3 -m http.server 8080',)

[//]: # (    cwd: '/var/www/html',)

[//]: # (    environmentVariables: {)

[//]: # (      MY_VAR: 'MY_VAR',)

[//]: # (    },)

[//]: # (    environmentFiles: ['/myvars.env'],)

[//]: # (  }&#41;,)

[//]: # (]&#41;)

[//]: # (```)

[//]: # ()
[//]: # (### Bastion Hosts)

[//]: # ()
[//]: # (A bastion host functions as an instance used to access servers and resources in a VPC without open up the complete VPC on a network level.)

[//]: # (You can use bastion hosts using a standard SSH connection targeting port 22 on the host. As an alternative, you can connect the SSH connection)

[//]: # (feature of AWS Systems Manager Session Manager, which does not need an opened security group. &#40;https://aws.amazon.com/about-aws/whats-new/2019/07/session-manager-launches-tunneling-support-for-ssh-and-scp/&#41;)

[//]: # ()
[//]: # (A default bastion host for use via SSM can be configured like:)

[//]: # ()
[//]: # (```ts fixture=with-vpc)

[//]: # (const host = new ec2.BastionHostLinux&#40;this, 'BastionHost', { vpc }&#41;;)

[//]: # (```)

[//]: # ()
[//]: # (If you want to connect from the internet using SSH, you need to place the host into a public subnet. You can then configure allowed source hosts.)

[//]: # ()
[//]: # (```ts fixture=with-vpc)

[//]: # (const host = new ec2.BastionHostLinux&#40;this, 'BastionHost', {)

[//]: # (  vpc,)

[//]: # (  subnetSelection: { subnetType: ec2.SubnetType.PUBLIC },)

[//]: # (}&#41;;)

[//]: # (host.allowSshAccessFrom&#40;ec2.Peer.ipv4&#40;'1.2.3.4/32'&#41;&#41;;)

[//]: # (```)

[//]: # ()
[//]: # (As there are no SSH public keys deployed on this machine, you need to use [EC2 Instance Connect]&#40;https://aws.amazon.com/de/blogs/compute/new-using-amazon-ec2-instance-connect-for-ssh-access-to-your-ec2-instances/&#41;)

[//]: # (with the command `aws ec2-instance-connect send-ssh-public-key` to provide your SSH public key.)

[//]: # ()
[//]: # (EBS volume for the bastion host can be encrypted like:)

[//]: # ()
[//]: # (```ts fixture=with-vpc)

[//]: # (const host = new ec2.BastionHostLinux&#40;this, 'BastionHost', {)

[//]: # (  vpc,)

[//]: # (  blockDevices: [{)

[//]: # (    deviceName: '/dev/sdh',)

[//]: # (    volume: ec2.BlockDeviceVolume.ebs&#40;10, {)

[//]: # (      encrypted: true,)

[//]: # (    }&#41;,)

[//]: # (  }],)

[//]: # (}&#41;;)

[//]: # (```)

[//]: # ()
[//]: # (### Placement Group)

[//]: # ()
[//]: # (Specify `placementGroup` to enable the placement group support:)

[//]: # ()
[//]: # (```ts fixture=with-vpc)

[//]: # (declare const instanceType: ec2.InstanceType;)

[//]: # ()
[//]: # (const pg = new ec2.PlacementGroup&#40;this, 'test-pg', {)

[//]: # (  strategy: ec2.PlacementGroupStrategy.SPREAD,)

[//]: # (}&#41;;)

[//]: # ()
[//]: # (new ec2.Instance&#40;this, 'Instance', {)

[//]: # (  vpc,)

[//]: # (  instanceType,)

[//]: # (  machineImage: ec2.MachineImage.latestAmazonLinux2023&#40;&#41;,)

[//]: # (  placementGroup: pg,)

[//]: # (}&#41;;)

[//]: # (```)

[//]: # ()
[//]: # (### Block Devices)

[//]: # ()
[//]: # (To add EBS block device mappings, specify the `blockDevices` property. The following example sets the EBS-backed)

[//]: # (root device &#40;`/dev/sda1`&#41; size to 50 GiB, and adds another EBS-backed device mapped to `/dev/sdm` that is 100 GiB in)

[//]: # (size:)

[//]: # ()
[//]: # (```ts)

[//]: # (declare const vpc: ec2.Vpc;)

[//]: # (declare const instanceType: ec2.InstanceType;)

[//]: # (declare const machineImage: ec2.IMachineImage;)

[//]: # ()
[//]: # (new ec2.Instance&#40;this, 'Instance', {)

[//]: # (  vpc,)

[//]: # (  instanceType,)

[//]: # (  machineImage,)

[//]: # ()
[//]: # (  // ...)

[//]: # ()
[//]: # (  blockDevices: [)

[//]: # (    {)

[//]: # (      deviceName: '/dev/sda1',)

[//]: # (      volume: ec2.BlockDeviceVolume.ebs&#40;50&#41;,)

[//]: # (    },)

[//]: # (    {)

[//]: # (      deviceName: '/dev/sdm',)

[//]: # (      volume: ec2.BlockDeviceVolume.ebs&#40;100&#41;,)

[//]: # (    },)

[//]: # (  ],)

[//]: # (}&#41;;)

[//]: # ()
[//]: # (```)

[//]: # ()
[//]: # (It is also possible to encrypt the block devices. In this example we will create an customer managed key encrypted EBS-backed root device:)

[//]: # ()
[//]: # (```ts)

[//]: # (import { Key } from 'aws-cdk-lib/aws-kms';)

[//]: # ()
[//]: # (declare const vpc: ec2.Vpc;)

[//]: # (declare const instanceType: ec2.InstanceType;)

[//]: # (declare const machineImage: ec2.IMachineImage;)

[//]: # ()
[//]: # (const kmsKey = new Key&#40;this, 'KmsKey'&#41;)

[//]: # ()
[//]: # (new ec2.Instance&#40;this, 'Instance', {)

[//]: # (  vpc,)

[//]: # (  instanceType,)

[//]: # (  machineImage,)

[//]: # ()
[//]: # (  // ...)

[//]: # ()
[//]: # (  blockDevices: [)

[//]: # (    {)

[//]: # (      deviceName: '/dev/sda1',)

[//]: # (      volume: ec2.BlockDeviceVolume.ebs&#40;50, {)

[//]: # (        encrypted: true,)

[//]: # (        kmsKey: kmsKey,)

[//]: # (      }&#41;,)

[//]: # (    },)

[//]: # (  ],)

[//]: # (}&#41;;)

[//]: # ()
[//]: # (```)

[//]: # ()
[//]: # (To specify the throughput value for `gp3` volumes, use the `throughput` property:)

[//]: # ()
[//]: # (```ts)

[//]: # (declare const vpc: ec2.Vpc;)

[//]: # (declare const instanceType: ec2.InstanceType;)

[//]: # (declare const machineImage: ec2.IMachineImage;)

[//]: # ()
[//]: # (new ec2.Instance&#40;this, 'Instance', {)

[//]: # (  vpc,)

[//]: # (  instanceType,)

[//]: # (  machineImage,)

[//]: # ()
[//]: # (  // ...)

[//]: # ()
[//]: # (  blockDevices: [)

[//]: # (    {)

[//]: # (      deviceName: '/dev/sda1',)

[//]: # (      volume: ec2.BlockDeviceVolume.ebs&#40;100, {)

[//]: # (        volumeType: ec2.EbsDeviceVolumeType.GP3,)

[//]: # (        throughput: 250,)

[//]: # (      }&#41;,)

[//]: # (    },)

[//]: # (  ],)

[//]: # (}&#41;;)

[//]: # ()
[//]: # (```)

[//]: # ()
[//]: # (#### EBS Optimized Instances)

[//]: # ()
[//]: # (An Amazon EBS–optimized instance uses an optimized configuration stack and provides additional, dedicated capacity for Amazon EBS I/O. This optimization provides the best performance for your EBS volumes by minimizing contention between Amazon EBS I/O and other traffic from your instance.)

[//]: # ()
[//]: # (Depending on the instance type, this features is enabled by default while others require explicit activation. Please refer to the [documentation]&#40;https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ebs-optimized.html&#41; for details.)

[//]: # ()
[//]: # (```ts)

[//]: # (declare const vpc: ec2.Vpc;)

[//]: # (declare const instanceType: ec2.InstanceType;)

[//]: # (declare const machineImage: ec2.IMachineImage;)

[//]: # ()
[//]: # (new ec2.Instance&#40;this, 'Instance', {)

[//]: # (  vpc,)

[//]: # (  instanceType,)

[//]: # (  machineImage,)

[//]: # (  ebsOptimized: true,)

[//]: # (  blockDevices: [{)

[//]: # (    deviceName: '/dev/xvda',)

[//]: # (    volume: ec2.BlockDeviceVolume.ebs&#40;8&#41;,)

[//]: # (  }],)

[//]: # (}&#41;;)

[//]: # (```)

[//]: # ()
[//]: # (### Volumes)

[//]: # ()
[//]: # (Whereas a `BlockDeviceVolume` is an EBS volume that is created and destroyed as part of the creation and destruction of a specific instance. A `Volume` is for when you want an EBS volume separate from any particular instance. A `Volume` is an EBS block device that can be attached to, or detached from, any instance at any time. Some types of `Volume`s can also be attached to multiple instances at the same time to allow you to have shared storage between those instances.)

[//]: # ()
[//]: # (A notable restriction is that a Volume can only be attached to instances in the same availability zone as the Volume itself.)

[//]: # ()
[//]: # (The following demonstrates how to create a 500 GiB encrypted Volume in the `us-west-2a` availability zone, and give a role the ability to attach that Volume to a specific instance:)

[//]: # ()
[//]: # (```ts)

[//]: # (declare const instance: ec2.Instance;)

[//]: # (declare const role: iam.Role;)

[//]: # ()
[//]: # (const volume = new ec2.Volume&#40;this, 'Volume', {)

[//]: # (  availabilityZone: 'us-west-2a',)

[//]: # (  size: Size.gibibytes&#40;500&#41;,)

[//]: # (  encrypted: true,)

[//]: # (}&#41;;)

[//]: # ()
[//]: # (volume.grantAttachVolume&#40;role, [instance]&#41;;)

[//]: # (```)

[//]: # ()
[//]: # (#### Instances Attaching Volumes to Themselves)

[//]: # ()
[//]: # (If you need to grant an instance the ability to attach/detach an EBS volume to/from itself, then using `grantAttachVolume` and `grantDetachVolume` as outlined above)

[//]: # (will lead to an unresolvable circular reference between the instance role and the instance. In this case, use `grantAttachVolumeByResourceTag` and `grantDetachVolumeByResourceTag` as follows:)

[//]: # ()
[//]: # (```ts)

[//]: # (declare const instance: ec2.Instance;)

[//]: # (declare const volume: ec2.Volume;)

[//]: # ()
[//]: # (const attachGrant = volume.grantAttachVolumeByResourceTag&#40;instance.grantPrincipal, [instance]&#41;;)

[//]: # (const detachGrant = volume.grantDetachVolumeByResourceTag&#40;instance.grantPrincipal, [instance]&#41;;)

[//]: # (```)

[//]: # ()
[//]: # (#### Attaching Volumes)

[//]: # ()
[//]: # (The Amazon EC2 documentation for)

[//]: # ([Linux Instances]&#40;https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/AmazonEBS.html&#41; and)

[//]: # ([Windows Instances]&#40;https://docs.aws.amazon.com/AWSEC2/latest/WindowsGuide/ebs-volumes.html&#41; contains information on how)

[//]: # (to attach and detach your Volumes to/from instances, and how to format them for use.)

[//]: # ()
[//]: # (The following is a sample skeleton of EC2 UserData that can be used to attach a Volume to the Linux instance that it is running on:)

[//]: # ()
[//]: # (```ts)

[//]: # (declare const instance: ec2.Instance;)

[//]: # (declare const volume: ec2.Volume;)

[//]: # ()
[//]: # (volume.grantAttachVolumeByResourceTag&#40;instance.grantPrincipal, [instance]&#41;;)

[//]: # (const targetDevice = '/dev/xvdz';)

[//]: # (instance.userData.addCommands&#40;)

[//]: # (  // Retrieve token for accessing EC2 instance metadata &#40;https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instancedata-data-retrieval.html&#41;)

[//]: # (  `TOKEN=$&#40;curl -SsfX PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600"&#41;`,)

[//]: # (  // Retrieve the instance Id of the current EC2 instance)

[//]: # (  `INSTANCE_ID=$&#40;curl -SsfH "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/instance-id&#41;`,)

[//]: # (  // Attach the volume to /dev/xvdz)

[//]: # (  `aws --region ${Stack.of&#40;this&#41;.region} ec2 attach-volume --volume-id ${volume.volumeId} --instance-id $INSTANCE_ID --device ${targetDevice}`,)

[//]: # (  // Wait until the volume has attached)

[//]: # (  `while ! test -e ${targetDevice}; do sleep 1; done`)

[//]: # (  // The volume will now be mounted. You may have to add additional code to format the volume if it has not been prepared.)

[//]: # (&#41;;)

[//]: # (```)

[//]: # ()
[//]: # (#### Tagging Volumes)

[//]: # ()
[//]: # (You can configure [tag propagation on volume creation]&#40;https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-instance.html#cfn-ec2-instance-propagatetagstovolumeoncreation&#41;.)

[//]: # ()
[//]: # (```ts)

[//]: # (  declare const vpc: ec2.Vpc;)

[//]: # (  declare const instanceType: ec2.InstanceType;)

[//]: # (  declare const machineImage: ec2.IMachineImage;)

[//]: # ()
[//]: # (  new ec2.Instance&#40;this, 'Instance', {)

[//]: # (    vpc,)

[//]: # (    machineImage,)

[//]: # (    instanceType,)

[//]: # (    propagateTagsToVolumeOnCreation: true,)

[//]: # (  }&#41;;)

[//]: # (```)

[//]: # ()
[//]: # (#### Throughput on GP3 Volumes)

[//]: # ()
[//]: # (You can specify the `throughput` of a GP3 volume from 125 &#40;default&#41; to 1000.)

[//]: # ()
[//]: # (```ts)

[//]: # (new ec2.Volume&#40;this, 'Volume', {)

[//]: # (  availabilityZone: 'us-east-1a',)

[//]: # (  size: Size.gibibytes&#40;125&#41;,)

[//]: # (  volumeType: ec2.EbsDeviceVolumeType.GP3,)

[//]: # (  throughput: 125,)

[//]: # (}&#41;;)

[//]: # (```)

[//]: # ()
[//]: # (### Configuring Instance Metadata Service &#40;IMDS&#41;)

[//]: # ()
[//]: # (#### Toggling IMDSv1)

[//]: # ()
[//]: # (You can configure [EC2 Instance Metadata Service]&#40;https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-metadata.html&#41; options to either)

[//]: # (allow both IMDSv1 and IMDSv2 or enforce IMDSv2 when interacting with the IMDS.)

[//]: # ()
[//]: # (To do this for a single `Instance`, you can use the `requireImdsv2` property.)

[//]: # (The example below demonstrates IMDSv2 being required on a single `Instance`:)

[//]: # ()
[//]: # (```ts)

[//]: # (declare const vpc: ec2.Vpc;)

[//]: # (declare const instanceType: ec2.InstanceType;)

[//]: # (declare const machineImage: ec2.IMachineImage;)

[//]: # ()
[//]: # (new ec2.Instance&#40;this, 'Instance', {)

[//]: # (  vpc,)

[//]: # (  instanceType,)

[//]: # (  machineImage,)

[//]: # ()
[//]: # (  // ...)

[//]: # ()
[//]: # (  requireImdsv2: true,)

[//]: # (}&#41;;)

[//]: # (```)

[//]: # ()
[//]: # (You can also use the either the `InstanceRequireImdsv2Aspect` for EC2 instances or the `LaunchTemplateRequireImdsv2Aspect` for EC2 launch templates)

[//]: # (to apply the operation to multiple instances or launch templates, respectively.)

[//]: # ()
[//]: # (The following example demonstrates how to use the `InstanceRequireImdsv2Aspect` to require IMDSv2 for all EC2 instances in a stack:)

[//]: # ()
[//]: # (```ts)

[//]: # (const aspect = new ec2.InstanceRequireImdsv2Aspect&#40;&#41;;)

[//]: # (Aspects.of&#40;this&#41;.add&#40;aspect&#41;;)

[//]: # (```)

[//]: # ()
[//]: # (### Associating a Public IP Address with an Instance)

[//]: # ()
[//]: # (All subnets have an attribute that determines whether instances launched into that subnet are assigned a public IPv4 address. This attribute is set to true by default for default public subnets. Thus, an EC2 instance launched into a default public subnet will be assigned a public IPv4 address. Nondefault public subnets have this attribute set to false by default and any EC2 instance launched into a nondefault public subnet will not be assigned a public IPv4 address automatically. To automatically assign a public IPv4 address to an instance launched into a nondefault public subnet, you can set the `associatePublicIpAddress` property on the `Instance` construct to true. Alternatively, to not automatically assign a public IPv4 address to an instance launched into a default public subnet, you can set `associatePublicIpAddress` to false. Including this property, removing this property, or updating the value of this property on an existing instance will result in replacement of the instance.)

[//]: # ()
[//]: # (```ts)

[//]: # (const vpc = new ec2.Vpc&#40;this, 'VPC', {)

[//]: # (  cidr: '10.0.0.0/16',)

[//]: # (  natGateways: 0,)

[//]: # (  maxAzs: 3,)

[//]: # (  subnetConfiguration: [)

[//]: # (    {)

[//]: # (      name: 'public-subnet-1',)

[//]: # (      subnetType: ec2.SubnetType.PUBLIC,)

[//]: # (      cidrMask: 24,)

[//]: # (    },)

[//]: # (  ],)

[//]: # (}&#41;;)

[//]: # ()
[//]: # (const instance = new ec2.Instance&#40;this, 'Instance', {)

[//]: # (  vpc,)

[//]: # (  vpcSubnets: { subnetGroupName: 'public-subnet-1' },)

[//]: # (  instanceType: ec2.InstanceType.of&#40;ec2.InstanceClass.T3, ec2.InstanceSize.NANO&#41;,)

[//]: # (  machineImage: new ec2.AmazonLinuxImage&#40;{ generation: ec2.AmazonLinuxGeneration.AMAZON_LINUX_2 }&#41;,)

[//]: # (  detailedMonitoring: true,)

[//]: # (  associatePublicIpAddress: true,)

[//]: # (}&#41;;)

[//]: # (```)

[//]: # ()
[//]: # (### Specifying a key pair)

[//]: # ()
[//]: # (To allow SSH access to an EC2 instance by default, a Key Pair must be specified. Key pairs can)

[//]: # (be provided with the `keyPair` property to instances and launch templates. You can create a)

[//]: # (key pair for an instance like this:)

[//]: # ()
[//]: # (```ts)

[//]: # (declare const vpc: ec2.Vpc;)

[//]: # (declare const instanceType: ec2.InstanceType;)

[//]: # ()
[//]: # (const keyPair = new ec2.KeyPair&#40;this, 'KeyPair', {)

[//]: # (  type: ec2.KeyPairType.ED25519,)

[//]: # (  format: ec2.KeyPairFormat.PEM,)

[//]: # (}&#41;;)

[//]: # (const instance = new ec2.Instance&#40;this, 'Instance', {)

[//]: # (  vpc,)

[//]: # (  instanceType,)

[//]: # (  machineImage: ec2.MachineImage.latestAmazonLinux2023&#40;&#41;,)

[//]: # (  // Use the custom key pair)

[//]: # (  keyPair,)

[//]: # (}&#41;;)

[//]: # (```)

[//]: # ()
[//]: # (When a new EC2 Key Pair is created &#40;without imported material&#41;, the private key material is)

[//]: # (automatically stored in Systems Manager Parameter Store. This can be retrieved from the key pair)

[//]: # (construct:)

[//]: # ()
[//]: # (```ts)

[//]: # (const keyPair = new ec2.KeyPair&#40;this, 'KeyPair'&#41;;)

[//]: # (const privateKey = keyPair.privateKey;)

[//]: # (```)

[//]: # ()
[//]: # (If you already have an SSH key that you wish to use in EC2, that can be provided when constructing the)

[//]: # (`KeyPair`. If public key material is provided, the key pair is considered "imported" and there)

[//]: # (will not be any data automatically stored in Systems Manager Parameter Store and the `type` property)

[//]: # (cannot be specified for the key pair.)

[//]: # ()
[//]: # (```ts)

[//]: # (const keyPair = new ec2.KeyPair&#40;this, 'KeyPair', {)

[//]: # (  publicKeyMaterial: "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIB7jpNzG+YG0s+xIGWbxrxIZiiozHOEuzIJacvASP0mq",)

[//]: # (}&#41;)

[//]: # (```)

[//]: # ()
[//]: # (#### Using an existing EC2 Key Pair)

[//]: # ()
[//]: # (If you already have an EC2 Key Pair created outside of the CDK, you can import that key to)

[//]: # (your CDK stack.)

[//]: # ()
[//]: # (You can import it purely by name:)

[//]: # ()
[//]: # (```ts)

[//]: # (const keyPair = ec2.KeyPair.fromKeyPairName&#40;this, 'KeyPair', 'the-keypair-name'&#41;;)

[//]: # (```)

[//]: # ()
[//]: # (Or by specifying additional attributes:)

[//]: # ()
[//]: # (```ts)

[//]: # (const keyPair = ec2.KeyPair.fromKeyPairAttributes&#40;this, 'KeyPair', {)

[//]: # (  keyPairName: 'the-keypair-name',)

[//]: # (  type: ec2.KeyPairType.RSA,)

[//]: # (}&#41;)

[//]: # (```)

[//]: # ()
[//]: # (### Using IPv6 IPs)

[//]: # ()
[//]: # (Instances can be given IPv6 IPs by launching them into a subnet of a dual stack VPC.)

[//]: # ()
[//]: # (```ts)

[//]: # (const vpc = new ec2.Vpc&#40;this, 'Ip6VpcDualStack', {)

[//]: # (  ipProtocol: ec2.IpProtocol.DUAL_STACK,)

[//]: # (  subnetConfiguration: [)

[//]: # (    {)

[//]: # (      name: 'Public',)

[//]: # (      subnetType: ec2.SubnetType.PUBLIC,)

[//]: # (      mapPublicIpOnLaunch: true,)

[//]: # (    },)

[//]: # (    {)

[//]: # (      name: 'Private',)

[//]: # (      subnetType: ec2.SubnetType.PRIVATE_ISOLATED,)

[//]: # (    },)

[//]: # (  ],)

[//]: # (}&#41;;)

[//]: # ()
[//]: # (const instance = new ec2.Instance&#40;this, 'MyInstance', {)

[//]: # (  instanceType: ec2.InstanceType.of&#40;ec2.InstanceClass.T2, ec2.InstanceSize.MICRO&#41;,)

[//]: # (  machineImage: ec2.MachineImage.latestAmazonLinux2&#40;&#41;,)

[//]: # (  vpc: vpc,)

[//]: # (  vpcSubnets: { subnetType: ec2.SubnetType.PUBLIC },)

[//]: # (  allowAllIpv6Outbound: true,)

[//]: # ()
[//]: # (  // ...)

[//]: # (}&#41;;)

[//]: # ()
[//]: # (instance.connections.allowFrom&#40;ec2.Peer.anyIpv6&#40;&#41;, ec2.Port.allIcmpV6&#40;&#41;, 'allow ICMPv6'&#41;;)

[//]: # (```)

[//]: # ()
[//]: # (Note to set `mapPublicIpOnLaunch` to true in the `subnetConfiguration`.)

[//]: # ()
[//]: # (Additionally, IPv6 support varies by instance type. Most instance types have IPv6 support with exception of m1-m3, c1, g2, and t1.micro. A full list can be found here: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-eni.html#AvailableIpPerENI.)

[//]: # ()
[//]: # (#### Specifying the IPv6 Address)

[//]: # ()
[//]: # (If you want to specify [the number of IPv6 addresses]&#40;https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/MultipleIP.html#assign-multiple-ipv6&#41; to assign to the instance, you can use the `ipv6AddresseCount` property:)

[//]: # ()
[//]: # (```ts)

[//]: # (// dual stack VPC)

[//]: # (declare const vpc: ec2.Vpc;)

[//]: # ()
[//]: # (const instance = new ec2.Instance&#40;this, 'MyInstance', {)

[//]: # (  instanceType: ec2.InstanceType.of&#40;ec2.InstanceClass.M5, ec2.InstanceSize.LARGE&#41;,)

[//]: # (  machineImage: ec2.MachineImage.latestAmazonLinux2&#40;&#41;,)

[//]: # (  vpc: vpc,)

[//]: # (  vpcSubnets: { subnetType: ec2.SubnetType.PUBLIC },)

[//]: # (  // Assign 2 IPv6 addresses to the instance)

[//]: # (  ipv6AddressCount: 2,)

[//]: # (}&#41;;)

[//]: # (```)

[//]: # ()
[//]: # (### Credit configuration modes for burstable instances)

[//]: # ()
[//]: # (You can set the [credit configuration mode]&#40;https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/burstable-credits-baseline-concepts.html&#41; for burstable instances &#40;T2, T3, T3a and T4g instance types&#41;:)

[//]: # ()
[//]: # (```ts)

[//]: # (declare const vpc: ec2.Vpc;)

[//]: # ()
[//]: # (const instance = new ec2.Instance&#40;this, 'Instance', {)

[//]: # (  instanceType: ec2.InstanceType.of&#40;ec2.InstanceClass.T3, ec2.InstanceSize.MICRO&#41;,)

[//]: # (  machineImage: ec2.MachineImage.latestAmazonLinux2&#40;&#41;,)

[//]: # (  vpc: vpc,)

[//]: # (  creditSpecification: ec2.CpuCredits.STANDARD,)

[//]: # (}&#41;;)

[//]: # (```)

[//]: # ()
[//]: # (It is also possible to set the credit configuration mode for NAT instances.)

[//]: # ()
[//]: # (```ts)

[//]: # (const natInstanceProvider = ec2.NatProvider.instance&#40;{)

[//]: # (  instanceType: ec2.InstanceType.of&#40;ec2.InstanceClass.T4G, ec2.InstanceSize.LARGE&#41;,)

[//]: # (  machineImage: new ec2.AmazonLinuxImage&#40;&#41;,)

[//]: # (  creditSpecification: ec2.CpuCredits.UNLIMITED,)

[//]: # (}&#41;;)

[//]: # (new ec2.Vpc&#40;this, 'VPC', {)

[//]: # (  natGatewayProvider: natInstanceProvider,)

[//]: # (}&#41;;)

[//]: # (```)

[//]: # ()
[//]: # (**Note**: `CpuCredits.UNLIMITED` mode is not supported for T3 instances that are launched on a Dedicated Host.)

[//]: # ()
[//]: # (### Shutdown behavior)

[//]: # ()
[//]: # (You can specify the behavior of the instance when you initiate shutdown from the instance &#40;using the operating system command for system shutdown&#41;.)

[//]: # ()
[//]: # (```ts)

[//]: # (declare const vpc: ec2.Vpc;)

[//]: # ()
[//]: # (new ec2.Instance&#40;this, 'Instance', {)

[//]: # (  vpc,)

[//]: # (  instanceType: ec2.InstanceType.of&#40;ec2.InstanceClass.T3, ec2.InstanceSize.NANO&#41;,)

[//]: # (  machineImage: new ec2.AmazonLinuxImage&#40;{ generation: ec2.AmazonLinuxGeneration.AMAZON_LINUX_2 }&#41;,)

[//]: # (  instanceInitiatedShutdownBehavior: ec2.InstanceInitiatedShutdownBehavior.TERMINATE, // default is STOP)

[//]: # (}&#41;;)

[//]: # (```)

[//]: # ()
[//]: # (### Enabling Nitro Enclaves)

[//]: # ()
[//]: # (You can enable [AWS Nitro Enclaves]&#40;https://docs.aws.amazon.com/enclaves/latest/user/nitro-enclave.html&#41; for)

[//]: # (your EC2 instances by setting the `enclaveEnabled` property to `true`. Nitro Enclaves is a feature of)

[//]: # (AWS Nitro System that enables creating isolated and highly constrained CPU environments known as enclaves.)

[//]: # ()
[//]: # (```ts)

[//]: # (declare const vpc: ec2.Vpc;)

[//]: # ()
[//]: # (const instance = new ec2.Instance&#40;this, 'Instance', {)

[//]: # (  instanceType: ec2.InstanceType.of&#40;ec2.InstanceClass.M5, ec2.InstanceSize.XLARGE&#41;,)

[//]: # (  machineImage: new ec2.AmazonLinuxImage&#40;&#41;,)

[//]: # (  vpc: vpc,)

[//]: # (  enclaveEnabled: true,)

[//]: # (}&#41;;)

[//]: # (```)

[//]: # ()
[//]: # (> NOTE: You must use an instance type and operating system that support Nitro Enclaves.)

[//]: # (> For more information, see [Requirements]&#40;https://docs.aws.amazon.com/enclaves/latest/user/nitro-enclave.html#nitro-enclave-reqs&#41;.)

[//]: # ()
[//]: # (### Enabling Instance Hibernation)

[//]: # ()
[//]: # (You can enable [Instance Hibernation]&#40;https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/Hibernate.html&#41; for)

[//]: # (your EC2 instances by setting the `hibernationEnabled` property to `true`. Instance Hibernation saves the)

[//]: # (instance's in-memory &#40;RAM&#41; state when an instance is stopped, and restores that state when the instance is started.)

[//]: # ()
[//]: # (```ts)

[//]: # (declare const vpc: ec2.Vpc;)

[//]: # ()
[//]: # (const instance = new ec2.Instance&#40;this, 'Instance', {)

[//]: # (  instanceType: ec2.InstanceType.of&#40;ec2.InstanceClass.M5, ec2.InstanceSize.XLARGE&#41;,)

[//]: # (  machineImage: new ec2.AmazonLinuxImage&#40;&#41;,)

[//]: # (  vpc: vpc,)

[//]: # (  hibernationEnabled: true,)

[//]: # (  blockDevices: [{)

[//]: # (    deviceName: '/dev/xvda',)

[//]: # (    volume: ec2.BlockDeviceVolume.ebs&#40;30, {)

[//]: # (      volumeType: ec2.EbsDeviceVolumeType.GP3,)

[//]: # (      encrypted: true,)

[//]: # (      deleteOnTermination: true,)

[//]: # (    }&#41;,)

[//]: # (  }],)

[//]: # (}&#41;;)

[//]: # (```)

[//]: # ()
[//]: # (> NOTE: You must use an instance and a volume that meet the requirements for hibernation.)

[//]: # (> For more information, see [Prerequisites for Amazon EC2 instance hibernation]&#40;https://docs.aws.amazon.com/enclaves/latest/user/nitro-enclave.html#nitro-enclave-reqs&#41;.)

[//]: # ()
[//]: # ()
[//]: # (## VPC Flow Logs)

[//]: # ()
[//]: # (VPC Flow Logs is a feature that enables you to capture information about the IP traffic going to and from network interfaces in your VPC. Flow log data can be published to Amazon CloudWatch Logs and Amazon S3. After you've created a flow log, you can retrieve and view its data in the chosen destination. &#40;<https://docs.aws.amazon.com/vpc/latest/userguide/flow-logs.html>&#41;.)

[//]: # ()
[//]: # (By default, a flow log will be created with CloudWatch Logs as the destination.)

[//]: # ()
[//]: # (You can create a flow log like this:)

[//]: # ()
[//]: # (```ts)

[//]: # (declare const vpc: ec2.Vpc;)

[//]: # ()
[//]: # (new ec2.FlowLog&#40;this, 'FlowLog', {)

[//]: # (  resourceType: ec2.FlowLogResourceType.fromVpc&#40;vpc&#41;)

[//]: # (}&#41;)

[//]: # (```)

[//]: # ()
[//]: # (Or you can add a Flow Log to a VPC by using the addFlowLog method like this:)

[//]: # ()
[//]: # (```ts)

[//]: # (const vpc = new ec2.Vpc&#40;this, 'Vpc'&#41;;)

[//]: # ()
[//]: # (vpc.addFlowLog&#40;'FlowLog'&#41;;)

[//]: # (```)

[//]: # ()
[//]: # (You can also add multiple flow logs with different destinations.)

[//]: # ()
[//]: # (```ts)

[//]: # (const vpc = new ec2.Vpc&#40;this, 'Vpc'&#41;;)

[//]: # ()
[//]: # (vpc.addFlowLog&#40;'FlowLogS3', {)

[//]: # (  destination: ec2.FlowLogDestination.toS3&#40;&#41;)

[//]: # (}&#41;;)

[//]: # ()
[//]: # (// Only reject traffic and interval every minute.)

[//]: # (vpc.addFlowLog&#40;'FlowLogCloudWatch', {)

[//]: # (  trafficType: ec2.FlowLogTrafficType.REJECT,)

[//]: # (  maxAggregationInterval: ec2.FlowLogMaxAggregationInterval.ONE_MINUTE,)

[//]: # (}&#41;;)

[//]: # (```)

[//]: # ()
[//]: # (To create a Transit Gateway flow log, you can use the `fromTransitGatewayId` method:)

[//]: # ()
[//]: # (```ts)

[//]: # (declare const tgw: ec2.CfnTransitGateway;)

[//]: # ()
[//]: # (new ec2.FlowLog&#40;this, 'TransitGatewayFlowLog', {)

[//]: # (  resourceType: ec2.FlowLogResourceType.fromTransitGatewayId&#40;tgw.ref&#41;)

[//]: # (}&#41;)

[//]: # (```)

[//]: # ()
[//]: # (To create a Transit Gateway Attachment flow log, you can use the `fromTransitGatewayAttachmentId` method:)

[//]: # ()
[//]: # (```ts)

[//]: # (declare const tgwAttachment: ec2.CfnTransitGatewayAttachment;)

[//]: # ()
[//]: # (new ec2.FlowLog&#40;this, 'TransitGatewayAttachmentFlowLog', {)

[//]: # (  resourceType: ec2.FlowLogResourceType.fromTransitGatewayAttachmentId&#40;tgwAttachment.ref&#41;)

[//]: # (}&#41;)

[//]: # (```)

[//]: # ()
[//]: # (For flow logs targeting TransitGateway and TransitGatewayAttachment, specifying the `trafficType` is not possible.)

[//]: # ()
[//]: # (### Custom Formatting)

[//]: # ()
[//]: # (You can also custom format flow logs.)

[//]: # ()
[//]: # (```ts)

[//]: # (const vpc = new ec2.Vpc&#40;this, 'Vpc'&#41;;)

[//]: # ()
[//]: # (vpc.addFlowLog&#40;'FlowLog', {)

[//]: # (  logFormat: [)

[//]: # (    ec2.LogFormat.DST_PORT,)

[//]: # (    ec2.LogFormat.SRC_PORT,)

[//]: # (  ],)

[//]: # (}&#41;;)

[//]: # ()
[//]: # (// If you just want to add a field to the default field)

[//]: # (vpc.addFlowLog&#40;'FlowLog', {)

[//]: # (  logFormat: [)

[//]: # (    ec2.LogFormat.VERSION,)

[//]: # (    ec2.LogFormat.ALL_DEFAULT_FIELDS,)

[//]: # (  ],)

[//]: # (}&#41;;)

[//]: # ()
[//]: # (// If AWS CDK does not support the new fields)

[//]: # (vpc.addFlowLog&#40;'FlowLog', {)

[//]: # (  logFormat: [)

[//]: # (    ec2.LogFormat.SRC_PORT,)

[//]: # (    ec2.LogFormat.custom&#40;'${new-field}'&#41;,)

[//]: # (  ],)

[//]: # (}&#41;;)

[//]: # (```)

[//]: # ()
[//]: # ()
[//]: # (By default, the CDK will create the necessary resources for the destination. For the CloudWatch Logs destination)

[//]: # (it will create a CloudWatch Logs Log Group as well as the IAM role with the necessary permissions to publish to)

[//]: # (the log group. In the case of an S3 destination, it will create the S3 bucket.)

[//]: # ()
[//]: # (If you want to customize any of the destination resources you can provide your own as part of the `destination`.)

[//]: # ()
[//]: # (*CloudWatch Logs*)

[//]: # ()
[//]: # (```ts)

[//]: # (declare const vpc: ec2.Vpc;)

[//]: # ()
[//]: # (const logGroup = new logs.LogGroup&#40;this, 'MyCustomLogGroup'&#41;;)

[//]: # ()
[//]: # (const role = new iam.Role&#40;this, 'MyCustomRole', {)

[//]: # (  assumedBy: new iam.ServicePrincipal&#40;'vpc-flow-logs.amazonaws.com'&#41;)

[//]: # (}&#41;;)

[//]: # ()
[//]: # (new ec2.FlowLog&#40;this, 'FlowLog', {)

[//]: # (  resourceType: ec2.FlowLogResourceType.fromVpc&#40;vpc&#41;,)

[//]: # (  destination: ec2.FlowLogDestination.toCloudWatchLogs&#40;logGroup, role&#41;)

[//]: # (}&#41;;)

[//]: # (```)

[//]: # ()
[//]: # (*S3*)

[//]: # ()
[//]: # (```ts)

[//]: # (declare const vpc: ec2.Vpc;)

[//]: # ()
[//]: # (const bucket = new s3.Bucket&#40;this, 'MyCustomBucket'&#41;;)

[//]: # ()
[//]: # (new ec2.FlowLog&#40;this, 'FlowLog', {)

[//]: # (  resourceType: ec2.FlowLogResourceType.fromVpc&#40;vpc&#41;,)

[//]: # (  destination: ec2.FlowLogDestination.toS3&#40;bucket&#41;)

[//]: # (}&#41;;)

[//]: # ()
[//]: # (new ec2.FlowLog&#40;this, 'FlowLogWithKeyPrefix', {)

[//]: # (  resourceType: ec2.FlowLogResourceType.fromVpc&#40;vpc&#41;,)

[//]: # (  destination: ec2.FlowLogDestination.toS3&#40;bucket, 'prefix/'&#41;)

[//]: # (}&#41;;)

[//]: # (```)

[//]: # ()
[//]: # (*Kinesis Data Firehose*)

[//]: # ()
[//]: # (```ts)

[//]: # (import * as firehose from 'aws-cdk-lib/aws-kinesisfirehose';)

[//]: # ()
[//]: # (declare const vpc: ec2.Vpc;)

[//]: # (declare const deliveryStream: firehose.CfnDeliveryStream;)

[//]: # ()
[//]: # (vpc.addFlowLog&#40;'FlowLogsKinesisDataFirehose', {)

[//]: # (  destination: ec2.FlowLogDestination.toKinesisDataFirehoseDestination&#40;deliveryStream.attrArn&#41;,)

[//]: # (}&#41;;)

[//]: # (```)

[//]: # ()
[//]: # (When the S3 destination is configured, AWS will automatically create an S3 bucket policy)

[//]: # (that allows the service to write logs to the bucket. This makes it impossible to later update)

[//]: # (that bucket policy. To have CDK create the bucket policy so that future updates can be made,)

[//]: # (the `@aws-cdk/aws-s3:createDefaultLoggingPolicy` [feature flag]&#40;https://docs.aws.amazon.com/cdk/v2/guide/featureflags.html&#41; can be used. This can be set)

[//]: # (in the `cdk.json` file.)

[//]: # ()
[//]: # (```json)

[//]: # ({)

[//]: # (  "context": {)

[//]: # (    "@aws-cdk/aws-s3:createDefaultLoggingPolicy": true)

[//]: # (  })

[//]: # (})

[//]: # (```)

[//]: # ()
[//]: # (## User Data)

[//]: # ()
[//]: # (User data enables you to run a script when your instances start up.  In order to configure these scripts you can add commands directly to the script)

[//]: # ( or you can use the UserData's convenience functions to aid in the creation of your script.)

[//]: # ()
[//]: # (A user data could be configured to run a script found in an asset through the following:)

[//]: # ()
[//]: # (```ts)

[//]: # (import { Asset } from 'aws-cdk-lib/aws-s3-assets';)

[//]: # ()
[//]: # (declare const instance: ec2.Instance;)

[//]: # ()
[//]: # (const asset = new Asset&#40;this, 'Asset', {)

[//]: # (  path: './configure.sh')

[//]: # (}&#41;;)

[//]: # ()
[//]: # (const localPath = instance.userData.addS3DownloadCommand&#40;{)

[//]: # (  bucket:asset.bucket,)

[//]: # (  bucketKey:asset.s3ObjectKey,)

[//]: # (  region: 'us-east-1', // Optional)

[//]: # (}&#41;;)

[//]: # (instance.userData.addExecuteFileCommand&#40;{)

[//]: # (  filePath:localPath,)

[//]: # (  arguments: '--verbose -y')

[//]: # (}&#41;;)

[//]: # (asset.grantRead&#40;instance.role&#41;;)

[//]: # (```)

[//]: # ()
[//]: # (### Persisting user data)

[//]: # ()
[//]: # (By default, EC2 UserData is run once on only the first time that an instance is started. It is possible to make the)

[//]: # (user data script run on every start of the instance.)

[//]: # ()
[//]: # (When creating a Windows UserData you can use the `persist` option to set whether or not to add)

[//]: # (`<persist>true</persist>` [to the user data script]&#40;https://docs.aws.amazon.com/AWSEC2/latest/WindowsGuide/ec2-windows-user-data.html#user-data-scripts&#41;. it can be used as follows:)

[//]: # ()
[//]: # (```ts)

[//]: # (const windowsUserData = ec2.UserData.forWindows&#40;{ persist: true }&#41;;)

[//]: # (```)

[//]: # ()
[//]: # (For a Linux instance, this can be accomplished by using a Multipart user data to configure cloud-config as detailed)

[//]: # (in: https://aws.amazon.com/premiumsupport/knowledge-center/execute-user-data-ec2/)

[//]: # ()
[//]: # (### Multipart user data)

[//]: # ()
[//]: # (In addition, to above the `MultipartUserData` can be used to change instance startup behavior. Multipart user data are composed)

[//]: # (from separate parts forming archive. The most common parts are scripts executed during instance set-up. However, there are other)

[//]: # (kinds, too.)

[//]: # ()
[//]: # (The advantage of multipart archive is in flexibility when it's needed to add additional parts or to use specialized parts to)

[//]: # (fine tune instance startup. Some services &#40;like AWS Batch&#41; support only `MultipartUserData`.)

[//]: # ()
[//]: # (The parts can be executed at different moment of instance start-up and can serve a different purpose. This is controlled by `contentType` property.)

[//]: # (For common scripts, `text/x-shellscript; charset="utf-8"` can be used as content type.)

[//]: # ()
[//]: # (In order to create archive the `MultipartUserData` has to be instantiated. Than, user can add parts to multipart archive using `addPart`. The `MultipartBody` contains methods supporting creation of body parts.)

[//]: # ()
[//]: # (If the very custom part is required, it can be created using `MultipartUserData.fromRawBody`, in this case full control over content type,)

[//]: # (transfer encoding, and body properties is given to the user.)

[//]: # ()
[//]: # (Below is an example for creating multipart user data with single body part responsible for installing `awscli` and configuring maximum size)

[//]: # (of storage used by Docker containers:)

[//]: # ()
[//]: # (```ts)

[//]: # (const bootHookConf = ec2.UserData.forLinux&#40;&#41;;)

[//]: # (bootHookConf.addCommands&#40;'cloud-init-per once docker_options echo \'OPTIONS="${OPTIONS} --storage-opt dm.basesize=40G"\' >> /etc/sysconfig/docker'&#41;;)

[//]: # ()
[//]: # (const setupCommands = ec2.UserData.forLinux&#40;&#41;;)

[//]: # (setupCommands.addCommands&#40;'sudo yum install awscli && echo Packages installed らと > /var/tmp/setup'&#41;;)

[//]: # ()
[//]: # (const multipartUserData = new ec2.MultipartUserData&#40;&#41;;)

[//]: # (// The docker has to be configured at early stage, so content type is overridden to boothook)

[//]: # (multipartUserData.addPart&#40;ec2.MultipartBody.fromUserData&#40;bootHookConf, 'text/cloud-boothook; charset="us-ascii"'&#41;&#41;;)

[//]: # (// Execute the rest of setup)

[//]: # (multipartUserData.addPart&#40;ec2.MultipartBody.fromUserData&#40;setupCommands&#41;&#41;;)

[//]: # ()
[//]: # (new ec2.LaunchTemplate&#40;this, '', {)

[//]: # (  userData: multipartUserData,)

[//]: # (  blockDevices: [)

[//]: # (    // Block device configuration rest)

[//]: # (  ])

[//]: # (}&#41;;)

[//]: # (```)

[//]: # ()
[//]: # (For more information see)

[//]: # ([Specifying Multiple User Data Blocks Using a MIME Multi Part Archive]&#40;https://docs.aws.amazon.com/AmazonECS/latest/developerguide/bootstrap_container_instance.html#multi-part_user_data&#41;)

[//]: # ()
[//]: # (#### Using add*Command on MultipartUserData)

[//]: # ()
[//]: # (To use the `add*Command` methods, that are inherited from the `UserData` interface, on `MultipartUserData` you must add a part)

[//]: # (to the `MultipartUserData` and designate it as the receiver for these methods. This is accomplished by using the `addUserDataPart&#40;&#41;`)

[//]: # (method on `MultipartUserData` with the `makeDefault` argument set to `true`:)

[//]: # ()
[//]: # (```ts)

[//]: # (const multipartUserData = new ec2.MultipartUserData&#40;&#41;;)

[//]: # (const commandsUserData = ec2.UserData.forLinux&#40;&#41;;)

[//]: # (multipartUserData.addUserDataPart&#40;commandsUserData, ec2.MultipartBody.SHELL_SCRIPT, true&#41;;)

[//]: # ()
[//]: # (// Adding commands to the multipartUserData adds them to commandsUserData, and vice-versa.)

[//]: # (multipartUserData.addCommands&#40;'touch /root/multi.txt'&#41;;)

[//]: # (commandsUserData.addCommands&#40;'touch /root/userdata.txt'&#41;;)

[//]: # (```)

[//]: # ()
[//]: # (When used on an EC2 instance, the above `multipartUserData` will create both `multi.txt` and `userdata.txt` in `/root`.)

[//]: # ()
[//]: # (## Importing existing subnet)

[//]: # ()
[//]: # (To import an existing Subnet, call `Subnet.fromSubnetAttributes&#40;&#41;` or)

[//]: # (`Subnet.fromSubnetId&#40;&#41;`. Only if you supply the subnet's Availability Zone)

[//]: # (and Route Table Ids when calling `Subnet.fromSubnetAttributes&#40;&#41;` will you be)

[//]: # (able to use the CDK features that use these values &#40;such as selecting one)

[//]: # (subnet per AZ&#41;.)

[//]: # ()
[//]: # (Importing an existing subnet looks like this:)

[//]: # ()
[//]: # (```ts)

[//]: # (// Supply all properties)

[//]: # (const subnet1 = ec2.Subnet.fromSubnetAttributes&#40;this, 'SubnetFromAttributes', {)

[//]: # (  subnetId: 's-1234',)

[//]: # (  availabilityZone: 'pub-az-4465',)

[//]: # (  routeTableId: 'rt-145')

[//]: # (}&#41;;)

[//]: # ()
[//]: # (// Supply only subnet id)

[//]: # (const subnet2 = ec2.Subnet.fromSubnetId&#40;this, 'SubnetFromId', 's-1234'&#41;;)

[//]: # (```)

[//]: # ()
[//]: # (## Launch Templates)

[//]: # ()
[//]: # (A Launch Template is a standardized template that contains the configuration information to launch an instance.)

[//]: # (They can be used when launching instances on their own, through Amazon EC2 Auto Scaling, EC2 Fleet, and Spot Fleet.)

[//]: # (Launch templates enable you to store launch parameters so that you do not have to specify them every time you launch)

[//]: # (an instance. For information on Launch Templates please see the)

[//]: # ([official documentation]&#40;https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-launch-templates.html&#41;.)

[//]: # ()
[//]: # (The following demonstrates how to create a launch template with an Amazon Machine Image, security group, and an instance profile.)

[//]: # ()
[//]: # (```ts)

[//]: # (declare const vpc: ec2.Vpc;)

[//]: # ()
[//]: # (const role = new iam.Role&#40;this, 'Role', {)

[//]: # (  assumedBy: new iam.ServicePrincipal&#40;'ec2.amazonaws.com'&#41;,)

[//]: # (}&#41;;)

[//]: # (const instanceProfile = new iam.InstanceProfile&#40;this, 'InstanceProfile', {)

[//]: # (  role,)

[//]: # (}&#41;;)

[//]: # ()
[//]: # (const template = new ec2.LaunchTemplate&#40;this, 'LaunchTemplate', {)

[//]: # (  launchTemplateName: 'MyTemplateV1',)

[//]: # (  versionDescription: 'This is my v1 template',)

[//]: # (  machineImage: ec2.MachineImage.latestAmazonLinux2023&#40;&#41;,)

[//]: # (  securityGroup: new ec2.SecurityGroup&#40;this, 'LaunchTemplateSG', {)

[//]: # (    vpc: vpc,)

[//]: # (  }&#41;,)

[//]: # (  instanceProfile,)

[//]: # (}&#41;;)

[//]: # (```)

[//]: # ()
[//]: # (And the following demonstrates how to enable metadata options support.)

[//]: # ()
[//]: # (```ts)

[//]: # (new ec2.LaunchTemplate&#40;this, 'LaunchTemplate', {)

[//]: # (  httpEndpoint: true,)

[//]: # (  httpProtocolIpv6: true,)

[//]: # (  httpPutResponseHopLimit: 1,)

[//]: # (  httpTokens: ec2.LaunchTemplateHttpTokens.REQUIRED,)

[//]: # (  instanceMetadataTags: true,)

[//]: # (}&#41;;)

[//]: # (```)

[//]: # ()
[//]: # (And the following demonstrates how to add one or more security groups to launch template.)

[//]: # ()
[//]: # (```ts)

[//]: # (declare const vpc: ec2.Vpc;)

[//]: # ()
[//]: # (const sg1 = new ec2.SecurityGroup&#40;this, 'sg1', {)

[//]: # (  vpc: vpc,)

[//]: # (}&#41;;)

[//]: # (const sg2 = new ec2.SecurityGroup&#40;this, 'sg2', {)

[//]: # (  vpc: vpc,)

[//]: # (}&#41;;)

[//]: # ()
[//]: # (const launchTemplate = new ec2.LaunchTemplate&#40;this, 'LaunchTemplate', {)

[//]: # (  machineImage: ec2.MachineImage.latestAmazonLinux2023&#40;&#41;,)

[//]: # (  securityGroup: sg1,)

[//]: # (}&#41;;)

[//]: # ()
[//]: # (launchTemplate.addSecurityGroup&#40;sg2&#41;;)

[//]: # (```)

[//]: # ()
[//]: # (To use [AWS Systems Manager parameters instead of AMI IDs]&#40;https://docs.aws.amazon.com/autoscaling/ec2/userguide/using-systems-manager-parameters.html&#41; in launch templates and resolve the AMI IDs at instance launch time:)

[//]: # ()
[//]: # (```ts)

[//]: # (const launchTemplate = new ec2.LaunchTemplate&#40;this, 'LaunchTemplate', {)

[//]: # (  machineImage: ec2.MachineImage.resolveSsmParameterAtLaunch&#40;'parameterName'&#41;,)

[//]: # (}&#41;;)

[//]: # (```)

[//]: # ()
[//]: # (Please note this feature does not support Launch Configurations.)

[//]: # ()
[//]: # (## Detailed Monitoring)

[//]: # ()
[//]: # (The following demonstrates how to enable [Detailed Monitoring]&#40;https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-cloudwatch-new.html&#41; for an EC2 instance. Keep in mind that Detailed Monitoring results in [additional charges]&#40;http://aws.amazon.com/cloudwatch/pricing/&#41;.)

[//]: # ()
[//]: # (```ts)

[//]: # (declare const vpc: ec2.Vpc;)

[//]: # (declare const instanceType: ec2.InstanceType;)

[//]: # ()
[//]: # (new ec2.Instance&#40;this, 'Instance1', {)

[//]: # (  vpc,)

[//]: # (  instanceType,)

[//]: # (  machineImage: ec2.MachineImage.latestAmazonLinux2023&#40;&#41;,)

[//]: # (  detailedMonitoring: true,)

[//]: # (}&#41;;)

[//]: # (```)

[//]: # ()
[//]: # (## Connecting to your instances using SSM Session Manager)

[//]: # ()
[//]: # (SSM Session Manager makes it possible to connect to your instances from the)

[//]: # (AWS Console, without preparing SSH keys.)

[//]: # ()
[//]: # (To do so, you need to:)

[//]: # ()
[//]: # (* Use an image with [SSM agent]&#40;https://docs.aws.amazon.com/systems-manager/latest/userguide/ssm-agent.html&#41; installed)

[//]: # (  and configured. [Many images come with SSM Agent)

[//]: # (  preinstalled]&#40;https://docs.aws.amazon.com/systems-manager/latest/userguide/ami-preinstalled-agent.html&#41;, otherwise you)

[//]: # (  may need to manually put instructions to [install SSM)

[//]: # (  Agent]&#40;https://docs.aws.amazon.com/systems-manager/latest/userguide/sysman-manual-agent-install.html&#41; into your)

[//]: # (  instance's UserData or use EC2 Init&#41;.)

[//]: # (* Create the instance with `ssmSessionPermissions: true`.)

[//]: # ()
[//]: # (If these conditions are met, you can connect to the instance from the EC2 Console. Example:)

[//]: # ()
[//]: # (```ts)

[//]: # (declare const vpc: ec2.Vpc;)

[//]: # (declare const instanceType: ec2.InstanceType;)

[//]: # ()
[//]: # (new ec2.Instance&#40;this, 'Instance1', {)

[//]: # (  vpc,)

[//]: # (  instanceType,)

[//]: # ()
[//]: # (  // Amazon Linux 2023 comes with SSM Agent by default)

[//]: # (  machineImage: ec2.MachineImage.latestAmazonLinux2023&#40;&#41;,)

[//]: # ()
[//]: # (  // Turn on SSM)

[//]: # (  ssmSessionPermissions: true,)

[//]: # (}&#41;;)

[//]: # (```)

[//]: # ()
[//]: # (## Managed Prefix Lists)

[//]: # ()
[//]: # (Create and manage customer-managed prefix lists. If you don't specify anything in this construct, it will manage IPv4 addresses.)

[//]: # ()
[//]: # (You can also create an empty Prefix List with only the maximum number of entries specified, as shown in the following code. If nothing is specified, maxEntries=1.)

[//]: # ()
[//]: # (```ts)

[//]: # (new ec2.PrefixList&#40;this, 'EmptyPrefixList', {)

[//]: # (  maxEntries: 100,)

[//]: # (}&#41;;)

[//]: # (```)

[//]: # ()
[//]: # (`maxEntries` can also be omitted as follows. In this case `maxEntries: 2`, will be set.)

[//]: # ()
[//]: # (```ts)

[//]: # (new ec2.PrefixList&#40;this, 'PrefixList', {)

[//]: # (  entries: [)

[//]: # (    { cidr: '10.0.0.1/32' },)

[//]: # (    { cidr: '10.0.0.2/32', description: 'sample1' },)

[//]: # (  ],)

[//]: # (}&#41;;)

[//]: # (```)

[//]: # ()
[//]: # (For more information see [Work with customer-managed prefix lists]&#40;https://docs.aws.amazon.com/vpc/latest/userguide/working-with-managed-prefix-lists.html&#41;)