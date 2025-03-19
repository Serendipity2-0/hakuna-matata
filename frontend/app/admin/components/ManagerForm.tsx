'use client'

import { setRole } from '../actions'

export function ManagerForm({ user }: { user: any }) {
  return (
    <form action={async (formData) => {
      'use server'
      await setRole(formData)
    }}>
      <input type="hidden" value={user.id} name="id" />
      <input type="hidden" value="Manager" name="role" />
      <select 
        name="department" 
        className="border p-2 rounded mr-2"
        required
      >
        <option value="">Select Department</option>
        <option value="serendipity">Serendipity</option>
        <option value="dhoomstudios">Dhoom Studios</option>
        <option value="trademan">TradeMan</option>
      </select>
      <button 
        type="submit"
        className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
      >
        Make Manager
      </button>
    </form>
  )
}
