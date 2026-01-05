# ShiroInk Usability Enhancement Plan v2.1

**Status**: Formal Decision Document  
**Date Created**: 2026-01-05  
**Last Updated**: 2026-01-05  
**Phase**: Planning Complete, Ready for Phase 1 Implementation  

---

## Executive Summary

ShiroInk usability enhancement plan focused on **CLI-first improvements** without web interface. 
Two deployment options: Python native (pip) + Docker. Phased approach (3 phases) with incremental 
releases. No hard deadlines.

**Total Effort**: ~6-8 weeks across 3 phases  
**Architecture**: Fully backward compatible, zero breaking changes

---

## Part 1: Critical Decisions (13 Questions Resolved)

### Decision 1: Wizard Activation Strategy
**Question**: When user runs `shiroink` without arguments?  
**Decision**: **Opzione C - Wizard Opzionale con Prompt**
```
Behavior:
  $ shiroink
  → Chiede: "First time? Run interactive setup? (y/n)"
  → Se Y: lancia wizard
  → Se N: mostra help sommario
```
**Rationale**: Bilancia guidance per nuovi utenti + flessibilità per power users

---

### Decision 2: Profile Storage Location & Format
**Question**: Dove salvare profili (config riutilizzabili)?  
**Decision**: **JSON in ~/.config/shiroink/profiles/ (cross-platform POSIX)**
```
Structure:
  Linux/macOS:   ~/.config/shiroink/profiles/my_profile.json
  Windows:       %APPDATA%\shiroink\profiles\my_profile.json
  
Format:
{
  "name": "my_manga_kobo",
  "device": "kobo_libra_2",
  "rtl": true,
  "quality": 8,
  "workers": 4,
  "description": "Manga giapponese per Kobo",
  "created": "2026-01-05T10:30:00Z",
  "last_used": "2026-01-05T15:45:00Z"
}
```
**Rationale**: 
- Zero dipendenze aggiuntive (JSON è built-in)
- POSIX-compliant cross-platform
- XDG Base Directory specification respected
- Leggibile e editabile manualmente

---

### Decision 3: Entry Point Installation (pip)
**Question**: Quale comando dopo `pip install shiroink`?  
**Decision**: **`shiroink` command diretto**
```
Usage:
  $ shiroink --wizard
  $ shiroink manga/ output/ --device kobo_libra_2
  $ shiroink --list-devices
```
**Rationale**: 
- Standard di fatto per CLI tools Python
- Intuitivo e semplice
- Conflitti improbabili
- `python -m shiroink` rimane come fallback

---

### Decision 4: Error Messages & Localization
**Question**: Quale lingua per messaggi d'errore?  
**Decision**: **Inglese di default + architettura per localization (i18n)**
```
Implementation:
  - Default: English only (for now)
  - Structure: locales/en.json, locales/it.json, etc.
  - Phase 2: Aggiungeremo Italian translations
  - Future: Scalabile per altre lingue
```
**Rationale**:
- Open source standard (English-first)
- Riduce manutenzione iniziale
- Architettura ready per localization
- Community contributions più semplici

---

### Decision 5: Error Message Verbosity
**Question**: Quanto dettagliati gli errori?  
**Decision**: **Conciso default + `--verbose` flag per dettagli**
```
Default (conciso):
  $ shiroink manga/ output/ -r 50x50
  ❌ Invalid resolution: 50x50 (minimum: 200x200)
  📖 shiroink --help

Con --verbose:
  $ shiroink manga/ output/ -r 50x50 --verbose
  ❌ Invalid resolution: 50x50
     Reason: Resolution too small for e-reader
  💡 Suggestions:
     • Minimum: 200x200
     • Try: --list-devices
  📖 Full docs: ...
```
**Rationale**: Power users non disturbati, novizi hanno help disponibile

---

