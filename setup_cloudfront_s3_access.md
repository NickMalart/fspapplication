# CloudFront S3 Access Setup Guide

This guide will help you set up proper access between CloudFront and your S3 bucket to prevent 403 Forbidden errors.

## 1. Create a CloudFront Origin Access Identity (OAI)

```bash
# Create a new OAI
aws cloudfront create-cloud-front-origin-access-identity \
    --cloud-front-origin-access-identity-config CallerReference=my-access-identity,Comment="OAI for FSP Application"
```

This will return a response with the OAI ID and S3 canonical user ID. Save these values.

## 2. Update your CloudFront Distribution

Go to your CloudFront distribution in the AWS Console:
1. Go to "Origins and Origin Groups"
2. Edit the S3 origin
3. For "Origin Access Identity", select "Use an OAI"
4. Select your newly created OAI
5. For "Bucket Policy", select "Yes, update the bucket policy"
6. Save changes

## 3. Update S3 Bucket Policy Manually

If the automatic policy update didn't work, you can manually add this policy to your S3 bucket:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "CloudFrontOAIAccess",
            "Effect": "Allow",
            "Principal": {
                "Service": "cloudfront.amazonaws.com"
            },
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::fspapplication-dev/*",
            "Condition": {
                "StringEquals": {
                    "AWS:SourceArn": "arn:aws:cloudfront::405439564869:distribution/E3HKY1PQO7X067"
                }
            }
        }
    ]
}
```

This policy uses the CloudFront service principal approach which is more secure and reliable than the legacy OAI approach.

Alternatively, if you prefer the OAI approach, use this policy:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "CloudFrontOAIAccess",
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::cloudfront:user/CloudFront Origin Access Identity YOUR_OAI_ID"
            },
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::fspapplication-dev/*"
        }
    ]
}
```

Replace `YOUR_OAI_ID` with your CloudFront OAI ID (starts with "E").

## 4. Update your Environment Variables

Add these to your `.env` file:

```
CLOUDFRONT_OAI_ID=YOUR_OAI_ID
AWS_S3_USE_OAI=True
```

## 5. Test your setup

After making these changes:
1. Wait for the CloudFront distribution to deploy (check status in AWS Console)
2. Try accessing your files through CloudFront again

## Troubleshooting

If you still see 403 errors:
1. Check that the CloudFront distribution status is "Deployed"
2. Verify the S3 bucket policy is correctly set up
3. Check that the S3 bucket and objects exist
4. Ensure the object permissions in S3 allow the CloudFront OAI to access them
5. Try invalidating the CloudFront cache for the path

```bash
aws cloudfront create-invalidation --distribution-id YOUR_DISTRIBUTION_ID --paths "/*"
```

Replace `YOUR_DISTRIBUTION_ID` with your CloudFront distribution ID. 