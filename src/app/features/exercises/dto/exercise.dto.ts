export interface ExerciseDto {
  id: string;
  kind?: string;
  durationMin?: number;
  title: string;
  difficulty: string;
  topic: string;
  description: string;
  starterCode: string;
  tests: { name: string; code: string }[];
  hints: string[];
  solution: string;
  preview?: string;
}