### Decision 6: Help Output Style
**Question**: Come formattare `--help` output?  
**Decision**: **Rich Library (enhanced, visuale, organizzato)**
```
Style:
  - Colori e box graphics
  - Organizzato per categorie (Essential, Advanced, etc.)
  - Esempi pratici inclusi
  - Links a documentazione
  - Facilmente leggibile
```
**Rationale**: 
- Rich già in requirements.txt
- Accogliente per nuovi utenti
- Non overkill, è built-in Python standard

---

### Decision 7: Wizard Language & Default
**Question**: Quale lingua nel wizard interattivo?  
**Decision**: **Auto-detect da locale sistema + fallback menu + env var override**
```
Priority:
  1. Auto-detect da $LANG, $LOCALE, or Windows locale settings
  2. Se ambiguo/non rilevato → mostra menu linguistico
  3. User seleziona → salva in ~/.config/shiroink/config.json
  4. Override: SHIROINK_LANG=it shiroink
```
**Rationale**: 
- Massima UX per utenti locali
- Zero configurazione per chi ha locale impostato
- Fallback menu è discoverable
- Power users hanno env var override

---

### Decision 8: Docker Integration Strategy
**Question**: Come funziona wizard con Docker?  
**Decision**: **Docker usa CLI standard + documentazione separata (no duplicate logic)**
```
Behavior:
  - Docker container ha STESSI comandi di Python native
  - Wizard funziona con -it flags (TTY interactive)
  - Docs separate spiegano best practices
  
Example:
  docker run --rm -it ghcr.io/esoso/shiroink --wizard
  docker run --rm -it -v ~/.config/shiroink:/root/.config/shiroink \
    ghcr.io/esoso/shiroink --profile my_manga
```
**Rationale**: 
- Zero logica duplicata
- Docker è "just a container", stessi comandi
- Documentazione centralizzata
- Manutenzione più semplice

---

### Decision 9: Profile Auto-Suggestion
**Question**: Suggerire di salvare config come profilo?  
**Decision**: **Suggestion semplice al completamento (non invasivo)**
```
Output:
  ✓ Processing complete: 150 files in 8 minuti
  ✓ Output: /home/user/output/
  
  💡 Tip: Save this configuration as profile for next time?
     shiroink --save-profile my_manga_kobo
     
     Then reuse: shiroink manga/ output/ --profile my_manga_kobo
```
**Rationale**: Educational, discoverable, non obbligatorio, non noisy

---

### Decision 10: Dry-Run Mode Behavior
**Question**: Cosa mostra `--dry-run`?  
**Decision**: **Preview dettagliato + menu interattivo con opzioni**
```
Flow:
  1. Mostra configurazione completa
  2. Analizza input (file count, formati, etc.)
  3. Mostra estimate (tempo, size, processing plan)
  4. Offers menu:
     [y] Yes, start processing
     [n] No, abort
     [m] Modify configuration (ritorna al wizard)
     [s] Save as profile before proceeding
```
**Rationale**: Massimo controllo utente, non richiede redigitare comando

---

### Decision 11: Configuration File Support
**Question**: Supportare file config (TOML/JSON)?  
**Decision**: **No config file - Profiles sono sufficienti**
```
Reasoning:
  - Profiles già fanno il lavoro di salvare/riusare
  - Chi vuol file config → simple shell script
  - Se richiesto in futuro → aggiungeremo Opzione B (TOML)
  
Alternative per automation:
  #!/bin/bash
  # script.sh
  shiroink manga/ output/ --profile my_setup
```
**Rationale**: Keep it simple, evita complessità precedence rules

---

