<# 
Combine-Files-Interactive.ps1

Interactive combiner for .md, .txt, .docx, .doc, .pdf:
- Prompts you with simple 1/2/3 choices for key decisions.
- Uses Pandoc to normalize .docx -> markdown (best quality).
- Uses pdftotext (if installed) for .pdf; otherwise can skip with a note.
- Creates one cohesive Markdown, with optional DOCX/PDF outputs via Pandoc.
- Leaves originals in place.

REQUIREMENTS:
- Pandoc (you said you have it).
- Optional: 'pdftotext' in PATH for PDFs (Poppler/Xpdf). If missing, PDFs are skipped with a note.
- Optional: Microsoft Word for legacy .doc (not .docx) text extraction.

USAGE:
  powershell -ExecutionPolicy Bypass -File .\Combine-Files-Interactive.ps1

TIP:
- Press ENTER to accept defaults on most prompts.
#>

# --- Helpers -------------------------------------------------------------

function Choice {
  param(
    [string]$Title,
    [string]$Message,
    [string[]]$Options,
    [int]$Default = 0
  )
  $choices = for ($i=0; $i -lt $Options.Count; $i++) {
    New-Object System.Management.Automation.Host.ChoiceDescription("&$($i+1) $($Options[$i])")
  }
  $idx = $Host.UI.PromptForChoice($Title, $Message, $choices, $Default)
  return $idx
}

function Ask-Text {
  param(
    [string]$Prompt,
    [string]$Default = ""
  )
  if ($Default) {
    $ans = Read-Host "$Prompt [Default: $Default]"
    if ([string]::IsNullOrWhiteSpace($ans)) { return $Default } else { return $ans }
  } else {
    return (Read-Host $Prompt)
  }
}

function YesNo {
  param(
    [string]$Title,
    [string]$Message,
    [bool]$DefaultYes = $true
  )
  $opts = @("Yes","No")
  $def = $DefaultYes ? 0 : 1
  return (Choice -Title $Title -Message $Message -Options $opts -Default $def) -eq 0
}

function Ensure-Word {
  try {
    $app = New-Object -ComObject Word.Application
    $app.Visible = $false
    return $app
  } catch {
    return $null
  }
}

# --- Discover tools ------------------------------------------------------

$pandoc    = Get-Command pandoc -ErrorAction SilentlyContinue
$pdftotext = Get-Command pdftotext -ErrorAction SilentlyContinue

if (-not $pandoc) {
  Write-Host "Pandoc is required but not found in PATH. Install Pandoc and re-run." -ForegroundColor Red
  exit 1
}

# --- Interactive flow ----------------------------------------------------

# 1) Target folder
$folderChoice = Choice -Title "Target Folder" -Message "Which folder should we combine from?" -Options @("Current folder","Browse by typing a path") -Default 0
if ($folderChoice -eq 0) {
  $Folder = (Get-Location).Path
} else {
  $Folder = Ask-Text -Prompt "Enter full path to the folder" -Default (Get-Location).Path
}
try { $Folder = (Resolve-Path $Folder).Path } catch { Write-Host "Folder not found." -ForegroundColor Red; exit 1 }

# 2) Recurse?
$recurse = YesNo -Title "Include Subfolders" -Message "Include files from subfolders (recursive)?" -DefaultYes:$true

# 3) File types
$fileTypeChoice = Choice -Title "File Types" -Message "Which file types do you want to combine?" `
  -Options @("MD + TXT","MD + TXT + DOCX","All (MD/TXT/DOCX/DOC/PDF)","Custom (type a list)") -Default 2

switch ($fileTypeChoice) {
  0 { $exts = @(".md",".markdown",".txt") }
  1 { $exts = @(".md",".markdown",".txt",".docx") }
  2 { $exts = @(".md",".markdown",".txt",".docx",".doc",".pdf") }
  3 {
      $raw = Ask-Text -Prompt "Enter extensions comma-separated (e.g. .md,.txt,.docx,.pdf)" -Default ".md,.txt,.docx,.pdf"
      $exts = $raw.Split(",") | ForEach-Object { $_.Trim() } | Where-Object { $_ }
    }
}

# 4) Sort order
$sortChoice = Choice -Title "Sort Order" -Message "How should we order the files?" `
  -Options @("By name (A→Z)","By modified time (newest→oldest)","By modified time (oldest→newest)") -Default 0

# 5) Output formats
$outChoice = Choice -Title "Output Format" -Message "What outputs do you want?" `
  -Options @("Markdown only",".md + .docx",".md + .pdf",".md + .docx + .pdf",".docx only",".pdf only") -Default 3

# 6) TOC?
$useToc = YesNo -Title "Table of Contents" -Message "Generate a Table of Contents?" -DefaultYes:$true

# 7) Page breaks
$pbChoice = Choice -Title "Page Breaks" -Message "Insert page breaks between files?" `
  -Options @("No (just a horizontal rule)","Hard page breaks (use Pandoc Lua filter)") -Default 0

