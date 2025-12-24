function Get-MarkdownLinks {
    param (
        [string]$FilePath
    )

    $content = Get-Content -Path $FilePath -Raw
    $links = @()

    # Regex for inline links: [text](url "title") or [text](url)
    $inlineLinkPattern = '\[([^\]]+)\]\(([^)]+)\)'
    # Regex for image links: ![alt text](url "title") or ![alt text](url)
    $imageLinkPattern = '!\[([^\]]*)\]\(([^)]+)\)'

    # Find inline links
    Select-String -InputObject $content -Pattern $inlineLinkPattern -AllMatches | ForEach-Object {
        foreach ($match in $_.Matches) {
            $links += [PSCustomObject]@{
                Type = "Inline"
                Text = $match.Groups[1].Value
                Url  = $match.Groups[2].Value
                SourceFile = $FilePath
            }
        }
    }

    # Find image links
    Select-String -InputObject $content -Pattern $imageLinkPattern -AllMatches | ForEach-Object {
        foreach ($match in $_.Matches) {
            $links += [PSCustomObject]@{
                Type = "Image"
                Text = $match.Groups[1].Value
                Url  = $match.Groups[2].Value
                SourceFile = $FilePath
            }
        }
    }

    return $links
}

function Test-ExternalLink {
    param (
        [string]$Url
    )
    try {
        # Use -Method Head to avoid downloading the entire content, just check headers
        $response = Invoke-WebRequest -Uri $Url -Method Head -TimeoutSec 10 -ErrorAction SilentlyContinue
        if ($response.StatusCode -ge 200 -and $response.StatusCode -lt 400) {
            return $true
        } else {
            return $false
        }
    } catch {
        # Catch any errors like DNS resolution failure, connection timeout, etc.
        return $false
    }
}

function Test-InternalLink {
    param (
        [string]$RelativePath,
        [string]$BaseDirectory
    )
    # Handle URL-encoded paths if necessary (e.g., spaces as %20)
    $decodedPath = [System.Uri]::UnescapeDataString($RelativePath)

    # Construct the full path
    # Ensure the path is treated as relative to the base directory
    $fullPath = Join-Path -Path $BaseDirectory -ChildPath $decodedPath

    # Test-Path can check for files or directories
    return Test-Path -Path $fullPath -PathType Leaf
}

# --- Main Script Logic ---

$rootPath = "D:\THEOPHYSICS_MASTER\03_PUBLICATIONS\Logos_Papers\COMPLETE_LOGOS_PAPERS_FINAL"
$markdownFiles = Get-ChildItem -Path $rootPath -Recurse -Include "*.md" -File

$brokenLinks = @()

foreach ($file in $markdownFiles) {
    Write-Host "Processing file: $($file.FullName)"
    $links = Get-MarkdownLinks -FilePath $file.FullName
    $baseDirectory = Split-Path -Path $file.FullName -Parent

    foreach ($link in $links) {
        if ($link.Url -match '^(http|https)://') {
            # External link
            if (-not (Test-ExternalLink -Url $link.Url)) {
                $brokenLinks += [PSCustomObject]@{
                    File = $file.FullName
                    Link = $link.Url
                    Type = $link.Type
                    Reason = "External link is broken or unreachable."
                }
            }
        } elseif ($link.Url -match '^#') {
            # Anchor link within the same file.
            # Validating these accurately requires parsing the Markdown for headers/IDs,
            # which is beyond the scope of a simple regex-based script.
            # For now, we'll assume they are valid.
        } else {
            # Internal file link (could be relative or absolute)
            # We need to handle cases where the link might be a relative path like "../images/pic.png"
            # or a direct file name "document.pdf"
            if (-not (Test-InternalLink -RelativePath $link.Url -BaseDirectory $baseDirectory)) {
                $brokenLinks += [PSCustomObject]@{
                    File = $file.FullName
                    Link = $link.Url
                    Type = $link.Type
                    Reason = "Internal file link does not exist."
                }
            }
        }
    }
}

if ($brokenLinks.Count -gt 0) {
    Write-Host "`n--- Broken Links Found ---" -ForegroundColor Red
    $brokenLinks | Format-Table -AutoSize
} else {
    Write-Host "`nNo broken links found." -ForegroundColor Green
}
