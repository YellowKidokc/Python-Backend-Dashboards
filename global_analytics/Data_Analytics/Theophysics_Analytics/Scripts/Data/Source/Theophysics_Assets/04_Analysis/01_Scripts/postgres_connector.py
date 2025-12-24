"""
PostgreSQL Connector - Enhanced connection utilities
Supports: Local Postgres, Cloudflare Hyperdrive, Remote Postgres
"""

import os
import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2 import sql
from typing import Dict, Optional, Any, List
from pathlib import Path
import json
from dataclasses import dataclass


@dataclass
class PostgresConfig:
    """PostgreSQL connection configuration."""
    host: str = "localhost"
    port: int = 5432
    database: str = "theophysics_research"
    user: str = "postgres"
    password: str = ""
    sslmode: str = "prefer"
    # For Cloudflare Hyperdrive
    hyperdrive_id: Optional[str] = None
    # Connection pool settings
    max_connections: int = 10


class PostgresConnector:
    """Enhanced PostgreSQL connector with utilities."""
    
    def __init__(self, config: Optional[PostgresConfig] = None):
        """Initialize PostgreSQL connector."""
        self.config = config or PostgresConfig()
        self.conn = None
        self._load_config()
    
    def _load_config(self) -> None:
        """Load config from environment or file."""
        # Try environment variables first
        if os.getenv("POSTGRES_HOST"):
            self.config.host = os.getenv("POSTGRES_HOST")
        if os.getenv("POSTGRES_PORT"):
            self.config.port = int(os.getenv("POSTGRES_PORT"))
        if os.getenv("POSTGRES_DB"):
            self.config.database = os.getenv("POSTGRES_DB")
        if os.getenv("POSTGRES_USER"):
            self.config.user = os.getenv("POSTGRES_USER")
        if os.getenv("POSTGRES_PASSWORD"):
            self.config.password = os.getenv("POSTGRES_PASSWORD")
        
        # Try config file
        config_file = Path.home() / ".postgres" / "config.json"
        if config_file.exists():
            with open(config_file, "r") as f:
                file_config = json.load(f)
                for key, value in file_config.items():
                    if hasattr(self.config, key) and value:
                        setattr(self.config, key, value)
    
    def connect(self) -> bool:
        """Connect to PostgreSQL database."""
        try:
            self.conn = psycopg2.connect(
                host=self.config.host,
                port=self.config.port,
                database=self.config.database,
                user=self.config.user,
                password=self.config.password,
                sslmode=self.config.sslmode
            )
            return True
        except psycopg2.OperationalError as e:
            print(f"❌ Database connection failed: {e}")
            return False
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return False
    
    def disconnect(self) -> None:
        """Disconnect from database."""
        if self.conn:
            self.conn.close()
            self.conn = None
    
    def test_connection(self) -> bool:
        """Test database connection."""
        if not self.connect():
            return False
        try:
            with self.conn.cursor() as cur:
                cur.execute("SELECT version();")
                version = cur.fetchone()[0]
                print(f"✅ Connected to PostgreSQL: {version[:50]}...")
                return True
        except Exception as e:
            print(f"❌ Connection test failed: {e}")
            return False
        finally:
            self.disconnect()
    
    def execute_query(self, query: str, params: tuple = None) -> List[Dict[str, Any]]:
        """Execute a SELECT query and return results."""
        if not self.connect():
            return []
        
        try:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query, params)
                return [dict(row) for row in cur.fetchall()]
        except Exception as e:
            print(f"❌ Query error: {e}")
            return []
        finally:
            self.disconnect()
    
    def execute_command(self, command: str, params: tuple = None) -> bool:
        """Execute an INSERT/UPDATE/DELETE command."""
        if not self.connect():
            return False
        
        try:
            with self.conn.cursor() as cur:
                cur.execute(command, params)
                self.conn.commit()
                return True
        except Exception as e:
            print(f"❌ Command error: {e}")
            if self.conn:
                self.conn.rollback()
            return False
        finally:
            self.disconnect()
    
    def get_table_info(self, table_name: str) -> List[Dict[str, Any]]:
        """Get table schema information."""
        query = """
            SELECT 
                column_name,
                data_type,
                is_nullable,
                column_default
            FROM information_schema.columns
            WHERE table_name = %s
            ORDER BY ordinal_position;
        """
        return self.execute_query(query, (table_name,))
    
    def list_tables(self) -> List[str]:
        """List all tables in the database."""
        query = """
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """
        results = self.execute_query(query)
        return [row["table_name"] for row in results]
    
    def get_database_stats(self) -> Dict[str, Any]:
        """Get database statistics."""
        if not self.connect():
            return {}
        
        try:
            stats = {}
            
            with self.conn.cursor() as cur:
                # Database size
                cur.execute("SELECT pg_size_pretty(pg_database_size(current_database()));")
                stats["database_size"] = cur.fetchone()[0]
                
                # Number of tables
                cur.execute("""
                    SELECT COUNT(*) 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public';
                """)
                stats["table_count"] = cur.fetchone()[0]
                
                # Connection count
                cur.execute("SELECT COUNT(*) FROM pg_stat_activity;")
                stats["active_connections"] = cur.fetchone()[0]
                
                # PostgreSQL version
                cur.execute("SELECT version();")
                stats["version"] = cur.fetchone()[0]
            
            return stats
        except Exception as e:
            print(f"❌ Error getting stats: {e}")
            return {}
        finally:
            self.disconnect()


