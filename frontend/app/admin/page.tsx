import { redirect } from 'next/navigation';
import React from 'react';
import { checkRole } from '@/utils/roles';

export default async function AdminRoute() {

        const isAdmin = await checkRole('marketing_admin')
  if (!isAdmin) {
    redirect('/')
  }
    return (
        <div>
            <h1>Only Admins can access this page</h1>
        </div>
    );
}
