// Self-verification for the Zod 4 config validator. Run: node test.mjs
import assert from 'node:assert/strict';
import { z } from 'zod';
import { ConfigSchema } from './schema.mjs';

const validConfig = {
  server: { host: 'api.example.com', port: 8443, https: true },
  database: { url: 'postgres://db.internal:5432/app' },
  admins: ['ops@example.com'],
  auth: { kind: 'apiKey', key: 'k'.repeat(20) },
};

let passed = 0;
function check(name, fn) {
  fn();
  passed++;
  console.log(`  ok - ${name}`);
}

// 1. Valid config parses; defaults are applied.
check('valid config parses and defaults apply', () => {
  const r = ConfigSchema.safeParse(validConfig);
  assert.equal(r.success, true, JSON.stringify(r.error?.issues));
  assert.equal(r.data.logLevel, 'info');           // enum default
  assert.equal(r.data.database.poolSize, 10);      // int default
  assert.deepEqual(r.data.featureFlags, {});       // record default
});

// 2. Port boundary: 65535 ok, 65536 rejected with the custom message.
check('port boundaries enforced with custom error', () => {
  const ok = ConfigSchema.safeParse({ ...validConfig, server: { ...validConfig.server, port: 65535 } });
  assert.equal(ok.success, true);
  const bad = ConfigSchema.safeParse({ ...validConfig, server: { ...validConfig.server, port: 65536 } });
  assert.equal(bad.success, false);
  assert.ok(bad.error.issues.some(i => i.message === 'port must be between 1 and 65535'),
    JSON.stringify(bad.error.issues));
});

// 3. Wrong DB scheme rejected via refine with v4 `error` param.
check('non-postgres/mysql scheme rejected', () => {
  const bad = ConfigSchema.safeParse({ ...validConfig, database: { url: 'https://not-a-db.example.com' } });
  assert.equal(bad.success, false);
  assert.ok(bad.error.issues.some(i => i.message.includes('postgres:// or mysql://')));
});

// 4. Bad admin email: error callback interpolates the input.
check('email error callback receives the input value', () => {
  const bad = ConfigSchema.safeParse({ ...validConfig, admins: ['not-an-email'] });
  assert.equal(bad.success, false);
  assert.ok(bad.error.issues.some(i => i.message === '"not-an-email" is not a valid admin email'),
    JSON.stringify(bad.error.issues));
});

// 5. Discriminated union: oauth variant requires its own fields.
check('discriminated union routes to the right variant', () => {
  const bad = ConfigSchema.safeParse({ ...validConfig, auth: { kind: 'oauth', clientId: 'abc' } });
  assert.equal(bad.success, false);
  const paths = bad.error.issues.map(i => i.path.join('.'));
  assert.ok(paths.includes('auth.clientSecret'), JSON.stringify(paths));
  assert.ok(paths.includes('auth.tokenUrl'), JSON.stringify(paths));
});

// 6. strictObject rejects unknown keys.
check('unknown top-level keys rejected (strictObject)', () => {
  const bad = ConfigSchema.safeParse({ ...validConfig, sneaky: true });
  assert.equal(bad.success, false);
  assert.ok(bad.error.issues.some(i => i.code === 'unrecognized_keys'), JSON.stringify(bad.error.issues));
});

// 7. prettifyError produces path-annotated readable output.
check('prettifyError includes message and path', () => {
  const bad = ConfigSchema.safeParse({ ...validConfig, admins: ['nope'] });
  const pretty = z.prettifyError(bad.error);
  assert.ok(pretty.includes('is not a valid admin email'), pretty);
  assert.ok(pretty.includes('admins'), pretty);
});

// 8. treeifyError nests by schema shape.
check('treeifyError exposes per-field errors', () => {
  const bad = ConfigSchema.safeParse({ ...validConfig, server: { ...validConfig.server, port: 0 } });
  const tree = z.treeifyError(bad.error);
  const portErrors = tree.properties?.server?.properties?.port?.errors;
  assert.ok(Array.isArray(portErrors) && portErrors.length > 0, JSON.stringify(tree));
});

console.log(`\n${passed}/8 checks passed`);