# ========== Helper Functions ==========

def get_postgres_config() -> PostgresConfig:
    """Get Postgres config from environment or config file."""
    config_file = Path.home() / ".postgres" / "config.json"
    
    if config_file.exists():
        with open(config_file, "r") as f:
            config_dict = json.load(f)
            return PostgresConfig(**config_dict)
    
    return PostgresConfig()


def save_postgres_config(config: PostgresConfig) -> None:
    """Save Postgres config to file."""
    config_dir = Path.home() / ".postgres"
    config_dir.mkdir(exist_ok=True)
    
    config_file = config_dir / "config.json"
    with open(config_file, "w") as f:
        # Don't save password in plain text (use env var instead)
        config_dict = {
            "host": config.host,
            "port": config.port,
            "database": config.database,
            "user": config.user,
            "sslmode": config.sslmode
        }
        json.dump(config_dict, f, indent=2)
    
    print(f"✅ Config saved to {config_file}")
    print("⚠️  Password not saved - use POSTGRES_PASSWORD environment variable")


# ========== Cloudflare Hyperdrive Support ==========

class HyperdriveConnector(PostgresConnector):
    """PostgreSQL connector via Cloudflare Hyperdrive."""
    
    def __init__(self, hyperdrive_id: str, config: Optional[PostgresConfig] = None):
        """
        Initialize Hyperdrive connector.
        
        Args:
            hyperdrive_id: Cloudflare Hyperdrive connection ID
            config: Base Postgres config (host will be overridden)
        """
        super().__init__(config)
        self.hyperdrive_id = hyperdrive_id
        # Hyperdrive provides a connection string via Cloudflare
        # In production, you'd get this from Cloudflare Workers env
        self.config.host = f"hyperdrive-{hyperdrive_id}.cloudflare"
    
    def get_connection_string(self) -> str:
        """Get Hyperdrive connection string (for use in Workers)."""
        # This would be provided by Cloudflare Workers environment
        return f"postgresql://{self.config.user}:{self.config.password}@{self.config.host}:{self.config.port}/{self.config.database}"


# ========== Example Usage ==========

if __name__ == "__main__":
    # Test connection
    connector = PostgresConnector()
    
    if connector.test_connection():
        print("\n📊 Database Statistics:")
        stats = connector.get_database_stats()
        for key, value in stats.items():
            print(f"  {key}: {value}")
        
        print("\n📋 Tables:")
        tables = connector.list_tables()
        for table in tables:
            print(f"  - {table}")
        
        if tables:
            print(f"\n🔍 Schema for '{tables[0]}':")
            columns = connector.get_table_info(tables[0])
            for col in columns:
                print(f"  - {col['column_name']} ({col['data_type']})")
    else:
        print("\n💡 To set up PostgreSQL:")
        print("1. Install PostgreSQL: https://www.postgresql.org/download/")
        print("2. Create database: createdb theophysics_research")
        print("3. Set environment variables:")
        print("   export POSTGRES_HOST='localhost'")
        print("   export POSTGRES_PORT='5432'")
        print("   export POSTGRES_DB='theophysics_research'")
        print("   export POSTGRES_USER='postgres'")
        print("   export POSTGRES_PASSWORD='your-password'")

