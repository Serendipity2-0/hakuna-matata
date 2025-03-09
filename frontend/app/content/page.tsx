'use client';
import { Calendar } from '../../components/Calendar';

export default function ContentPage() {
  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-6">Content Calendar</h1>
      <Calendar posts={[]} />
    </div>
  );
}
