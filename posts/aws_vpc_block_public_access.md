title: AWS VPC Block Public Access: The Greatest Thing in Securing AWS Networks Since Sliced Bread
date: 2025-03-23
tags: ["aws","vpc","security"]
author: "Ben Aylott"
filename: aws_vpc_block_public_access.html
draft: false

# AWS VPC Block Public Access: The Greatest Thing Since Sliced Bread

Introduced relatively quietly before re:invent 2024, [AWS VPC Block Public Access (BPA)](https://aws.amazon.com/blogs/virtualization/announcing-aws-vpc-block-public-access/) is a new feature of AWS VPC that finally provides a security invariant which controls whether or not a VPC or subnet is accessible from the public internet. BPA is reminiscent of the S3 Block Public Access feature which was introduced in 2019 and is now default enabled for new buckets.

Historically we always had a concept of a 'private' and 'public' subnet, but this was in a sense implicit - the internet accessibility of a VPC/subnet was controlled by an appropriate combination of security groups, routing tables, and NACLs which was easily misconfigured. There was no switch or flag we could use to enforce this. I have lost count of number of times I have shown up to new site and found various subnets and resources open which were not supposed to be. This will prevent 99% of that.

A key aspect of BPA is you can exempt specific subnets from the block. This is the opposite of the 'implicit' model above where one has to be careful not to open up a subnet to the public internet.

With the ability to exempt VPCs and subnets from the block, there is no reason we all shouldnt just go and turn this on immediately. To ensure you do not wreck access for existing VPCs you can exempt all existing VPCs (and their subnets) from the block before turning it on. This will then ensure that any future VPC/subnets will by default not have internet access. If you are confident in the public/private-ness of your subnets (or can establish this easily using e.g. VPC flow logs) you can go further and exempt the 'public' or 'ingress only' subnets instead of the VPC before turning on BPA. You have option with BPA of either ingress only or bidirectional - bidirectional should IMO always be chosen as the default as its simplifies the model for the security invariant.

This is a great QoL feature for AWS VPC and you should be planning on when to deploy it to your AWS accounts immediately if you haven't already.
