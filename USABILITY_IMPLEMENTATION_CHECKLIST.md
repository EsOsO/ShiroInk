# USABILITY_IMPLEMENTATION_CHECKLIST.md

Master checklist for tracking Phase 1-3 implementation progress.  
Reference: `USABILITY_PLAN.md`

---

## Phase 1: Core Improvements (2-3 weeks)

### 1.1 Project Structure Setup
- [ ] Create `src/__main__.py` entry point
- [ ] Create `src/wizard/` directory structure
- [ ] Create `src/profiles/` directory structure
- [ ] Create `src/localization/` directory structure
- [ ] Update `pyproject.toml` with console_scripts entry points
- [ ] Verify `shiroink` command works after install

### 1.2 Localization Infrastructure
- [ ] Create `src/localization/loader.py` (base class)
- [ ] Create `src/localization/locales/en.json` (English strings)
- [ ] Implement language auto-detection (LANG, locale, Windows)
- [ ] Implement environment variable override (SHIROINK_LANG)
- [ ] Implement persistence (~/.config/shiroink/config.json)
- [ ] Test on Linux, macOS, Windows

### 1.3 Configuration Profiles System
- [ ] Create `src/profiles/schema.py` (JSON schema validation)
- [ ] Create `src/profiles/manager.py` (CRUD operations)
- [ ] Implement profile directory creation (POSIX-compliant)
- [ ] Implement `--save-profile NAME` functionality
- [ ] Implement `--profile NAME` loading
- [ ] Implement `--list-profiles` with metadata
- [ ] Implement `--edit-profile NAME` 
- [ ] Implement `--delete-profile NAME`
- [ ] Add profile suggestion at end of processing
- [ ] Test profile persistence across sessions

### 1.4 Interactive Wizard
- [ ] Create `src/wizard/steps.py` (base step class)
- [ ] Create `src/wizard/prompts.py` (input helpers)
- [ ] Implement device selection step
- [ ] Implement format (RTL/LTR) selection step
- [ ] Implement paths selection step (with validation)
- [ ] Implement quality selection step
- [ ] Implement performance (workers) selection step
- [ ] Implement review step (show summary)
- [ ] Implement confirmation menu ([y/n])
- [ ] Add [m] modify option (loop back to wizard)
- [ ] Add [s] save as profile option
- [ ] Test wizard flow end-to-end

### 1.5 Enhanced Help System
- [ ] Modify `src/cli.py` to use Rich for help output
- [ ] Organize help by categories (Essential, Advanced, Configuration, Help)
- [ ] Add practical examples to help
- [ ] Add links to documentation
- [ ] Add device/pipeline suggestions in help
- [ ] Test help output readability

### 1.6 Better Error Messages
- [ ] Create `src/error_messages.py` (error message formatting)
- [ ] Implement error message templates (localization-ready)
- [ ] Implement typo suggestions (--resolution vs --resolutoin)
- [ ] Add `--verbose` flag for detailed error explanations
- [ ] Add suggestion context (e.g., "did you mean...")
- [ ] Test error messages with various invalid inputs

### 1.7 Parameter Validation
- [ ] Create `src/parameter_validator.py`
- [ ] Implement pre-flight validation (before processing)
- [ ] Implement warnings for suspicious configurations
- [ ] Implement suggestions based on parameters
- [ ] Test validator with edge cases

### 1.8 Integration with Main Flow
- [ ] Modify `src/cli.py` to add new flags (--wizard, --profile, etc.)
- [ ] Modify `src/main.py` to detect first-run and prompt wizard
- [ ] Modify `src/main.py` to load profiles when --profile is used
- [ ] Add profile suggestion after successful processing
- [ ] Test complete flow: wizard → processing → profile suggestion

### 1.9 Testing (Phase 1)
- [ ] Create `tests/unit/test_wizard.py`
- [ ] Create `tests/unit/test_profiles.py`
- [ ] Create `tests/unit/test_error_messages.py`
- [ ] Create `tests/unit/test_parameter_validator.py`
- [ ] Update `tests/unit/test_cli.py` for new flags
- [ ] Run all tests, achieve >90% coverage
- [ ] Test on Python 3.11, 3.12, 3.13

### 1.10 Documentation (Phase 1)
- [ ] Create `docs/guides/wizard.md` (tutorial)
- [ ] Create `docs/guides/profiles.md` (management guide)
- [ ] Update `docs/guides/quickstart.md` with wizard
- [ ] Update `README.md` with new features
- [ ] Update `docs/guides/installation.md` with pip command
- [ ] Update `docs/guides/usage.md` with new examples

### 1.11 Backward Compatibility Verification
- [ ] Test existing CLI flags still work
- [ ] Test `python -m shiroink` still works
- [ ] Test Docker container still works
- [ ] Test that non-wizard users aren't affected

### 1.12 Code Quality
- [ ] Run `black src/ tests/`
- [ ] Run `flake8 src/ --max-line-length=88`
- [ ] Run `mypy src/ --ignore-missing-imports`
- [ ] Run `pytest tests/unit/ -v`
- [ ] Pass pre-commit hooks

---

## Phase 2: Localization & Progress (2-3 weeks)

### 2.1 Localization Expansion
- [ ] Create `src/localization/locales/it.json` (Italian translations)
- [ ] Translate all user-facing strings to Italian
- [ ] Test language switching (--lang it, SHIROINK_LANG=it)
- [ ] Test auto-detection on Italian-configured system
- [ ] Document how to add new languages

### 2.2 Enhanced Progress Reporting
- [ ] Enhance `src/progress_reporter.py` with ETA calculation
- [ ] Add speed (files/min) tracking
- [ ] Add current file display
- [ ] Add success/failed/skipped counters
- [ ] Add elapsed/remaining time
- [ ] Add estimated output size
- [ ] Test ETA accuracy with real files

