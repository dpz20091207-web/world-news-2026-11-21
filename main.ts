// News-image entry (Node 22, standard library only): the image is the
// entry.png beside this file, and the program copies it to
// /output/entry.png. The program runs with no network and writes the same
// bytes on every run. The output file is left world-readable (0644) so the
// grader can collect it as another user.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { chmodSync, copyFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });
const dest = join(outDir, 'entry.png');
copyFileSync(new URL('./entry.png', import.meta.url), dest);
chmodSync(dest, 0o644);
