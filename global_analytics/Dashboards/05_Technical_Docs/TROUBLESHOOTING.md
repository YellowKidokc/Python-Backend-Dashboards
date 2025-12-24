---
uuid: 21aa813c-9e8d-52b8-90f0-b685a95b9358
title: 🔧 WINDSURF VAULT TROUBLESHOOTING GUIDE
author: David Lowe
type: documentation
created: '2025-11-22'
updated: '2025-11-22'
status: draft
file_path: 00_VAULT_SYSTEM\03_Docs\TROUBLESHOOTING.md
uuid_generated_at: '2025-11-22T01:23:02.380723'
uuid_version: '1.0'
tags: []
pillars: []
category: theophysics-general
---

# 🔧 WINDSURF VAULT TROUBLESHOOTING GUIDE

## 🚨 Common Issues & Solutions

---

### Issue 1: PowerShell Window Closes Immediately

**Problem:** When you double-click the `.ps1` file, the window flashes and closes.

**Solution:**
1. **Use the batch file instead:**
   - Double-click `new-vault.bat` (not the `.ps1` file)
   - This keeps the window open

2. **Or run from PowerShell manually:**
   ```powershell
   # Open PowerShell
   # Navigate to folder
   cd "D:\Obsidian\THEOPHYSICS"
   
   # Run script
   .\New-TheophysicsVault.ps1
   
   # Window will now stay open
   ```

3. **Script now has pause built-in:**
   - I just added `Read-Host` at the end
   - Window won't close until you press Enter

---

### Issue 2: "Execution Policy" Error

**Error Message:**
```
File cannot be loaded because running scripts is disabled on this system
```

**Solution:**
```powershell
# Run this command ONCE in PowerShell (as Administrator):
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then try running the script again
```

**Alternative:**
```powershell
# Run script with bypass (no permanent changes):
powershell.exe -ExecutionPolicy Bypass -File "D:\Obsidian\THEOPHYSICS\New-TheophysicsVault.ps1"
```

---

### Issue 3: Script Does Nothing / No Output

**Problem:** Script runs but nothing happens.

**Troubleshooting Steps:**

1. **Check if you're in the right folder:**
   ```powershell
   # Should show: D:\Obsidian\THEOPHYSICS
   Get-Location
   
   # If not, navigate there:
   cd "D:\Obsidian\THEOPHYSICS"
   ```

2. **Check if script exists:**
   ```powershell
   # Should list the .ps1 file
   Get-ChildItem *.ps1
   ```

3. **Run with verbose output:**
   ```powershell
   .\New-TheophysicsVault.ps1 -Verbose
   ```

4. **Check for errors:**
   - Script now has error handling
   - Any errors will be displayed in RED
   - Stack trace will show where it failed

---

### Issue 4: "Path Not Found" Error

**Error Message:**
```
Cannot find path 'D:\...' because it does not exist
```

**Solution:**

1. **For Full Vault creation:**
   - Make sure parent directory exists
   - Script will create the vault folder, but parent must exist
   
   ```powershell
   # Create parent directory first if needed:
   New-Item -ItemType Directory -Path "D:\MyVaults" -Force
   
   # Then run script:
   .\New-TheophysicsVault.ps1 -VaultPath "D:\MyVaults" -VaultName "Windsurf-Vault"
   ```

2. **For Local Project creation:**
   - Make sure the vault already exists
   - Create full vault first, then add projects
   
   ```powershell
   # First create vault:
   .\New-TheophysicsVault.ps1
   
   # Then add project:
   .\New-TheophysicsVault.ps1 -StructureType LocalProject -VaultPath "D:\Obsidian\THEOPHYSICS\Windsurf-Vault"
   ```

---

### Issue 5: Permission Denied

**Error Message:**
```
Access to the path '...' is denied
```

**Solutions:**

1. **Run PowerShell as Administrator:**
   - Right-click PowerShell
   - Choose "Run as Administrator"
   - Navigate and run script

2. **Choose a different location:**
   ```powershell
   # Use a folder you have write access to:
   .\New-TheophysicsVault.ps1 -VaultPath "C:\Users\YourName\Documents"
   ```

3. **Check folder permissions:**
   - Right-click folder → Properties → Security
   - Make sure you have "Write" permission

---

### Issue 6: Interactive Menu Not Showing

**Problem:** Script runs but menu doesn't appear.

