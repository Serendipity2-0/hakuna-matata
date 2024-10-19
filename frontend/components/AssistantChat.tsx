'use client';

import React, { useState, useEffect, useRef } from 'react';
import { v4 as uuidv4 } from 'uuid';

interface Message {
  id: string;
  content: string;
  sender: 'user' | 'assistant';
}

const AssistantChat: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isConnected, setIsConnected] = useState(false);
  const [wa_id, setWaId] = useState('');
  const websocketRef = useRef<WebSocket | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const newWaId = uuidv4();
    setWaId(newWaId);

    const ws = new WebSocket(`ws://localhost:8000/ws/assistant`);
    websocketRef.current = ws;

    ws.onopen = () => {
      setIsConnected(true);
      ws.send(JSON.stringify({ type: 'init', wa_id: newWaId, name: 'User' }));
    };

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.type === 'message') {
        setMessages((prevMessages) => [
          ...prevMessages,
          { id: uuidv4(), content: data.content, sender: 'assistant' },
        ]);
      }
    };

    ws.onclose = () => setIsConnected(false);

    return () => {
      ws.close();
    };
  }, []);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const sendMessage = () => {
    if (input.trim() && isConnected) {
      const newMessage: Message = { id: uuidv4(), content: input, sender: 'user' };
      setMessages((prevMessages) => [...prevMessages, newMessage]);
      websocketRef.current?.send(JSON.stringify({ type: 'message', content: input }));
      setInput('');
    }
  };

  const resetThread = () => {
    if (isConnected) {
      websocketRef.current?.send(JSON.stringify({ type: 'reset' }));
      setMessages([]);
    }
  };

  return (
    <div className="flex flex-col h-full bg-green-100 p-4 rounded-lg">
      <div className="flex-grow overflow-y-auto mb-4">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`mb-2 p-2 rounded ${
              message.sender === 'user' ? 'bg-blue-200 ml-auto' : 'bg-white'
            }`}
            style={{ maxWidth: '80%' }}
          >
            {message.content}
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>
      <div className="flex">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
          className="flex-grow mr-2 p-2 rounded"
          placeholder="Type your message..."
        />
        <button
          onClick={sendMessage}
          className="bg-blue-500 text-white px-4 py-2 rounded"
          disabled={!isConnected}
        >
          Send
        </button>
        <button
          onClick={resetThread}
          className="bg-red-500 text-white px-4 py-2 rounded ml-2"
          disabled={!isConnected}
        >
          Reset
        </button>
      </div>
    </div>
  );
};

export default AssistantChat;
