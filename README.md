## About virtual env
To create virtual env in linux:
```
python -m venv env
```

To create virtual env in Windows:
```
python -m venv c:\path\to\env
```

To access virtual env in linux:
```
source env/bin/activate
```

To access virtual env in Windows:
```
wenv\Scripts\Activate.ps1
```

If you're using windows powershell on vscode, and get UnauthorizedAccess error, please run:
```
Set-ExecutionPolicy Unrestricted -Scope Process
```
before entering the virtual env. After that, you can run:
```
Set-ExecutionPolicy Default -Scope Process
```
to avoid any potential issues.