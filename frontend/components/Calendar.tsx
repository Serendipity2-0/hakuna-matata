import React, { useState, useRef, useEffect } from 'react';
import { ContentPost } from '../../types/calendar';
import ContentCard from './ContentCard';
import FullCalendar from '@fullcalendar/react';
import dayGridPlugin from '@fullcalendar/daygrid';
import timeGridPlugin from '@fullcalendar/timegrid';
import interactionPlugin from '@fullcalendar/interaction';
import { EventInput, DateSelectArg, EventClickArg } from '@fullcalendar/core';

// FullCalendar styles are imported in the component

interface CalendarProps {
    posts: ContentPost[];
}

export const Calendar: React.FC<CalendarProps> = ({ posts }) => {
    const [selectedPost, setSelectedPost] = useState<ContentPost | null>(null);
    const [isDarkMode, setIsDarkMode] = useState(false);
    const [currentView, setCurrentView] = useState<'dayGridMonth' | 'timeGridDay'>('dayGridMonth');
    const [selectedDate, setSelectedDate] = useState<string | null>(null);
    const calendarRef = useRef<FullCalendar>(null);

    // Convert posts to FullCalendar events
    const events: EventInput[] = posts.map(post => {
        // Parse the date string (assuming format like "01-Mar-25" or "2023-03-01 00:00:00")
        let date: Date;
        
        if (post.date.includes('-') && post.date.includes(':')) {
            // Format: "2023-03-01 00:00:00"
            date = new Date(post.date);
        } else {
            // Format: "01-Mar-25"
            const dateParts = post.date.split('-');
            const year = dateParts[2].length === 2 ? parseInt(`20${dateParts[2]}`) : parseInt(dateParts[2]); // Convert "25" to "2025"
            const monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
            const month = monthNames.indexOf(dateParts[1]);
            const day = parseInt(dateParts[0]);
            
            date = new Date(year, month, day);
        }
        
        // Parse the time (assuming format like "6:00 PM")
        let hour = 0;
        let minute = 0;
        if (post.scheduleTime) {
            // Try to extract time from scheduleTime field
            const timeParts = post.scheduleTime.match(/(\d+):(\d+)\s*(AM|PM)?/i);
            if (timeParts) {
                hour = parseInt(timeParts[1]);
                minute = parseInt(timeParts[2]);
                if (timeParts[3] && timeParts[3].toUpperCase() === 'PM' && hour < 12) hour += 12;
                if (timeParts[3] && timeParts[3].toUpperCase() === 'AM' && hour === 12) hour = 0;
                
                // Set the time on our date object
                date.setHours(hour, minute);
            }
        }
        
        // Create the event
        return {
            id: post.serialNo.toString(),
            title: post.contentType,
            start: date,
            extendedProps: {
                format: post.format,
                platform: post.platform,
                scheduleTime: post.scheduleTime,
                post: post
            },
            backgroundColor: getColorForPlatform(post.platform),
            borderColor: getColorForPlatform(post.platform)
        };
    });

    // Get color based on platform
    function getColorForPlatform(platform: string): string {
        switch (platform.toLowerCase()) {
            case 'instagram': return '#E1306C';
            case 'facebook': return '#4267B2';
            case 'linkedin': return '#0077B5';
            case 'youtube': return '#FF0000';
            default: return '#6c757d';
        }
    }

    // Handle date click
    const handleDateClick = (arg: any) => {
        setSelectedDate(arg.dateStr);
        if (calendarRef.current) {
            calendarRef.current.getApi().changeView('timeGridDay', arg.date);
            setCurrentView('timeGridDay');
        }
    };

    // Handle event click
    const handleEventClick = (arg: EventClickArg) => {
        const post = arg.event.extendedProps.post as ContentPost;
        setSelectedPost(post);
    };

    // Handle back to month view
    const handleBackToMonth = () => {
        if (calendarRef.current) {
            calendarRef.current.getApi().changeView('dayGridMonth');
            setCurrentView('dayGridMonth');
            setSelectedDate(null);
        }
    };

    const handleEdit = (post: ContentPost) => {
        // Implement edit functionality
        console.log('Editing post:', post);
        setSelectedPost(null);
    };

    return (
        <div className={`p-5 rounded-lg transition-colors ${isDarkMode ? 'bg-gray-800 text-white' : 'bg-gray-100 text-gray-900'}`}>
            <div className="flex justify-between items-center mb-5">
                <div className="flex items-center space-x-2">
                    {currentView === 'timeGridDay' && (
                        <button 
                            className="px-4 py-2 bg-gray-600 text-white rounded hover:bg-gray-700 transition-colors"
                            onClick={handleBackToMonth}
                        >
                            ← Back to Month
                        </button>
                    )}
                    <button 
                        className="p-2 rounded-full hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors"
                        onClick={() => setIsDarkMode(!isDarkMode)}
                    >
                        {isDarkMode ? '☀️' : '🌙'}
                    </button>
                </div>
                <button className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors">
                    +
                </button>
            </div>
            
            <div className={`mb-5 ${isDarkMode ? 'dark' : ''}`}>
                <FullCalendar
                    ref={calendarRef}
                    plugins={[dayGridPlugin, timeGridPlugin, interactionPlugin]}
                    initialView="dayGridMonth"
                    headerToolbar={{
                        left: 'prev,next today',
                        center: 'title',
                        right: 'dayGridMonth,timeGridDay'
                    }}
                    events={events}
                    dateClick={handleDateClick}
                    eventClick={handleEventClick}
                    height="auto"
                />
            </div>

            {selectedPost && (
                <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
                    <ContentCard 
                        post={selectedPost}
                        onClose={() => setSelectedPost(null)}
                        onEdit={handleEdit}
                    />
                </div>
            )}
        </div>
    );
};
