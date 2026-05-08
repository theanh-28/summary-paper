@echo off
REM =============================================================================
REM Export Metabase Dashboards
REM =============================================================================
REM =============================================================================
REM Script nay export TOAN BO cau hinh Metabase vao file SQL.
REM (Bao gom: Tai khoan Admin, Ket noi Database, Embedding, v.v.)
REM
REM Cach dung: Chay file nay tai thu muc goc cua project sau khi thiet ke xong.
REM =============================================================================

echo ============================================
echo   Exporting Metabase Dashboards...
echo ============================================

docker exec summary_mysql mysqldump -u summary_user -psummary_pass --databases metabase_appdb > database\metabase_restore.sql

if %ERRORLEVEL% EQU 0 (
    echo.
    echo   ✅ Export thanh cong!
    echo   File: database\metabase_restore.sql
    echo.
    echo   Buoc tiep theo:
    echo     git add database\metabase_restore.sql
    echo     git commit -m "chore: export metabase dashboards"
    echo     git push
    echo.
) else (
    echo.
    echo   ❌ Export that bai! Hay dam bao Docker dang chay.
    echo.
)
