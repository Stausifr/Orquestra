from pkg.audit.log import AuditLog, STORAGE_DIR, verify_chain


def test_audit_chain(tmp_path, monkeypatch):
    monkeypatch.setattr('pkg.audit.log.STORAGE_DIR', tmp_path)
    log = AuditLog('run')
    log.append({'a': 1})
    assert verify_chain(tmp_path / 'run.json')
