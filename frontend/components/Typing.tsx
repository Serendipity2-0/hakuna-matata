export default function Typing() {
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
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 5h12M9 3v2m1.048 9.5A18.022 18.022 0 016.412 9m6.088 9h7M11 21l5-10 5 10M12.751 5C11.783 10.77 8.07 15.61 3 18.129" />
        </svg>
        <h2 className="text-lg font-medium text-gray-700 dark:text-gray-200">Typing</h2>
      </div>
    </div>
  );
}
