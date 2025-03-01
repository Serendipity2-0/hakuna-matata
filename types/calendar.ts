export interface ContentPost {
    serialNo: number;
    date: string;
    contentType: string;
    format: 'Reel' | 'Post' | 'Story' | 'Carousel' | string;
    platform: 'Instagram' | 'Facebook' | 'LinkedIn' | 'Youtube';
    scheduleTime: string;
}

export interface ContentCardProps {
    post: ContentPost;
    onClose: () => void;
    onEdit: (post: ContentPost) => void;
}