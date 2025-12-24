# Theophysics Research Automation Plugin - FIX APPLIED ✅

## Problem Identified

The **theophysics-research-automation** plugin was failing to load because it used **custom icon names** that don't exist in Obsidian's icon library.

### Invalid Icons Used
- `axiom` ❌
- `evidence` ❌
- `claim` ❌
- `coherence` ❌
- `reference` ❌

These icons were used in the right-click context menu for epistemic classification.

---

## Fix Applied

### Icon Replacements

| Old Icon (Invalid) | New Icon (Valid) | Purpose |
|-------------------|------------------|---------|
| `axiom` | `book` | Mark as Axiom |
| `evidence` | `file-search` | Mark as Evidence |
| `claim` | `alert-circle` | Mark as Claim |
| `coherence` | `git-branch` | Mark as Coherence |
| `reference` | `link` | Mark as Reference |

### Changes Made

1. **Backed up original file**: `main.js.broken-backup`
2. **Replaced all invalid icons** with standard Obsidian icons
3. **Verified syntax**: All JavaScript is valid
4. **Verified exports**: All module dependencies are correct

---

## How to Enable the Plugin

### Step 1: Reload Obsidian

**Quick Reload:**
- Press `Ctrl+R` in Obsidian

**Full Restart:**
- Close Obsidian completely
- Reopen it

### Step 2: Enable the Plugin

1. Open Settings (`Ctrl+,`)
2. Go to **Community Plugins**
3. Find **"Theophysics Research Automation"**
4. Toggle it **ON**

### Step 3: Verify It Works

1. **Check Console** (`Ctrl+Shift+I`):
   - Should load without errors
   - Look for plugin initialization messages

2. **Test Right-Click Menu**:
   - Open any note
   - Select some text
   - Right-click
   - You should see options:
     - Mark as Axiom ⚛
     - Mark as Evidence ◉
     - Mark as Claim ◇
     - Mark as Coherence ⟷
     - Mark as Reference ◈

3. **Check Settings**:
   - Settings → Theophysics Research Automation
   - Should show all configuration options

---

## Plugin Features

### Epistemic Classification (Right-Click Menu)

Select text and classify it as:
- **Axiom**: Foundational assumptions
- **Evidence**: Supporting data
- **Claim**: Assertions to verify
- **Coherence**: Coherence relationships
- **Reference**: External references

### Glossary Management

- Automatically detects key terms
- Links terms to central glossary
- Manages term definitions
- Tracks term usage

### Auto-Linking

- Automatically creates links to glossary entries
- Configurable term detection
- Whitelist/blacklist support

### PostgreSQL Integration

- Stores classifications in database
- Requires backend setup (see `POSTGRES_SETUP.md`)
- Falls back gracefully if not configured

### AI Integration

- Claude and OpenAI support
- Automated research assistance
- Requires API keys

---

## Configuration

### Settings Available

1. **Glossary File Path**: Where to store the central glossary
2. **Auto-Link Terms**: Enable/disable automatic linking
3. **PostgreSQL URL**: Database connection (optional)
4. **API Keys**: OpenAI and Anthropic keys
5. **Excluded Folders**: Folders to skip during scanning
6. **Term Detection**: Whitelist/blacklist configuration

### Recommended Setup

1. **Set Glossary Path**:
   ```
   Theophysics_Custom_Terms.md
   ```

2. **Configure Auto-Linking**:
   - Enable if you want automatic term linking
   - Disable for manual control

3. **Add API Keys** (optional):
   - OpenAI API Key for GPT features
   - Anthropic API Key for Claude features

4. **PostgreSQL** (optional):
   - See `POSTGRES_SETUP.md` for backend setup
   - Not required for basic functionality

---

## File Structure

### Plugin Files