# 8) Section header level
$hdrChoice = Choice -Title "Section Heading Style" -Message "Header level for each file section?" `
  -Options @("H2 (##)","H3 (###)") -Default 0
$hdr = ($hdrChoice -eq 0) ? "##" : "###"

# 9) Show file path in headers?
$showPath = YesNo -Title "Header Path" -Message "Show full path in section header (instead of just filename)?" -DefaultYes:$false

# 10) Handle PDFs
$pdfChoice = Choice -Title "PDF Handling" -Message "How should we handle PDFs?" `
  -Options @("Use pdftotext if available, else skip with a note","Always skip PDFs with a note") -Default 0
$usePdfToText = ($pdfChoice -eq 0)

# 11) Output base name
$defaultName = "AllCombined"
$outBaseName = Ask-Text -Prompt "Base output name" -Default $defaultName

# --- Resolve file set ----------------------------------------------------

$search = Get-ChildItem -LiteralPath $Folder -File -Recurse:$recurse -ErrorAction SilentlyContinue
$files = $search | Where-Object { $exts -contains $_.Extension.ToLower() }

switch ($sortChoice) {
  0 { $files = $files | Sort-Object FullName }
  1 { $files = $files | Sort-Object LastWriteTime -Descending }
  2 { $files = $files | Sort-Object LastWriteTime }
}

if (-not $files) {
  Write-Host "No matching files found." -ForegroundColor Yellow
  exit 0
}

Write-Host ""
Write-Host "Found $($files.Count) files to combine." -ForegroundColor Cyan

# --- Prepare output paths ------------------------------------------------

$timestamp = Get-Date -Format "yyyyMMdd_HHmm"
$outBase   = Join-Path $Folder "$outBaseName`_$timestamp"
$outMD     = "$outBase.md"
$nl        = "`r`n"

# Optional Lua filter for hard page breaks
$luaFilterPath = Join-Path $env:TEMP "pagebreak.lua"
if ($pbChoice -eq 1) {
  @"
-- pagebreak.lua: convert '::: pagebreak' or '<div class="pagebreak"></div>' to real page breaks in docx/pdf
function RawBlock(el)
  return nil
end

function Div(el)
  if el.classes:includes('pagebreak') then
    return pandoc.RawBlock('openxml', '<w:p><w:r><w:br w:type="page"/></w:r></w:p>')
  end
  return nil
end

function Para(el)
  for i, inline in ipairs(el.content) do
    if inline.t == 'Str' and inline.text == '\\newpage' then
      return pandoc.RawBlock('openxml', '<w:p><w:r><w:br w:type="page"/></w:r></w:p>')
    end
  end
  return nil
end
"@ | Out-File -LiteralPath $luaFilterPath -Encoding UTF8
}

# --- Converters ----------------------------------------------------------

$WordApp = $null
function Convert-DocToText {
  param([string]$path)
  if (-not $script:WordApp) { $script:WordApp = Ensure-Word }
  if (-not $script:WordApp) {
    return "`n> NOTE: Skipped $([IO.Path]::GetFileName($path)) — Microsoft Word not available for .doc.`n"
  }
  $tmp = [IO.Path]::GetTempFileName()
  try {
    $doc = $script:WordApp.Documents.Open($path, $false, $true)
    # 2 = wdFormatText
    $doc.SaveAs([ref]$tmp, [ref]2)
    $doc.Close($false)
    $text = Get-Content -LiteralPath $tmp -Raw -ErrorAction SilentlyContinue
    Remove-Item $tmp -ErrorAction SilentlyContinue
    return $text
  } catch {
    try { if ($doc) { $doc.Close($false) } } catch {}
    Remove-Item $tmp -ErrorAction SilentlyContinue
    return "`n> NOTE: Failed to extract text from $([IO.Path]::GetFileName($path)).`n"
  }
}

function Convert-DocxToMarkdown {
  param([string]$path)
  $tmpMd = [IO.Path]::GetTempFileName() + ".md"
  try {
    & $pandoc.Path --from=docx --to=gfm --wrap=none --output="$tmpMd" -- "$path"
    return (Get-Content -LiteralPath $tmpMd -Raw -ErrorAction SilentlyContinue)
  } catch {
    return "`n> NOTE: Pandoc failed to convert $([IO.Path]::GetFileName($path)) to markdown.`n"
  } finally {
    Remove-Item $tmpMd -ErrorAction SilentlyContinue
  }
}

function Convert-PdfToText {
  param([string]$path)
  if (-not $usePdfToText -or -not $pdftotext) {
    return "`n> NOTE: Skipped $([IO.Path]::GetFileName($path)) — pdftotext not available.`n"
  }
  $tmp = [IO.Path]::GetTempFileName()
  try {
    & $pdftotext.Path -nopgbrk -layout -enc UTF-8 -q -- "$path" "$tmp" | Out-Null
    $text = Get-Content -LiteralPath $tmp -Raw -ErrorAction SilentlyContinue
    Remove-Item $tmp -ErrorAction SilentlyContinue
    if ([string]::IsNullOrWhiteSpace($text)) {
      return "`n> NOTE: $([IO.Path]::GetFileName($path)) produced no text (likely scanned).`n"
    }
    return $text
  } catch {
    Remove-Item $tmp -ErrorAction SilentlyContinue
    return "`n> NOTE: Failed to extract text from $([IO.Path]::GetFileName($path)).`n"
  }
}

