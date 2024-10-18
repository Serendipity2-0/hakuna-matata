'use client';

import { Button } from '@/components/ui/button';
import { Dialog, DialogContent, DialogFooter, DialogHeader, DialogTitle } from '@/components/ui/dialog';

interface HumanReviewModalProps {
  isOpen: boolean;
  onClose: () => void;
  pendingMessage: string;
  onApprove: (message: string) => void;
}

export default function HumanReviewModal({
  isOpen,
  onClose,
  pendingMessage,
  onApprove,
}: HumanReviewModalProps) {
  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Human Review Required</DialogTitle>
        </DialogHeader>
        <div>{pendingMessage}</div>
        <DialogFooter>
          <Button onClick={() => onApprove(pendingMessage)}>Approve</Button>
          <Button onClick={onClose}>Cancel</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
