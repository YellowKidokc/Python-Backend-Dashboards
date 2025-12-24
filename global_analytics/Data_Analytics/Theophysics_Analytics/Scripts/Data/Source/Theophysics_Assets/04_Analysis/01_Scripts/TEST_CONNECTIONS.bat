@echo off
echo ============================================================
echo  Testing Connections - Cloudflare + PostgreSQL
echo ============================================================
echo.

cd /d "%~dp0"

python -c "from cloudflare_connector import CloudflareConnector, get_cloudflare_config; from postgres_connector import PostgresConnector; print('\n🌐 Cloudflare:'); config = get_cloudflare_config(); connector = CloudflareConnector(config.get('api_token'), config.get('account_id')) if config.get('api_token') else None; print('✅ Connected' if connector and connector.test_connection() else '❌ Not configured'); print('\n🗄️  PostgreSQL:'); pg = PostgresConnector(); print('✅ Connected' if pg.test_connection() else '❌ Not configured')"

echo.
echo Done!
pause

