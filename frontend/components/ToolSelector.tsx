'use client';

import { useState, useEffect } from 'react';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';

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

  return (
    <div className="space-y-4">
      <Select value={department} onValueChange={(value) => setDepartment(value as Department)}>
        <SelectTrigger className="w-full">
          <SelectValue placeholder="Select Department" />
        </SelectTrigger>
        <SelectContent>
          {departments.map((dept) => (
            <SelectItem key={dept} value={dept}>{dept}</SelectItem>
          ))}
        </SelectContent>
      </Select>

      <Select value={role} onValueChange={(value) => setRole(value as Role)}>
        <SelectTrigger className="w-full">
          <SelectValue placeholder="Select Role" />
        </SelectTrigger>
        <SelectContent>
          {roles.map((r) => (
            <SelectItem key={r} value={r}>{r}</SelectItem>
          ))}
        </SelectContent>
      </Select>

      {department && (
        <Select value={project} onValueChange={(value) => setProject(value as Project)}>
          <SelectTrigger className="w-full">
            <SelectValue placeholder="Select Project" />
          </SelectTrigger>
          <SelectContent>
            {projectsByDepartment[department].map((proj) => (
              <SelectItem key={proj} value={proj}>{proj}</SelectItem>
            ))}
          </SelectContent>
        </Select>
      )}

      {project && tasks.length > 0 && (
        <Select>
          <SelectTrigger className="w-full">
            <SelectValue placeholder="Select Task" />
          </SelectTrigger>
          <SelectContent>
            {tasks.map((task) => (
              <SelectItem key={task} value={task}>{task}</SelectItem>
            ))}
          </SelectContent>
        </Select>
      )}

      {department && (
        <Select value={tool} onValueChange={(value) => handleToolSelect(value as Tool)}>
          <SelectTrigger className="w-full">
            <SelectValue placeholder="Select Tool" />
          </SelectTrigger>
          <SelectContent>
            {toolsByDepartment[department].map((t) => (
              <SelectItem key={t} value={t}>{t}</SelectItem>
            ))}
          </SelectContent>
        </Select>
      )}
    </div>
  );
}
