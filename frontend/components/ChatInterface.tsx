'use client';

import ChatMessage from '@/components/ChatMessage';
import HumanReviewModal from '@/components/HumanReviewModal';
import { Button } from '@/components/ui/button';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Textarea } from '@/components/ui/textarea';
import WorkingDirectoryModal from '@/components/WorkingDirectoryModal';
import { useState } from 'react';

const roles = ['Admin', 'Manager', 'Executive'];
const departments = ['Serendipity', 'Dhoom Studios', 'TradeMan'];
const tools = ['RepoInfo', 'GitCommitter'];

/**
 * Defines the structure of a chat message
 */
type ChatMessageType = {
  role: 'user' | 'assistant';
  content: string;
};

/**
 * ChatInterface component
 * 
 * This component represents the main chat interface of the application.
 * It handles user input, message display, and integration with various modals.
 */
export default function ChatInterface() {
  const [role, setRole] = useState<string>('');
  const [department, setDepartment] = useState<string>('');
  const [tool, setTool] = useState<string>('');
  const [taskSummary, setTaskSummary] = useState<string>('');
  const [messages, setMessages] = useState<ChatMessageType[]>([]);
  const [input, setInput] = useState<string>('');
  const [isHumanReviewOpen, setIsHumanReviewOpen] = useState<boolean>(false);
  const [pendingMessage, setPendingMessage] = useState<string>('');
  const [isWorkingDirectoryModalOpen, setIsWorkingDirectoryModalOpen] = useState<boolean>(false);
  const [workingDirectory, setWorkingDirectory] = useState<string>('');

  /**
   * Handles sending a new message
   */
  const handleSendMessage = async () => {
    if (!input.trim()) return;

    const newMessage: ChatMessageType = { role: 'user', content: input };
    setMessages((prevMessages) => [...prevMessages, newMessage]);
    console.log('User message sent:', input);

    // Simulate AI response
    const aiResponse: ChatMessageType = { role: 'assistant', content: `AI response to: ${input}` };
    
    // Check if human review is needed (you can implement your own logic here)
    if (Math.random() > 0.7) {
      console.log('Human review required for AI response');
      setPendingMessage(aiResponse.content);
      setIsHumanReviewOpen(true);
    } else {
      console.log('AI response added without review');
      setMessages((prevMessages) => [...prevMessages, aiResponse]);
    }

    setInput('');
  };

  /**
   * Handles the completion of human review
   * @param approvedMessage - The approved message content
   */
  const handleHumanReviewComplete = (approvedMessage: string) => {
    const reviewedMessage: ChatMessageType = { role: 'assistant', content: approvedMessage };
    setMessages((prevMessages) => [...prevMessages, reviewedMessage]);
    setIsHumanReviewOpen(false);
    setPendingMessage('');
    console.log('Human review completed, message added:', approvedMessage);
  };

  /**
   * Handles the selection of a working directory
   * @param directory - The selected working directory
   */
  const handleWorkingDirectorySelect = (directory: string) => {
    setWorkingDirectory(directory);
    setIsWorkingDirectoryModalOpen(false);
    console.log('Working directory selected:', directory);
  };

  return (
    <div className="flex flex-col space-y-4">
      <div className="flex space-x-4">
        <Select onValueChange={setRole}>
          <SelectTrigger className="w-[200px] bg-secondary text-secondary-foreground">
            <SelectValue placeholder="Select role" />
          </SelectTrigger>
          <SelectContent>
            {roles.map((r) => (
              <SelectItem key={r} value={r}>{r}</SelectItem>
            ))}
          </SelectContent>
        </Select>
        <Select onValueChange={setDepartment}>
          <SelectTrigger className="w-[200px] bg-secondary text-secondary-foreground">
            <SelectValue placeholder="Select department" />
          </SelectTrigger>
          <SelectContent>
            {departments.map((d) => (
              <SelectItem key={d} value={d}>{d}</SelectItem>
            ))}
          </SelectContent>
        </Select>
        <Select onValueChange={setTool}>
          <SelectTrigger className="w-[200px] bg-secondary text-secondary-foreground">
            <SelectValue placeholder="Select tool" />
          </SelectTrigger>
          <SelectContent>
            {tools.map((t) => (
              <SelectItem key={t} value={t}>{t}</SelectItem>
            ))}
          </SelectContent>
        </Select>
        <Button 
          onClick={() => setIsWorkingDirectoryModalOpen(true)}
          className="bg-secondary text-secondary-foreground hover:bg-secondary/90"
        >
          Select Working Directory
        </Button>
      </div>
      {workingDirectory && (
        <div className="text-sm text-muted-foreground">
          Working Directory: {workingDirectory}
        </div>
      )}
      <Textarea
        placeholder="Enter task summary"
        value={taskSummary}
        onChange={(e) => setTaskSummary(e.target.value)}
        className="bg-secondary text-secondary-foreground"
      />
      <div className="border rounded-lg p-4 h-[400px] overflow-y-auto bg-secondary/30">
        {messages.map((message, index) => (
          <ChatMessage key={index} message={message} />
        ))}
      </div>
      <div className="flex space-x-2">
        <Textarea
          placeholder="Type your message..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          className="flex-grow bg-secondary text-secondary-foreground"
        />
        <Button onClick={handleSendMessage} className="bg-primary text-primary-foreground hover:bg-primary/90">Send</Button>
      </div>
      <HumanReviewModal
        isOpen={isHumanReviewOpen}
        onClose={() => setIsHumanReviewOpen(false)}
        pendingMessage={pendingMessage}
        onApprove={handleHumanReviewComplete}
      />
      <WorkingDirectoryModal
        isOpen={isWorkingDirectoryModalOpen}
        onClose={() => setIsWorkingDirectoryModalOpen(false)}
        onSelect={handleWorkingDirectorySelect}
      />
    </div>
  );
}