### 2.3 Dry-Run Interactive Mode
- [ ] Create `src/dry_run_interactive.py`
- [ ] Implement preview display (configuration + analysis)
- [ ] Implement menu options ([y/n/m/s])
- [ ] Implement modification loop (m → wizard)
- [ ] Implement profile save before start (s option)
- [ ] Test complete dry-run flow

### 2.4 Device & Pipeline Discovery
- [ ] Enhance `--list-devices` output with Rich formatting
- [ ] Add device categorization (E-Ink B&W, Color, Tablets)
- [ ] Add detailed specs for each device
- [ ] Create `--list-pipelines` command
- [ ] Add pipeline descriptions and use cases
- [ ] Test output readability and usefulness

### 2.5 Testing (Phase 2)
- [ ] Create `tests/unit/test_progress_reporter.py`
- [ ] Create `tests/unit/test_dry_run_interactive.py`
- [ ] Create `tests/unit/test_localization.py` (EN + IT)
- [ ] Test language persistence across sessions
- [ ] Run integration tests (wizard → localized processing)

### 2.6 Documentation (Phase 2)
- [ ] Create `docs/guides/localization.md`
- [ ] Create `docs/guides/advanced-usage.md`
- [ ] Create `localization/README.md` (for translators)
- [ ] Update changelog with Phase 2 features
- [ ] Add translation examples for contributors

---

## Phase 3: Polish & Testing (1-2 weeks)

### 3.1 Integration & E2E Tests
- [ ] Create `tests/integration/test_wizard_integration.py`
- [ ] Create `tests/integration/test_profiles_integration.py`
- [ ] Create `tests/integration/test_docker_integration.py`
- [ ] Create `tests/e2e/test_complete_workflow.py`
- [ ] Test complete workflows on real data
- [ ] Test on multiple systems (Linux, macOS, Windows)

### 3.2 Docker Documentation
- [ ] Create `docs/guides/docker-advanced.md`
- [ ] Document wizard usage with `-it` flags
- [ ] Document profile persistence with volume mounts
- [ ] Document language settings in containers
- [ ] Add real examples (copy-paste ready)
- [ ] Test all Docker examples

### 3.3 User Documentation
- [ ] Create `docs/guides/troubleshooting.md`
- [ ] Create `docs/guides/profiles-advanced.md`
- [ ] Create `docs/architecture/cli-design.md`
- [ ] Add FAQ section to docs
- [ ] Add tips & tricks section

### 3.4 Edge Cases & Polish
- [ ] Handle malformed profile JSON gracefully
- [ ] Handle missing profile directories
- [ ] Handle locale detection failures
- [ ] Handle TTY detection (for colors/formatting)
- [ ] Handle very long paths/filenames
- [ ] Handle special characters in profile names

### 3.5 Release Preparation
- [ ] Create `RELEASE_NOTES_v2.1.md`
- [ ] Document all Phase 1-3 changes
- [ ] Document migration guide (if any)
- [ ] Update version numbers
- [ ] Update CHANGELOG.md
- [ ] Tag release (v2.1.0)

### 3.6 Final Testing (Phase 3)
- [ ] Run full test suite: `pytest tests/ -v --cov=src`
- [ ] Achieve >85% code coverage
- [ ] Test on Python 3.11, 3.12, 3.13
- [ ] Test on Docker
- [ ] Manual smoke testing (realistic workflows)
- [ ] Test with real manga collections

### 3.7 Code Quality (Final)
- [ ] `black src/ tests/ --check`
- [ ] `flake8 src/ --max-line-length=88`
- [ ] `mypy src/ --ignore-missing-imports`
- [ ] `pre-commit run --all-files`
- [ ] No linting errors

---

## Success Criteria Verification

### Phase 1 Success
- [ ] Wizard reduces first-time setup from 20min to <5min
- [ ] Help output is clearer and more navigable
- [ ] Error messages are actionable and helpful
- [ ] Profiles save/load/persist correctly
- [ ] All Phase 1 tests pass
- [ ] No backward compatibility issues

### Phase 2 Success
- [ ] Italian language translations are complete and accurate
- [ ] Progress reporting shows accurate ETA
- [ ] Dry-run interactive menu works as intended
- [ ] Device discovery is more helpful
- [ ] Localization infrastructure is clean and maintainable
- [ ] All Phase 2 tests pass

### Phase 3 Success
- [ ] All integration tests pass
- [ ] E2E workflows complete successfully
- [ ] Docker documentation is comprehensive
- [ ] Zero support tickets for "how do I use wizard"
- [ ] Code coverage >85%
- [ ] Production-ready quality

---

## Tracking Notes

### Current Phase: Planning Complete ✓
- [x] 13 critical decisions documented
- [x] USABILITY_PLAN.md created and committed
- [x] This checklist created

### Next Steps:
1. Review USABILITY_PLAN.md for any issues
2. Create feature branch for Phase 1: `feat/phase-1-usability`
3. Begin implementation following Phase 1 checklist
4. Create PR when Phase 1 is complete

---

## Quick Reference

**Documents**:
- Master plan: `USABILITY_PLAN.md`
- This checklist: `USABILITY_IMPLEMENTATION_CHECKLIST.md`

**Key Dates**:
- Planning: Complete ✓
- Phase 1 Start: [TBD]
- Phase 1 End: [Estimated 2-3 weeks from start]
- Phase 2 Start: [After Phase 1 merge]
- Phase 3 Start: [After Phase 2 merge]

**Contacts/Decisions**:
- Owner: esoso
- Last Updated: 2026-01-05

---

**End of Checklist**
