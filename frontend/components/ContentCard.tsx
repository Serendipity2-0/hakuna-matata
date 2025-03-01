import React from 'react';
import { ContentCardProps } from '../../types/calendar';

const ContentCard: React.FC<ContentCardProps> = ({ post, onClose, onEdit }) => {
    const getIcon = (format: string) => {
        switch (format.toLowerCase()) {
            case 'reel': return '📹';
            case 'post': return '📝';
            case 'story': return '📱';
            case 'carousel': return '🎠';
            default: return '📄';
        }
    };

    const getPlatformColor = (platform: string): string => {
        switch (platform.toLowerCase()) {
            case 'instagram': return 'bg-pink-600';
            case 'facebook': return 'bg-blue-600';
            case 'linkedin': return 'bg-blue-700';
            case 'youtube': return 'bg-red-600';
            default: return 'bg-gray-600';
        }
    };

    return (
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-xl p-6 w-full max-w-md relative">
            <button 
                className="absolute top-4 right-4 text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200 text-2xl font-bold" 
                onClick={onClose}
            >
                ×
            </button>
            
            <div className="flex items-center mb-6">
                <span className="text-3xl mr-3">{getIcon(post.format)}</span>
                <h2 className="text-xl font-bold text-gray-800 dark:text-white">{post.contentType}</h2>
            </div>

            <div className="mb-6 space-y-4">
                <div className="flex items-center">
                    <span className={`${getPlatformColor(post.platform)} text-white text-xs font-bold px-3 py-1 rounded-full mr-2`}>
                        {post.platform}
                    </span>
                    <span className="text-gray-600 dark:text-gray-300 text-sm">
                        {post.format}
                    </span>
                </div>
                
                <div className="bg-gray-100 dark:bg-gray-700 p-3 rounded-lg">
                    <p className="text-sm text-gray-600 dark:text-gray-300 font-semibold">Scheduled for:</p>
                    <div className="flex items-center mt-1">
                        <span className="text-gray-800 dark:text-white">{post.date}</span>
                        <span className="mx-2 text-gray-400">•</span>
                        <span className="text-gray-800 dark:text-white">{post.scheduleTime}</span>
                    </div>
                </div>
            </div>

            <div className="flex justify-end space-x-3">
                <button className="px-4 py-2 bg-gray-500 text-white rounded hover:bg-gray-600 transition-colors">
                    View Content
                </button>
                <button 
                    className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors"
                    onClick={() => onEdit(post)}
                >
                    Edit Content
                </button>
            </div>
        </div>
    );
};

export default ContentCard;