### Decision 12: Progress Reporting
**Question**: Come mostrare progresso durante elaborazione?  
**Decision**: **Enhanced progress dettagliato con ETA, velocità, file corrente**
```
Output:
  Processing: /home/user/manga/
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  
  [████████████░░░░░░░░░░░░░░░░░] 45%
  
  Files:       67 / 150 completed
  Time:        ⏱️  Elapsed: 6 min 32 sec | Remaining: ~8 min
  Speed:       10.3 files/min
  Current:     processing manga_page_045.jpg (250 KB)
  Success:     ✓ 67 | Failed: ✗ 0 | Skipped: ○ 0
  
  Estimated output size: ~45 MB (75% reduction)
```
**Rationale**: 
- Utente sa esattamente dov'è
- ETA utile per batch lunghi
- Feedback real-time su successi/errori
- Tranquillità (sistema sta lavorando, non appeso)

---

### Decision 13: Implementation Timeline
**Question**: Quale approccio: MVP veloce, complete solution, o phased?  
**Decision**: **Opzione C - Phased Approach (no hard deadlines)**

```
PHASE 1 (2-3 settimane): MVP - CORE IMPROVEMENTS
├─ Interactive Wizard
├─ Enhanced Help System (Rich format)
├─ Better Error Messages + --verbose
├─ Configuration Profiles (save/load/list/edit/delete)
└─ Output: +80% usabilità migliorata

PHASE 2 (2-3 settimane): EXPANSION - LOCALIZATION & PROGRESS
├─ Full Localization i18n infrastructure
├─ Italian translations (IT)
├─ Enhanced progress reporting (ETA, velocità, stats)
├─ Dry-run interattivo con menu modifiche
└─ Device/Pipeline discovery migliorato

PHASE 3 (1-2 settimane): POLISH - DOCS & TESTING
├─ Comprehensive Docker docs
├─ User guide per wizard & profiles
├─ Integration & E2E tests
├─ Release notes
└─ Polish UX edge cases
```

**Total Effort**: ~6-8 weeks  
**Approach**: Incremental, no hard deadlines  
**Releases**: One per phase (v2.1, v2.2, v2.3)

---

## Part 2: Implementation Structure

### Phase 1 Deliverables

#### New Files
```
src/
├── __main__.py                          # Entry point for `shiroink` command
├── interactive_wizard.py                # Wizard coordinator
├── wizard/
│   ├── __init__.py
│   ├── steps.py                         # Wizard step implementations
│   ├── prompts.py                       # Helper functions for user input
│   └── utils.py                         # Validation & helpers
├── parameter_validator.py               # Pro-active validation
├── profiles/
│   ├── __init__.py
│   ├── manager.py                       # Profile save/load/edit/delete
│   └── schema.py                        # Profile JSON schema validation
└── localization/
    ├── __init__.py
    ├── loader.py                        # Translation loader
    └── locales/
        └── en.json                      # English translations (structure ready)

docs/
├── guides/
│   ├── wizard.md                        # Wizard tutorial
│   ├── profiles.md                      # Profile management guide
│   └── quickstart.md                    # Update with wizard info

tests/
├── unit/
│   ├── test_wizard.py
│   ├── test_profiles.py
│   ├── test_error_messages.py
│   └── test_parameter_validator.py
```

#### Modified Files
```
src/
├── cli.py                               # Add --wizard, --profile, --list-profiles flags
├── main.py                              # Integrate wizard + profile loading
├── error_handler.py                     # Enhance with context-aware suggestions
├── progress_reporter.py                 # Keep as-is for now (enhance in Phase 2)

pyproject.toml                           # Add console_scripts entry points

tests/
├── unit/
│   └── test_cli.py                      # Update with new flags
```

### Phase 1 Key Features

**1. Interactive Wizard**
- Device selection (with descriptions)
- Format selection (LTR/RTL)
- Path selection (with validation)
- Quality selection (with recommendations)
- Performance selection (workers/threads)
- Review step with options
- Confirmation + abort/modify/save options

**2. Enhanced Help System**
- Rich formatted output
- Categorized options (Essential, Advanced, Configuration, Help)
- Practical examples
- Links to documentation
- Device/pipeline suggestions

**3. Better Error Messages**
- Concise by default
- Automatic typo suggestions
- `--verbose` for detailed explanations
- Localization-ready JSON structure

