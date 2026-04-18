Test harness scripts for ollama_workbench.

Layout:
- scripts/ai_status.sh and scripts/ai_health.sh are operator/runtime helpers
- scripts/tests/* are validation and smoke-test harnesses

Current intent:
- doctor_test.sh: verify normal doctor passes and test_data doctor fails on malformed fixture
- status_test.sh: verify --data-dir switches resolved paths
- fixtures_check.sh: verify expected test fixture files exist
- ollama_workbench_smoketest.sh: broader end-to-end smoke pass
