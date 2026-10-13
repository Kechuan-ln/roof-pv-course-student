"""Validate the imported course environment without importing heavy plotting packages."""
from importlib.metadata import version, PackageNotFoundError
from pathlib import Path
import sys


def check(requirements):
    errors=[]
    if sys.version_info[:2] != (3,12):
        errors.append(f'Python 3.12 required; found {sys.version.split()[0]}')
    for line in Path(requirements).read_text().splitlines():
        line=line.strip()
        if not line or line.startswith('#'):
            continue
        name,expected=line.split('==',1)
        try:
            actual=version(name)
        except PackageNotFoundError:
            actual='missing'
        if actual.split('+')[0]!=expected:
            errors.append(f'{name}: expected {expected}, found {actual}')
    if errors:
        print('\n'.join(errors),file=sys.stderr)
        return 1
    print('PV Course 2026 environment ready (Python 3.12, required package versions checked).')
    return 0


if __name__=='__main__':
    raise SystemExit(check(sys.argv[1]))
