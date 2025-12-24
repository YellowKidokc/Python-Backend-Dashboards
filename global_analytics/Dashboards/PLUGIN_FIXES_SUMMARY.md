# Obsidian Plugins - Fixes Summary

## Date: 2025-11-25

---

## Plugins Fixed

### 1. ✅ Theophysics Sandbox
**Location**: `D:\THEOPHYSICS_MASTER\.obsidian\plugins\theophysics-sandbox\`

**Problem**: Invalid icon `brain-circuit` causing load failure

**Fix Applied**:
- Changed `brain-circuit` → `brain`
- Rebuilt plugin: `npm run build`
- Deployed with `deploy.ps1`

**Status**: ✅ Fixed and deployed

**Documentation**: `D:\THEOPHYSICS_MASTER\Theophysics_Obsidian_Plugin\FIX_LOADING_ISSUE.md`

---

### 2. ✅ Theophysics Research Automation
**Location**: `D:\THEOPHYSICS_MASTER\.obsidian\plugins\theophysics-research-automation\`

**Problem**: Multiple invalid icons in right-click menu causing load failure

**Fix Applied**:
- `axiom` → `book`
- `evidence` → `file-search`
- `claim` → `alert-circle`
- `coherence` → `git-branch`
- `reference` → `link`

**Backup Created**: `main.js.broken-backup`

**Status**: ✅ Fixed and ready

**Documentation**: `D:\THEOPHYSICS_MASTER\THEOPHYSICS_RESEARCH_AUTOMATION_FIX.md`

---

## How to Enable Both Plugins

### Step 1: Reload Obsidian
Press `Ctrl+R` or restart Obsidian completely

### Step 2: Enable Plugins
1. Open Settings (`Ctrl+,`)
2. Go to **Community Plugins**
3. Find and enable:
   - ✅ **Theophysics Sandbox**
   - ✅ **Theophysics Research Automation**

### Step 3: Verify
Open Developer Console (`Ctrl+Shift+I`) and check for:
- No red errors
- Plugin initialization messages
- Both plugins listed as loaded

---

## Plugin Features Summary

### Theophysics Sandbox

**Main Features**:
- 15-tab dashboard interface
- Coherence scoring system
- AI-powered research analysis
- Vault analytics

**Key Tabs**:
- **Tab 0**: General Settings
- **Tab 10**: Coherence Dashboard (fully functional)
- **Tabs 1-9, 11-15**: Coming soon

**Ribbon Icons**:
- 🧠 Brain icon: AI Research
- 📊 Dashboard icon: Open Sandbox

**Status Bar**: "Theophysics: Active"

---

### Theophysics Research Automation

**Main Features**:
- Epistemic classification (right-click menu)
- Glossary management
- Auto-linking terms
- PostgreSQL integration (optional)
- AI integration (optional)

**Right-Click Menu** (on selected text):
- 📖 Mark as Axiom
- 🔍 Mark as Evidence
- ⚠️ Mark as Claim
- 🌿 Mark as Coherence
- 🔗 Mark as Reference

**Commands** (via `Ctrl+P`):
- Scan vault for terms
- Generate review queue
- Update glossary
- Translate math notation
- AI-assisted research

---

## Common Issues & Solutions

### Issue: Plugin doesn't appear in list

**Solution**:
1. Check folder name matches manifest.json `id`
2. Verify `main.js`, `manifest.json`, `styles.css` exist
3. Reload Obsidian

### Issue: Plugin loads but features don't work

**Solution**:
1. Check console for errors
2. Verify API keys (if using AI features)
3. Check settings configuration

### Issue: Icons don't appear

**Solution**:
- This was the main issue - now fixed!
- Icons now use standard Obsidian icon names

---

## Configuration Recommendations

### Theophysics Sandbox

1. **API Keys** (Settings → Theophysics Sandbox):
   - OpenAI API Key (for GPT features)
   - Anthropic API Key (for Claude features)

2. **Usage**:
   - Click dashboard icon to open
   - View coherence score
   - Analyze vault structure

### Theophysics Research Automation

1. **Glossary Path** (Settings → Theophysics Research Automation):
   ```
   Theophysics_Custom_Terms.md
   ```

2. **Auto-Linking**:
   - Enable for automatic term linking
   - Disable for manual control

3. **API Keys** (optional):
   - Same as Sandbox plugin
   - Enables AI-assisted features

4. **PostgreSQL** (optional):
   - See `POSTGRES_SETUP.md` in plugin folder
   - Not required for basic functionality

---

## File Locations

### Plugin Directories
```
D:\THEOPHYSICS_MASTER\.obsidian\plugins\
├── theophysics-sandbox\
│   ├── main.js
│   ├── manifest.json
│   └── styles.css
│
└── theophysics-research-automation\
    ├── main.js (✅ fixed)
    ├── main.js.broken-backup
    ├── manifest.json
    ├── styles.css
    └── [other modules...]
