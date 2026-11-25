#!/usr/bin/env pwsh
# agentic-harness-seo manual-install uninstaller (Windows)
#
# Removes the orchestrator skill (~/.claude/skills/harness-seo), all sub-skills
# (~/.claude/skills/seo-*), and all sub-agents (~/.claude/agents/seo-*.md).
#
# Uses glob enumeration rather than a hardcoded list so future skill
# additions are cleaned up automatically without releasing a new
# uninstaller.
#
# Plugin-install users should use Claude Code's own command instead:
#   /plugin uninstall agentic-harness-seo@zafajardo9-agentic-harness-seo
#   /plugin marketplace remove zafajardo9/agentic-harness-seo

$ErrorActionPreference = "Stop"

function Write-Color($Color, $Text) {
    Write-Host $Text -ForegroundColor $Color
}

function Main {
    $SkillDir = Join-Path (Join-Path $env:USERPROFILE ".claude") "skills"
    $AgentDir = Join-Path (Join-Path $env:USERPROFILE ".claude") "agents"

    Write-Color Cyan "=== Uninstalling agentic-harness-seo ==="
    Write-Host ""

    $removedSkills = 0
    $removedAgents = 0

    # Remove orchestrator if present
    $orchestratorPath = Join-Path $SkillDir "harness-seo"
    if (Test-Path $orchestratorPath -PathType Container) {
        Remove-Item -Recurse -Force $orchestratorPath
        Write-Color Green "  Removed: $orchestratorPath"
        $removedSkills++
    }

    # Remove every seo-* sub-skill directory
    if (Test-Path $SkillDir -PathType Container) {
        foreach ($subSkill in @(Get-ChildItem -Path $SkillDir -Directory -Filter "seo-*" -ErrorAction SilentlyContinue)) {
            Remove-Item -Recurse -Force $subSkill.FullName
            Write-Color Green "  Removed: $($subSkill.FullName)"
            $removedSkills++
        }
    }

    # Remove every seo-*.md agent file
    if (Test-Path $AgentDir -PathType Container) {
        foreach ($agentFile in @(Get-ChildItem -Path $AgentDir -File -Filter "seo-*.md" -ErrorAction SilentlyContinue)) {
            Remove-Item -Force $agentFile.FullName
            Write-Color Green "  Removed: $($agentFile.FullName)"
            $removedAgents++
        }
    }

    Write-Host ""
    if ($removedSkills -eq 0 -and $removedAgents -eq 0) {
        Write-Color Yellow "Nothing to remove. Agentic Harness SEO does not appear to be installed."
        Write-Color Yellow "If you installed via /plugin install, run /plugin uninstall instead."
        return
    }

    Write-Color Cyan "=== agentic-harness-seo uninstalled ($removedSkills skill dirs, $removedAgents agent files) ==="
    Write-Host ""
    Write-Color Yellow "Restart Claude Code to complete removal."
}

Main
