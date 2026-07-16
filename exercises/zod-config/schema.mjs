// App config schema — Zod 4 idioms throughout (verified against zod 4.4.3 at runtime).
import { z } from 'zod';

export const ConfigSchema = z.strictObject({
  server: z.strictObject({
    host: z.string().min(1, { error: 'host must be a non-empty string' }),
    port: z
      .int({ error: 'port must be an integer' })
      .min(1, { error: 'port must be between 1 and 65535' })
      .max(65535, { error: 'port must be between 1 and 65535' }),
    https: z.boolean().default(false),
  }),

  database: z.strictObject({
    url: z
      .url({ error: 'database.url must be a valid URL' })
      .refine((u) => u.startsWith('postgres://') || u.startsWith('mysql://'), {
        error: 'database.url must use the postgres:// or mysql:// scheme',
      }),
    poolSize: z.int().min(1).max(100).default(10),
  }),

  logLevel: z.enum(['debug', 'info', 'warn', 'error']).default('info'),

  admins: z
    .array(z.email({ error: (iss) => `"${iss.input}" is not a valid admin email` }))
    .min(1, { error: 'at least one admin email is required' }),

  featureFlags: z.record(z.string(), z.boolean()).default({}),

  auth: z.discriminatedUnion('kind', [
    z.strictObject({
      kind: z.literal('apiKey'),
      key: z.string().min(16, { error: 'apiKey.key must be at least 16 characters' }),
    }),
    z.strictObject({
      kind: z.literal('oauth'),
      clientId: z.string().min(1),
      clientSecret: z.string().min(1),
      tokenUrl: z.url(),
    }),
  ]),
});
