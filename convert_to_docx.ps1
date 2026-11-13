param(
    [string]$MdPath = "D:\CoinCollector_HananVictor\Laporan_Fitur_Game.md",
    [string]$DocxDest1 = "C:\Users\ASUS\Documents\Laporan_ProjectGame\Laporan_Fitur_Game.docx",
    [string]$DocxDest2 = "D:\CoinCollector_HananVictor\Laporan_Fitur_Game.docx"
)

$mdLines = Get-Content -Path $MdPath -Encoding UTF8

$htmlBody = New-Object System.Text.StringBuilder

function Format-Inline([string]$text) {
    if ([string]::IsNullOrEmpty($text)) { return "" }
    
    # Replace math arrows and symbols
    $text = $text.Replace('$\rightarrow$', '&rarr;')
    $text = $text.Replace('$\le$', '&le;')
    $text = $text.Replace('\rightarrow', '&rarr;')
    $text = $text.Replace('\le', '&le;')
    
    # Replace markdown links: [text](url) -> text
    $text = [regex]::Replace($text, '\[([^\]]+)\]\([^\)]+\)', '<strong>$1</strong>')
    
    # Replace bold: **text**
    $text = [regex]::Replace($text, '\*\*([^\*]+)\*\*', '<strong>$1</strong>')
    
    # Replace inline code: `code`
    $text = [regex]::Replace($text, '`([^`]+)`', '<code class="inline-code">$1</code>')
    
    return $text
}

$inTable = $false
$tableRows = New-Object System.Collections.Generic.List[string]
$inUl = $false
$inSubUl = $false
$inOl = $false

function Flush-Table() {
    if (-not $script:inTable -or $script:tableRows.Count -eq 0) { 
        $script:inTable = $false
        $script:tableRows.Clear()
        return 
    }
    
    [void]$htmlBody.AppendLine('<table class="report-table">')
    $isHeader = $true
    
    foreach ($row in $script:tableRows) {
        # Check if separator row (e.g. | :--- | :--- |)
        if ($row -match '^[\|\s\-:]+$') {
            $isHeader = $false
            continue
        }
        
        $cells = $row.Trim().Trim('|').Split('|')
        
        if ($isHeader) {
            [void]$htmlBody.AppendLine('  <thead><tr>')
            foreach ($cell in $cells) {
                $c = Format-Inline $cell.Trim()
                [void]$htmlBody.AppendLine("    <th>$c</th>")
            }
            [void]$htmlBody.AppendLine('  </tr></thead><tbody>')
            $isHeader = $false
        } else {
            [void]$htmlBody.AppendLine('  <tr>')
            foreach ($cell in $cells) {
                $c = Format-Inline $cell.Trim()
                # support <br>
                [void]$htmlBody.AppendLine("    <td>$c</td>")
            }
            [void]$htmlBody.AppendLine('  </tr>')
        }
    }
    
    [void]$htmlBody.AppendLine('</tbody></table>')
    $script:inTable = $false
    $script:tableRows.Clear()
}

function Close-Lists() {
    if ($script:inSubUl) {
        [void]$htmlBody.AppendLine('    </ul>')
        $script:inSubUl = $false
    }
    if ($script:inUl) {
        [void]$htmlBody.AppendLine('</ul>')
        $script:inUl = $false
    }
    if ($script:inOl) {
        [void]$htmlBody.AppendLine('</ol>')
        $script:inOl = $false
    }
}

for ($i = 0; $i -lt $mdLines.Count; $i++) {
    $line = $mdLines[$i]
    $trimmed = $line.Trim()

    # Table handling
    if ($trimmed.StartsWith('|') -and $trimmed.EndsWith('|')) {
        Close-Lists
        $inTable = $true
        $tableRows.Add($trimmed)
        continue
    } else {
        if ($inTable) {
            Flush-Table
        }
    }

    # Blank line
    if ([string]::IsNullOrWhiteSpace($trimmed)) {
        Close-Lists
        continue
    }

    # Horizontal Rule
    if ($trimmed -eq '---') {
        Close-Lists
        [void]$htmlBody.AppendLine('<hr class="divider"/>')
        continue
    }

    # Headers
    if ($trimmed.StartsWith('### ')) {
        Close-Lists
        $content = Format-Inline $trimmed.Substring(4).Trim()
        [void]$htmlBody.AppendLine("<h3 class='h3-title'>$content</h3>")
        continue
    }
    if ($trimmed.StartsWith('## ')) {
        Close-Lists
        $content = Format-Inline $trimmed.Substring(3).Trim()
        [void]$htmlBody.AppendLine("<h2 class='h2-title'>$content</h2>")
        continue
    }
    if ($trimmed.StartsWith('# ')) {
        Close-Lists
        $content = Format-Inline $trimmed.Substring(2).Trim()
        [void]$htmlBody.AppendLine("<h1 class='h1-title'>$content</h1>")
        continue
    }

    # Sub-bullet list (indented)
    if ($line.StartsWith('  * ') -or $line.StartsWith('    * ')) {
        if (-not $inSubUl) {
            if (-not $inUl) {
                [void]$htmlBody.AppendLine('<ul class="report-list">')
                $inUl = $true
            }
            [void]$htmlBody.AppendLine('    <ul class="sub-list">')
            $inSubUl = $true
        }
        $bulletContent = Format-Inline $trimmed.Substring(2).Trim()
        [void]$htmlBody.AppendLine("      <li>$bulletContent</li>")
        continue
    }

    # Top-level bullet list
    if ($trimmed.StartsWith('* ')) {
        if ($inSubUl) {
            [void]$htmlBody.AppendLine('    </ul>')
            $inSubUl = $false
        }
        if (-not $inUl) {
            [void]$htmlBody.AppendLine('<ul class="report-list">')
            $inUl = $true
        }
        $bulletContent = Format-Inline $trimmed.Substring(2).Trim()
        [void]$htmlBody.AppendLine("  <li>$bulletContent</li>")
        continue
    }

    # Numbered list
    if ($trimmed -match '^\d+\.\s+(.*)$') {
        Close-Lists
        if (-not $inOl) {
            [void]$htmlBody.AppendLine('<ol class="report-ol">')
            $inOl = $true
        }
        $olContent = Format-Inline $matches[1].Trim()
        [void]$htmlBody.AppendLine("  <li>$olContent</li>")
        continue
    }

    # Standard Paragraph
    Close-Lists
    $pContent = Format-Inline $trimmed
    [void]$htmlBody.AppendLine("<p class='report-p'>$pContent</p>")
}

