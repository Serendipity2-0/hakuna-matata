import React from 'react';
import { ContentCardProps } from '../types/calendar';

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

    return (
        <div className="content-card-modal">
            <div className="content-card">
                <button className="close-button" onClick={onClose}>×</button>
                
                <div className="content-header">
                    <span className="format-icon">{getIcon(post.format)}</span>
                    <h2>{post.contentType}</h2>
                </div>

                <div className="content-details">
                    <div className="platform">
                        <label>Platform:</label>
                        <span>{post.platform}</span>
                    </div>
                    
                    <div className="schedule">
                        <label>Scheduled for:</label>
                        <span>{post.scheduleTime}</span>
                    </div>
                </div>

                <div className="action-buttons">
                    <button className="view-button">View Content</button>
                    <button 
                        className="edit-button"
                        onClick={() => onEdit(post)}
                    >
                        Edit Content
                    </button>
                </div>
            </div>
        </div>
    );
};

export default ContentCard;