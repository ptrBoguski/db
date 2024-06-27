# Discord Bot

This project is a Discord bot built with Python and Docker. The bot can be deployed using Docker and supports multiple guilds with one channel per guild for notifications.

## How to Run

### 1. Create a `.env` File

Create a `.env` file in the project root directory and add the following line, replacing `your_discord_api_key_here` with your actual Discord API key:

```plaintext
DISCORD_API_KEY=your_discord_api_key_here
```

### 2. Run the Deployment Script
Make sure the `deploy.sh` script is executable. If it's not, you can make it executable with the following command:

```sh
chmod +x deploy.sh
```

Then, run the deployment script:

```sh
./deploy.sh
```

### 3. Invite the Bot to Your Discord Guild
Invite the bot to your Discord guild using the OAuth2 URL generated from the Discord Developer Portal. Make sure to give the bot the necessary permissions to read messages and send notifications.

### 4. Set the Notification Channel
After inviting the bot to your guild, set the channel where the bot will send notifications using the `/set_channel` command in the desired channel.

## Notes
- The bot supports multiple guilds but only one notification channel per guild.
- The database is currently stored inside the Docker container, so it will not persist if the container is removed.


