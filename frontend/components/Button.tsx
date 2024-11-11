// src/components/Button.tsx

import React from 'react';

interface ButtonProps {
    label: string;
    onClick?: () => void;
    type?: 'button' | 'submit' | 'reset';
    className?: string;
}

const Button: React.FC<ButtonProps> = ({ label, onClick, type = 'button', className = '' }) => {
    return (
        <button
            type={type}
            onClick={onClick}
            className={`px-6 py-3 rounded-lg font-medium text-sm border transition duration-200 ${className}`}
        >
            {label}
        </button>
    );
};

export default Button;