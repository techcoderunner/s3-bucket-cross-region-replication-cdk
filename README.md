# s3-bucket-cross-region-replication-cdk

1. Two separate stack created. One in primary region and second in secondary region
2. Created the S3 bucksts using s3.CfnBucket construct as s3.Bucket dose not contains replication configuration implemented yet. Its currenlty in feature list of aws cdk.
3. deploy the secondary stack first as secondary bucket need to be present before running the primary stack.

# Steps to run(Windows Machine)

1. Open the CMD and go to app directory
2. Enabled the virtual environment
`source.bat`
3. install the required packages
`python -m pip install -r requirement.txt`
4. synthesized the code
`cdk synth`
it will generate the two cdk stack i.e primary-stack and secondary-stack
5. deploy the secondary-stack first
`cdk deploy secondary-stack`
6. deploy primary stack
`cdk deploy primary stack`

# How to test
1. Login to AWS console
2. Go to your primary bucket and create the 'testing' folder
3. upload any file to the testing folder
4. Go to secondary bucket for verification, if files are replicated or not.