# fetch_docs.ps1 - GitHub 文档下载器
# 使用 Git Sparse Checkout 高效下载指定目录，自动过滤非 MD/MDX 文件

param(
    [Parameter(Mandatory = $true)]
    [string]$Repo,
    
    [string]$DocsPath = "docs",
    
    [Parameter(Mandatory = $true)]
    [string]$OutputDir,
    
    [switch]$KeepGit = $false
)

$ErrorActionPreference = "Stop"

# 构建 GitHub URL
$RepoUrl = "https://github.com/$Repo.git"

Write-Host "========================================"
Write-Host " GitHub 文档下载器"
Write-Host "========================================"
Write-Host ""
Write-Host "仓库: $Repo"
Write-Host "文档路径: $DocsPath"
Write-Host "输出目录: $OutputDir"
Write-Host ""

# 检查 git 是否可用
$gitVersion = git --version
if (-not $gitVersion) {
    Write-Error "错误: Git 未安装或不在 PATH 中"
    exit 1
}

# 创建临时目录
$timestamp = Get-Date -Format 'yyyyMMddHHmmss'
$TempDir = Join-Path $env:TEMP "github-docs-$timestamp"
Write-Host "[1/5] 创建临时目录: $TempDir"

# Sparse Checkout 克隆
Write-Host "[2/5] 执行 Sparse Checkout..."
$cloneResult = git clone --filter=blob:none --sparse $RepoUrl $TempDir 2>&1
Push-Location $TempDir
$sparseResult = git sparse-checkout set $DocsPath 2>&1
Pop-Location

# 检查 docs 目录是否存在
$SourceDocsDir = Join-Path $TempDir $DocsPath
if (-not (Test-Path $SourceDocsDir)) {
    Write-Error "错误: 仓库中不存在 '$DocsPath' 目录"
    Remove-Item $TempDir -Recurse -Force -ErrorAction SilentlyContinue
    exit 1
}

# 创建输出目录
Write-Host "[3/5] 准备输出目录: $OutputDir"
if (Test-Path $OutputDir) {
    Remove-Item $OutputDir -Recurse -Force
}
New-Item -ItemType Directory -Path $OutputDir -Force | Out-Null

# 复制文件（只保留 .md 和 .mdx）
Write-Host "[4/5] 复制并过滤 Markdown 文件..."
$mdFiles = Get-ChildItem $SourceDocsDir -Recurse -File | Where-Object { $_.Extension -in @('.md', '.mdx') }

$fileCount = 0
foreach ($file in $mdFiles) {
    # 计算相对路径
    $relativePath = $file.FullName.Substring($SourceDocsDir.Length + 1)
    $destPath = Join-Path $OutputDir $relativePath
    
    # 确保目标目录存在
    $destDir = Split-Path $destPath -Parent
    if (-not (Test-Path $destDir)) {
        New-Item -ItemType Directory -Path $destDir -Force | Out-Null
    }
    
    # 复制文件
    Copy-Item $file.FullName $destPath
    $fileCount++
}

Write-Host "  已复制 $fileCount 个 Markdown 文件"

# 清理临时目录
Write-Host "[5/5] 清理临时文件..."
Remove-Item $TempDir -Recurse -Force -ErrorAction SilentlyContinue

# 生成索引
$indexPath = Join-Path $OutputDir "_index.md"
$now = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'

$indexContent = "# 文档索引`n`n"
$indexContent += "> 自动生成于 $now`n"
$indexContent += "> 来源: https://github.com/$Repo`n`n"
$indexContent += "## 统计`n`n"
$indexContent += "- 总文件数: $fileCount`n"
$indexContent += "- 来源目录: $DocsPath`n`n"
$indexContent += "## 文件列表`n"

$allFiles = Get-ChildItem $OutputDir -Recurse -File | Where-Object { $_.Extension -in @('.md', '.mdx') -and $_.Name -ne "_index.md" } | Sort-Object DirectoryName, Name

$currentDir = ""
foreach ($file in $allFiles) {
    $relativePath = $file.FullName.Substring($OutputDir.Length + 1)
    $dir = Split-Path $relativePath -Parent
    
    if ($dir -ne $currentDir) {
        $currentDir = $dir
        if ($dir) {
            $indexContent += "`n### $dir`n`n"
        }
        else {
            $indexContent += "`n### 根目录`n`n"
        }
    }
    
    $indexContent += "- [$($file.BaseName)]($relativePath)`n"
}

Set-Content -Path $indexPath -Value $indexContent -Encoding UTF8

Write-Host ""
Write-Host "========================================"
Write-Host " 下载完成!"
Write-Host "========================================"
Write-Host ""
Write-Host "输出目录: $OutputDir"
Write-Host "文件数量: $fileCount"
Write-Host "索引文件: $indexPath"
Write-Host ""
