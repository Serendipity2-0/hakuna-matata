'use client';

import { useState } from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';

interface WorkingDirectoryModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSelect: (directory: string) => void;
}

export default function WorkingDirectoryModal({
  isOpen,
  onClose,
  onSelect,
}: WorkingDirectoryModalProps) {
  const [directory, setDirectory] = useState('');

  const handleSelect = () => {
    onSelect(directory);
    setDirectory('');
  };

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>Select Working Directory</DialogTitle>
        </DialogHeader>
        <Input
          value={directory}
          onChange={(e) => setDirectory(e.target.value)}
          placeholder="Enter working directory path"
        />
        <DialogFooter>
          <Button variant="outline" onClick={onClose}>Cancel</Button>
          <Button onClick={handleSelect}>Select</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}