@echo off
for /r %%i in (__pycache__) do (
    if exist "%%i" (
        echo Deleting "%%i"
        rd /s /q "%%i"
    )
)
echo Clear completed.
:: pause