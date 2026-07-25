"""Tests each concrete check's simulated (demo mode) output — deterministic and OS-independent."""

from app.services.audit.admin_accounts_check import AdminAccountsCheck
from app.services.audit.bitlocker_check import BitLockerCheck
from app.services.audit.defender_check import DefenderCheck
from app.services.audit.firewall_check import FirewallCheck
from app.services.audit.guest_account_check import GuestAccountCheck
from app.services.audit.installed_software_check import InstalledSoftwareCheck
from app.services.audit.os_version_check import OsVersionCheck
from app.services.audit.password_policy_check import PasswordPolicyCheck
from app.services.audit.system_info_check import SystemInfoCheck
from app.services.audit.windows_update_check import WindowsUpdateCheck


def _assert_all_simulated(findings):
    assert len(findings) > 0
    assert all(f.source == "simulated" for f in findings)


def test_password_policy_simulated():
    findings = PasswordPolicyCheck().run_simulated()
    _assert_all_simulated(findings)
    assert all(f.status == "pass" for f in findings)


def test_admin_accounts_simulated():
    findings = AdminAccountsCheck().run_simulated()
    _assert_all_simulated(findings)


def test_guest_account_simulated_is_disabled_and_passes():
    findings = GuestAccountCheck().run_simulated()
    _assert_all_simulated(findings)
    assert findings[0].status == "pass"


def test_defender_simulated_passes():
    findings = DefenderCheck().run_simulated()
    _assert_all_simulated(findings)
    assert findings[0].status == "pass"


def test_firewall_simulated_all_profiles_enabled():
    findings = FirewallCheck().run_simulated()
    _assert_all_simulated(findings)
    assert findings[0].status == "pass"


def test_bitlocker_simulated_fully_encrypted():
    findings = BitLockerCheck().run_simulated()
    _assert_all_simulated(findings)
    assert findings[0].status == "pass"


def test_windows_update_simulated_recent():
    findings = WindowsUpdateCheck().run_simulated()
    _assert_all_simulated(findings)
    assert findings[0].status == "pass"


def test_os_version_simulated_is_informational():
    findings = OsVersionCheck().run_simulated()
    _assert_all_simulated(findings)
    assert findings[0].status == "info"
    assert findings[0].weight == 0.0


def test_installed_software_simulated_lists_apps():
    findings = InstalledSoftwareCheck().run_simulated()
    _assert_all_simulated(findings)
    assert findings[0].status == "info"
    assert "Chrome" in findings[0].evidence


def test_system_info_simulated_is_informational():
    findings = SystemInfoCheck().run_simulated()
    _assert_all_simulated(findings)
    assert findings[0].status == "info"
    assert findings[0].weight == 0.0
