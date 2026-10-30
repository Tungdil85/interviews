export interface ExerciseDto {
  id: string;
  title: string;
  difficulty: string;
  topic: string;
  description: string;
  starterCode: string;
  tests: { name: string; code: string }[];
  hints: string[];
  solution: string;
}
