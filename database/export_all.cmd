@echo off
REM =============================================================================
REM Export Database: App (Seed Data) & Metabase Dashboards
REM =============================================================================
REM Script nay export TOAN BO du lieu tu MySQL container bao gom:
REM  1. App Database (summary_paper) vao database_restore.sql
REM  2. Metabase App DB (metabase_appdb) vao metabase_restore.sql
REM =============================================================================

echo ============================================
echo   1/2: Exporting App Database (Seed Data)...
echo ============================================

docker exec summary_mysql sh -c "mysqldump -u root -proot --default-character-set=utf8mb4 --no-tablespaces summary_paper > /tmp/database_restore.sql"
docker cp summary_mysql:/tmp/database_restore.sql "%~dp0database_restore.sql"
if %ERRORLEVEL% NEQ 0 goto error_app

echo.
echo ============================================
echo   2/2: Exporting Metabase Dashboards...
echo ============================================

docker exec summary_mysql sh -c "mysqldump -u summary_user -psummary_pass --default-character-set=utf8mb4 --no-tablespaces --databases metabase_appdb > /tmp/metabase_restore.sql"
docker cp summary_mysql:/tmp/metabase_restore.sql "%~dp0metabase_restore.sql"
if %ERRORLEVEL% NEQ 0 goto error_meta

echo.
echo   ✅ Export THANH CONG ca 2 databases!
echo   - database\database_restore.sql
echo   - database\metabase_restore.sql
echo.
echo   Buoc tiep theo:
echo     git add database\database_restore.sql database\metabase_restore.sql
echo     git commit -m "chore: export databases"
echo     git push
echo.
exit /b 0

:error_app
echo.
echo   ❌ Export App Database that bai! Hay dam bao Docker dang chay.
echo.
exit /b 1

:error_meta
echo.
echo   ❌ Export Metabase that bai! Hay dam bao Docker dang chay.
echo.
exit /b 1
