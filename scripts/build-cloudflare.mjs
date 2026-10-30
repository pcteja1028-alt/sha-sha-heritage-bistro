import { cp, mkdir, readdir, stat } from 'node:fs/promises';
import { resolve, join } from 'node:path';

// Retain the editable original in the repo; publish the compressed model.
const source = resolve('dist');
const output = resolve('.cloudflare-dist');
await mkdir(output, { recursive: true });
await cp(source, output, {
  recursive: true,
  filter: path => !['heritage-a01.glb', 'heritage-a01-web.glb'].includes(path.split(/[\\/]/).pop())
});
await cp(join(source, 'assets/heritage-a01-web.glb'), join(output, 'assets/heritage-a01.glb'));
async function check(directory) {
  for (const entry of await readdir(directory, { withFileTypes: true })) {
    const path = join(directory, entry.name);
    if (entry.isDirectory()) await check(path);
    else if ((await stat(path)).size > 25 * 1024 * 1024) throw new Error(`Asset exceeds 25 MiB: ${path}`);
  }
}
await check(output);
console.log('Cloudflare static assets ready; every file is below 25 MiB.');
