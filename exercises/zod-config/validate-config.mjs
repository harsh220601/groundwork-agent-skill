#!/usr/bin/env node
// CLI: validate a JSON config file against ConfigSchema.
// Usage: node validate-config.mjs <path-to-config.json>
// Exit 0 = valid (prints normalized config), exit 1 = invalid (prints readable errors).
import { readFileSync } from 'node:fs';
import { z } from 'zod';
import { ConfigSchema } from './schema.mjs';

const path = process.argv[2];
if (!path) {
  console.error('usage: node validate-config.mjs <config.json>');
  process.exit(2);
}

let raw;
try {
  raw = JSON.parse(readFileSync(path, 'utf8'));
} catch (e) {
  console.error(`Could not read/parse ${path}: ${e.message}`);
  process.exit(2);
}

const result = ConfigSchema.safeParse(raw);
if (result.success) {
  console.log('Config OK. Normalized:');
  console.log(JSON.stringify(result.data, null, 2));
  process.exit(0);
} else {
  console.error(`Config INVALID (${result.error.issues.length} issue(s)):`);
  console.error(z.prettifyError(result.error));
  process.exit(1);
}
