'use client';
import { useState, useEffect, useRef } from 'react';

export default function TypingPage() {
  const [text, setText] = useState('');
  const [timeLeft, setTimeLeft] = useState(60);
  const [isTyping, setIsTyping] = useState(false);
  const [wpm, setWpm] = useState(0);
  const [accuracy, setAccuracy] = useState(0);
  
  const sampleText = "The quick brown fox jumps over the lazy dog. Programming is the art of telling another human what one wants the computer to do. The best way to predict the future is to invent it.";
  
  const inputRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    let timer: NodeJS.Timeout;
    if (isTyping && timeLeft > 0) {
      timer = setInterval(() => {
        setTimeLeft((prev) => prev - 1);
      }, 1000);
    } else if (timeLeft === 0) {
      calculateResults();
    }

    return () => clearInterval(timer);
  }, [isTyping, timeLeft]);

  const startTyping = () => {
    setText('');
    setTimeLeft(60);
    setIsTyping(true);
    setWpm(0);
    setAccuracy(0);
    if (inputRef.current) {
      inputRef.current.focus();
    }
  };

  const calculateResults = () => {
    const words = text.trim().split(' ').length;
    const newWpm = Math.round((words / (60 - timeLeft)) * 60);
    
    let correctChars = 0;
    const minLength = Math.min(text.length, sampleText.length);
    for (let i = 0; i < minLength; i++) {
      if (text[i] === sampleText[i]) correctChars++;
    }
    const newAccuracy = Math.round((correctChars / sampleText.length) * 100);

    setWpm(newWpm);
    setAccuracy(newAccuracy);
    setIsTyping(false);
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    if (!isTyping) return;
    setText(e.target.value);
  };

  return (
    <div className="container mx-auto p-6 max-w-3xl">
      <h1 className="text-3xl font-bold mb-8 text-center text-gray-800 dark:text-white">
        Typing Speed Test
      </h1>

      <div className="mb-6 p-4 bg-gray-100 dark:bg-gray-800 rounded-lg">
        <p className="text-lg text-gray-700 dark:text-gray-300 font-mono">
          {sampleText}
        </p>
      </div>

      <div className="mb-6 flex justify-between items-center">
        <div className="text-xl font-semibold text-gray-700 dark:text-gray-300">
          Time Left: {timeLeft}s
        </div>
        <button
          onClick={startTyping}
          className="px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors"
          disabled={isTyping}
        >
          Start Test
        </button>
      </div>

      <textarea
        ref={inputRef}
        value={text}
        onChange={handleInputChange}
        disabled={!isTyping}
        className="w-full h-32 p-4 mb-6 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-800 dark:text-white"
        placeholder="Start typing here..."
      />

      {!isTyping && wpm > 0 && (
        <div className="mt-8 p-6 bg-white dark:bg-gray-800 rounded-lg shadow-lg">
          <h2 className="text-2xl font-bold mb-4 text-center text-gray-800 dark:text-white">
            Results
          </h2>
          <div className="grid grid-cols-2 gap-4">
            <div className="text-center">
              <p className="text-gray-600 dark:text-gray-400">Words per Minute</p>
              <p className="text-3xl font-bold text-blue-500">{wpm}</p>
            </div>
            <div className="text-center">
              <p className="text-gray-600 dark:text-gray-400">Accuracy</p>
              <p className="text-3xl font-bold text-green-500">{accuracy}%</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
