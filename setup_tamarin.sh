#!/bin/bash
# Complete Tamarin Prover Setup Script - Option 3

set -e  # Exit on any error

echo "🚀 Starting Tamarin Prover Setup (Option 3)..."

# Step 1: Navigate to directory
cd ~/Desktop/tatou-team2/tamarin-prover
echo "📁 Working in: $(pwd)"

# Step 2: Backup existing configuration
if [ -f "cabal.project" ]; then
    cp cabal.project cabal.project.backup
    echo "✅ Backed up existing cabal.project"
fi

# Step 3: Create cabal.project
echo "📝 Creating cabal.project configuration..."
cat > cabal.project << 'EOF'
packages: .

-- Allow newer dependencies to resolve version conflicts
allow-newer: *

-- Explicit package versions if available
constraints:
  tamarin-prover-utils ==1.11.0

-- Optimization flags
optimization: 2

-- Parallel builds
jobs: $ncpus
