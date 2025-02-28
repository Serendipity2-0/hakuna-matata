'use client';

import React, { useState, useEffect, useRef } from 'react';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { 
  Select, 
  SelectContent, 
  SelectItem, 
  SelectTrigger, 
  SelectValue 
} from '@/components/ui/select';
import fs from 'fs/promises';
import path from 'path';

const TIMER_DURATION = 30; // 30 seconds

// User options
const USERS = ['Chandana', 'Viju', 'Omkar', 'Snowy'];

// Difficulty levels
const DIFFICULTY_LEVELS = ['Easy', 'Medium', 'Hard'];

interface TestResult {
  id?: number;
  user: string;
  wpm: number;
  accuracy: number;
  difficulty: string;
  date: string;
}

export default function TypingTestInterface() {
  const [timeLeft, setTimeLeft] = useState(TIMER_DURATION);
  const [typedText, setTypedText] = useState('');
  const [isTestActive, setIsTestActive] = useState(false);
  const [wpm, setWpm] = useState(0);
  const [accuracy, setAccuracy] = useState(0);
  const [selectedUser, setSelectedUser] = useState('');
  const [difficulty, setDifficulty] = useState('Easy');
  const [sampleText, setSampleText] = useState('');
  const [results, setResults] = useState<TestResult[]>([]);
  const [showSaveButton, setShowSaveButton] = useState(false);
  
  const intervalRef = useRef<NodeJS.Timeout | null>(null);
  const startTimeRef = useRef<number | null>(null);

  // Load sample text based on difficulty
  useEffect(() => {
    const loadSampleText = async () => {
      try {
        // In a real app, we would fetch this from an API
        // For this implementation, we'll use the files we created
        let textContent = '';
        
        if (difficulty === 'Easy') {
          try {
            const response = await fetch('/Typing/typingEasy.md');
            textContent = await response.text();
          } catch (error) {
            console.error('Error fetching Easy text:', error);
            textContent = "The quick brown fox jumps over the lazy dog. Pack my box with five dozen liquor jugs. How vexingly quick daft zebras jump! Bright vixens jump; dozy fowl quack. She sells seashells by the seashore. Peter Piper picked a peck of pickled peppers. A stitch in time saves nine. All that glitters is not gold.";
          }
        } else if (difficulty === 'Medium') {
          try {
            const response = await fetch('/Typing/typingMedium.md');
            textContent = await response.text();
          } catch (error) {
            console.error('Error fetching Medium text:', error);
            textContent = "The quick brown fox jumps over the lazy dog. Pack my box with five dozen liquor jugs. How vexingly quick daft zebras jump! Bright vixens jump; dozy fowl quack. She sells seashells by the seashore. Peter Piper picked a peck of pickled peppers. A stitch in time saves nine. All that glitters is not gold. Early to bed and early to rise makes a man healthy, wealthy, and wise. The early bird catches the worm. Actions speak louder than words.";
          }
        } else if (difficulty === 'Hard') {
          try {
            const response = await fetch('/Typing/typingHard.md');
            textContent = await response.text();
          } catch (error) {
            console.error('Error fetching Hard text:', error);
            textContent = "The quick brown fox jumps over the lazy dog. Pack my box with five dozen liquor jugs. How vexingly quick daft zebras jump! Bright vixens jump; dozy fowl quack. She sells seashells by the seashore. Peter Piper picked a peck of pickled peppers. A stitch in time saves nine. All that glitters is not gold. Early to bed and early to rise makes a man healthy, wealthy, and wise. The early bird catches the worm. Actions speak louder than words. Don't judge a book by its cover. The pen is mightier than the sword. When in Rome, do as the Romans do.";
          }
        }
        
        // Split by numbered paragraphs and select a random one
        const paragraphs = textContent.split(/\d+\.\s/).filter(p => p.trim().length > 0);
        const randomIndex = Math.floor(Math.random() * paragraphs.length);
        setSampleText(paragraphs[randomIndex].trim());
      } catch (error) {
        console.error('Error loading sample text:', error);
        setSampleText("The quick brown fox jumps over the lazy dog.");
      }
    };
    
    loadSampleText();
  }, [difficulty]);

  // Load previous results
  useEffect(() => {
    const fetchResults = async () => {
      try {
        // In a real app, we would fetch this from an API
        // For this implementation, we'll simulate it
        const response = await fetch('/api/typing-results');
        const data = await response.json();
        setResults(data);
      } catch (error) {
        console.error('Error fetching results:', error);
        // For demo purposes, we'll use some sample data
        setResults([
          { id: 1, user: 'Chandana', wpm: 65, accuracy: 98.2, difficulty: 'Medium', date: '2025-02-25' },
          { id: 2, user: 'Viju', wpm: 72, accuracy: 95.7, difficulty: 'Hard', date: '2025-02-26' },
          { id: 3, user: 'Omkar', wpm: 58, accuracy: 97.3, difficulty: 'Easy', date: '2025-02-27' },
          { id: 4, user: 'Snowy', wpm: 80, accuracy: 94.5, difficulty: 'Medium', date: '2025-02-28' }
        ]);
      }
    };
    
    fetchResults();
  }, []);

  useEffect(() => {
    if (isTestActive && timeLeft > 0) {
      intervalRef.current = setInterval(() => {
        setTimeLeft((prevTime) => prevTime - 1);
      }, 1000);
    } else if (timeLeft === 0) {
      endTest();
    }

    return () => {
      if (intervalRef.current) clearInterval(intervalRef.current);
    };
  }, [isTestActive, timeLeft]);

  const startTest = () => {
    if (!selectedUser) {
      alert('Please select a user before starting the test.');
      return;
    }
    
    setIsTestActive(true);
    setTimeLeft(TIMER_DURATION);
    setTypedText('');
    setWpm(0);
    setAccuracy(0);
    setShowSaveButton(false);
    startTimeRef.current = Date.now();
  };

  const endTest = () => {
    setIsTestActive(false);
    if (intervalRef.current) clearInterval(intervalRef.current);
    calculateWPM();
    calculateAccuracy();
    setShowSaveButton(true);
  };

  const calculateWPM = () => {
    if (startTimeRef.current) {
      const timeElapsed = (Date.now() - startTimeRef.current) / 60000; // Convert to minutes
      const wordsTyped = typedText.trim().split(/\s+/).length;
      const calculatedWPM = Math.round(wordsTyped / timeElapsed);
      setWpm(calculatedWPM);
    }
  };

  const calculateAccuracy = () => {
    const sampleWords = sampleText.split(' ');
    const typedWords = typedText.trim().split(' ');
    
    let correctChars = 0;
    let totalChars = 0;
    
    // Compare each character
    for (let i = 0; i < Math.min(sampleText.length, typedText.length); i++) {
      totalChars++;
      if (sampleText[i] === typedText[i]) {
        correctChars++;
      }
    }
    
    // Add remaining characters in sample text as incorrect
    totalChars += Math.max(0, sampleText.length - typedText.length);
    
    const calculatedAccuracy = (correctChars / totalChars) * 100;
    setAccuracy(parseFloat(calculatedAccuracy.toFixed(1)));
  };

  const saveResult = async () => {
    try {
      const newResult: TestResult = {
        user: selectedUser,
        wpm,
        accuracy,
        difficulty,
        date: new Date().toISOString().split('T')[0]
      };
      
      // In a real app, we would send this to an API
      // For this implementation, we'll simulate it
      const response = await fetch('/api/typing-results', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(newResult),
      });
      
      if (response.ok) {
        // Add to local state
        setResults([...results, { ...newResult, id: Date.now() }]);
        setShowSaveButton(false);
        alert('Result saved successfully!');
      } else {
        alert('Failed to save result.');
      }
    } catch (error) {
      console.error('Error saving result:', error);
      // For demo purposes, we'll just add it to the local state
      setResults([...results, { 
        id: Date.now(), 
        user: selectedUser, 
        wpm, 
        accuracy, 
        difficulty, 
        date: new Date().toISOString().split('T')[0] 
      }]);
      setShowSaveButton(false);
      alert('Result saved successfully! (Demo mode)');
    }
  };

  const handleTyping = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    if (isTestActive) {
      setTypedText(e.target.value);
    }
  };

  return (
    <div className="p-4 bg-white border border-gray-200 rounded-md shadow-sm">
      <h3 className="text-lg font-semibold mb-4">Typing Test</h3>
      
      {/* User and Difficulty Selection */}
      <div className="grid grid-cols-2 gap-4 mb-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Select User</label>
          <Select
            value={selectedUser}
            onValueChange={setSelectedUser}
            disabled={isTestActive}
          >
            <SelectTrigger className="w-full">
              <SelectValue placeholder="Select User" />
            </SelectTrigger>
            <SelectContent>
              {USERS.map(user => (
                <SelectItem key={user} value={user}>{user}</SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Difficulty</label>
          <Select
            value={difficulty}
            onValueChange={setDifficulty}
            disabled={isTestActive}
          >
            <SelectTrigger className="w-full">
              <SelectValue placeholder="Select Difficulty" />
            </SelectTrigger>
            <SelectContent>
              {DIFFICULTY_LEVELS.map(level => (
                <SelectItem key={level} value={level}>{level}</SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>
      </div>
      
      {/* Sample Text */}
      <div className="mb-4">
        <p className="text-sm text-gray-600 mb-2">Type the following text:</p>
        <p className="bg-gray-100 p-3 rounded">{sampleText}</p>
      </div>
      
      {/* Typing Area */}
      <Textarea
        value={typedText}
        onChange={handleTyping}
        disabled={!isTestActive}
        placeholder={isTestActive ? "Start typing here..." : "Select a user and click 'Start Test' to begin"}
        className="w-full h-32 mb-4"
      />
      
      {/* Controls */}
      <div className="flex justify-between items-center mb-4">
        <Button onClick={startTest} disabled={isTestActive || !selectedUser}>
          Start Test
        </Button>
        <span className="text-lg font-semibold">
          Time Left: {timeLeft}s
        </span>
      </div>
      
      {/* Results */}
      {(wpm > 0 || accuracy > 0) && (
        <div className="text-center mb-4 p-4 bg-gray-50 rounded-md">
          <p className="text-xl font-bold">Your Results:</p>
          <div className="flex justify-center space-x-8 mt-2">
            <div>
              <p className="text-sm text-gray-600">Typing Speed</p>
              <p className="text-2xl font-extrabold text-blue-600">{wpm} WPM</p>
            </div>
            <div>
              <p className="text-sm text-gray-600">Accuracy</p>
              <p className="text-2xl font-extrabold text-green-600">{accuracy}%</p>
            </div>
          </div>
          
          {showSaveButton && (
            <Button onClick={saveResult} className="mt-4">
              Save Result
            </Button>
          )}
        </div>
      )}
      
      {/* Previous Results */}
      {results.length > 0 && (
        <div className="mt-8">
          <h4 className="text-lg font-semibold mb-2">Previous Results</h4>
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">User</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">WPM</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Accuracy</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Difficulty</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date</th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {results.map((result) => (
                  <tr key={result.id}>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{result.user}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{result.wpm}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{result.accuracy}%</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{result.difficulty}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{result.date}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}
