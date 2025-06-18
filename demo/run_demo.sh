#!/bin/bash

# Claude Knowledge Catalyst Demo Manager
# Central script to run and manage all demos

DEMO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

show_help() {
    echo "🎯 Claude Knowledge Catalyst Demo Manager"
    echo "========================================"
    echo ""
    echo "Centralized demo management for all CKC demonstrations."
    echo ""
    echo "Usage: $0 [COMMAND] [OPTIONS]"
    echo ""
    echo "Commands:"
    echo "  user        Run main user experience demo (recommended for new users)"
    echo "  quick       Run quick development demo (fast feature overview)"
    echo "  multi       Run multi-team development workflow demo"
    echo "  cleanup     Clean up all demo files and directories"
    echo "  status      Show current demo environment status"
    echo "  help        Show this help message"
    echo ""
    echo "Options:"
    echo "  --force     Skip confirmation prompts (for cleanup command)"
    echo ""
    echo "Examples:"
    echo "  $0 user              # Full user experience demo"
    echo "  $0 quick             # Fast developer demo"
    echo "  $0 multi             # Multi-team workflow demo"
    echo "  $0 cleanup           # Clean up with confirmation"
    echo "  $0 cleanup --force   # Clean up without confirmation"
    echo "  $0 status            # Check demo environment status"
    echo ""
    echo "🔍 Available Demos:"
    echo "  👤 user:  Complete user journey with modern hybrid structure"
    echo "  ⚡ quick: Fast feature demonstration for developers"
    echo "  👥 multi: Multi-team development workflow with shared vault"
}

show_status() {
    echo "📊 Demo Status"
    echo "=============="
    echo ""
    
    # Count demo directories (updated for current naming)
    DEMO_DIRS=(
        "quick_test" "test_vault"
        "my_project" "my_obsidian_vault"
        "frontend_team" "backend_team" "shared_vault"
        "demo_project" "demo_vault"
    )
    
    FOUND_DIRS=()
    for dir in "${DEMO_DIRS[@]}"; do
        if [[ -d "$DEMO_DIR/$dir" ]]; then
            FOUND_DIRS+=("$dir")
        fi
    done
    
    if [[ ${#FOUND_DIRS[@]} -eq 0 ]]; then
        echo "✨ Demo directory is clean"
        echo "📂 No demo files found"
    else
        echo "📂 Found ${#FOUND_DIRS[@]} demo directories:"
        for dir in "${FOUND_DIRS[@]}"; do
            SIZE=$(du -sh "$DEMO_DIR/$dir" 2>/dev/null | cut -f1)
            echo "  📁 $dir ($SIZE)"
        done
    fi
    
    echo ""
    echo "📄 Available demo scripts:"
    if [[ -f "$DEMO_DIR/demo.sh" ]]; then
        echo "  👤 demo.sh - User experience demo"
    fi
    if [[ -f "$DEMO_DIR/quick_demo.sh" ]]; then
        echo "  ⚡ quick_demo.sh - Quick development demo"
    fi
    if [[ -f "$DEMO_DIR/multi_project_demo.sh" ]]; then
        echo "  👥 multi_project_demo.sh - Multi-team workflow demo"
    fi
    if [[ -f "$DEMO_DIR/cleanup.sh" ]]; then
        echo "  🧹 cleanup.sh - Demo cleanup utility"
    fi
}

run_user_demo() {
    echo "🎯 Running User Experience Demo..."
    echo "Complete demonstration of Claude Knowledge Catalyst features"
    echo ""
    if [[ -f "$DEMO_DIR/demo.sh" ]]; then
        "$DEMO_DIR/demo.sh"
    else
        echo "❌ demo.sh not found"
        echo "Make sure you're running this from the demo directory"
        exit 1
    fi
}

run_quick_demo() {
    echo "⚡ Running Quick Development Demo..."
    echo "Fast demonstration of core CKC features for developers"
    echo ""
    if [[ -f "$DEMO_DIR/quick_demo.sh" ]]; then
        "$DEMO_DIR/quick_demo.sh"
    else
        echo "❌ quick_demo.sh not found"
        echo "Make sure you're running this from the demo directory"
        exit 1
    fi
}

run_multi_demo() {
    echo "👥 Running Multi-Team Development Workflow Demo..."
    echo "Demonstrates how multiple teams can share a knowledge vault"
    echo ""
    if [[ -f "$DEMO_DIR/multi_project_demo.sh" ]]; then
        "$DEMO_DIR/multi_project_demo.sh"
    else
        echo "❌ multi_project_demo.sh not found"
        echo "Make sure you're running this from the demo directory"
        exit 1
    fi
}

run_cleanup() {
    local force_flag=""
    if [[ "$2" == "--force" || "$2" == "-f" ]]; then
        force_flag="--force"
    fi
    
    echo "🧹 Running Demo Cleanup..."
    echo "Removing all demo files and directories"
    echo ""
    if [[ -f "$DEMO_DIR/cleanup.sh" ]]; then
        "$DEMO_DIR/cleanup.sh" $force_flag
    else
        echo "❌ cleanup.sh not found"
        echo "Make sure you're running this from the demo directory"
        exit 1
    fi
}

# Main logic
case "$1" in
    "user")
        run_user_demo
        ;;
    "quick")
        run_quick_demo
        ;;
    "multi")
        run_multi_demo
        ;;
    "cleanup")
        run_cleanup "$@"
        ;;
    "status")
        show_status
        ;;
    "help"|"--help"|"-h"|"")
        show_help
        ;;
    *)
        echo "❌ Unknown command: '$1'"
        echo ""
        echo "Use '$0 help' to see available commands."
        echo ""
        show_help
        exit 1
        ;;
esac