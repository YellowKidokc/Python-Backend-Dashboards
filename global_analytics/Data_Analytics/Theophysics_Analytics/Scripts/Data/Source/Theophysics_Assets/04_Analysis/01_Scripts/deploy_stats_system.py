"""
Deploy Stats System - Create portable instances of the stats system
Handles global vs local instances and aggregation
"""

import shutil
import yaml
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime
import uuid


class StatsSystemDeployer:
    """Deploy and manage stats system instances."""
    
    def __init__(self, source_path: Path):
        """
        Initialize deployer.
        
        Args:
            source_path: Path to source stats system (this folder)
        """
        self.source_path = Path(source_path)
        self.config_file = self.source_path / "config.yaml"
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration."""
        if self.config_file.exists():
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f) or {}
        return {}
    
    def _save_config(self, config: Dict[str, Any], target_file: Path) -> None:
        """Save configuration."""
        with open(target_file, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, default_flow_style=False, allow_unicode=True)
    
    def create_deployment_package(self, output_folder: Path) -> Path:
        """
        Create a deployment package (everything needed for stats system).
        
        Args:
            output_folder: Where to create the package
        
        Returns:
            Path to created package
        """
        output_folder = Path(output_folder)
        package_name = f"stats-system-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        package_path = output_folder / package_name
        package_path.mkdir(parents=True, exist_ok=True)
        
        # Files to include
        files_to_copy = [
            "generate_stats.py",
            "generate_comparisons.py",
            "generate_global.py",
            "deploy_stats_system.py",
            "config.yaml",
            "RUN_ALL_STATS.bat",
            "STATS_README.md"
        ]
        
        # Copy files
        for file_name in files_to_copy:
            source_file = self.source_path / file_name
            if source_file.exists():
                shutil.copy2(source_file, package_path / file_name)
        
        # Create Stats folder structure
        (package_path / "Stats" / "Local").mkdir(parents=True, exist_ok=True)
        (package_path / "Stats" / "Comparisons").mkdir(parents=True, exist_ok=True)
        (package_path / "Stats" / "Global").mkdir(parents=True, exist_ok=True)
        
        print(f"✅ Package created: {package_path}")
        return package_path
    
    def deploy_local_instance(
        self,
        target_vault: Path,
        instance_name: str,
        global_vault: Path
    ) -> Path:
        """
        Deploy a local instance that aggregates to global.
        
        Args:
            target_vault: Where to deploy (another vault)
            instance_name: Name for this instance
            global_vault: Path to global vault (master)
        
        Returns:
            Path to deployed instance
        """
        target_vault = Path(target_vault)
        global_vault = Path(global_vault)
        
        # Create deployment folder
        deploy_folder = target_vault / "00_VAULT_SYSTEM" / "04_Analysis" / "01_Scripts"
        deploy_folder.mkdir(parents=True, exist_ok=True)
        
        # Copy all files
        files_to_copy = [
            "generate_stats.py",
            "generate_comparisons.py",
            "generate_global.py",
            "deploy_stats_system.py",
            "RUN_ALL_STATS.bat",
            "STATS_README.md"
        ]
        
        for file_name in files_to_copy:
            source_file = self.source_path / file_name
            if source_file.exists():
                shutil.copy2(source_file, deploy_folder / file_name)
        
        # Create local config
        local_config = self.config.copy()
        local_config["instance"]["type"] = "local"
        local_config["instance"]["name"] = instance_name
        local_config["instance"]["global_path"] = str(global_vault)
        local_config["aggregation"]["enabled"] = True
        local_config["aggregation"]["mode"] = "manual"
        
        # Save local config
        local_config_file = deploy_folder / "config.yaml"
        self._save_config(local_config, local_config_file)
        
        # Create Stats folders
        stats_folder = target_vault / "Stats"
        (stats_folder / "Local").mkdir(parents=True, exist_ok=True)
        (stats_folder / "Comparisons").mkdir(parents=True, exist_ok=True)
        (stats_folder / "Global").mkdir(parents=True, exist_ok=True)
        
        # Register instance in global registry
        self._register_instance(global_vault, instance_name, target_vault)
        
        print(f"✅ Local instance deployed: {deploy_folder}")
        print(f"   Instance name: {instance_name}")
        print(f"   Aggregates to: {global_vault}")
        
        return deploy_folder
    
    def _register_instance(
        self,
        global_vault: Path,
        instance_name: str,
        instance_path: Path
    ) -> None:
        """Register a local instance in the global registry."""
        registry_file = global_vault / "00_VAULT_SYSTEM" / "global_instance_registry.yaml"
        registry_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Load existing registry
        if registry_file.exists():
            with open(registry_file, 'r', encoding='utf-8') as f:
                registry = yaml.safe_load(f) or {}
        else:
            registry = {"instances": {}}
        
        # Add this instance
        instance_id = str(uuid.uuid4())
        registry["instances"][instance_id] = {
            "name": instance_name,
            "path": str(instance_path),
            "registered_at": datetime.now().isoformat(),
            "status": "active"
        }
        
        # Save registry
        with open(registry_file, 'w', encoding='utf-8') as f:
            yaml.dump(registry, f, default_flow_style=False, allow_unicode=True)
        
        print(f"✅ Instance registered in global registry: {instance_id}")
    
    def aggregate_to_global(self) -> None:
        """Aggregate this local instance's stats to global."""
        if self.config["instance"]["type"] != "local":
            print("⚠️  This is a global instance. No aggregation needed.")
            return
        
        if not self.config["aggregation"]["enabled"]:
            print("⚠️  Aggregation is disabled in config.")
            return
        
        global_path = Path(self.config["instance"]["global_path"])
        if not global_path.exists():
            print(f"❌ Global path not found: {global_path}")
            return
        
        # Get local stats folder
        local_stats = self.source_path.parent.parent.parent / "Stats"
        
        # Get global stats folder
        global_stats = global_path / "Stats" / "Local"
        global_stats.mkdir(parents=True, exist_ok=True)
        
        # Copy local stats to global (with instance prefix)
        instance_name = self.config["instance"]["name"]
        copied = 0
        
        for stats_file in (local_stats / "Local").glob("*.stats.json"):
            # Prefix with instance name to avoid conflicts
            target_name = f"{instance_name}_{stats_file.name}"
            target_file = global_stats / target_name
            
            shutil.copy2(stats_file, target_file)
            copied += 1
        
        print(f"✅ Aggregated {copied} stats files to global instance")
        print(f"   From: {local_stats}")
        print(f"   To: {global_stats}")
    
    def list_registered_instances(self) -> Dict[str, Any]:
        """List all registered instances (for global instance only)."""
        if self.config["instance"]["type"] != "global":
            print("⚠️  This is not a global instance.")
            return {}
        
        registry_file = self.source_path.parent.parent.parent / "00_VAULT_SYSTEM" / "global_instance_registry.yaml"
        
        if not registry_file.exists():
            print("No instances registered yet.")
            return {}
        
        with open(registry_file, 'r', encoding='utf-8') as f:
            registry = yaml.safe_load(f) or {}
        
        instances = registry.get("instances", {})
        
        print(f"\n📋 Registered Instances ({len(instances)}):")
        for instance_id, info in instances.items():
            print(f"   {info['name']}")
            print(f"      ID: {instance_id}")
            print(f"      Path: {info['path']}")
            print(f"      Status: {info['status']}")
            print(f"      Registered: {info['registered_at']}")
            print()
        
        return instances


