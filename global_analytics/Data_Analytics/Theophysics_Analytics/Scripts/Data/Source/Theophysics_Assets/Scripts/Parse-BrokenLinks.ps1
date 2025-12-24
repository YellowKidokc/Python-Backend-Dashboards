$inputFile = "D:\THEOPHYSICS_MASTER\parsed_broken_links.csv"
$outputFile = "D:\THEOPHYSICS_MASTER\parsed_broken_links_4.txt"

Clear-Content $outputFile -ErrorAction SilentlyContinue

$csv = Import-Csv -Path $inputFile

foreach ($row in $csv) {
    Write-Output $row
    $file = $row.File
    $link = $row.Link
    $type = $row.Type
    $reason = $row.Reason
    Add-Content -Path $outputFile -Value "File: $file, Link: $link, Type: $type, Reason: $reason"
}
