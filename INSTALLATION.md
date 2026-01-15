# Installation Guide

## Quick Installation Steps

### Method 1: Copy to Home Assistant

1. **Locate your Home Assistant configuration directory**
   - Typically located at `/config` or `~/.homeassistant`

2. **Create custom_components folder if it doesn't exist**
   ```bash
   mkdir -p /config/custom_components
   ```

3. **Copy the integration**
   ```bash
   cp -r custom_components/mojdomek /config/custom_components/
   ```

4. **Restart Home Assistant**
   - Go to Settings → System → Restart
   - Or use the CLI: `ha core restart`

5. **Add the integration**
   - Go to Settings → Devices & Services
   - Click "+ Add Integration"
   - Search for "MójDomek"
   - Enter your API ID from https://mojdomek.eu/api/api2.php?id=YOUR_ID

### Method 2: HACS Installation (When Published)

1. Open HACS
2. Go to "Integrations"
3. Click the menu (three dots) → "Custom repositories"
4. Add repository URL and select "Integration"
5. Find "MójDomek Septic Tank Monitor" and install
6. Restart Home Assistant
7. Add integration via Settings → Devices & Services

## Verifying Installation

After restarting Home Assistant, check the logs:

```bash
tail -f /config/home-assistant.log | grep mojdomek
```

You should see no errors. If the integration loads successfully, you'll be able to add it via the UI.

## Troubleshooting

### Integration not showing up
- Verify the folder structure: `/config/custom_components/mojdomek/`
- Check that `manifest.json` exists in the mojdomek folder
- Restart Home Assistant completely (not just reload)

### API ID not working
- Verify your API ID by testing it directly:
  ```bash
  curl "https://mojdomek.eu/api/api2.php?id=YOUR_API_ID"
  ```
- Ensure the response shows `"active": true` and has locations

### No sensors appearing
- Check that your account has active locations
- Verify the API response includes measurement data
- Check Home Assistant logs for errors

## Getting Your API ID

1. Log into your MójDomek account
2. Navigate to the API section or check your device settings
3. Your API URL will look like: `https://mojdomek.eu/api/api2.php?id=YOUR_ID`
4. The ID is the value after `id=` (in this example: `YOUR_ID`)

## Next Steps

Once installed and configured:
- View your devices under Settings → Devices & Services → MójDomek
- Add sensor cards to your dashboard
- Create automations for tank level alerts
- Monitor battery levels for maintenance planning
