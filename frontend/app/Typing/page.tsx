'use client';
import { useState, useEffect, useRef } from 'react';
import { useUser } from '@clerk/nextjs';

interface TypingResult {
  wpm: number;
  accuracy: number;
  test_duration: number;
  test_date: string;
}

export default function TypingPage() {
  const [text, setText] = useState('');
  const [timeLeft, setTimeLeft] = useState(60);
  const [isTyping, setIsTyping] = useState(false);
  const [wpm, setWpm] = useState(0);
  const [accuracy, setAccuracy] = useState(0);
  const [typingHistory, setTypingHistory] = useState<TypingResult[]>([]);
  const [showHistory, setShowHistory] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  
  const { isSignedIn } = useUser();
  
  const sampleText = "The quick brown fox jumps over the lazy dog. Programming is the art of telling another human what one wants the computer to do. The best way to predict the future is to invent it.";
  
  const inputRef = useRef<HTMLTextAreaElement>(null);

  // Save user info when the page loads
  useEffect(() => {
    if (isSignedIn) {
      // Save user info to the database
      fetch('/api/typing', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({}),
      }).catch(console.error);
      
      loadTypingHistory();
    }
  }, [isSignedIn]);

  const loadTypingHistory = async () => {
    if (!isSignedIn) return;
    
    try {
      setIsLoading(true);
      const response = await fetch('/api/typing');
      const data = await response.json();
      
      if (data.success) {
        setTypingHistory(data.results);
      } else {
        console.error('Error loading typing history:', data.error);
      }
    } catch (error) {
      console.error('Error loading typing history:', error);
    } finally {
      setIsLoading(false);
    }
  };

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
    
    // Save results to database if user is signed in
    if (isSignedIn) {
      fetch('/api/typing', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          wpm: newWpm,
          accuracy: newAccuracy,
          testDuration: 60 - timeLeft,
        }),
      })
        .then(() => loadTypingHistory())
        .catch(console.error);
    }
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

      {isSignedIn && (
        <div className="mt-8">
          <button
            onClick={() => setShowHistory(!showHistory)}
            className="w-full py-2 bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-white rounded-lg hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors mb-4"
          >
            {showHistory ? 'Hide History' : 'Show Typing History'}
          </button>
          
          {showHistory && (
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
              <h2 className="text-2xl font-bold mb-4 text-center text-gray-800 dark:text-white">
                Your Typing History
              </h2>
              
              {isLoading ? (
                <p className="text-center text-gray-600 dark:text-gray-400">Loading...</p>
              ) : typingHistory.length === 0 ? (
                <p className="text-center text-gray-600 dark:text-gray-400">No typing history found</p>
              ) : (
                <div className="overflow-x-auto">
                  <table className="w-full">
                    <thead>
                      <tr className="border-b dark:border-gray-700">
                        <th className="py-2 text-left text-gray-600 dark:text-gray-400">Date</th>
                        <th className="py-2 text-left text-gray-600 dark:text-gray-400">WPM</th>
                        <th className="py-2 text-left text-gray-600 dark:text-gray-400">Accuracy</th>
                        <th className="py-2 text-left text-gray-600 dark:text-gray-400">Duration</th>
                      </tr>
                    </thead>
                    <tbody>
                      {typingHistory.map((result, index) => (
                        <tr key={index} className="border-b dark:border-gray-700">
                          <td className="py-2 text-gray-800 dark:text-white">
                            {new Date(result.test_date).toLocaleDateString()}
                          </td>
                          <td className="py-2 text-gray-800 dark:text-white">{result.wpm}</td>
                          <td className="py-2 text-gray-800 dark:text-white">{result.accuracy}%</td>
                          <td className="py-2 text-gray-800 dark:text-white">{result.test_duration}s</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