# CLI Interface
if __name__ == "__main__":
    import sys
    
    source_path = Path(__file__).parent
    deployer = StatsSystemDeployer(source_path)
    
    if len(sys.argv) < 2:
        print("Stats System Deployer")
        print("=" * 60)
        print()
        print("Commands:")
        print("  package <output_folder>")
        print("      Create deployment package")
        print()
        print("  deploy <target_vault> <instance_name> <global_vault>")
        print("      Deploy local instance")
        print()
        print("  aggregate")
        print("      Aggregate local stats to global")
        print()
        print("  list")
        print("      List registered instances (global only)")
        sys.exit(0)
    
    command = sys.argv[1]
    
    if command == "package":
        if len(sys.argv) < 3:
            print("Usage: deploy_stats_system.py package <output_folder>")
            sys.exit(1)
        
        output_folder = Path(sys.argv[2])
        deployer.create_deployment_package(output_folder)
    
    elif command == "deploy":
        if len(sys.argv) < 5:
            print("Usage: deploy_stats_system.py deploy <target_vault> <instance_name> <global_vault>")
            sys.exit(1)
        
        target_vault = Path(sys.argv[2])
        instance_name = sys.argv[3]
        global_vault = Path(sys.argv[4])
        
        deployer.deploy_local_instance(target_vault, instance_name, global_vault)
    
    elif command == "aggregate":
        deployer.aggregate_to_global()
    
    elif command == "list":
        deployer.list_registered_instances()
    
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

