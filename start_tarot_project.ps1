# Tarot Deck Creation System - One-Click Startup (PowerShell Script)

# Set paths
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$sdPath = "C:\Users\kjfsw\sd-scripts"
$webuiUserPath = Join-Path $sdPath "webui-user.bat"

# Function to show colorful messages
function Write-ColorOutput($ForegroundColor) {
    $fc = $host.UI.RawUI.ForegroundColor
    $host.UI.RawUI.ForegroundColor = $ForegroundColor
    if ($args) {
        Write-Output $args
    }
    $host.UI.RawUI.ForegroundColor = $fc
}

# Show header
Write-ColorOutput Green "Tarot Deck Creation System - One-Click Startup"
Write-ColorOutput Green "==========================================="
Write-Output ""

# Step 1: Check for running Automatic1111 instances
Write-ColorOutput Cyan "Step 1: Checking for running Automatic1111 instances..."
Write-Output ""

# Check if the API is already accessible (meaning an instance is running)
$apiAlreadyRunning = $false
try {
    $response = Invoke-WebRequest -Uri "http://127.0.0.1:7860/sdapi/v1/sd-models" -TimeoutSec 2 -ErrorAction SilentlyContinue
    if ($response.StatusCode -eq 200) {
        Write-ColorOutput Green "Automatic1111 API is already accessible."
        Write-Output "Using the existing instance running in Chrome."
        $apiAlreadyRunning = $true
    }
} catch {
    Write-Output "No accessible Automatic1111 API found."
    $apiAlreadyRunning = $false
}

if (-not $apiAlreadyRunning) {
    # Ask user if they want to close any running instances
    Write-Output ""
    $closeInstances = Read-Host "Would you like to close any running Automatic1111 instances? (Y/N)"

    if ($closeInstances -eq "Y" -or $closeInstances -eq "y") {
        Write-Output "Closing running Automatic1111 instances..."

        # Find and kill any running Automatic1111 processes
        $a1111Processes = Get-Process | Where-Object { $_.CommandLine -like "*webui.py*" -or $_.CommandLine -like "*sd-scripts*" }
        if ($a1111Processes) {
            Write-Output "Found running Automatic1111 instances. Terminating..."
            foreach ($process in $a1111Processes) {
                try {
                    Stop-Process -Id $process.Id -Force
                    Write-Output "Terminated process: $($process.Id)"
                } catch {
                    Write-ColorOutput Yellow "Warning: Could not terminate process $($process.Id): $_"
                }
            }
            Write-Output "Automatic1111 processes terminated."
            # Wait a moment to ensure processes are fully terminated
            Start-Sleep -Seconds 2
        } else {
            Write-Output "No running Automatic1111 command-line instances found."
        }
    } else {
        Write-Output "Keeping any running Automatic1111 instances."
    }
}

# Step 2: Install dependencies
Write-Output ""
Write-ColorOutput Cyan "Step 2: Installing dependencies..."
Write-Output ""

# Change to script directory
Set-Location $scriptPath

# Run install_dependencies.bat
$installProcess = Start-Process -FilePath "cmd.exe" -ArgumentList "/c install_dependencies.bat" -Wait -PassThru
if ($installProcess.ExitCode -ne 0) {
    Write-ColorOutput Red "Error: Dependencies installation failed."
    Write-Output "Press any key to exit..."
    $null = $host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit
}

# Create necessary directories for prompt refiner
Write-Output "Creating necessary directories..."
Start-Process -FilePath "python" -ArgumentList "create_directory_structure.py" -Wait

# Setup style templates for prompt refiner
Write-Output "Setting up style templates..."
Start-Process -FilePath "python" -ArgumentList "setup_style_templates.py" -Wait

# Setup tarot reference database
Write-Output "Setting up tarot reference database..."
Start-Process -FilePath "python" -ArgumentList "setup_tarot_reference_db.py" -Wait

Write-Output ""
Write-ColorOutput Cyan "Step 2.5: Installing enhanced dependencies and plugins..."
Write-Output ""

# Ask if user wants to install enhanced dependencies
$installDeps = Read-Host "Would you like to install enhanced dependencies for advanced features? (Y/N, default: N)"

if ($installDeps -eq "Y" -or $installDeps -eq "y") {
    Write-Output "Installing enhanced dependencies..."
    Start-Process -FilePath "python" -ArgumentList "install_enhanced_dependencies.py --all" -Wait
} else {
    Write-Output "Skipping enhanced dependencies installation."
}

