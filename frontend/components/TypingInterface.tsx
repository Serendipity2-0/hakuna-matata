import React, { useState, useEffect, useRef } from 'react';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';

const TIMER_DURATION = 30; // 30 seconds
const SAMPLE_TEXT = "The quick brown fox jumps over the lazy dog. Pack my box with five dozen liquor jugs. How vexingly quick daft zebras jump! Bright vixens jump; dozy fowl quack. Sphinx of black quartz, judge my vow.";

export default function ReconciliationInterface() {
  const [timeLeft, setTimeLeft] = useState(TIMER_DURATION);
  const [typedText, setTypedText] = useState('');
  const [isTestActive, setIsTestActive] = useState(false);
  const [wpm, setWpm] = useState(0);
  const intervalRef = useRef<NodeJS.Timeout | null>(null);
  const startTimeRef = useRef<number | null>(null);

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
    setIsTestActive(true);
    setTimeLeft(TIMER_DURATION);
    setTypedText('');
    setWpm(0);
    startTimeRef.current = Date.now();
  };

  const endTest = () => {
    setIsTestActive(false);
    if (intervalRef.current) clearInterval(intervalRef.current);
    calculateWPM();
  };

  const calculateWPM = () => {
    if (startTimeRef.current) {
      const timeElapsed = (Date.now() - startTimeRef.current) / 60000; // Convert to minutes
      const wordsTyped = typedText.trim().split(/\s+/).length;
      const calculatedWPM = Math.round(wordsTyped / timeElapsed);
      setWpm(calculatedWPM);
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
      <div className="mb-4">
        <p className="text-sm text-gray-600 mb-2">Type the following text:</p>
        <p className="bg-gray-100 p-3 rounded">{SAMPLE_TEXT}</p>
      </div>
      <Textarea
        value={typedText}
        onChange={handleTyping}
        disabled={!isTestActive}
        placeholder={isTestActive ? "Start typing here..." : "Click 'Start Test' to begin"}
        className="w-full h-32 mb-4"
      />
      <div className="flex justify-between items-center mb-4">
        <Button onClick={startTest} disabled={isTestActive}>
          Start Test
        </Button>
        <span className="text-lg font-semibold">
          Time Left: {timeLeft}s
        </span>
      </div>
      {wpm > 0 && (
        <div className="text-center">
          <p className="text-xl font-bold">Your typing speed:</p>
          <p className="text-3xl font-extrabold text-blue-600">{wpm} WPM</p>
        </div>
      )}
    </div>
  );
}
