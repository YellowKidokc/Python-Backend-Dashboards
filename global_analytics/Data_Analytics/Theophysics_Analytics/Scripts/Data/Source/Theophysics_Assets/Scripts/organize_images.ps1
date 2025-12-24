# PowerShell script to consolidate images and update markdown links

# Set the base path
$basePath = "D:\THEOPHYSICS_MASTER\03_PUBLICATIONS\Logos_Papers\COMPLETE_LOGOS_PAPERS_FINAL"
$legacyAssetPath1 = "D:\THEOPHYSICS_MASTER\03_PUBLICATIONS\Logos_Papers\Assets"
$legacyAssetPath2 = "D:\THEOPHYSICS_MASTER\03_PUBLICATIONS\Logos_Papers\09_ASSETS\images"
$legacyAssetPath3 = "D:\THEOPHYSICS_MASTER\00_VAULT_SYSTEM\Assets\Images\logos papers"

# Get all paper files
$papers = Get-ChildItem -Path $basePath -Filter "Paper-*.md"

foreach ($paper in $papers) {
    # Get paper number
    $paperName = $paper.BaseName
    $paperNumber = $paperName.Split("-")[1]
    $paperNameShort = $paperName.Split("-")[2]
    $paperNameFull = "P" + $paperNumber + "-" + $paperNameShort

    # Create destination directory if it doesn't exist
    $destinationDir = Join-Path $basePath "Assets\images\$paperNameFull"
    if (-not (Test-Path $destinationDir)) {
        New-Item -ItemType Directory -Path $destinationDir
    }

    # Move images from legacy folders
    # Legacy Path 1
    $legacyDir1 = Join-Path $legacyAssetPath1 "P$paperNumber`_*"
    if (Test-Path $legacyDir1) {
        Get-ChildItem -Path $legacyDir1 -Recurse | Move-Item -Destination $destinationDir -Force
    }
    
    # Legacy Path 2
    Get-ChildItem -Path $legacyAssetPath2 -Filter "P$paperNumber`_*" | Move-Item -Destination $destinationDir -Force
    Get-ChildItem -Path $legacyAssetPath2 -Filter "P0$paperNumber`_*" | Move-Item -Destination $destinationDir -Force

    # Legacy Path 3
    $legacyDir3 = Join-Path $legacyAssetPath3 "P$paperNumber`_*"
    if (Test-Path $legacyDir3) {
        Get-ChildItem -Path $legacyDir3 -Recurse | Move-Item -Destination $destinationDir -Force
    }

    # Read paper content
    $content = Get-Content -Path $paper.FullName -Raw

    # Find all image links
    $regex = '!\[(.*?)\]\((.*?)\)'
    $matches = [regex]::Matches($content, $regex)

    foreach ($match in $matches) {
        $altText = $match.Groups[1].Value
        $oldPath = $match.Groups[2].Value
        $imageName = [System.IO.Path]::GetFileName($oldPath)

        # Find the image in the consolidated folder
        $newImagePath = Get-ChildItem -Path $destinationDir -Filter "*$imageName*" | Select-Object -First 1
        if ($newImagePath) {
            $newLink = "Assets/images/$paperNameFull/" + $newImagePath.Name
            $newMarkdownLink = "![$altText]($newLink)"
            $oldMarkdownLink = $match.Value
            $content = $content.Replace($oldMarkdownLink, $newMarkdownLink)
        }
    }

    # Write updated content back to the paper
    Set-Content -Path $paper.FullName -Value $content
}