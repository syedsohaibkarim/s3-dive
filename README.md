S3 Bucket Explorer & Brute-Forcer (s3-dive)
Author: Syed Sohaib Karim
A pure Python script that scans, brute-forces, and explores AWS S3 buckets based on a domain/keyword. It checks if a bucket is valid, accessible, and public, retrieves bucket size, lists files & directories, and detects AWS regions where the bucket is available.

🚀 Features

✅ Brute-forces bucket names using common prefixes and suffixes (dev, staging, qa, etc.).

✅ Checks if an S3 bucket exists & is accessible.

✅ Retrieves total bucket size (if public).

✅ Lists files and directories within the bucket.

✅ Explores all AWS regions for bucket availability.

✅ Displays full file paths for easy access.

✅ Pure Python – No external dependencies required.

Example-Output
[INFO] Scanning possible S3 bucket names for: mycompany...
[INFO] Valid Buckets Found:
 - mycompany-staging
   [INFO] Accessible in Regions: us-east-1, us-west-2
   [INFO] Total Bucket Size: 45.32 MB
   [INFO] Directories: ['images', 'logs', 'documents']
   [INFO] Files with Paths:
     - https://mycompany-staging.s3.amazonaws.com/images/logo.png
     - https://mycompany-staging.s3.amazonaws.com/logs/error.log
     - https://mycompany-staging.s3.amazonaws.com/documents/report.pdf
       
🛠 How It Works
Generates possible S3 bucket names based on the input domain/keyword:
example.com, example-com
example.com-dev, example.com-staging, example.com-qa
examplecom-backup, examplecom-test, etc.
Checks if each bucket exists (valid & publicly accessible).
Verifies AWS regions where the bucket is accessible.
Retrieves bucket size (if accessible).
Lists directories and files (if accessible).
Displays full file paths for easy access.

📌 Limitations
Only works for publicly accessible S3 buckets.
Private buckets return 403 Forbidden.
Large buckets may require pagination (not included).

🔒 Legal Disclaimer
This tool is intended for educational and security research purposes only.
Do not use it on unauthorized S3 buckets. Unauthorized scanning of S3 buckets may violate AWS policies and local laws.

🙌 Contributing
Pull requests and feature suggestions are welcome! 🚀
