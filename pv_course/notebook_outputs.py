"""Display and download the same course results in Colab and local Jupyter."""
from pathlib import Path
import html
import json
import zipfile


def in_colab():
    try:
        import google.colab  # noqa: F401
        return True
    except ImportError:
        return False


def preview_website(path):
    from IPython.display import HTML, FileLink, display
    path = Path(path).resolve()
    if in_colab():
        document = path.read_text(encoding='utf-8')
        display(HTML('<iframe title="Rooftop PV results" sandbox="allow-scripts" '
                     'style="width:100%;height:1000px;border:0" srcdoc="' +
                     html.escape(document, quote=True) + '"></iframe>'))
        print('The website below includes building results and 3D shadows. Download it with the next cell to open it in a separate browser tab.')
    else:
        display(FileLink(str(path.relative_to(Path.cwd())), result_html_prefix='Open the course results website: '))
    return path


def export_results(root):
    root = Path(root).resolve()
    result = root / 'result'
    if not (result / 'course_website.html').is_file():
        raise RuntimeError('Run the website export cell first.')
    destination = root / 'PV_Results.zip'
    # Only course outputs, excluding input data, credentials and the current ZIP.
    files = [p for p in result.rglob('*') if p.is_file() and not p.is_symlink()
             and p.suffix in {'.html', '.csv', '.json', '.png', '.svg', '.pdf', '.md'}]
    with zipfile.ZipFile(destination, 'w', zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(files):
            archive.write(path, path.relative_to(root).as_posix())
        archive.writestr('README.txt', 'Open result/course_website.html in your browser.\n'
                         'Save or download your edited Notebook separately from the Notebook File menu.\n')
    if in_colab():
        from google.colab import files
        files.download(str(destination))
    else:
        from IPython.display import FileLink, display
        display(FileLink(destination.name, result_html_prefix='Download results: '))
    print('Results ZIP ready. Save or download your edited Notebook separately using the File menu.')
    return destination
