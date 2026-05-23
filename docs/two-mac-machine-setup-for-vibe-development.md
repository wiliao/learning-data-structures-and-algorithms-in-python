# 🚀 The Distributed "Vibe Coding" Setup Guide

A comprehensive guide to building a high-performance, dual-machine local AI development environment.

This setup separates concerns cleanly: the M1 Max is your coding cockpit — VS Code, source code, Vibe Coding tools, Job Automation (Hermes), and the local LLM all live here. The Mac mini is a headless backend server — Docker, databases, and microservices run there and are accessed over the network. You never SSH into the Mini to edit code; you code locally and your app talks to the backend across Tailscale.

## 🏗️ Architecture Overview

```mermaid
graph TD
    subgraph "The Cockpit (MacBook Pro M1 Max - 64GB)"
        direction TB
        subgraph "Vibe Coding (Interactive Flow)"
            VC["Vibe Coding Tools\n(Copilot OR Claude Code)"] -->|Edits local source| B[Source Code]
        end

        subgraph "Job Automation (Background)"
            HM[Hermes Agent] -->|Automated Tasks| B
        end

        VC -.->|Cloud API| EXT[GitHub / Anthropic Cloud]
        VC -->|Local API| C
        HM -->|OpenAI API :8000/v1| C
        C[oMLX :8000\nQwen3-30B-A3B]

        B -->|App connects to backend| NET
    end

    subgraph "Tailscale Mesh"
        NET{Tailscale\nmac-mini}
    end

    subgraph "The Engine Room (Mac mini M4 - 16GB)"
        NET -->|:5432| D[PostgreSQL]
        NET -->|:6379| E[Redis]
        NET -->|:*| F[Docker / OrbStack Services]
        NET -->|:*| G[Microservices / CI]
    end
```

**Key principle:** Source code never leaves the M1 Max. The Mac mini exposes service ports over Tailscale; your local app connects to them exactly as it would connect to a cloud dev environment.

---

## 🛠️ Phase 1: The Engine Room (Mac mini M4)

_Goal: Turn the Mac mini into a headless, always-on backend server._

### 1. Enable Remote Access (Admin Only)

You will rarely need to log into the Mini directly, but enable SSH for occasional maintenance:

- **System Settings > General > Sharing**
- Toggle on **Remote Login (SSH)** — for admin tasks only, not for coding.

### 2. Prevent Sleep

The Mini must never sleep or your databases and containers will drop.

- **System Settings > Energy Saver:** Set "Prevent automatic sleeping when the display is off" to **ON**.

```bash
# Or lock it from the terminal
caffeinate -s &
```

### 3. Install the Backend Stack

```bash
# Install Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install OrbStack (Docker & Linux VM replacement) and essential CLI tools
# OrbStack is significantly faster than Docker Desktop, uses a fraction of RAM,
# and integrates natively with macOS networking
brew install orbstack git wget jq
```

### 4. Configure Services to Bind on All Interfaces

By default some services bind only to `127.0.0.1`. For Tailscale access from the M1 Max, they need to listen on `0.0.0.0` (or the Tailscale interface). Do this per-service in your `docker-compose.yml`:

```yaml
services:
  postgres:
    image: postgres:16
    ports:
      - "0.0.0.0:5432:5432" # Accessible over Tailscale
    environment:
      POSTGRES_PASSWORD: yourpassword

  redis:
    image: redis:7
    ports:
      - "0.0.0.0:6379:6379"
```

_Security note: Tailscale creates an encrypted private mesh — traffic on the `100.x.y.z` range is not exposed to the public internet. It is safe to bind services on `0.0.0.0` within this context, but never do this on a machine with a public IP without a firewall._

### 5. Start Services

```bash
docker compose up -d
# Verify services are reachable
docker ps
```

---

## 🧠 Phase 2: The Cockpit (MacBook Pro M1 Max)

_Goal: Optimise the laptop for local AI inference, Vibe Coding, and Job Automation — all source code lives here._

### 1. Install oMLX

