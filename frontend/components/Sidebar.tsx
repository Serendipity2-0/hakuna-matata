import ContentCalendar from './ContentCalendar';
import Typing from './Typing';

export default function Sidebar() {
  return (
    <aside className="w-[400px] min-h-screen bg-pink-100 dark:bg-pink-900 border-r border-gray-200 dark:border-gray-700 shadow-lg">
      {/* Sidebar Header */}
      <div className="p-4 border-b border-gray-200 dark:border-gray-700">
        <h1 className="text-xl font-bold text-gray-800 dark:text-white">Dashboard</h1>
      </div>

      {/* Navigation Items */}
      <nav className="p-4 space-y-6">
        {/* You can add icons and better styling to each component */}
        <div className="hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors">
          <ContentCalendar />
        </div>

        <div className="hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors">
          <Typing />
        </div>
      </nav>

      {/* Optional: Footer Section */}
      <div className="absolute bottom-0 w-full p-4 border-t border-gray-200 dark:border-gray-700">
        <p className="text-sm text-gray-600 dark:text-gray-400">© 2025 Serendipity</p>
      </div>
    </aside>
  );
}