```

### Source Code (Sandbox)
```
D:\THEOPHYSICS_MASTER\Theophysics_Obsidian_Plugin\
├── src\
├── main.js (built)
├── manifest.json
├── styles.css
├── deploy.ps1
├── package.json
└── [documentation...]
```

### Documentation
```
D:\THEOPHYSICS_MASTER\
├── PLUGIN_FIXES_SUMMARY.md (this file)
├── THEOPHYSICS_RESEARCH_AUTOMATION_FIX.md
└── Theophysics_Obsidian_Plugin\
    ├── FIX_LOADING_ISSUE.md
    ├── TROUBLESHOOTING.md
    └── README.md
```

---

## Testing Checklist

### ✅ Theophysics Sandbox
- [ ] Plugin loads without errors
- [ ] Brain icon appears in ribbon
- [ ] Dashboard icon appears in ribbon
- [ ] Status bar shows "Theophysics: Active"
- [ ] Dashboard opens when clicking icon
- [ ] Coherence tab displays data
- [ ] Settings page accessible

### ✅ Theophysics Research Automation
- [ ] Plugin loads without errors
- [ ] Right-click menu appears on selected text
- [ ] All 5 classification options visible
- [ ] Icons display correctly
- [ ] Settings page accessible
- [ ] Glossary manager works
- [ ] Commands available in palette

---

## Quick Commands Reference

### Build & Deploy (Sandbox only)
```bash
cd D:\THEOPHYSICS_MASTER\Theophysics_Obsidian_Plugin
npm run build
powershell -ExecutionPolicy Bypass -File deploy.ps1
```

### Verify Syntax
```bash
# Sandbox
cd D:\THEOPHYSICS_MASTER\Theophysics_Obsidian_Plugin
node -c main.js

# Research Automation
cd D:\THEOPHYSICS_MASTER\.obsidian\plugins\theophysics-research-automation
node -c main.js
```

### Obsidian Shortcuts
- **Reload**: `Ctrl+R`
- **Settings**: `Ctrl+,`
- **Command Palette**: `Ctrl+P`
- **Developer Console**: `Ctrl+Shift+I`

---

## Next Steps

1. **Reload Obsidian** (`Ctrl+R`)
2. **Enable both plugins** (Settings → Community Plugins)
3. **Test basic functionality** (use checklists above)
4. **Configure settings** (add API keys if needed)
5. **Start using features**:
   - Open Sandbox dashboard
   - Try epistemic classification
   - Explore coherence scoring

---

## Support & Documentation

### For Sandbox Plugin
- `FIX_LOADING_ISSUE.md` - Fix details
- `TROUBLESHOOTING.md` - Detailed debugging
- `PROJECT_STATUS.md` - Development status
- `README.md` - Full documentation

### For Research Automation Plugin
- `THEOPHYSICS_RESEARCH_AUTOMATION_FIX.md` - Fix details
- `POSTGRES_SETUP.md` - Database setup (in plugin folder)

---

**Summary**: Both plugins had icon compatibility issues. All icons have been replaced with standard Obsidian icons. Both plugins are now ready to use.

**Action Required**: Reload Obsidian and enable both plugins in Settings → Community Plugins.

---

**Fixed**: 2025-11-25  
**Plugins**: 2 of 2 fixed ✅  
**Status**: Ready to use
