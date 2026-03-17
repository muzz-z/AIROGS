import shutil, os

proj_dir = r"C:\python projects\glaucoma_ai\AIROGS Challenge\glaucoma_project"
out_base = os.path.join(proj_dir, 'glaucoma_project')
# Remove any existing archive
for ext in ('.zip', '.tar', '.gztar'):
    p = out_base + ext
    if os.path.exists(p):
        try:
            os.remove(p)
        except Exception:
            pass

shutil.make_archive(out_base, 'zip', proj_dir)
print('Created', out_base + '.zip')
