import os, shutil, subprocess, sys

proj_dir = r"C:\python projects\glaucoma_ai\AIROGS Challenge\glaucoma_project"
# potential rar.exe locations
candidates = [shutil.which('rar'),
              r"C:\Program Files\WinRAR\Rar.exe",
              r"C:\Program Files (x86)\WinRAR\Rar.exe"]
rar_exe = None
for c in candidates:
    if not c:
        continue
    try:
        if shutil.which('rar'):
            rar_exe = shutil.which('rar')
            break
    except Exception:
        pass
    if os.path.exists(c):
        rar_exe = c
        break

if not rar_exe:
    print('WinRAR CLI not found on this machine (rar.exe). Cannot create RAR.')
    sys.exit(2)

out_path = os.path.join(proj_dir, 'glaucoma_project.rar')
# remove existing
if os.path.exists(out_path):
    try:
        os.remove(out_path)
    except Exception:
        pass

# Run rar from within project folder to include contents
cmd = [rar_exe, 'a', '-r', out_path, '*']
print('Running:', ' '.join(cmd))
proc = subprocess.run(cmd, cwd=proj_dir)
if proc.returncode == 0:
    print('Created', out_path)
    sys.exit(0)
else:
    print('rar returned code', proc.returncode)
    sys.exit(proc.returncode)
