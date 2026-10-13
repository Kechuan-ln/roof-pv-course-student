"""Save classroom figures and export the resulting files."""
from pathlib import Path
import zipfile
import matplotlib.pyplot as plt
from IPython.display import FileLink, display


def show_figure(name, folder):
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    plt.gcf().savefig(folder / (name + '.png'), dpi=130, bbox_inches='tight')
    plt.show()
    plt.close()


def download_results(root):
    root = Path(root)
    path = root / 'Solar_PV_Results.zip'
    with zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED) as archive:
        for item in sorted((root / 'result').rglob('*')):
            if item.is_file() and not item.is_symlink() and item.suffix in {'.csv', '.png', '.json', '.md'}:
                archive.write(item, item.relative_to(root).as_posix())
    try:
        from google.colab import files
    except ImportError:
        display(FileLink(path.name, result_html_prefix='Download results: '))
    else:
        files.download(str(path))
    print('Save the edited Notebook separately using the File menu.')
    return path
