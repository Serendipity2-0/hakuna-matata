import { cn } from '@/lib/utils';

interface ChatMessageProps {
  message: {
    role: 'user' | 'assistant';
    content: string;
  };
}

export default function ChatMessage({ message }: ChatMessageProps) {
  return (
    <div
      className={cn(
        'mb-4 p-3 rounded-lg',
        message.role === 'user' ? 'bg-primary/20 ml-auto' : 'bg-secondary'
      )}
    >
      <p className="text-sm font-semibold mb-1 text-primary">
        {message.role === 'user' ? 'You' : 'AI Assistant'}
      </p>
      <p className="text-foreground">{message.content}</p>
    </div>
  );
}