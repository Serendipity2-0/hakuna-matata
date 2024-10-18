'use client';

import { useState, useEffect } from 'react';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Button } from '@/components/ui/button';
import { ChevronRight, CheckCircle } from 'lucide-react';

type Department = 'Serendipity' | 'Dhoom Studios' | 'TradeMan';
type Role = 'Admin' | 'Manager' | 'Executive';
type Project = 'AccQt' | 'HRQt' | 'BrandQt' | 'Hakuna-Matata';
type Tool = 'ReconciliationAgent' | 'ScriptWriterAgent' | 'GitCommitterAgent' | 'RepoInfoAgent';

interface ToolSelectorProps {
  onToolSelect: (tool: Tool) => void;
}

const departments: Department[] = ['Serendipity', 'Dhoom Studios', 'TradeMan'];
const roles: Role[] = ['Admin', 'Manager', 'Executive'];
const projectsByDepartment: Record<Department, Project[]> = {
  Serendipity: ['AccQt', 'HRQt'],
  'Dhoom Studios': ['BrandQt'],
  TradeMan: ['Hakuna-Matata'],
};
const toolsByDepartment: Record<Department, Tool[]> = {
  Serendipity: ['ReconciliationAgent'],
  'Dhoom Studios': ['ScriptWriterAgent'],
  TradeMan: ['GitCommitterAgent', 'RepoInfoAgent'],
};

export default function ToolSelector({ onToolSelect }: ToolSelectorProps) {
  const [step, setStep] = useState(0);
  const [department, setDepartment] = useState<Department | ''>('');
  const [role, setRole] = useState<Role | ''>('');
  const [project, setProject] = useState<Project | ''>('');
  const [tool, setTool] = useState<Tool | ''>('');
  const [tasks, setTasks] = useState<string[]>([]);

  useEffect(() => {
    if (department) {
      setProject('');
      setTool('');
    }
  }, [department]);

  useEffect(() => {
    if (project) {
      fetchTasks(project);
    }
  }, [project]);

  const fetchTasks = async (selectedProject: Project) => {
    try {
      const response = await fetch(`/api/tasks?project=${selectedProject}`);
      if (!response.ok) {
        throw new Error('Failed to fetch tasks');
      }
      const taskList = await response.json();
      setTasks(taskList);
    } catch (error) {
      console.error('Error fetching tasks:', error);
      setTasks([]);
    }
  };

  const handleToolSelect = (selectedTool: Tool) => {
    setTool(selectedTool);
    onToolSelect(selectedTool);
  };

  const nextStep = () => {
    setStep((prevStep) => prevStep + 1);
  };

  const renderStep = () => {
    switch (step) {
      case 0:
        return (
          <div className="space-y-4">
            <h3 className="text-lg font-semibold">Select Department</h3>
            <Select value={department} onValueChange={(value) => setDepartment(value as Department)}>
              <SelectTrigger className="w-full">
                <SelectValue placeholder="Choose department" />
              </SelectTrigger>
              <SelectContent>
                {departments.map((dept) => (
                  <SelectItem key={dept} value={dept}>{dept}</SelectItem>
                ))}
              </SelectContent>
            </Select>
            <Button onClick={nextStep} disabled={!department} className="w-full">
              Next <ChevronRight className="ml-2 h-4 w-4" />
            </Button>
          </div>
        );
      case 1:
        return (
          <div className="space-y-4">
            <h3 className="text-lg font-semibold">Select Role</h3>
            <Select value={role} onValueChange={(value) => setRole(value as Role)}>
              <SelectTrigger className="w-full">
                <SelectValue placeholder="Choose role" />
              </SelectTrigger>
              <SelectContent>
                {roles.map((r) => (
                  <SelectItem key={r} value={r}>{r}</SelectItem>
                ))}
              </SelectContent>
            </Select>
            <Button onClick={nextStep} disabled={!role} className="w-full">
              Next <ChevronRight className="ml-2 h-4 w-4" />
            </Button>
          </div>
        );
      case 2:
        return (
          <div className="space-y-4">
            <h3 className="text-lg font-semibold">Select Project</h3>
            <Select value={project} onValueChange={(value) => setProject(value as Project)}>
              <SelectTrigger className="w-full">
                <SelectValue placeholder="Choose project" />
              </SelectTrigger>
              <SelectContent>
                {projectsByDepartment[department].map((proj) => (
                  <SelectItem key={proj} value={proj}>{proj}</SelectItem>
                ))}
              </SelectContent>
            </Select>
            <Button onClick={nextStep} disabled={!project} className="w-full">
              Next <ChevronRight className="ml-2 h-4 w-4" />
            </Button>
          </div>
        );
      case 3:
        return (
          <div className="space-y-4">
            <h3 className="text-lg font-semibold">Select Tool</h3>
            <Select value={tool} onValueChange={(value) => handleToolSelect(value as Tool)}>
              <SelectTrigger className="w-full">
                <SelectValue placeholder="Choose tool" />
              </SelectTrigger>
              <SelectContent>
                {toolsByDepartment[department].map((t) => (
                  <SelectItem key={t} value={t}>{t}</SelectItem>
                ))}
              </SelectContent>
            </Select>
            <Button onClick={nextStep} disabled={!tool} className="w-full">
              Finish <CheckCircle className="ml-2 h-4 w-4" />
            </Button>
          </div>
        );
      default:
        return null;
    }
  };

  return (
    <div className="bg-gray-100 p-6 rounded-lg shadow-md">
      <div className="flex justify-between mb-6">
        {['Department', 'Role', 'Project', 'Tool'].map((label, index) => (
          <div key={label} className={`flex items-center ${index <= step ? 'text-blue-600' : 'text-gray-400'}`}>
            <div className={`w-8 h-8 rounded-full flex items-center justify-center ${index < step ? 'bg-blue-600 text-white' : 'bg-gray-200'}`}>
              {index < step ? <CheckCircle className="h-5 w-5" /> : index + 1}
            </div>
            <span className="ml-2 text-sm font-medium">{label}</span>
          </div>
        ))}
      </div>
      {renderStep()}
    </div>
  );
}
