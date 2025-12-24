"""
Cloudflare Connector - Connect to Cloudflare services
Supports: Workers, R2, Pages, D1, AI Gateway
"""

import os
import requests
from typing import Dict, Optional, Any, List
from pathlib import Path
import json


class CloudflareConnector:
    """Connect to Cloudflare services."""
    
    def __init__(self, api_token: Optional[str] = None, account_id: Optional[str] = None):
        """
        Initialize Cloudflare connector.
        
        Args:
            api_token: Cloudflare API token (or from CLOUDFLARE_API_TOKEN env var)
            account_id: Cloudflare account ID (or from CLOUDFLARE_ACCOUNT_ID env var)
        """
        self.api_token = api_token or os.getenv("CLOUDFLARE_API_TOKEN")
        self.account_id = account_id or os.getenv("CLOUDFLARE_ACCOUNT_ID")
        self.base_url = "https://api.cloudflare.com/client/v4"
        
        if not self.api_token:
            raise ValueError("Cloudflare API token required. Set CLOUDFLARE_API_TOKEN env var or pass api_token.")
    
    def _headers(self) -> Dict[str, str]:
        """Get request headers."""
        return {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }
    
    # ========== Workers ==========
    
    def list_workers(self) -> List[Dict[str, Any]]:
        """List all Cloudflare Workers."""
        url = f"{self.base_url}/accounts/{self.account_id}/workers/scripts"
        response = requests.get(url, headers=self._headers())
        response.raise_for_status()
        return response.json().get("result", [])
    
    def deploy_worker(self, script_name: str, script_content: str) -> Dict[str, Any]:
        """Deploy a Worker script."""
        url = f"{self.base_url}/accounts/{self.account_id}/workers/scripts/{script_name}"
        response = requests.put(
            url,
            headers={**self._headers(), "Content-Type": "application/javascript"},
            data=script_content
        )
        response.raise_for_status()
        return response.json()
    
    # ========== R2 Storage ==========
    
    def list_r2_buckets(self) -> List[Dict[str, Any]]:
        """List R2 buckets."""
        url = f"{self.base_url}/accounts/{self.account_id}/r2/buckets"
        response = requests.get(url, headers=self._headers())
        response.raise_for_status()
        return response.json().get("result", [])
    
    def create_r2_bucket(self, bucket_name: str, location: str = "apac") -> Dict[str, Any]:
        """Create an R2 bucket."""
        url = f"{self.base_url}/accounts/{self.account_id}/r2/buckets"
        data = {"name": bucket_name, "location": location}
        response = requests.post(url, headers=self._headers(), json=data)
        response.raise_for_status()
        return response.json()
    
    def upload_to_r2(self, bucket_name: str, object_key: str, file_path: Path) -> bool:
        """
        Upload file to R2 bucket.
        Note: Requires R2 API token (different from main API token).
        """
        # This is simplified - R2 uses S3-compatible API
        # You'd need boto3 or similar for actual upload
        print(f"⚠️ R2 upload requires S3-compatible API. Use boto3 or wrangler.")
        return False
    
    # ========== Pages ==========
    
    def list_pages_projects(self) -> List[Dict[str, Any]]:
        """List Cloudflare Pages projects."""
        url = f"{self.base_url}/accounts/{self.account_id}/pages/projects"
        response = requests.get(url, headers=self._headers())
        response.raise_for_status()
        return response.json().get("result", [])
    
    def create_pages_project(self, project_name: str, production_branch: str = "main") -> Dict[str, Any]:
        """Create a Pages project."""
        url = f"{self.base_url}/accounts/{self.account_id}/pages/projects"
        data = {
            "name": project_name,
            "production_branch": production_branch
        }
        response = requests.post(url, headers=self._headers(), json=data)
        response.raise_for_status()
        return response.json()
    
    # ========== D1 Database ==========
    
    def list_d1_databases(self) -> List[Dict[str, Any]]:
        """List D1 databases."""
        url = f"{self.base_url}/accounts/{self.account_id}/d1/database"
        response = requests.get(url, headers=self._headers())
        response.raise_for_status()
        return response.json().get("result", [])
    
    def create_d1_database(self, database_name: str) -> Dict[str, Any]:
        """Create a D1 database."""
        url = f"{self.base_url}/accounts/{self.account_id}/d1/database"
        data = {"name": database_name}
        response = requests.post(url, headers=self._headers(), json=data)
        response.raise_for_status()
        return response.json()
    
    # ========== AI Gateway ==========
    
    def list_ai_gateways(self) -> List[Dict[str, Any]]:
        """List AI Gateway configurations."""
        url = f"{self.base_url}/accounts/{self.account_id}/ai/gateways"
        response = requests.get(url, headers=self._headers())
        response.raise_for_status()
        return response.json().get("result", [])
    
    # ========== Account Info ==========
    
    def get_account_info(self) -> Dict[str, Any]:
        """Get account information."""
        if not self.account_id:
            # Get first account if not specified
            url = f"{self.base_url}/accounts"
            response = requests.get(url, headers=self._headers())
            response.raise_for_status()
            accounts = response.json().get("result", [])
            if accounts:
                self.account_id = accounts[0]["id"]
        
        url = f"{self.base_url}/accounts/{self.account_id}"
        response = requests.get(url, headers=self._headers())
        response.raise_for_status()
        return response.json().get("result", {})
    
    def test_connection(self) -> bool:
        """Test Cloudflare API connection."""
        try:
            self.get_account_info()
            return True
        except Exception as e:
            print(f"Connection failed: {e}")
            return False


# ========== Helper Functions ==========

def get_cloudflare_config() -> Dict[str, str]:
    """Get Cloudflare config from environment or config file."""
    config_file = Path.home() / ".cloudflare" / "config.json"
    
    if config_file.exists():
        with open(config_file, "r") as f:
            return json.load(f)
    
    return {
        "api_token": os.getenv("CLOUDFLARE_API_TOKEN", ""),
        "account_id": os.getenv("CLOUDFLARE_ACCOUNT_ID", "")
    }


def save_cloudflare_config(api_token: str, account_id: str) -> None:
    """Save Cloudflare config to file."""
    config_dir = Path.home() / ".cloudflare"
    config_dir.mkdir(exist_ok=True)
    
    config_file = config_dir / "config.json"
    with open(config_file, "w") as f:
        json.dump({
            "api_token": api_token,
            "account_id": account_id
        }, f, indent=2)
    
    print(f"✅ Config saved to {config_file}")


# ========== Example Usage ==========

if __name__ == "__main__":
    # Test connection
    try:
        config = get_cloudflare_config()
        connector = CloudflareConnector(
            api_token=config.get("api_token"),
            account_id=config.get("account_id")
        )
        
        if connector.test_connection():
            print("✅ Cloudflare connection successful!")
            
            # List workers
            workers = connector.list_workers()
            print(f"📦 Found {len(workers)} Workers")
            
            # List R2 buckets
            buckets = connector.list_r2_buckets()
            print(f"🪣 Found {len(buckets)} R2 buckets")
            
            # List Pages projects
            projects = connector.list_pages_projects()
            print(f"📄 Found {len(projects)} Pages projects")
            
        else:
            print("❌ Connection failed")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n💡 To set up:")
        print("1. Get API token: https://dash.cloudflare.com/profile/api-tokens")
        print("2. Get account ID: https://dash.cloudflare.com/ (right sidebar)")
        print("3. Set environment variables:")
        print("   export CLOUDFLARE_API_TOKEN='your-token'")
        print("   export CLOUDFLARE_ACCOUNT_ID='your-account-id'")

