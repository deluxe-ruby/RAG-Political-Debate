# bash_helpers.sh — helper commands for WISHES dev

# Reopen this file in the Cloud Shell Editor
alias wishes_edit="cloudshell edit ~/wishes/bash_helpers.sh"

# Show helpful development commands
wishes_help() {
  echo ""
  echo "🌟 WISHES Project Bash Helper 🌟"
  echo "----------------------------------"
  echo "📁 Navigate to project:      cd ~/wishes"
  echo "🚀 Start Flask dev server:   ./flask_start.sh"
  echo "🐍 Activate venv:            source venv/bin/activate"
  echo "⬆️  Push to GitHub:          git push origin main"
  echo "📝 Edit helper file:         wishes_edit"
  echo "❓ Show this menu:           wishes_help"
  echo ""
}
