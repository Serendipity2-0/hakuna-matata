"use client";
import React, { useState } from 'react';
import InputField from '../components/InputField';
import Button from './Button';
import axios from 'axios';
import { useRouter } from 'next/navigation';
import Link from 'next/link';

const RegisterForm = () => {
    const [formData, setFormData] = useState({
        email: '',
        department: '',
        phone_number: '',
        password: '',
        name: ''
    });
    const [error, setError] = useState<string | null>(null);
    const [success, setSuccess] = useState<string | null>(null);
    const router = useRouter();

    const getDepartmentId = (department: string) => {
        const departmentMap: { [key: string]: number } = {
            'Serendipity': 1,
            'Trademan': 2,
            'DhoomStudios': 3
        };
        return departmentMap[department] || 0;
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError(null);
        setSuccess(null);

        // Validate form data
        if (!formData.name || !formData.email || !formData.department ||
            !formData.phone_number || !formData.password) {
            setError('All fields are required');
            return;
        }

        // Validate phone number
        if (!/^\d{10}$/.test(formData.phone_number)) {
            setError('Please enter a valid 10-digit phone number');
            return;
        }

        try {
            // Format payload according to API requirements
            const payload = {
                phone_number: formData.phone_number,
                password: formData.password,
                email: formData.email,
                name: formData.name,
                department_id: getDepartmentId(formData.department)
            };

            console.log('Sending registration request:', {
                ...payload,
                password: '***hidden***'
            });

            // Use the full API URL
            const response = await axios.post('https://hakuna-matata.trademan.ai/register', payload, {
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                }
            });

            console.log('Registration response:', response.data);

            if (response.data && response.status === 200) {
                setSuccess('Registration successful! Redirecting to login...');
                setTimeout(() => {
                    router.push('/login');
                }, 1500);
            } else {
                throw new Error('Invalid response from server');
            }
        } catch (error: any) {
            console.error('Registration error:', error);

            // Handle different types of errors
            if (axios.isAxiosError(error)) {
                if (error.response?.status === 409) {
                    setError('User already exists with this phone number or email');
                } else if (error.response?.status === 422) {
                    setError('Invalid input format. Please check all fields');
                } else if (error.response?.data?.message) {
                    setError(error.response.data.message);
                } else {
                    setError('Registration failed. Please try again.');
                }
            } else {
                setError('An unexpected error occurred. Please try again.');
            }
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center bg-black">
            <div className="bg-[#121212] p-8 rounded-lg shadow-xl w-full max-w-md">
                <h1 className="text-4xl font-bold text-center mb-8 text-white">Register</h1>

                <form className="space-y-4" onSubmit={handleSubmit}>
                    <InputField
                        type="text"
                        placeholder="Name"
                        value={formData.name}
                        onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                        className="bg-[#1e1e1e] text-white border-gray-700 focus:border-gray-500"
                    />

                    <InputField
                        type="email"
                        placeholder="Email"
                        value={formData.email}
                        onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                        className="bg-[#1e1e1e] text-white border-gray-700 focus:border-gray-500"
                    />

                    <select
                        className="w-full p-3 rounded-md bg-[#1e1e1e] text-gray-300 border border-gray-700 focus:border-gray-500"
                        value={formData.department}
                        onChange={(e) => setFormData({ ...formData, department: e.target.value })}
                    >
                        <option value="">Select Department</option>
                        <option value="Serendipity">Serendipity</option>
                        <option value="Trademan">Trademan</option>
                        <option value="DhoomStudios">DhoomStudios</option>
                    </select>

                    <InputField
                        type="tel"
                        placeholder="Enter 10 Digits mobile number"
                        value={formData.phone_number}
                        onChange={(e) => {
                            const value = e.target.value.trim();
                            if (value === '' || /^[0-9+]+$/.test(value)) {
                                setFormData({ ...formData, phone_number: value });
                            }
                        }}
                        className="bg-[#1e1e1e] text-white border-gray-700 focus:border-gray-500"
                    />

                    <InputField
                        type="password"
                        placeholder="Enter Password"
                        value={formData.password}
                        onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                        className="bg-[#1e1e1e] text-white border-gray-700 focus:border-gray-500"
                    />

                    {error && (
                        <div className="bg-red-500/10 border border-red-500 text-red-500 px-4 py-2 rounded-md">
                            {error}
                        </div>
                    )}

                    {success && (
                        <div className="bg-green-500/10 border border-green-500 text-green-500 px-4 py-2 rounded-md">
                            {success}
                        </div>
                    )}

                    <Button
                        label="Register"
                        type="submit"
                        className="w-full bg-blue-500 text-white border-0 hover:bg-blue-600"
                    />
                </form>

                <p className="text-gray-400 text-sm text-center mt-6">
                    Already have an account?{' '}
                    <Link href="/login" className="text-blue-500 hover:text-blue-400">
                        Login
                    </Link>
                </p>
            </div>
        </div>
    );
};

export default RegisterForm;