# Ask if user wants to install Automatic1111 plugins
$installPlugins = Read-Host "Would you like to install recommended Automatic1111 plugins? (Y/N, default: N)"

if ($installPlugins -eq "Y" -or $installPlugins -eq "y") {
    Write-Output "Installing Automatic1111 plugins..."
    Start-Process -FilePath "python" -ArgumentList "install_a1111_plugins.py" -Wait
} else {
    Write-Output "Skipping Automatic1111 plugins installation."
}

# Step 3: Check Automatic1111 configuration
Write-Output ""
Write-ColorOutput Cyan "Step 3: Checking Automatic1111 configuration..."
Write-Output ""

# Check if webui-user.bat exists
if (-not (Test-Path $webuiUserPath)) {
    Write-ColorOutput Red "ERROR: webui-user.bat not found at $webuiUserPath"
    Write-ColorOutput Red "Please make sure Automatic1111 is installed correctly."
    Write-Output "Press any key to exit..."
    $null = $host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit
}

# Check if API is enabled in webui-user.bat
$webuiUserContent = Get-Content $webuiUserPath -Raw
if ($webuiUserContent -notlike "*--api*") {
    Write-Output "API not enabled in webui-user.bat. Adding --api flag..."

    # Backup original file
    Copy-Item $webuiUserPath "$webuiUserPath.bak"

    # Add --api flag to COMMANDLINE_ARGS
    $newContent = $webuiUserContent -replace 'set COMMANDLINE_ARGS=', 'set COMMANDLINE_ARGS=--api '
    Set-Content -Path $webuiUserPath -Value $newContent

    Write-Output "API flag added to webui-user.bat."
} else {
    Write-Output "API is already enabled in webui-user.bat."
}

# Step 4: Ensure Automatic1111 is running with API enabled
Write-Output ""
Write-ColorOutput Cyan "Step 4: Ensuring Automatic1111 is running with API enabled..."
Write-Output ""

if ($apiAlreadyRunning) {
    Write-ColorOutput Green "Using existing Automatic1111 instance running in Chrome."
    Write-Output "API is already accessible at http://127.0.0.1:7860"
    $apiReady = $true
} else {
    # Start Automatic1111 in a new window
    Write-Output "Starting Automatic1111 in a new window..."
    Start-Process -FilePath "cmd.exe" -ArgumentList "/c cd /d $sdPath && call webui.bat" -PassThru

    Write-Output "Waiting for Automatic1111 to start..."
    Write-Output "This may take a minute or two..."

    # Wait for the API to become available
    $maxAttempts = 30
    $attempt = 0
    $apiReady = $false

    while ($attempt -lt $maxAttempts -and -not $apiReady) {
        $attempt++
        Write-Output "Checking API (attempt $attempt of $maxAttempts)..."
        Start-Sleep -Seconds 5

        # Check if API is responding
        try {
            $response = Invoke-WebRequest -Uri "http://127.0.0.1:7860/sdapi/v1/sd-models" -TimeoutSec 2 -ErrorAction SilentlyContinue
            if ($response.StatusCode -eq 200) {
                $apiReady = $true
            }
        } catch {
            # API not ready yet
        }
    }

    if ($apiReady) {
        Write-Output ""
        Write-ColorOutput Green "Automatic1111 API is ready!"
    } else {
        Write-Output ""
        Write-ColorOutput Yellow "WARNING: Automatic1111 API did not respond within the expected time."
        Write-ColorOutput Yellow "The process will continue, but you may need to check if Automatic1111 is running correctly."
    }
}

# Step 5: Start Tarot Deck Creation System
Write-Output ""
Write-ColorOutput Cyan "Step 5: Starting Tarot Deck Creation System..."
Write-Output ""

# Start the Tarot Master Control Panel
Start-Process -FilePath "cmd.exe" -ArgumentList "/c call tarot_master.bat"

Write-Output ""
Write-ColorOutput Green "Tarot Deck Creation System has been started!"
Write-Output ""
Write-Output "You can now:"
Write-Output "1. Use the Master Control Panel to create your tarot deck"
Write-Output "2. Follow the step-by-step process from reference images to final cards"
Write-Output "3. Check the Automatic1111 interface at http://127.0.0.1:7860 if needed"
Write-Output ""
Write-Output "Press any key to exit this startup script..."
$null = $host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
