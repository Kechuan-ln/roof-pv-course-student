"""Prepare the downloaded student package in a Colab runtime."""
from importlib import metadata
from pathlib import Path
import hashlib
import importlib
import json
import os
import platform
import subprocess
import sys


def prepare(root):
    root = Path(root).resolve()
    from packaging.requirements import Requirement
    requirements = [Requirement(line) for line in (root / 'requirements.txt').read_text().splitlines()
                    if line.strip() and not line.startswith('#')]
    needs_install = []
    for req in requirements:
        try:
            installed = metadata.version(req.name)
        except metadata.PackageNotFoundError:
            installed = None
        if installed is None or installed not in req.specifier:
            needs_install.append(str(req))
    if needs_install:
        # Install before importing any course scientific modules.
        print('Installing course libraries. Keep this cell running.', flush=True)
        before = {name: metadata.version(name) for name in ['numpy', 'pandas', 'scipy', 'matplotlib', 'shapely']
                  if name in sys.modules}
        subprocess.run([sys.executable, '-m', 'pip', 'install', '--quiet', '-r', str(root / 'requirements.txt')], check=True)
        importlib.invalidate_caches()
        changed = [name for name, version in before.items() if metadata.version(name) != version]
        if changed:
            raise RuntimeError('Updated loaded libraries: ' + ', '.join(changed) +
                               '. Choose Runtime > Restart session, then run this cell again.')
    for req in requirements:
        if metadata.version(req.name) not in req.specifier:
            raise RuntimeError(f'Course dependency check failed: {req}')
    checks = json.loads((root / 'data_checksums.json').read_text())
    for rel, digest in checks.items():
        if hashlib.sha256((root / rel).read_bytes()).hexdigest() != digest:
            raise RuntimeError(f'Input data checksum mismatch: {rel}')
    os.chdir(root)
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
    import numpy as np
    import pandas as pd
    import geopandas as gpd
    import pvlib
    from pv_course.poa_calculation import get_timezone
    from shapely.geometry import box
    assert get_timezone(13.7, 100.5) is not None
    sun = pvlib.solarposition.get_solarposition(pd.date_range('2019-06-21', periods=3, freq='h', tz='Asia/Bangkok'), 13.7, 100.5)
    assert np.isfinite(sun.zenith).all()
    assert gpd.GeoSeries([box(0, 0, 10, 10)], crs=32647).area.iloc[0] == 100
    report = {'python': sys.version.split()[0], 'platform': platform.platform(),
              'packages': {req.name: metadata.version(req.name) for req in requirements},
              'input_files_verified': len(checks)}
    (root / 'result').mkdir(exist_ok=True)
    (root / 'result/environment.json').write_text(json.dumps(report, indent=2))
    print('Ready: four-city weather and building data, PV libraries and geometry checks passed.')
    print('Continue with the next cell. Save your Notebook and download results before ending the session.')
    return root
