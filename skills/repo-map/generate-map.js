#!/usr/bin/env node

import { execSync } from 'node:child_process';
import { readFileSync } from 'node:fs';
import { basename, dirname, extname, join, resolve } from 'node:path';

const targetDir = process.argv[2] || '.';
const absDir = resolve(targetDir);
const repoName = basename(absDir);

// Get tracked files
let files;
try {
  files = execSync('git ls-files', { cwd: absDir, encoding: 'utf8' })
    .trim()
    .split('\n')
    .filter(Boolean);
} catch {
  console.error('Not a git repository or git not available');
  process.exit(1);
}

function lineCount(filePath) {
  try {
    return readFileSync(filePath, 'utf8').split('\n').length;
  } catch {
    return 0;
  }
}

function extractSignatures(filePath) {
  const ext = extname(filePath);
  try {
    const content = readFileSync(filePath, 'utf8');
    const sigs = [];

    if (ext === '.js' || ext === '.ts' || ext === '.mjs') {
      const re = /export\s+(?:async\s+)?(?:function|const|let|var|default|class)\s+(\w+)/g;
      let m;
      while ((m = re.exec(content)) !== null) sigs.push(m[1]);
    } else if (ext === '.py') {
      const re = /^(?:def|class)\s+(\w+)/gm;
      let m;
      while ((m = re.exec(content)) !== null) sigs.push(m[1]);
    } else if (ext === '.ahk') {
      const re = /^([#!^+]*\w+)\s*::/gm;
      let m;
      while ((m = re.exec(content)) !== null) sigs.push(m[1]);
    }

    return sigs;
  } catch {
    return [];
  }
}

const sourceExts = new Set(['.js', '.ts', '.mjs', '.py', '.ahk', '.jsx', '.tsx']);
const configFiles = new Set([
  'package.json',
  'pyproject.toml',
  'eslint.config.js',
  'tsconfig.json',
]);
const skipExts = new Set([
  '.png',
  '.jpg',
  '.gif',
  '.pdf',
  '.csv',
  '.xlsx',
  '.ico',
  '.svg',
  '.woff',
  '.ttf',
  '.lock',
  '.pem',
]);

const tree = {};
const deps = [];

for (const file of files) {
  const ext = extname(file);
  if (skipExts.has(ext)) continue;
  if (file.startsWith('node_modules/')) continue;

  const dir = dirname(file) === '.' ? '' : dirname(file);
  if (!tree[dir]) tree[dir] = [];

  const fullPath = join(absDir, file);
  const name = basename(file);
  const lines = lineCount(fullPath);

  if (sourceExts.has(ext)) {
    const sigs = extractSignatures(fullPath);
    const sigStr = sigs.length > 0 ? ` — exports: ${sigs.join(', ')}` : '';
    tree[dir].push(`${name} (${lines} lines)${sigStr}`);
  } else if (configFiles.has(name)) {
    tree[dir].push(`${name} (config)`);
    if (name === 'package.json') {
      try {
        const pkg = JSON.parse(readFileSync(fullPath, 'utf8'));
        if (pkg.dependencies) deps.push(...Object.keys(pkg.dependencies));
      } catch {
        /* skip */
      }
    }
  }
}

console.log(`## Repository Map: ${repoName}`);
console.log(`Generated: ${new Date().toISOString().split('T')[0]}\n`);
console.log('### Structure');

const sortedDirs = Object.keys(tree).sort();
for (const dir of sortedDirs) {
  const depth = dir ? dir.split(/[/\\]/).length : 0;
  const indent = '  '.repeat(depth);
  if (dir) console.log(`${indent}${basename(dir)}/`);
  for (const entry of tree[dir]) {
    console.log(`${'  '.repeat(depth + 1)}${entry}`);
  }
}

if (deps.length > 0) {
  console.log('\n### Dependencies');
  console.log(deps.join(', '));
}