**Solution:**

1. **Make sure you're using Interactive mode:**
   ```powershell
   .\New-TheophysicsVault.ps1 -StructureType Interactive
   ```

2. **Or use the batch file:**
   ```
   Double-click: new-vault.bat
   ```

3. **Check startup info:**
   - Script now shows:
     - Current directory
     - Structure type
     - Vault path
     - Vault name
   - This helps verify settings

---

### Issue 7: Files Created in Wrong Location

**Problem:** Vault created in unexpected folder.

**Solution:**

1. **Check current directory before running:**
   ```powershell
   Get-Location
   ```

2. **Specify exact path:**
   ```powershell
   .\New-TheophysicsVault.ps1 -VaultPath "D:\Obsidian\THEOPHYSICS" -VaultName "My-Vault"
   ```

3. **Use absolute paths (not relative):**
   ```powershell
   # Good:
   -VaultPath "D:\Obsidian\THEOPHYSICS"
   
   # Avoid:
   -VaultPath ".\THEOPHYSICS"
   ```

---

### Issue 8: Dry-Run Shows Nothing

**Problem:** Running with `-DryRun` but no output.

**Explanation:** This is normal!

**What Dry-Run Does:**
- Shows what WOULD be created
- Prefixes output with `[DRY-RUN]`
- Does NOT create any files
- Useful for testing

**To Actually Create Files:**
```powershell
# Remove -DryRun flag:
.\New-TheophysicsVault.ps1
```

---

## 🔍 Diagnostic Commands

### Check Script Location
```powershell
Get-ChildItem "D:\Obsidian\THEOPHYSICS\*.ps1"
```

### Check PowerShell Version
```powershell
$PSVersionTable.PSVersion
# Should be 5.1 or higher
```

### Test Script Syntax
```powershell
# Check for syntax errors:
Get-Content "D:\Obsidian\THEOPHYSICS\New-TheophysicsVault.ps1" | Out-Null
```

### View Script Parameters
```powershell
Get-Help "D:\Obsidian\THEOPHYSICS\New-TheophysicsVault.ps1" -Full
```

---

## 📋 Pre-Flight Checklist

Before running the script, verify:

- [ ] You're in the correct directory (`D:\Obsidian\THEOPHYSICS`)
- [ ] Script file exists (`New-TheophysicsVault.ps1`)
- [ ] You have write permissions to target folder
- [ ] PowerShell execution policy allows scripts
- [ ] Parent directory exists (for vault creation)
- [ ] You know what structure type you want (Full/Local/Interactive)

---

## 🆘 Still Having Issues?

### Get Detailed Error Info

The script now includes:
- ✅ Error messages in RED
- ✅ Stack traces showing where errors occur
- ✅ Startup info (directory, paths, settings)
- ✅ Pause at end (window won't close)

### Manual Troubleshooting Steps

1. **Open PowerShell**
2. **Navigate to script folder:**
   ```powershell
   cd "D:\Obsidian\THEOPHYSICS"
   ```

3. **Check files:**
   ```powershell
   Get-ChildItem
   ```

4. **Run script with full output:**
   ```powershell
   .\New-TheophysicsVault.ps1 -Verbose
   ```

5. **Read any error messages carefully**
   - Error will be in RED
   - Stack trace shows exact line that failed

6. **Try dry-run first:**
   ```powershell
   .\New-TheophysicsVault.ps1 -DryRun
   ```

---

## 🎯 Quick Fixes Summary

| Problem | Quick Fix |
|---------|-----------|
| Window closes immediately | Use `new-vault.bat` instead |
| Execution policy error | `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser` |
| Path not found | Create parent directory first |
| Permission denied | Run as Administrator or choose different folder |
| No output | Check you're in right directory, use `-Verbose` |
| Wrong location | Specify `-VaultPath` explicitly |

---

## ✅ Verified Working Setup

```powershell
# This should work:
cd "D:\Obsidian\THEOPHYSICS"
.\New-TheophysicsVault.ps1

# Or double-click:
new-vault.bat
```

**Script now includes:**
- ✅ Automatic error handling
- ✅ Startup diagnostics
- ✅ Pause at end (won't close)
- ✅ Detailed error messages
- ✅ Stack traces for debugging

---

**Last Updated:** 2025-11-07  
**Script Version:** 2.0 (Production + Error Handling)
