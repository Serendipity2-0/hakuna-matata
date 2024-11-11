// src/components/InputField.tsx

import React from 'react';

interface InputFieldProps {
    type: string;
    value: string;
    onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
    placeholder: string;
    className?: string;
    required?: boolean;
}

const InputField: React.FC<InputFieldProps> = ({
    type = 'text',
    placeholder,
    value,
    onChange,
    className = '',
    required = false,
}) => {
    return (
        <input
            type={type}
            placeholder={placeholder}
            value={value}
            onChange={onChange}
            className={`w-full p-3 rounded-md bg-transparent border focus:outline-none focus:ring-1 focus:ring-gray-500 ${className}`}
        />
    );
};

export default InputField;