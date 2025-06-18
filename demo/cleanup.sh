#!/bin/bash

# Claude Knowledge Catalyst Demo Cleanup Script
# Removes all demo-generated files and directories

DEMO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "🧹 Claude Knowledge Catalyst Demo Cleanup"
echo "========================================="
echo ""

# List what will be cleaned up
echo "📂 Scanning for demo files..."
echo ""

ITEMS_TO_CLEAN=()

# Check for demo directories (current and legacy names)
# Current demo directories
DEMO_DIRS=(
    "quick_test" "test_vault"                    # quick_demo.sh
    "my_project" "my_obsidian_vault"             # demo.sh
    "frontend_team" "backend_team" "shared_vault" # multi_project_demo.sh
    # Legacy directories (for backward compatibility)
    "demo_project" "demo_vault"
    "my_modern_vault" "user_project" "user_vault"
    "project_A" "project_B" "vault"
    "test_modern" "test_modern2"
)

for dir in "${DEMO_DIRS[@]}"; do
    if [[ -d "$DEMO_DIR/$dir" ]]; then
        ITEMS_TO_CLEAN+=("$dir/")
    fi
done

# Also check for any ckc_config.yaml files in demo subdirectories
for config_file in "$DEMO_DIR"/*/ckc_config.yaml; do
    if [[ -f "$config_file" ]]; then
        parent_dir=$(basename "$(dirname "$config_file")")
        # Add to cleanup list if not already included
        if [[ ! " ${ITEMS_TO_CLEAN[*]} " =~ " ${parent_dir}/ " ]]; then
            ITEMS_TO_CLEAN+=("$parent_dir/")
        fi
    fi
done

# Check if there's anything to clean
if [[ ${#ITEMS_TO_CLEAN[@]} -eq 0 ]]; then
    echo "✨ Demo directory is already clean!"
    echo "No demo files found to remove."
    exit 0
fi

# Show what will be removed
echo "🗑️  The following demo files will be removed:"
for item in "${ITEMS_TO_CLEAN[@]}"; do
    echo "  - $item"
done

echo ""

# Confirm with user (unless --force flag is used)
if [[ "$1" != "--force" && "$1" != "-f" ]]; then
    echo "⚠️  This will permanently delete all demo data."
    echo ""
    read -p "Are you sure you want to continue? (y/N): " -n 1 -r
    echo ""
    
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "❌ Cleanup cancelled."
        exit 0
    fi
    echo ""
fi

# Perform cleanup
echo "🧹 Cleaning up demo files..."
echo ""

CLEANED_COUNT=0
for item in "${ITEMS_TO_CLEAN[@]}"; do
    FULL_PATH="$DEMO_DIR/$item"
    if [[ -d "$FULL_PATH" ]]; then
        echo "  🗑️  Removing $item"
        rm -rf "$FULL_PATH"
        CLEANED_COUNT=$((CLEANED_COUNT + 1))
    fi
done

echo ""
echo "✅ Cleanup complete!"
echo "📊 Removed $CLEANED_COUNT demo directories"
echo ""

# Show remaining files (excluding scripts and README)
echo "📂 Remaining files in demo directory:"
find "$DEMO_DIR" -maxdepth 1 -type f -name "*.sh" -o -name "*.md" | sort | while read -r file; do
    echo "  📄 $(basename "$file")"
done

echo ""
echo "💡 Demo scripts are preserved and ready for next use"
echo ""
echo "🚀 To run demos again:"
echo "  ./demo/demo.sh                     # User experience demo (recommended)"
echo "  ./demo/quick_demo.sh              # Quick development demo"
echo "  ./demo/multi_project_demo.sh      # Multi-team workflow demo"
echo "  ./demo/run_demo.sh help           # Show all available demos"