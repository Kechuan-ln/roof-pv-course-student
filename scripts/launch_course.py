"""Conda bootstrap and isolated-kernel Jupyter launch; standard library only."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys

ENV_NAME='pv-course-2026'
ROOT=Path(__file__).resolve().parents[1]


def run(command, **kwargs):
    return subprocess.run([str(x) for x in command],check=True,**kwargs)


def find_environment(environments, name=ENV_NAME, prefix=None):
    if prefix:
        expected=os.path.normcase(str(Path(prefix).resolve()))
        return next((p for p in environments if os.path.normcase(str(Path(p).resolve()))==expected),None)
    return next((p for p in environments if Path(p).name==name),None)


def kernel_directory(python_prefix):
    return str(Path(python_prefix)/'share'/'jupyter'/'kernels')


def main(argv=None):
    parser=argparse.ArgumentParser()
    parser.add_argument('--conda',required=True,help='Path to conda executable')
    parser.add_argument('--prepare-only',action='store_true',help='Teacher verification: do not open browser')
    parser.add_argument('--prefix',help='Optional isolated environment path for teacher verification')
    args=parser.parse_args(argv)
    conda=args.conda
    selector=['--prefix',str(Path(args.prefix).resolve())] if args.prefix else ['--name',ENV_NAME]
    captured=run([conda,'env','list','--json'],capture_output=True,text=True)
    existing=find_environment(json.loads(captured.stdout)['envs'],prefix=args.prefix)
    execute=[conda,'run','--no-capture-output',*selector]
    check_command=[*execute,'python',ROOT/'scripts'/'check_environment.py',ROOT/'requirements.txt']
    if existing:
        checked=subprocess.run([str(x) for x in check_command],cwd=ROOT)
    else:
        checked=None
    if checked is None or checked.returncode:
        print('Preparing or updating the course environment. Stay connected and keep this window open during downloads.',flush=True)
        action='update' if existing else 'create'
        run([conda,'env',action,*selector,'--file',ROOT/'mini_project.yml'],cwd=ROOT,
            env={**os.environ,'CONDA_ALWAYS_YES':'true'})
    run(check_command,cwd=ROOT)
    run([*execute,'python','-m','pip','check'],cwd=ROOT)
    run([*execute,'python',ROOT/'scripts'/'smoke_check.py'],cwd=ROOT)
    # Both the existing notebooks' python3 name and the explicit course name resolve
    # to this environment. Registration is confined to sys.prefix, not user/global.
    for name in ['python3',ENV_NAME]:
        run([*execute,'python','-m','ipykernel','install','--sys-prefix',
             '--name',name,'--display-name','PV Course 2026'],cwd=ROOT)
    if args.prepare_only:
        return 0
    located=run([conda,'run',*selector,'python','-c','import sys; print(sys.prefix)'],capture_output=True,text=True)
    prefix=located.stdout.strip().splitlines()[-1]
    kernel_env={**os.environ,'JUPYTER_PATH':str(Path(prefix)/'share'/'jupyter')}
    kernels=json.dumps(['python3',ENV_NAME])
    print('The environment is ready. Opening the course; close this window when you finish.',flush=True)
    run([*execute,'python','-m','jupyterlab',str(ROOT/'PV_Practical.ipynb'),
         f'--ServerApp.root_dir={ROOT}',f'--KernelSpecManager.allowed_kernelspecs={kernels}'],cwd=ROOT,env=kernel_env)
    return 0


if __name__=='__main__':
    try:
        raise SystemExit(main())
    except (subprocess.CalledProcessError,FileNotFoundError,ValueError,KeyError) as error:
        print(f'Course startup did not complete:{error}\nKeep the error message for your instructor. For a connection failure, reconnect and run the launcher again.',file=sys.stderr)
        raise SystemExit(1)
