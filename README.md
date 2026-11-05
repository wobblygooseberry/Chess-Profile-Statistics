# Chess Profile Statistics Discord Bot

A Python-based Discord bot that integrates with the [Lichess API](https://lichess.org/api) to retrieve and analyze chess player statistics directly through Discord slash commands.

The bot allows users to look up chess performance across different time controls, filter game results, and retrieve puzzle ratings.

## Features

### Chess Game Statistics — `/chess`

Retrieve the number of wins, losses, or draws for a specified Lichess player.

Supported filters:

- **Username:** Any valid Lichess username
- **Color:** White or Black
- **Time Control:** Bullet, Blitz, Rapid, Classical, Ultrabullet, or Correspondence
- **Variant:** Standard chess
- **Result:** Win, Loss, or Draw
- **Game Mode:** Rated, Unrated, or All

Example command:

`/chess username:DrNykterstein color:white format:bullet result:win mode:all`

Example output:

`DrNykterstein: 3441 win(s) as white in bullet`

### Puzzle Statistics — `/puzzles`

Retrieve a player's current Lichess puzzle rating and total number of puzzles played.

Example command:

`/puzzles username:Nigeriann`

Example output:

```text
Nigeriann's puzzle rating: 2315
Puzzles played: 56871
```

## Technologies Used

- **Python** — Core application and statistics processing
- **discord.py** — Discord bot integration and slash commands
- **Berserk** — Python client for the Lichess API
- **Requests** — HTTP session management
- **asyncio** — Asynchronous command handling
- **python-dotenv** — Environment variable management

## Project Structure

```text
chess_profile_stats/
├── src/
│   ├── bot.py          # Discord commands and interactions
│   ├── lichess.py      # Lichess API client configuration
│   └── stats.py        # Chess statistics and filtering logic
├── .gitignore
├── .env                # Local credentials (not uploaded)
└── README.md
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/wobblygooseberry/Chess-Profile-Statistics.git
cd Chess-Profile-Statistics
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install discord.py berserk requests python-dotenv
```

### 4. Configure the Discord bot

Create a Discord application and bot through the [Discord Developer Portal](https://discord.com/developers/applications).

Create a `.env` file in the project root:

```env
DISCORD_TOKEN=your_discord_bot_token
```

Never share or commit your actual Discord token.

Invite the bot to your Discord server with the necessary bot and application command permissions.

### 5. Run the bot

```bash
python src/bot.py
```

Once the bot is online and its commands are synchronized, use `/chess` or `/puzzles` in your Discord server.

## How It Works

1. A user submits a slash command through Discord.
2. The bot validates the requested parameters.
3. The application requests player information or game history from the Lichess API.
4. For game statistics, the backend filters games by color, time control, variant, rated status, and result.
5. The bot calculates the requested statistic and sends the result back to Discord.

Blocking API operations are executed using `asyncio.to_thread()` to avoid blocking the Discord event loop.

## Known Limitations

- **Performance:** Requests involving accounts with extensive game histories may take several minutes because the application processes exported games.
- **Caching:** Game statistics are recalculated for each request; caching has not yet been implemented.
- **Variants:** Game statistics currently support standard chess only.
- **Availability:** The bot must be running to respond to Discord commands. It is not currently hosted as an always-on service.

## Potential Future Improvements

- Implement caching to reduce repeated API requests.
- Optimize game-history retrieval and processing.
- Add support for additional chess variants.
- Improve response formatting with Discord embeds.
- Add automated tests.
- Deploy the bot for continuous availability.

## Project Status

**Version 1.0 — Functional prototype**

This project was developed to gain hands-on experience with Python backend development, REST API integration, asynchronous programming, and Discord bot development.

The primary goal was to build a functional application that retrieves and processes real-world chess data.
