title: A no-op IAM policy?
date: 2025-03-12
tags: ["til","aws","iam"]
author: "Ben Aylott"
filename: a_no_op_iam_policy.html
draft: false

# A no-op IAM policy?

What if for some (probably not great) reason you need an IAM policy that has no effect? A stack overflow post on the topic of a 'no-op' IAM policy suggested using a policy with an empty statement like follows:

```{ .json }
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "NoOpThatDoesntWorkSometimes",
            "Effect": "Allow",
            "Action": "none:null",
            "Resource": "*"
        }
    ]
}
```

Whilst this works in some contexts, it throws an error e.g. if you try to use it as a bucket (resource) policy. Also, whilst AWS are unlikely to ever introduce an action "none:null" (except potentially as some extension of IAM policy language) it cannot be a security invariant if it's effect is officially undefined.

If you know IAM you will know that there is one specific action that does not require any permissions to use - `sts:GetCallerIdentity`. The same information is returned by `aws sts get-caller-identity` whether you have this permission or not. We can exploit this therefore to create a no-op policy:

```{ .json }
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "NoOp",
            "Effect": "Allow",
            "Action": "sts:GetCallerIdentity",
            "Resource": "*"
        }
    ]
}
```
