#!/bin/bash
# macOS: double-click; Linux: bash Start_Course.command
cd -- "$(dirname -- "$0")" || exit 1
COURSE_CONDA="${CONDA_EXE:-}"
if [ ! -x "$COURSE_CONDA" ]; then COURSE_CONDA="$(command -v conda 2>/dev/null)"; fi
if [ ! -x "$COURSE_CONDA" ]; then
    for candidate in "$HOME/miniconda3/bin/conda" "$HOME/anaconda3/bin/conda" "$HOME/miniforge3/bin/conda" \
        /opt/anaconda3/bin/conda /opt/miniconda3/bin/conda /opt/homebrew/Caskroom/miniconda/base/bin/conda; do
        if [ -x "$candidate" ]; then COURSE_CONDA="$candidate"; break; fi
    done
fi
if [ ! -x "$COURSE_CONDA" ]; then
    echo 'Install Anaconda or Miniconda first, then double-click this file. Python is included.'
    read -r -p 'Press Enter to close... ' unused
    exit 1
fi
"$COURSE_CONDA" run --no-capture-output --name base python "$PWD/scripts/launch_course.py" --conda "$COURSE_CONDA"
result=$?
if [ "$result" -ne 0 ]; then read -r -p 'Startup did not complete. Keep the error message above. Press Enter to close... ' unused; fi
exit "$result"
