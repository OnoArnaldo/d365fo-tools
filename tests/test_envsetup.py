from d365fo_tools.envsetup import EnvironmentSetup
from .conftest import PACKAGES_DIR, LOG_DIR


def test_setup(log):
    EnvironmentSetup(
        'user@domain.com', 'p@ss', '$proj000/trunk/main/metadata', ['Cost.*']
    ).run()

    assert log == [
        'LOG:INFO:Stop services',
        'LOG:None:    stop iis',
        'CALL:#iisreset /stop#:shell=True',
        'LOG:None:    stop D365 services',
        'CALL:#Get-Service *Dynamics*|Stop-Service#:shell=True',
        'LOG:INFO:Delete package folders',
        'LOG:None:    deleting: CostAccountingAX',
        f'FOLDER:DELETE:{PACKAGES_DIR}/CostAccountingAX',
        'LOG:None:    deleting: CostAccounting',
        f'FOLDER:DELETE:{PACKAGES_DIR}/CostAccounting',
        'LOG:None:    deleting: CostAccountingService',
        f'FOLDER:DELETE:{PACKAGES_DIR}/CostAccountingService',
        'LOG:INFO:Change workspace mapping',
        f'CALL:"tf.exe" workfold /unmap /workspace:"vm0000-1 "{PACKAGES_DIR}" /login:"user@domain.com","p@ss":shell=True',
        f'CALL:"tf.exe" workfold /map "$proj000/trunk/main/metadata" "{PACKAGES_DIR}" /workspace:"vm0000-1 /login:"user@domain.com","p@ss":shell=True',
        'CALL:"tf.exe" workfold /workspace:"vm0000-1 /login:"user@domain.com","p@ss":shell=True',
        'LOG:INFO:Get latest version',
        'CALL:"tf.exe" get /force /recursive /noautoresolve /noprompt /login:"user@domain.com","p@ss":shell=True',
        f'LOG:INFO:Build: {PACKAGES_DIR}',
        'LOG:None:  Level: 0',
        f'CALL:#{PACKAGES_DIR}#CostAccounting#{LOG_DIR}#:shell=True',
        "LOG:INFO:0: 'CostAccounting' has been built.",
        'LOG:None:  Level: 1',
        f'CALL:#{PACKAGES_DIR}#CostAccountingAX#{LOG_DIR}#:shell=True',
        "LOG:INFO:0: 'CostAccountingAX' has been built.",
        'LOG:None:  Level: 2',
        f'CALL:#{PACKAGES_DIR}#CostAccountingService#{LOG_DIR}#:shell=True',
        "LOG:INFO:0: 'CostAccountingService' has been built.",
        'LOG:INFO:Synchronise DB',
        f'CALL:#{PACKAGES_DIR}#vm0000#:shell=True'
    ]


def test_setup_without_arguments(log):
    EnvironmentSetup().run()

    assert log == [
        'LOG:INFO:Stop services',
        'LOG:None:    stop iis',
        'CALL:#iisreset /stop#:shell=True',
        'LOG:None:    stop D365 services',
        'CALL:#Get-Service *Dynamics*|Stop-Service#:shell=True',
        'LOG:INFO:Delete package folders',
        'LOG:None:    deleting: CaseManagement',
        f'FOLDER:DELETE:{PACKAGES_DIR}/CaseManagement',
        'LOG:None:    deleting: BankTypes',
        f'FOLDER:DELETE:{PACKAGES_DIR}/BankTypes',
        'LOG:INFO:Change workspace mapping',
        'CALL:"tf.exe" workfold /unmap /workspace:"vm0000-1 '
        f'"{PACKAGES_DIR}" '
        '/login:"the-user@domain.com","the-pass":shell=True',
        'CALL:"tf.exe" workfold /map "$metadata" '
        f'"{PACKAGES_DIR}" '
        '/workspace:"vm0000-1 /login:"the-user@domain.com","the-pass":shell=True',
        'CALL:"tf.exe" workfold /workspace:"vm0000-1 '
        '/login:"the-user@domain.com","the-pass":shell=True',
        'LOG:INFO:Get latest version',
        'CALL:"tf.exe" get /force /recursive /noautoresolve /noprompt '
        '/login:"the-user@domain.com","the-pass":shell=True',
        'LOG:INFO:Build: '
        f'{PACKAGES_DIR}',
        'LOG:None:  Level: 0',
        f'CALL:#{PACKAGES_DIR}#BankTypes#{LOG_DIR}#:shell=True',
        "LOG:INFO:0: 'BankTypes' has been built.",
        f'CALL:#{PACKAGES_DIR}#CaseManagement#{LOG_DIR}#:shell=True',
        "LOG:INFO:0: 'CaseManagement' has been built.",
        'LOG:INFO:Synchronise DB',
        f'CALL:#{PACKAGES_DIR}#vm0000#:shell=True'
    ]
