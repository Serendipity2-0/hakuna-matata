'use client';

import React, { useState, useEffect } from 'react';
import { Calendar } from '../../components/Calendar';
import { ContentPost } from '../../types/calendar';
import '../ContentCalendar/styles.css';

// Transform database data to ContentPost format
const transformDatabaseData = (data: any[]): ContentPost[] => {
  return data.map(item => ({
    serialNo: item.id || item.serialNo || 0,
    date: item.date || '',
    contentType: item.content_type || item.contentType || '',
    format: item.format || '',
    platform: item.platform || '',
    scheduleTime: item.schedule_time || item.scheduleTime || ''
  }));
};

export default function ContentCalendarPage() {
  const [posts, setPosts] = useState<ContentPost[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        // Fetch data from our API endpoint
        const response = await fetch('/api/calendar-data');
        
        if (!response.ok) {
          throw new Error(`API error: ${response.status}`);
        }
        
        const result = await response.json();
        console.log('API response:', result); // For debugging
        
        // Transform the data based on the structure we received
        const transformedData = transformDatabaseData(result.data || []);
        setPosts(transformedData);
        setError(null);
      } catch (err) {
        console.error('Error fetching calendar data:', err);
        setError('Failed to load calendar data. Please try again later.');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-6">Content Calendar</h1>
      
      {loading && <p className="text-center py-4">Loading calendar data...</p>}
      
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          <p>{error}</p>
        </div>
      )}
      
      {!loading && !error && (
        <div className="bg-white rounded-lg shadow-lg">
          {posts.length > 0 ? (
            <Calendar posts={posts} />
          ) : (
            <p className="text-center py-8">No content scheduled. Add some content to get started.</p>
          )}
        </div>
      )}
    </div>
  );
}
