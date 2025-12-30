# Documentation Files

## Architecture Diagrams

This directory contains PlantUML source files for system architecture diagrams.

### Files

1. **architecture.puml** - High-level system architecture
2. **multi-agent-workflow.puml** - Multi-agent workflow sequence diagram
3. **SYSTEM_ARCHITECTURE.md** - Complete architecture documentation (2 pages)
4. **SAMPLE_INPUTS_OUTPUTS.md** - Sample inputs and outputs

### How to Generate Diagram Images

#### Option 1: Using PlantUML Online (Easiest)

1. Go to http://www.plantuml.com/plantuml/uml/
2. Copy the contents of `architecture.puml` or `multi-agent-workflow.puml`
3. Paste into the text box
4. Click "Submit"
5. Download as PNG or SVG

#### Option 2: Using draw.io (Recommended for Editing)

1. Go to https://app.diagrams.net/
2. Click **Arrange → Insert → Advanced → PlantUML**
3. Paste the contents of the `.puml` file
4. Click "Insert"
5. Edit as needed
6. Export as PNG/PDF: **File → Export as → PNG/PDF**

#### Option 3: Using VS Code (For Developers)

1. Install "PlantUML" extension in VS Code
2. Open the `.puml` file
3. Press `Alt+D` to preview
4. Right-click preview → "Export Current Diagram"
5. Save as PNG/SVG

#### Option 4: Using Command Line

```bash
# Install PlantUML (requires Java)
brew install plantuml

# Generate PNG images
plantuml docs/architecture.puml
plantuml docs/multi-agent-workflow.puml

# This creates:
# - docs/architecture.png
# - docs/multi-agent-workflow.png
```

### Compressing Videos

The demo videos are large. To compress them for GitHub:

```bash
# Install ffmpeg
brew install ffmpeg

# Compress Sago-website.mov (59.87 MB → ~20 MB)
ffmpeg -i Sago-website.mov -vcodec h264 -acodec aac -b:v 2000k Sago-website-compressed.mov

# Compress Sago-email.mov
ffmpeg -i Sago-email.mov -vcodec h264 -acodec aac -b:v 2000k Sago-email-compressed.mov
```

Or upload to:
- **YouTube** (unlisted)
- **Loom** (free screen recordings)
- **Google Drive** (share link)

### Using Diagrams in Documentation

After generating PNG images:

```markdown
# In README.md or SYSTEM_ARCHITECTURE.md

## System Architecture
![System Architecture](docs/architecture.png)

## Multi-Agent Workflow
![Multi-Agent Workflow](docs/multi-agent-workflow.png)
```

### For PDF Submission

To create the architecture PDF:

1. Open `SYSTEM_ARCHITECTURE.md` in VS Code
2. Install "Markdown PDF" extension
3. Right-click → "Markdown PDF: Export (pdf)"
4. Or use Pandoc:
   ```bash
   pandoc docs/SYSTEM_ARCHITECTURE.md -o SYSTEM_ARCHITECTURE.pdf
   ```

### Quick Links

- **PlantUML Online Editor:** http://www.plantuml.com/plantuml/uml/
- **draw.io:** https://app.diagrams.net/
- **PlantUML Documentation:** https://plantuml.com/