**4. Configuration Profiles**
- Save: `shiroink --save-profile NAME`
- Load: `shiroink --profile NAME`
- List: `shiroink --list-profiles` (with metadata)
- Edit: `shiroink --edit-profile NAME`
- Delete: `shiroink --delete-profile NAME`
- Auto-suggest after processing (non-invasive)

### Phase 2 Deliverables

#### New Files
```
src/
└── localization/
    └── locales/
        ├── it.json                      # Italian translations
        └── [future langs]

tests/
└── unit/
    ├── test_progress_reporter.py
    ├── test_dry_run_interactive.py
    └── test_localization.py

docs/
├── guides/
│   ├── localization.md
│   └── advanced-usage.md
```

#### Key Features
- Full i18n infrastructure (English + Italian)
- Enhanced progress reporting (ETA, speed, current file)
- Interactive dry-run with modification menu
- Device/pipeline discovery improvements

### Phase 3 Deliverables

#### New Files
```
docs/
├── guides/
│   ├── docker-advanced.md
│   ├── profiles-advanced.md
│   └── troubleshooting.md
├── architecture/
│   └── cli-design.md
└── RELEASE_NOTES_v2.1.md

tests/
├── integration/
│   ├── test_wizard_integration.py
│   ├── test_profiles_integration.py
│   └── test_docker_integration.py
└── e2e/
    └── test_complete_workflow.py
```

#### Key Activities
- Comprehensive documentation
- Integration & E2E testing
- Polish & edge cases
- Release & changelog

---

## Part 3: Deployment Options

### Option 1: Python Native (pip install)

**Installation**:
```bash
pip install shiroink
```

**Entry point**: `shiroink` command globally available

**Usage examples**:
```bash
shiroink --wizard                                    # Interactive setup
shiroink manga/ output/ --device kobo_libra_2       # Direct processing
shiroink manga/ output/ --profile my_setup          # Use saved profile
shiroink --list-devices                             # Device discovery
shiroink --list-profiles                            # List saved profiles
```

**Configuration**:
```
Profiles:     ~/.config/shiroink/profiles/*.json
Settings:     ~/.config/shiroink/config.json
Languages:    Auto-detected from $LANG or system locale
```

### Option 2: Docker

**Usage examples**:
```bash
# Interactive wizard (with TTY)
docker run --rm -it ghcr.io/esoso/shiroink --wizard

# Direct processing
docker run --rm -v /manga:/input -v /out:/output \
  ghcr.io/esoso/shiroink /input /output --device kobo_libra_2

# Persistent profiles (volume mount for ~/.config)
docker run --rm -it \
  -v /manga:/manga \
  -v ~/.config/shiroink:/root/.config/shiroink \
  ghcr.io/esoso/shiroink --profile my_manga /manga /output
```

**Documentation**: Comprehensive guide in `docs/guides/docker.md`

---

## Part 4: Backward Compatibility

**CRITICAL**: All changes are fully backward compatible

- Existing CLI flags remain unchanged
- `python -m shiroink` still works
- New features are opt-in (wizard, profiles, etc.)
- No breaking changes to API or behavior
- Existing users unaffected

---

## Part 5: Testing Strategy

### Phase 1
- Unit tests for wizard steps
- Unit tests for profile manager
- Unit tests for error message formatting
- Unit tests for parameter validator
- CLI tests for new flags

### Phase 2
- Unit tests for localization loader
- Unit tests for progress reporter enhancements
- Unit tests for dry-run interactive flow
- Localization tests (EN + IT)

### Phase 3
- Integration tests (wizard → processing → profile save)
- E2E tests (complete workflows)
- Docker container tests
- Multi-language validation tests

---

## Part 6: Documentation Updates

### Phase 1
- `docs/guides/wizard.md` - Interactive setup guide
- `docs/guides/profiles.md` - Profile management
- `docs/guides/quickstart.md` - Update with wizard info
- Update README.md with new features

