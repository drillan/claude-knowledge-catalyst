#!/bin/bash

# Claude Knowledge Catalyst Demo Cleanup Script
# デモで生成されたすべてのファイルとディレクトリを削除

set -e

# Dynamic path detection (portable across environments)
DEMO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "🧹 Claude Knowledge Catalyst Demo Cleanup"
echo "========================================"
echo ""
echo "⚠️  This will remove ALL demo-generated artifacts:"
echo "   • Main demo artifacts (my_project/, my_vault/)"
echo "   • Tag-centered migration demo (obsidian_vault/, enhanced_ckc_vault/, ckc_project/)"
echo "   • Multi-team demo (frontend_team/, backend_team/, shared_vault/)"
echo ""

# Confirmation prompt
read -p "Are you sure you want to proceed? [y/N]: " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cleanup cancelled."
    exit 0
fi

echo ""
echo "🗑️  Removing demo artifacts..."

# Main demo artifacts (demo.sh)
if [ -d "$DEMO_DIR/my_project" ]; then
    echo "   Removing my_project/"
    rm -rf "$DEMO_DIR/my_project"
fi

if [ -d "$DEMO_DIR/my_vault" ]; then
    echo "   Removing my_vault/"
    rm -rf "$DEMO_DIR/my_vault"
fi

# Tag-centered migration demo artifacts (tag_centered_demo.sh)
if [ -d "$DEMO_DIR/obsidian_vault" ]; then
    echo "   Removing obsidian_vault/"
    rm -rf "$DEMO_DIR/obsidian_vault"
fi

if [ -d "$DEMO_DIR/enhanced_ckc_vault" ]; then
    echo "   Removing enhanced_ckc_vault/"
    rm -rf "$DEMO_DIR/enhanced_ckc_vault"
fi

if [ -d "$DEMO_DIR/ckc_project" ]; then
    echo "   Removing ckc_project/"
    rm -rf "$DEMO_DIR/ckc_project"
fi

# Multi-team demo artifacts (multi_project_demo.sh)
if [ -d "$DEMO_DIR/frontend_team" ]; then
    echo "   Removing frontend_team/"
    rm -rf "$DEMO_DIR/frontend_team"
fi

if [ -d "$DEMO_DIR/backend_team" ]; then
    echo "   Removing backend_team/"
    rm -rf "$DEMO_DIR/backend_team"
fi

if [ -d "$DEMO_DIR/shared_vault" ]; then
    echo "   Removing shared_vault/"
    rm -rf "$DEMO_DIR/shared_vault"
fi

# Remove any leftover temporary files
if [ -f "$DEMO_DIR/migration_report.md" ]; then
    echo "   Removing migration_report.md"
    rm -f "$DEMO_DIR/migration_report.md"
fi

# Remove any log files or temporary artifacts
find "$DEMO_DIR" -name "*.log" -type f -exec rm -f {} \; 2>/dev/null || true
find "$DEMO_DIR" -name "*.tmp" -type f -exec rm -f {} \; 2>/dev/null || true
find "$DEMO_DIR" -name ".DS_Store" -type f -exec rm -f {} \; 2>/dev/null || true

echo ""
echo "✅ Cleanup complete!"
echo ""
echo "📁 Remaining demo files:"
echo "   • demo.sh - Main pure tag-centered demo"
echo "   • tag_centered_demo.sh - Migration experience demo"
echo "   • multi_project_demo.sh - Multi-team collaboration demo"
echo "   • README.md - Demo documentation"
echo "   • cleanup.sh - This cleanup script"
echo ""
echo "🚀 Ready to run demos again with clean environment!"
echo "   Run './demo/demo.sh' to start fresh"
