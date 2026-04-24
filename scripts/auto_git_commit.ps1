# Move to the project directory
Set-Location -Path "D:\skbc"

# Get current date for the commit message
$currentDate = Get-Date -Format "yyyy-MM-dd"

# Check for changes (staged, unstaged, and untracked)
$changes = git status --porcelain

if ($changes) {
    Write-Host "Changes detected. Proceeding with automated commit..." -ForegroundColor Cyan
    
    # Stage all changes
    git add .
    
    # Commit using Conventional Commits syntax
    # Type 'chore' is used for routine maintenance/automated tasks
    git commit -m "chore: automated progress update for $currentDate"
    
    # Optional: Push to remote if configured
    # git push origin main
    
    Write-Host "Progress for $currentDate has been committed successfully!" -ForegroundColor Green
} else {
    Write-Host "No changes detected for $currentDate. Skipping commit." -ForegroundColor Yellow
}