### Phase 2
- `docs/guides/localization.md` - Language support
- `docs/guides/advanced-usage.md` - Complex scenarios
- `localization/README.md` - Translation guidelines

### Phase 3
- `docs/guides/docker-advanced.md` - Docker with wizard/profiles
- `docs/guides/troubleshooting.md` - Common issues
- Release notes for each phase

---

## Part 7: Dependencies

### Current (No Changes)
```
rich>=13.0.0          (already required)
pillow>=11.3.0        (already required)
```

### Phase 1-2 (No Additions)
- Use only Python stdlib + existing deps
- JSON (stdlib)
- Locale detection (stdlib)

### Phase 3+ (If Needed)
- Optional: `toml` (if file-based config added later)
- Optional: `click` (if CLI framework upgrade needed)

---

## Part 8: Success Metrics

### Phase 1
- [ ] Wizard reduces first-time setup from 20min to <5min
- [ ] Help output is clearer and more navigable
- [ ] Error messages are actionable
- [ ] Profiles successfully save/load/persist

### Phase 2
- [ ] Italian language support is complete and accurate
- [ ] Progress reporting shows accurate ETA
- [ ] Dry-run interactive menu works as intended
- [ ] Device discovery is more helpful

### Phase 3
- [ ] All integration tests pass
- [ ] E2E workflows complete successfully
- [ ] Docker documentation is comprehensive
- [ ] Zero support tickets for "how do I use wizard"

---

## Part 9: Future Enhancements (Post-v2.3)

These are NOT in scope but documented for future reference:

- [ ] Config file support (TOML) - if user demand
- [ ] GUI/TUI (Terminal UI) - if significant user request
- [ ] API server - if automation needed
- [ ] Additional languages beyond Italian
- [ ] Cloud processing integration
- [ ] Performance optimizations (GPU, parallel improvement)

---

## Part 10: Risk Mitigation

### Risk: Backward Compatibility Break
**Mitigation**: All changes are CLI additions, no removals/changes to existing flags

### Risk: Wizard complexity overwhelms users
**Mitigation**: Wizard is optional, `--help` remains simple fallback

### Risk: Localization becomes unmaintainable
**Mitigation**: Start with English + Italian only, structure ready for more

### Risk: Docker integration gets too complex
**Mitigation**: Docker uses same CLI, docs handle complexity (not code)

---

## Next Steps (After Document Approval)

1. ✅ Review & approve this document
2. ⏳ Begin Phase 1 implementation
3. ⏳ Commit initial structure with appropriate branch
4. ⏳ Implement wizard step by step
5. ⏳ Add tests as features are added
6. ⏳ Create PR for Phase 1 with release notes

---

## Document History

| Date | Version | Author | Change |
|------|---------|--------|--------|
| 2026-01-05 | 1.0 | OpenCode Agent | Initial formalization of 13 decisions |

---

## Appendix: Decision Matrix Summary

| # | Decision | Choice | Rationale |
|---|----------|--------|-----------|
| 1 | Wizard Activation | Opzione C | Balance guidance + flexibility |
| 2 | Profile Storage | JSON in ~/.config | POSIX-compliant, zero deps |
| 3 | Entry Point | `shiroink` cmd | Standard for CLI tools |
| 4 | Error Language | English + i18n ready | Open-source standard |
| 5 | Error Verbosity | Concise + --verbose | Power users + novices |
| 6 | Help Style | Rich library | Visuale, accogliente |
| 7 | Wizard Language | Auto-detect + menu | Smart defaults |
| 8 | Docker | CLI standard + docs | No duplication |
| 9 | Profile Suggestion | Simple message | Educational, not invasive |
| 10 | Dry-Run | Interactive menu | Max control for user |
| 11 | Config File | No (profiles enough) | Keep simple |
| 12 | Progress | Enhanced detailed | Full visibility |
| 13 | Timeline | Phased (no deadline) | Incremental, quality-focused |

---

**End of Document**
