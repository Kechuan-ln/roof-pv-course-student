"""Install pinned course dependencies into the notebook's current Python."""
from importlib import metadata
from pathlib import Path
import subprocess
import sys


def ensure_environment(root):
    root = Path(root)
    requirements = root / 'requirements.txt'
    if not requirements.is_file():
        raise RuntimeError('Extract the complete student package and use the folder containing PV_Practical.ipynb as the working directory.')
    if sys.version_info[:2] != (3, 12):
        raise RuntimeError(
            'This course requires Python 3.12. Use the course launcher to select the correct environment. '
            'Close the Notebook, double-click Start_Course in the package, then run this cell again.')
    missing = []
    for line in requirements.read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        name, expected = line.split('==', 1)
        try:
            actual = metadata.version(name).split('+')[0]
        except metadata.PackageNotFoundError:
            actual = None
        if actual != expected:
            missing.append(name)
    if not missing:
        subprocess.run([sys.executable, '-m', 'pip', 'check'], check=True)
        print('The course environment is ready. Continue to the next cell.')
        return
    print('Installing course dependencies into the current Notebook environment. The first installation requires internet access.', flush=True)
    print('Packages to install or update: ' + ', '.join(missing), flush=True)
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', str(requirements)], check=True)
        subprocess.run([sys.executable, str(root/'scripts'/'check_environment.py'), str(requirements)], check=True)
        subprocess.run([sys.executable, '-m', 'pip', 'check'], check=True)
    except subprocess.CalledProcessError as error:
        raise RuntimeError('Dependency installation or checking did not complete. Keep the error above and rerun this cell when the network is available.') from error
    # Stop Run All: already-imported binary modules cannot safely use new files.
    raise RuntimeError(
        'Installation complete. Select Kernel → Restart Kernel,'
        ' then rerun this cell and continue once the environment check passes.')
