"""
S3 Bucket Explorer & Brute-Forcer
Author: Syed Sohaib Karim
Description: A pure Python script that checks for valid S3 buckets, retrieves bucket size, 
lists directories & files, explores all AWS regions, and brute-forces possible bucket names.
"""

import urllib.request
import urllib.error
import xml.etree.ElementTree as ET

# AWS S3 Regions List
AWS_REGIONS = [
    "us-east-1", "us-east-2", "us-west-1", "us-west-2",
    "af-south-1", "ap-east-1", "ap-south-1", "ap-northeast-1",
    "ap-northeast-2", "ap-northeast-3", "ap-southeast-1", "ap-southeast-2",
    "ca-central-1", "eu-central-1", "eu-west-1", "eu-west-2", "eu-west-3",
    "eu-north-1", "eu-south-1", "me-south-1", "sa-east-1"
]

# Common suffixes for brute-force
SUFFIXES = ["", "www", "dev", "staging", "qa", "uat", "test", "prod", "backup", "old", "new"]

class S3BucketBruteForcer:
    def __init__(self, domain):
        self.domain = domain
        self.bucket_variants = self.generate_bucket_names()
        self.valid_buckets = []

    def generate_bucket_names(self):
        """Generates various bucket name permutations based on the given domain/keyword."""
        domain_variations = [self.domain, self.domain.replace(".", "-")]
        bucket_names = []
        for var in domain_variations:
            for suffix in SUFFIXES:
                bucket = f"{var}-{suffix}" if suffix else var
                bucket_names.append(bucket)
        return list(set(bucket_names))  # Remove duplicates

    def check_bucket(self, bucket_name):
        """Checks if an S3 bucket is valid and accessible."""
        url = f"https://{bucket_name}.s3.amazonaws.com"
        try:
            urllib.request.urlopen(url)
            return True
        except urllib.error.HTTPError as e:
            if e.code in [403, 200]:  # 403 = private bucket, 200 = public bucket
                return True
        except urllib.error.URLError:
            return False
        return False

    def check_regions(self, bucket_name):
        """Checks in which AWS regions the S3 bucket is accessible."""
        valid_regions = []
        for region in AWS_REGIONS:
            url = f"https://{bucket_name}.s3.{region}.amazonaws.com"
            try:
                urllib.request.urlopen(url)
                valid_regions.append(region)
            except urllib.error.HTTPError as e:
                if e.code in [403, 200]:
                    valid_regions.append(region)
            except urllib.error.URLError:
                pass
        return valid_regions

    def list_objects(self, bucket_name, prefix=""):
        """Lists files and directories inside an S3 bucket."""
        url = f"https://{bucket_name}.s3.amazonaws.com/?list-type=2&prefix={prefix}"
        try:
            response = urllib.request.urlopen(url)
            xml_data = response.read()
            root = ET.fromstring(xml_data)

            files = []
            directories = set()
            
            for content in root.findall(".//{http://s3.amazonaws.com/doc/2006-03-01/}Contents"):
                key = content.find("{http://s3.amazonaws.com/doc/2006-03-01/}Key").text
                if "/" in key[len(prefix):]:
                    dir_name = key[len(prefix):].split("/")[0]
                    directories.add(dir_name)
                else:
                    files.append(key)
                    
            return {"directories": sorted(directories), "files": files}
        except urllib.error.HTTPError:
            return None

    def get_bucket_size(self, bucket_name):
        """Calculates the total size of an S3 bucket."""
        url = f"https://{bucket_name}.s3.amazonaws.com/?list-type=2"
        total_size = 0
        try:
            response = urllib.request.urlopen(url)
            xml_data = response.read()
            root = ET.fromstring(xml_data)

            for content in root.findall(".//{http://s3.amazonaws.com/doc/2006-03-01/}Contents"):
                size = int(content.find("{http://s3.amazonaws.com/doc/2006-03-01/}Size").text)
                total_size += size

            return total_size
        except urllib.error.HTTPError:
            return None

    def scan_buckets(self):
        """Scans multiple bucket variations to check their validity."""
        print(f"\n[INFO] Scanning possible S3 bucket names for: {self.domain}...\n")
        
        for bucket in self.bucket_variants:
            if self.check_bucket(bucket):
                self.valid_buckets.append(bucket)

        if not self.valid_buckets:
            print("[ERROR] No valid buckets found for this domain.")
            return

        print("\n[INFO] Valid Buckets Found:")
        for bucket in self.valid_buckets:
            print(f" - {bucket}")

            regions = self.check_regions(bucket)
            if regions:
                print(f"   [INFO] Accessible in Regions: {', '.join(regions)}")
            else:
                print("   [INFO] No specific region found.")

            bucket_size = self.get_bucket_size(bucket)
            if bucket_size is not None:
                print(f"   [INFO] Total Bucket Size: {bucket_size / (1024 * 1024):.2f} MB")

            objects = self.list_objects(bucket)
            if objects:
                print(f"   [INFO] Directories: {objects['directories']}")
                print(f"   [INFO] Files with Paths:")
                for file in objects['files']:
                    print(f"     - https://{bucket}.s3.amazonaws.com/{file}")


if __name__ == "__main__":
    domain = input("Enter a domain or keyword to check for associated S3 buckets: ").strip()
    scanner = S3BucketBruteForcer(domain)
    scanner.scan_buckets()
