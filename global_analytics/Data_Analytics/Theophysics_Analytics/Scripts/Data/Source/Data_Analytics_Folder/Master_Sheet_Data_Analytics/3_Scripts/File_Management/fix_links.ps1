# PowerShell script to update markdown links

# Set the base path
$basePath = "D:\THEOPHYSICS_MASTER\03_PUBLICATIONS\Logos_Papers\COMPLETE_LOGOS_PAPERS_FINAL"

for ($i = 5; $i -le 12; $i++) {
    $paperNumber = "{0:D2}" -f $i
    $paperFile = Get-ChildItem -Path $basePath -Filter "Paper-$paperNumber*.md"
    if ($paperFile) {
        $folderName = $paperFile.Name.Split("-")[2]
        $imageDir = "Assets/images/P$paperNumber-$folderName"
        
        $content = Get-Content -Path $paperFile.FullName -Raw

        $regex = '!\[(.*?)\]\((.*?)\)'
        $matches = [regex]::Matches($content, $regex)

        foreach ($match in $matches) {
            $altText = $match.Groups[1].Value
            $oldPath = $match.Groups[2].Value
            $imageName = [System.IO.Path]::GetFileName($oldPath)
            
            $newLink = "$imageDir/$imageName"
            $newMarkdownLink = "![$altText]($newLink)"
            $oldMarkdownLink = $match.Value
            $content = $content.Replace($oldMarkdownLink, $newMarkdownLink)
        }
        Set-Content -Path $paperFile.FullName -Value $content
    }
}
