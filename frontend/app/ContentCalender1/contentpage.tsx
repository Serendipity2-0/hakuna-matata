import React, { useState } from "react";
import { Calendar } from "@mantine/dates";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Dialog, DialogContent, DialogTitle } from "@/components/ui/dialog";
import { useToast } from "@/components/ui/use-toast";
import { MessageSquare } from "lucide-react";

const sampleData = {
  "2025-03-01": { type: "Reel", platform: "Instagram", content: "https://via.placeholder.com/400" },
  "2025-03-05": { type: "Carousel", platform: "Facebook", content: "https://via.placeholder.com/400" },
  "2025-03-10": { type: "Post", platform: "LinkedIn", content: "https://via.placeholder.com/400" },
};

export default function ContentCalendar() {
  const [selectedDate, setSelectedDate] = useState(null);
  const [isOpen, setIsOpen] = useState(false);
  const { toast } = useToast();

  const handleDateClick = (date) => {
    const formattedDate = date.toISOString().split("T")[0];
    if (sampleData[formattedDate]) {
      setSelectedDate(formattedDate);
      setIsOpen(true);
    } else {
      toast({ title: "No content scheduled for this date" });
    }
  };

  return (
    <div className="flex flex-col items-center justify-center p-6">
      <h1 className="text-2xl font-bold mb-4">Content Calendar</h1>
      <Calendar
        className="rounded-lg shadow-md p-4"
        onChange={handleDateClick}
      />

      <Dialog open={isOpen} onOpenChange={setIsOpen}>
        <DialogContent>
          <DialogTitle>Scheduled Content</DialogTitle>
          {selectedDate && (
            <Card>
              <CardContent className="flex flex-col items-center p-4">
                <p className="font-semibold text-lg">{sampleData[selectedDate].type}</p>
                <p className="text-sm text-gray-500">{sampleData[selectedDate].platform}</p>
                <img
                  src={sampleData[selectedDate].content}
                  alt="Scheduled Content"
                  className="mt-3 rounded-lg shadow"
                  width={300}
                />
                <div className="mt-4 flex gap-2">
                  <Button onClick={() => window.open(sampleData[selectedDate].content, "_blank")}>View Content</Button>
                  <Button variant="outline" onClick={() => setIsOpen(false)}>Close</Button>
                </div>
              </CardContent>
            </Card>
          )}
        </DialogContent>
      </Dialog>
    </div>
  );
}