[oMLX](https://github.com/jundot/omlx) is an MLX-native inference server built specifically for Apple Silicon. It runs on Apple's MLX framework, which treats CPU and GPU memory as a single unified pool — making it significantly faster than Metal-based alternatives on the same hardware, especially for MoE models.

**Option A — macOS App (recommended for menu bar management):**
Download the `.dmg` from [github.com/jundot/omlx/releases](https://github.com/jundot/omlx/releases), open it, and drag `oMLX.app` to `/Applications`.

**Option B — Homebrew (recommended for CLI + background service):**

```bash
# Add the oMLX tap and install
brew tap jundot/omlx https://github.com/jundot/omlx
brew install omlx

# Start as a background service (auto-restarts on crash)
brew services start omlx

# Verify the server is running
curl http://localhost:8000/health
```

_oMLX runs on port 8000 by default and exposes an OpenAI-compatible API at `http://localhost:8000/v1`._

### 2. Pull the Model

Open the admin dashboard at [http://localhost:8000/admin](http://localhost:8000/admin) and download the model:
**`mlx-community/Qwen3-30B-A3B-4bit`**

_Why this model? It is a Mixture-of-Experts (MoE) architecture — only 3B parameters are active per token. The KV cache costs ~48 KB/token, so a full 128k context occupies just ~6 GB of unified memory. This leaves the vast majority of your 64 GB free for the IDE, app runtime, and OS._

### 3. Configure oMLX Settings

In the admin dashboard under Global Settings:

| Setting                | Value | Reason                                                          |
| :--------------------- | :---- | :-------------------------------------------------------------- |
| **Max Context Window** | 128k  | KV cache at 128k costs only ~6 GB — fits with headroom to spare |
| **Max Tokens**         | 8k    | Sufficient for all code generation tasks                        |
| **Hot Cache Limit**    | 28 GB | 3× current typical usage; leaves safe OS headroom               |

### 4. Install the Vibe Coding & Automation Tools

Your project source code lives in a local directory on the M1 Max — for example `~/Projects/myapp`.

**The Vibe Coding Tools (Choose your flow):**
You need an interactive coding environment. You can choose the IDE-native route, the terminal-native route, or use both depending on the task.

```bash
# Option 1: The IDE Route (VS Code + GitHub Copilot)
brew install --cask visual-studio-code
# (Install the GitHub Copilot & Copilot Chat extensions from the VS Code marketplace)

# Option 2: The Terminal Route (Claude Code)
npm install -g @anthropic-ai/claude-code
```

**The Job Automation Tool (Hermes):**
Hermes is configured as a background Python/Node script that connects to oMLX to handle repetitive tasks (see Phase 4).

---

## 🔗 Phase 3: Connecting the Two Machines

_Goal: Make backend services on the Mac mini feel like local services to the app running on the M1 Max._

### 1. Install Tailscale on Both Machines

Install [Tailscale](https://tailscale.com/) on both machines and log in with the same account.

```bash
# Verify connectivity from the M1 Max
ping mac-mini
psql -h mac-mini -U postgres        # Postgres
redis-cli -h mac-mini ping          # Redis
```

### 2. Point Your App's Environment at the Mini

In your project on the M1 Max, create a `.env.local`:

```env
# .env.local (M1 Max — never commit this file)
DATABASE_URL=postgres://postgres:yourpassword@mac-mini:5432/mydb
REDIS_URL=redis://mac-mini:6379
API_BASE_URL=http://mac-mini:3001
```

### 3. Optional: Remote Docker Context for the Mini

If you want to manage the Mini's Docker containers from your M1 Max terminal without SSHing in:

```bash
ssh-keygen -t ed25519
ssh-copy-id your_username@mac-mini
docker context create engine --docker "host=ssh://mac-mini"
docker context use engine
```

---

## 💻 Phase 4: The Daily Workflow

### Tool Roles at a Glance

| Tool Category      | Choices                                              | Interaction Mode                                  | Backed by                                             |
| :----------------- | :--------------------------------------------------- | :------------------------------------------------ | :---------------------------------------------------- |
| **Vibe Coding**    | **VS Code + Copilot** <br> _OR_ <br> **Claude Code** | IDE Inline & Chat <br> _OR_ <br> Terminal Agentic | GitHub Cloud <br> _OR_ <br> oMLX (local) / Claude API |
| **Job Automation** | **Hermes Agent**                                     | Background Scripts                                | oMLX (local)                                          |

_Note: VS Code + Copilot and Claude Code serve the **exact same role** as your interactive Vibe Coding tools. They are simply two different interaction paradigms. Use VS Code + Copilot when you want to stay inside the editor UI with inline tabs and sidebar chat. Switch to Claude Code when you prefer a terminal-native, agentic flow that can traverse the file tree and execute commands. You can use either (or both) to stay in the flow state._

### Coding Session

1. Open your preferred Vibe Coding environment on the M1 Max.
2. **Vibe Coding:** Let Copilot handle inline suggestions in VS Code, or open your terminal and run `claude` for agentic multi-file refactors.
3. **App Runtime:** Run `npm run dev`. Your app talks to Postgres/Redis at `mac-mini` over Tailscale.
4. **Job Automation:** Trigger Hermes in the background to handle the boring stuff.

### Claude Code — Vibe Coding via oMLX

Route Claude Code through oMLX for offline, private vibe coding:

```bash
export ANTHROPIC_BASE_URL=http://127.0.0.1:8000
export ANTHROPIC_AUTH_TOKEN=your_omlx_api_key
claude
```

_Switch back to the official Claude API (`unset ANTHROPIC_BASE_URL`) when you hit genuinely hard architectural problems that require a frontier cloud model._

### Hermes Agent — Job Automation via oMLX

Hermes connects to oMLX's OpenAI-compatible endpoint to automate repetitive jobs in the background (e.g., "Generate docstrings for all new functions", "Write integration tests for the auth module").

```python
import openai

client = openai.OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="your_omlx_api_key"
)

response = client.chat.completions.create(
    model="mlx-community/Qwen3-30B-A3B-4bit",
    messages=[
        {"role": "system", "content": "You are an automated code-maintenance agent."},
        {"role": "user", "content": "Generate unit tests for the newly added auth module."}
    ]
)
```

_Hermes jobs run in the background on the M1 Max. oMLX handles concurrent requests via continuous batching — Hermes can generate tests in the background while you actively Vibe Code with Claude Code or Copilot in the foreground._

---

## 💡 Pro-Tips for the Vibe Coder

- **The Vibe Coding Stack:** Copilot and Claude Code are your flow-state tools. Copilot is for micro-interactions (autocomplete, quick questions). Claude Code is for macro-interactions (refactoring, terminal execution). They are two sides of the same Vibe Coding coin.
- **Offload the Chores to Hermes:** Don't waste your Vibe Coding context window on boilerplate. Let Hermes interact with the local LLM to generate your test suites, update your README, or format your JSON files in the background.
- **The "Brain Swap" Strategy:** Use local oMLX (Qwen3-30B) for 90% of your Vibe Coding and Automation. It's private, offline, and incredibly fast. Keep a cloud API key handy for the 10% of tasks that require massive reasoning capabilities.
- **No SSH for Code:** The Mini is an appliance. Keep all source on the M1 Max. This keeps your git history clean, your IDE fast, and your Vibe Coding tools' file access instant.
- **Resource Monitoring:** With Docker offloaded to the Mini, the M1 Max's memory pressure should stay in the green/yellow zone. The LLM, VS Code, and Hermes share the 64 GB unified pool without competition from containers.

---

## 💰 Hardware ROI Summary

| Machine                               | Role                                     | Cost (CAD)   |
| :------------------------------------ | :--------------------------------------- | :----------- |
| **MacBook Pro M1 Max 64 GB** (Refurb) | AI inference + Vibe Coding + Source Code | ~$2,379      |
| **Mac mini M4 16 GB** (New/Refurb)    | Docker + DB + Backend Services           | ~$800–$1,000 |
| **Total**                             |                                          | **~$3,300**  |

**Why this beats a single $4,000+ M3/M4 Max laptop:** Identical LLM generation speeds, superior backend compilation times (dedicated CPU on the Mini), zero thermal throttling on the laptop, backend stays running 24/7 without draining a battery, and a clean separation that scales.