# --- Build combined markdown --------------------------------------------

$sb = New-Object System.Text.StringBuilder
$null = $sb.AppendLine("---")
$null = $sb.AppendLine("title: ""$outBaseName""")
$null = $sb.AppendLine("date: ""$(Get-Date -Format o)""")
if ($useToc) { $null = $sb.AppendLine("toc: true") }
$null = $sb.AppendLine("---")
$null = $sb.AppendLine()

foreach ($f in $files) {
  $label = ($showPath) ? $f.FullName : $f.Name
  $null = $sb.AppendLine("$hdr Source: $label")
  $null = $sb.AppendLine()

  $content = switch ($f.Extension.ToLower()) {
    ".md"        { Get-Content -LiteralPath $f.FullName -Raw -ErrorAction SilentlyContinue }
    ".markdown"  { Get-Content -LiteralPath $f.FullName -Raw -ErrorAction SilentlyContinue }
    ".txt"       { Get-Content -LiteralPath $f.FullName -Raw -ErrorAction SilentlyContinue }
    ".docx"      { Convert-DocxToMarkdown -path $f.FullName }
    ".doc"       { Convert-DocToText -path $f.FullName }
    ".pdf"       { Convert-PdfToText -path $f.FullName }
    default      { "`n> NOTE: Skipped unsupported file: $($f.Name)`n" }
  }

  if (-not [string]::IsNullOrWhiteSpace($content)) {
    $null = $sb.AppendLine($content.TrimEnd())
    $null = $sb.AppendLine()
  }

  if ($pbChoice -eq 1) {
    # pagebreak marker understood by the lua filter
    $null = $sb.AppendLine("::: pagebreak")
    $null = $sb.AppendLine(":::")
  } else {
    $null = $sb.AppendLine("---")
  }
  $null = $sb.AppendLine()
}

[IO.File]::WriteAllText($outMD, $sb.ToString(), [Text.Encoding]::UTF8)
Write-Host "Wrote: $outMD" -ForegroundColor Green

# Close Word if opened
if ($WordApp) { try { $WordApp.Quit() } catch {} }

# --- Produce requested outputs via Pandoc --------------------------------

# Common Pandoc args
$pandocArgs = @("--from=markdown","--wrap=none","--metadata=title=$outBaseName")
if ($useToc) { $pandocArgs += @("--toc","--toc-depth=3") }
if ($pbChoice -eq 1) { $pandocArgs += @("--lua-filter=$luaFilterPath") }

switch ($outChoice) {
  0 { # md only
  }
  1 { # md + docx
    try {
      & $pandoc.Path @pandocArgs --to=docx --output="$outBase.docx" -- "$outMD"
      Write-Host "Wrote: $outBase.docx" -ForegroundColor Green
    } catch { Write-Host "DOCX export failed." -ForegroundColor Yellow }
  }
  2 { # md + pdf
    try {
      & $pandoc.Path @pandocArgs --to=pdf --output="$outBase.pdf" -- "$outMD"
      Write-Host "Wrote: $outBase.pdf" -ForegroundColor Green
    } catch { Write-Host "PDF export failed (LaTeX engine may be missing)." -ForegroundColor Yellow }
  }
  3 { # md + docx + pdf
    try {
      & $pandoc.Path @pandocArgs --to=docx --output="$outBase.docx" -- "$outMD"
      Write-Host "Wrote: $outBase.docx" -ForegroundColor Green
    } catch { Write-Host "DOCX export failed." -ForegroundColor Yellow }
    try {
      & $pandoc.Path @pandocArgs --to=pdf --output="$outBase.pdf" -- "$outMD"
      Write-Host "Wrote: $outBase.pdf" -ForegroundColor Green
    } catch { Write-Host "PDF export failed (LaTeX engine may be missing)." -ForegroundColor Yellow }
  }
  4 { # docx only
    try {
      & $pandoc.Path @pandocArgs --to=docx --output="$outBase.docx" -- "$outMD"
      Write-Host "Wrote: $outBase.docx" -ForegroundColor Green
      # Optionally remove the intermediate md here if you don't want it:
      # Remove-Item $outMD -ErrorAction SilentlyContinue
    } catch { Write-Host "DOCX export failed." -ForegroundColor Yellow }
  }
  5 { # pdf only
    try {
      & $pandoc.Path @pandocArgs --to=pdf --output="$outBase.pdf" -- "$outMD"
      Write-Host "Wrote: $outBase.pdf" -ForegroundColor Green
      # Optionally remove the intermediate md here if you don't want it:
      # Remove-Item $outMD -ErrorAction SilentlyContinue
    } catch { Write-Host "PDF export failed (LaTeX engine may be missing)." -ForegroundColor Yellow }
  }
}

# Cleanup lua filter if created
if (Test-Path $luaFilterPath) { Remove-Item $luaFilterPath -ErrorAction SilentlyContinue }

Write-Host "Done." -ForegroundColor Cyan
