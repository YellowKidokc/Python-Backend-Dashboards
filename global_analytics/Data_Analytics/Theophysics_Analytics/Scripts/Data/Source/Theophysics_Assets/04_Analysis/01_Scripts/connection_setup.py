"""
Connection Setup - Interactive setup for Cloudflare and Postgres
"""

import os
from pathlib import Path
from cloudflare_connector import CloudflareConnector, save_cloudflare_config
from postgres_connector import PostgresConnector, PostgresConfig, save_postgres_config


def setup_cloudflare() -> bool:
    """Interactive Cloudflare setup."""
    print("\n" + "="*60)
    print("🌐 Cloudflare Connection Setup")
    print("="*60)
    
    print("\n📝 You'll need:")
    print("  1. API Token: https://dash.cloudflare.com/profile/api-tokens")
    print("     (Create token with Workers, R2, Pages permissions)")
    print("  2. Account ID: https://dash.cloudflare.com/ (right sidebar)")
    
    api_token = input("\n🔑 Enter Cloudflare API Token: ").strip()
    if not api_token:
        print("❌ API token required")
        return False
    
    account_id = input("🆔 Enter Account ID: ").strip()
    if not account_id:
        print("❌ Account ID required")
        return False
    
    # Test connection
    print("\n🔍 Testing connection...")
    try:
        connector = CloudflareConnector(api_token=api_token, account_id=account_id)
        if connector.test_connection():
            print("✅ Connection successful!")
            
            # Save config
            save_cloudflare_config(api_token, account_id)
            
            # Show account info
            account_info = connector.get_account_info()
            print(f"\n📊 Account: {account_info.get('name', 'Unknown')}")
            
            # List resources
            workers = connector.list_workers()
            buckets = connector.list_r2_buckets()
            projects = connector.list_pages_projects()
            
            print(f"  Workers: {len(workers)}")
            print(f"  R2 Buckets: {len(buckets)}")
            print(f"  Pages Projects: {len(projects)}")
            
            return True
        else:
            print("❌ Connection failed")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def setup_postgres() -> bool:
    """Interactive Postgres setup."""
    print("\n" + "="*60)
    print("🗄️  PostgreSQL Connection Setup")
    print("="*60)
    
    print("\n📝 Enter database connection details:")
    
    host = input("Host [localhost]: ").strip() or "localhost"
    port = input("Port [5432]: ").strip() or "5432"
    database = input("Database [theophysics_research]: ").strip() or "theophysics_research"
    user = input("User [postgres]: ").strip() or "postgres"
    password = input("Password: ").strip()
    
    if not password:
        print("⚠️  No password provided - will use environment variable")
    
    # Create config
    config = PostgresConfig(
        host=host,
        port=int(port),
        database=database,
        user=user,
        password=password
    )
    
    # Test connection
    print("\n🔍 Testing connection...")
    connector = PostgresConnector(config)
    if connector.test_connection():
        print("✅ Connection successful!")
        
        # Save config (without password)
        save_postgres_config(config)
        
        # Show database stats
        stats = connector.get_database_stats()
        print(f"\n📊 Database Statistics:")
        print(f"  Size: {stats.get('database_size', 'Unknown')}")
        print(f"  Tables: {stats.get('table_count', 0)}")
        print(f"  Active Connections: {stats.get('active_connections', 0)}")
        
        # List tables
        tables = connector.list_tables()
        if tables:
            print(f"\n📋 Tables ({len(tables)}):")
            for table in tables[:10]:  # Show first 10
                print(f"  - {table}")
            if len(tables) > 10:
                print(f"  ... and {len(tables) - 10} more")
        
        return True
    else:
        print("❌ Connection failed")
        print("\n💡 Troubleshooting:")
        print("  1. Is PostgreSQL running?")
        print("  2. Is the database created? (createdb theophysics_research)")
        print("  3. Are credentials correct?")
        return False


def main():
    """Main setup menu."""
    print("\n" + "="*60)
    print("🔌 Connection Setup - Cloudflare & PostgreSQL")
    print("="*60)
    
    print("\nWhat would you like to set up?")
    print("  1. Cloudflare")
    print("  2. PostgreSQL")
    print("  3. Both")
    print("  4. Test existing connections")
    print("  0. Exit")
    
    choice = input("\nChoice: ").strip()
    
    if choice == "1":
        setup_cloudflare()
    elif choice == "2":
        setup_postgres()
    elif choice == "3":
        setup_cloudflare()
        setup_postgres()
    elif choice == "4":
        test_existing()
    elif choice == "0":
        print("👋 Goodbye!")
    else:
        print("❌ Invalid choice")


def test_existing():
    """Test existing connections."""
    print("\n" + "="*60)
    print("🔍 Testing Existing Connections")
    print("="*60)
    
    # Test Cloudflare
    print("\n🌐 Testing Cloudflare...")
    try:
        from cloudflare_connector import CloudflareConnector, get_cloudflare_config
        config = get_cloudflare_config()
        if config.get("api_token"):
            connector = CloudflareConnector(
                api_token=config.get("api_token"),
                account_id=config.get("account_id")
            )
            if connector.test_connection():
                print("✅ Cloudflare: Connected")
            else:
                print("❌ Cloudflare: Connection failed")
        else:
            print("⚠️  Cloudflare: No config found")
    except Exception as e:
        print(f"❌ Cloudflare: {e}")
    
    # Test Postgres
    print("\n🗄️  Testing PostgreSQL...")
    try:
        connector = PostgresConnector()
        if connector.test_connection():
            print("✅ PostgreSQL: Connected")
        else:
            print("❌ PostgreSQL: Connection failed")
    except Exception as e:
        print(f"❌ PostgreSQL: {e}")


if __name__ == "__main__":
    main()