```
D:\THEOPHYSICS_MASTER\.obsidian\plugins\theophysics-research-automation\
├── main.js                      ← Fixed main plugin file
├── main.js.broken-backup        ← Backup of broken version
├── main.js.backup               ← Previous backup
├── manifest.json                ← Plugin metadata
├── styles.css                   ← Plugin styles
├── settings.js                  ← Settings UI
├── glossary-manager.js          ← Glossary management
├── scanner.js                   ← Term detection
├── review-queue.js              ← Review queue generation
├── auto-linker.js               ← Automatic linking
├── detector.js                  ← Term detection logic
├── math-translator-command.js   ← Math translation
├── ai-integration.js            ← AI features
├── database-service.js          ← PostgreSQL integration
├── postgres-sync.js             ← Database sync
├── data.json                    ← Plugin settings data
└── POSTGRES_SETUP.md            ← Database setup guide
```

---

## Troubleshooting

### Plugin Still Won't Load

1. **Check Console** (`Ctrl+Shift+I`):
   - Look for specific error messages
   - Note any red errors

2. **Verify Files**:
   ```powershell
   cd "D:\THEOPHYSICS_MASTER\.obsidian\plugins\theophysics-research-automation"
   node -c main.js
   ```
   Should return no errors.

3. **Check Dependencies**:
   - All module files should exist
   - All exports should be correct

4. **Try Safe Mode**:
   - Disable all other plugins
   - Enable only this plugin
   - See if it loads

### Right-Click Menu Doesn't Appear

1. **Select Text First**: Menu only appears when text is selected
2. **Check Plugin is Enabled**: Settings → Community Plugins
3. **Reload Obsidian**: `Ctrl+R`

### Classifications Don't Save

1. **Check Console**: Look for database errors
2. **PostgreSQL Setup**: May need backend API (see `POSTGRES_SETUP.md`)
3. **Fallback Mode**: Plugin should work without database, but won't persist to PostgreSQL

### Auto-Linking Not Working

1. **Check Settings**: Ensure auto-linking is enabled
2. **Check Glossary Path**: Must point to valid file
3. **Check Whitelist**: Terms must be in whitelist or detected

---

## Known Limitations

### Current Version (0.1.0)

- **PostgreSQL**: Requires backend API setup (doesn't work directly in Obsidian)
- **Icons**: Now using standard icons (custom icons not supported)
- **Database**: Classifications stored locally, sync to PostgreSQL requires setup

### Planned Improvements

- Better icon support
- Improved database integration
- Enhanced AI features
- More classification types

---

## Testing Checklist

### ✅ Basic Functionality

- [ ] Plugin loads without errors
- [ ] Settings page accessible
- [ ] Right-click menu appears
- [ ] Can classify text
- [ ] Glossary manager works

### ✅ Advanced Features

- [ ] Auto-linking works (if enabled)
- [ ] Term detection works
- [ ] Review queue generates
- [ ] Math translator works (if configured)
- [ ] AI integration works (if API keys configured)

---

## Quick Reference

### Obsidian Shortcuts

- **Reload**: `Ctrl+R`
- **Settings**: `Ctrl+,`
- **Command Palette**: `Ctrl+P`
- **Developer Console**: `Ctrl+Shift+I`

### Plugin Commands

Access via Command Palette (`Ctrl+P`):
- Scan vault for terms
- Generate review queue
- Update glossary
- Translate math notation
- AI-assisted research

---

## Related Files

- **Main Plugin**: `D:\THEOPHYSICS_MASTER\.obsidian\plugins\theophysics-research-automation\`
- **Glossary**: `D:\THEOPHYSICS_MASTER\Theophysics_Custom_Terms.md`
- **Database Setup**: `POSTGRES_SETUP.md` (in plugin folder)

---

## Summary

### What Was Wrong
- Invalid icon names causing plugin load failure

### What Was Fixed
- Replaced all custom icons with standard Obsidian icons
- Backed up original file
- Verified all syntax and exports

### What to Do Now
1. Reload Obsidian (`Ctrl+R`)
2. Enable the plugin (Settings → Community Plugins)
3. Test right-click menu on selected text
4. Configure settings as needed

---

**Fixed**: 2025-11-25  
**Plugin Version**: 0.1.0  
**Issue**: Invalid icon names  
**Solution**: Replaced with standard Obsidian icons  
**Status**: ✅ Ready to use
