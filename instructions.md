# Typing Test Component Improvements

## 1. Discord Integration

### Setup Requirements
1. Create a Discord Application and Bot
   - Go to Discord Developer Portal (https://discord.com/developers/applications)
   - Create a new application
   - Add a bot to your application
   - Save the Bot Token and Client ID
   - Enable necessary OAuth2 scopes (bot, applications.commands)

2. Required Dependencies
   ```bash
   npm install discord.js @prisma/client
   ```

### Implementation Steps

#### 1. Create Discord Configuration
Create a new file `config/discord.ts`:
```typescript
export const DISCORD_CONFIG = {
  clientId: process.env.DISCORD_CLIENT_ID,
  botToken: process.env.DISCORD_BOT_TOKEN,
  webhookUrl: process.env.DISCORD_WEBHOOK_URL,
  resultChannelId: process.env.DISCORD_RESULT_CHANNEL_ID
};
```

#### 2. Create Discord Service
Create a new file `services/discord.ts`:
```typescript
import { WebhookClient } from 'discord.js';
import { DISCORD_CONFIG } from '@/config/discord';

export class DiscordService {
  private webhook: WebhookClient;

  constructor() {
    this.webhook = new WebhookClient({ url: DISCORD_CONFIG.webhookUrl });
  }

  async sendTypingResult(username: string, wpm: number, accuracy: number) {
    const embed = {
      title: '🎯 New Typing Test Result!',
      color: 0x00ff00,
      fields: [
        { name: 'User', value: username, inline: true },
        { name: 'WPM', value: wpm.toString(), inline: true },
        { name: 'Accuracy', value: `${accuracy}%`, inline: true }
      ],
      timestamp: new Date().toISOString()
    };

    await this.webhook.send({ embeds: [embed] });
  }
}
```

## 2. Dynamic Content System

### Database Schema
Add the following to your Prisma schema:

```prisma
model TypingContent {
  id          Int      @id @default(autoincrement())
  content     String
  difficulty  String   @default("medium")
  category    String
  language    String   @default("en")
  createdAt   DateTime @default(now())
  updatedAt   DateTime @updatedAt
}

model TypingResult {
  id        Int      @id @default(autoincrement())
  userId    String
  wpm       Int
  accuracy  Float
  contentId Int
  createdAt DateTime @default(now())
  content   TypingContent @relation(fields: [contentId], references: [id])
}
```

### Implementation Changes

#### 1. Create Content Service
Create a new file `services/content.ts`:
```typescript
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

export class ContentService {
  async getRandomContent(difficulty?: string, category?: string) {
    return await prisma.typingContent.findFirst({
      where: {
        difficulty: difficulty,
        category: category
      },
      orderBy: {
        random: true
      }
    });
  }

  async saveResult(result: {
    userId: string;
    wpm: number;
    accuracy: number;
    contentId: number;
  }) {
    return await prisma.typingResult.create({
      data: result
    });
  }
}
```

## 3. Component Modifications

Update the Typing Test component to include:

1. User authentication state
2. Dynamic content loading
3. Accuracy calculation
4. Discord result sharing
5. Progress tracking

### Key Features to Add:

1. User Authentication Integration
2. Content Difficulty Selection
3. Category Selection
4. Result History
5. Personal Best Tracking
6. Share to Discord Button
7. Accuracy Calculation
8. Real-time Progress Indicator
9. Error Highlighting
10. Practice Mode vs. Test Mode

## 4. Environment Variables

Add the following to your `.env` file:
```
DISCORD_CLIENT_ID=your_client_id
DISCORD_BOT_TOKEN=your_bot_token
DISCORD_WEBHOOK_URL=your_webhook_url
DISCORD_RESULT_CHANNEL_ID=your_channel_id
DATABASE_URL=your_database_url
```

## 5. Security Considerations

1. Implement rate limiting for typing tests
2. Validate typing results server-side
3. Secure Discord webhook URL
4. Implement user authentication
5. Add CSRF protection
6. Sanitize user inputs

## Next Steps

1. Set up the database using Prisma
2. Configure Discord bot and webhook
3. Implement user authentication
4. Create the content management system
5. Update the typing test component
6. Add result tracking and analytics
7. Implement sharing functionality
8. Add error handling and validation
9. Create admin interface for content management
10. Set up monitoring and analytics 