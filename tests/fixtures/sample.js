import { readFileSync } from 'fs';
import { join } from 'path'; // unused

function usedFunction() {
  return readFileSync('file.txt', 'utf8');
}

function deadFunction() {
  return "nobody calls me";
}

const activeVar = usedFunction();
const deadVar = "unused";

class UsedClass {
  run() {
    return activeVar;
  }
}

class DeadClass {
  noop() {}
}

const instance = new UsedClass();
instance.run();
