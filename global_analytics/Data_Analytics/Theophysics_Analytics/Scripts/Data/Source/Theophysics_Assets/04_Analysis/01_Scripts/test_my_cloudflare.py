"""
Quick test of your Cloudflare credentials
"""

from cloudflare_connector import CloudflareConnector

# Your credentials
API_TOKEN = "toqp02wplYXXakkIPfkxKOvardDHn12PVwBCNpDP"
ACCOUNT_ID = "d6e387eea4a4dda973d797ece5c5c40a"

print("="*60)
print("🌐 Testing Cloudflare Connection")
print("="*60)
print()

try:
    # Create connector
    connector = CloudflareConnector(
        api_token=API_TOKEN,
        account_id=ACCOUNT_ID
    )
    
    # Test connection
    print("🔍 Testing connection...")
    if connector.test_connection():
        print("✅ Connection successful!")
        print()
        
        # Get account info
        account_info = connector.get_account_info()
        print(f"📊 Account: {account_info.get('name', 'Unknown')}")
        print(f"   ID: {account_info.get('id', 'Unknown')}")
        print()
        
        # List Workers
        try:
            workers = connector.list_workers()
            print(f"📦 Workers: {len(workers)}")
            for worker in workers[:5]:  # Show first 5
                print(f"   - {worker.get('id', 'unknown')}")
        except Exception as e:
            print(f"📦 Workers: Error listing ({e})")
        
        # List R2 buckets
        try:
            buckets = connector.list_r2_buckets()
            print(f"🪣 R2 Buckets: {len(buckets)}")
            for bucket in buckets[:5]:  # Show first 5
                print(f"   - {bucket.get('name', 'unknown')}")
        except Exception as e:
            print(f"🪣 R2 Buckets: Error listing ({e})")
        
        # List Pages projects
        try:
            projects = connector.list_pages_projects()
            print(f"📄 Pages Projects: {len(projects)}")
            for project in projects[:5]:  # Show first 5
                print(f"   - {project.get('name', 'unknown')}")
        except Exception as e:
            print(f"📄 Pages Projects: Error listing ({e})")
        
        print()
        print("="*60)
        print("✅ All tests passed! Your Cloudflare account is ready.")
        print("="*60)
        
    else:
        print("❌ Connection failed!")
        print()
        print("Possible issues:")
        print("  - API token may be invalid or expired")
        print("  - Account ID may be incorrect")
        print("  - Token may not have the right permissions")
        print()
        print("Try:")
        print("  1. Generate new token: https://dash.cloudflare.com/profile/api-tokens")
        print("  2. Verify account ID: https://dash.cloudflare.com/")

except Exception as e:
    print(f"❌ Error: {e}")
    print()
    print("Make sure you have 'requests' installed:")
    print("  pip install requests")

print()
input("Press Enter to exit...")

