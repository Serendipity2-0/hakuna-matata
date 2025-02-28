"use client";

import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Factory, Lightbulb, Wine, Mountain, Building, Calendar, MapPin, Globe } from 'lucide-react';

const CompanyProfile = () => {
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    setIsVisible(true);
  }, []);

  const segments = [
    { icon: Factory, title: 'Sugar', color: 'text-amber-500' },
    { icon: Lightbulb, title: 'Power', color: 'text-yellow-500' },
    { icon: Wine, title: 'Industrial Alcohol', color: 'text-purple-500' },
    { icon: Mountain, title: 'Granite Products', color: 'text-gray-500' }
  ];

  const details = [
    { icon: Building, text: 'Headquartered in Coimbatore, Tamil Nadu', color: 'text-blue-500' },
    { icon: Calendar, text: 'Established in 1983', color: 'text-green-500' },
    { icon: MapPin, text: 'Multiple manufacturing facilities across India', color: 'text-red-500' },
    { icon: Globe, text: 'Leading presence in Indian sugar industry', color: 'text-indigo-500' }
  ];

  return (
    <Card className={`w-full max-w-6xl transition-all duration-1000 ${isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'}`}>
      <CardHeader className="text-center bg-gradient-to-r from-blue-500 to-purple-500 text-white rounded-t-lg">
        <CardTitle className="text-3xl font-bold">
          Bannari Amman Sugars Limited
        </CardTitle>
      </CardHeader>
      
      <CardContent className="p-6">
        {/* Business Segments - Now in a single line */}
        <div className="mb-8">
          <h2 className="text-xl font-semibold mb-4">Business Segments</h2>
          <div className="flex flex-row justify-between items-center gap-4">
            {segments.map((segment, index) => (
              <div
                key={segment.title}
                className={`flex-1 p-4 rounded-lg shadow-lg transition-all duration-500 hover:scale-105 text-center ${
                  isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'
                }`}
                style={{ transitionDelay: `${index * 200}ms` }}
              >
                <div className="flex flex-col items-center">
                  <segment.icon className={`w-8 h-8 ${segment.color} mb-2`} />
                  <h3 className="font-semibold">{segment.title}</h3>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Company Details - In a 2x2 grid */}
        <div className="space-y-4">
          <h2 className="text-xl font-semibold mb-4">Company Details</h2>
          <div className="grid grid-cols-2 gap-4">
            {details.map((detail, index) => (
              <div
                key={index}
                className={`flex items-center space-x-3 p-3 rounded-lg bg-gray-50 transition-all duration-500 hover:bg-gray-100 ${
                  isVisible ? 'opacity-100 translate-x-0' : 'opacity-0 -translate-x-10'
                }`}
                style={{ transitionDelay: `${index * 200}ms` }}
              >
                <detail.icon className={`w-6 h-6 ${detail.color}`} />
                <span className="text-gray-700">{detail.text}</span>
              </div>
            ))}
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default CompanyProfile;