if ($inTable) { Flush-Table }
Close-Lists

$fullHtml = @"
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8"/>
<title>Laporan Analisis Fitur Proyek Game</title>
<style>
  body {
    font-family: 'Calibri', 'Segoe UI', Arial, sans-serif;
    font-size: 11pt;
    line-height: 1.5;
    color: #2D3748;
    margin: 20px;
  }
  .h1-title {
    font-size: 22pt;
    font-weight: bold;
    color: #1A365D;
    border-bottom: 2.5pt solid #1A365D;
    padding-bottom: 6px;
    margin-top: 20px;
    margin-bottom: 15px;
    text-transform: uppercase;
  }
  .h2-title {
    font-size: 15pt;
    font-weight: bold;
    color: #2B6CB0;
    border-bottom: 1pt solid #CBD5E0;
    padding-bottom: 4px;
    margin-top: 24px;
    margin-bottom: 12px;
  }
  .h3-title {
    font-size: 12.5pt;
    font-weight: bold;
    color: #2D3748;
    margin-top: 18px;
    margin-bottom: 8px;
  }
  .report-p {
    margin-bottom: 8px;
    margin-top: 0;
    text-align: justify;
  }
  .inline-code {
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 10pt;
    background-color: #EDF2F7;
    color: #C53030;
    padding: 2px 4px;
    border: 1px solid #E2E8F0;
    border-radius: 3px;
  }
  .divider {
    border: 0;
    height: 1px;
    background-color: #E2E8F0;
    margin: 20px 0;
  }
  .report-list, .report-ol {
    margin-top: 4px;
    margin-bottom: 12px;
    padding-left: 24px;
  }
  .sub-list {
    margin-top: 3px;
    margin-bottom: 6px;
    padding-left: 20px;
  }
  li {
    margin-bottom: 5px;
  }
  .report-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 12px;
    margin-bottom: 18px;
    font-size: 10pt;
  }
  .report-table th {
    background-color: #1A365D;
    color: #FFFFFF;
    font-weight: bold;
    text-align: left;
    padding: 8px 10px;
    border: 1px solid #1A365D;
  }
  .report-table td {
    padding: 7px 10px;
    border: 1px solid #CBD5E0;
    vertical-align: top;
  }
  .report-table tr:nth-child(even) {
    background-color: #F7FAFC;
  }
</style>
</head>
<body>
$($htmlBody.ToString())
</body>
</html>
"@

$tempHtml = [System.IO.Path]::Combine([System.IO.Path]::GetTempPath(), "Laporan_Temp.html")
[System.IO.File]::WriteAllText($tempHtml, $fullHtml, [System.Text.Encoding]::UTF8)
Write-Output "Temp HTML generated at: $tempHtml"

# Convert to DOCX using Word COM
$word = New-Object -ComObject Word.Application
$word.Visible = $false
try {
    Write-Output "Opening HTML in Word..."
    $doc = $word.Documents.Open($tempHtml)
    
    # Configure page setup
    $doc.PageSetup.TopMargin = 72    # 1 inch = 72 pt
    $doc.PageSetup.BottomMargin = 72
    $doc.PageSetup.LeftMargin = 72
    $doc.PageSetup.RightMargin = 72
    
    # Save destination 1
    Write-Output "Saving DOCX to: $DocxDest1"
    $doc.SaveAs2($DocxDest1, 16) # 16 = wdFormatXMLDocument (.docx)
    
    # Save destination 2
    Write-Output "Saving DOCX to: $DocxDest2"
    $doc.SaveAs2($DocxDest2, 16)
    
    $doc.Close()
    Write-Output "Conversion successfully completed!"
}
finally {
    $word.Quit()
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($word) | Out-Null
    Remove-Item $tempHtml -ErrorAction SilentlyContinue
}
