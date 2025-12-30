# Google Apps Script - Gmail Monitor

This directory contains the Google Apps Script code for automatically monitoring Gmail for pitch deck PDFs.

## Files

- **Code.gs** - Main script file (copy this to Google Apps Script editor)
- **appsscript.json** - Manifest file with OAuth scopes

## How to Use

1. Go to https://script.google.com
2. Create a new project: "Sago Gmail Monitor"
3. Copy the contents of `Code.gs` into the script editor
4. Enable the manifest file and copy `appsscript.json` contents
5. Run the script to authorize permissions
6. Set up a 5-minute trigger

See the main [GOOGLE_APPS_SCRIPT_SETUP.md](../GOOGLE_APPS_SCRIPT_SETUP.md) for detailed instructions.

## Current Configuration

- **Backend URL:** `https://nine-rabbits-grin.loca.lt` (localtunnel - temporary)
- **Gmail:** collegePracticals118@gmail.com
- **Label:** Sago/Analyzed

## Trigger Phrases

The script only processes emails containing:
- "hey sago"
- "sago analyze"
- "analyze this pitch deck"
- "analyze pitch deck"
- "sago please analyze"

## Features

✅ Automatic email monitoring every 5 minutes
✅ Trigger phrase detection (prevents processing random PDFs)
✅ Beautiful HTML email replies with analysis results
✅ Automatic labeling (Sago/Analyzed)
✅ Prevents duplicate processing
✅ Multi-agent analysis with web search verification
