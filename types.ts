export enum HabitFrequency {
  DAILY = 'DAILY',
  WEEKLY = 'WEEKLY',
}

export interface Habit {
  id: string;
  title: string;
  description?: string;
  frequency: HabitFrequency;
  streak: number;
  completedDates: string[]; // ISO date strings YYYY-MM-DD
  createdAt: string;
  streakGoal?: number;
}

export interface ChatMessage {
  id: string;
  role: 'user' | 'model';
  text: string;
  timestamp: number;
}

export type ImageSize = '1K' | '2K' | '4K';

export interface VisionBoardItem {
  id: string;
  imageUrl: string;
  prompt: string;
  createdAt: number;
}