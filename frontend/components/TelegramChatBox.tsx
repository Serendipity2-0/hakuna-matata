'use client';

import React, { useState, useEffect, useCallback } from 'react';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { MessageCircle, Send, X } from 'lucide-react';
import EditableMarkdown from '@/components/EditableMarkdown';
import { useKeyboardShortcuts } from '@/hooks/useKeyboardShortcuts';

const baseUrl = process.env.NEXT_PUBLIC_BASE_URL;

export default function TelegramChatBox() {
  const [isOpen, setIsOpen] = useState(false);
  const [message, setMessage] = useState('');
  const [response, setResponse] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const openTelegramBubble = useCallback(() => {
    setIsOpen(true);
  }, []);

  const closeTelegramBubble = useCallback(() => {
    setIsOpen(false);
  }, []);

  useEffect(() => {
    window.addEventListener('openTelegramBubble', openTelegramBubble);
    return () => {
      window.removeEventListener('openTelegramBubble', openTelegramBubble);
    };
  }, [openTelegramBubble]);

  useKeyboardShortcuts({
    resetToHome: () => {}, // No-op for this component
    openTelegramBubble,
    closeModal: closeTelegramBubble,
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);

    try {
      const res = await fetch(`${baseUrl}/api/eod_message`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ eod_messages: message }),
      });

      if (!res.ok) {
        throw new Error('Failed to send message');
      }

      const data = await res.json();
      setResponse(data.eod_telegram_message);
    } catch (error) {
      console.error('Error sending message:', error);
      setResponse('Failed to send message. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <>
      <Button
        className="fixed bottom-4 right-4 rounded-full w-16 h-16 shadow-lg"
        onClick={openTelegramBubble}
      >
        <MessageCircle size={24} />
      </Button>

      {isOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <Card className="w-full max-w-md mx-4">
            <CardHeader className="flex flex-row items-center justify-between">
              <CardTitle>Telegram Chat</CardTitle>
              <Button variant="ghost" size="sm" onClick={closeTelegramBubble}>
                <X size={24} />
              </Button>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleSubmit} className="space-y-4">
                <Textarea
                  value={message}
                  onChange={(e) => setMessage(e.target.value)}
                  placeholder="Type your message here..."
                  className="w-full h-32"
                />
                <Button type="submit" disabled={isLoading} className="w-full">
                  {isLoading ? 'Sending...' : 'Send'}
                  <Send size={16} className="ml-2" />
                </Button>
              </form>
              {response && (
                <div className="mt-4">
                  <h3 className="text-lg font-semibold mb-2">Response:</h3>
                  <EditableMarkdown content={response} onChange={setResponse} />
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      )}
    </>
  );
}
