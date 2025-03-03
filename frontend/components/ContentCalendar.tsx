export default function ContentCalendar() {
  return (
    <div className="p-3">
      <div className="flex items-center space-x-3">
        {/* Optional: Add an icon */}
        <svg 
          className="w-5 h-5 text-gray-600 dark:text-gray-300" 
          fill="none" 
          stroke="currentColor" 
          viewBox="0 0 24 24"
        >
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
        </svg>
        <h2 className="text-lg font-medium text-gray-700 dark:text-gray-200">Content Calendar</h2>
      </div>
      {/* Add your calendar content here */}
    </div>
  );
} 