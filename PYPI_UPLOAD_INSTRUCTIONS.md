# PyPI Upload Instructions

## Step 1: Get PyPI API Token

1. Go to https://pypi.org/account/register/ (create account if needed)
2. Log in to https://pypi.org/account/login/
3. Go to Account Settings → API tokens
4. Click "Add API token"
5. Token name: "mini-os-scheduler" (or any name)
6. Scope: "Entire account" (or just this project)
7. Click "Add token"
8. **COPY THE TOKEN** - it starts with `pypi-` and you won't see it again!

## Step 2: Upload to PyPI

Run this command:
```bash
twine upload dist/*
```

When prompted:
- Username: `__token__`
- Password: `pypi-xxxxxxxxxxxxx` (paste your token)

## Alternative: Test PyPI First (Recommended)

1. Get Test PyPI token: https://test.pypi.org/manage/account/
2. Upload to Test PyPI:
   ```bash
   twine upload --repository testpypi dist/*
   ```
3. Test installation:
   ```bash
   pip install --index-url https://test.pypi.org/simple/ mini-os-scheduler
   ```
4. If successful, upload to production PyPI

