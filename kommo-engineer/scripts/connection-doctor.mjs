import { resolve } from 'node:path';
import { pathToFileURL } from 'node:url';

const validSubdomain = value => typeof value === 'string' &&
  /^[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?$/.test(value);
const validId = value => typeof value === 'string' && /^[1-9][0-9]*$/.test(value);

function parseArgs(args) {
  const options = { live: false };
  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if (arg === '--live' && !options.live) options.live = true;
    else if (['--expected-subdomain', '--expected-account-id'].includes(arg)) {
      const key = arg === '--expected-subdomain' ? 'expectedSubdomain' : 'expectedAccountId';
      if (options[key] !== undefined || !args[i + 1] || args[i + 1].startsWith('--'))
        return null;
      options[key] = args[++i];
    } else return null;
  }
  return options;
}

/** One fixed GET at most; never emits secrets, raw bodies, headers or exception text. */
export async function runDoctor(args = [], { env = process.env, fetchImpl = globalThis.fetch } = {}) {
  const base = { crm_writes: 0, requests: 0, write_permissions_verified: false };
  const fail = (code, extra = {}) => ({ ...base, status: 'failed', code, ...extra });
  const options = parseArgs(args);
  if (!options) return fail('INVALID_ARGUMENTS');

  const subdomain = (env.KOMMO_SUBDOMAIN ?? '').trim().toLowerCase();
  const token = (env.KOMMO_TOKEN ?? '').trim();
  const expectedSubdomain = options.expectedSubdomain?.trim().toLowerCase();
  const expectedId = options.expectedAccountId ?? env.KOMMO_EXPECTED_ACCOUNT_ID;
  if (!validSubdomain(subdomain)) return fail('INVALID_SUBDOMAIN');
  if (!token || /\s|[\u0000-\u001f\u007f]/.test(token)) return fail('MISSING_OR_INVALID_TOKEN');
  if (expectedSubdomain !== undefined && !validSubdomain(expectedSubdomain))
    return fail('INVALID_EXPECTED_SUBDOMAIN');
  if (expectedId !== undefined && !validId(expectedId)) return fail('INVALID_EXPECTED_ACCOUNT_ID');
  if (expectedSubdomain !== undefined && expectedSubdomain !== subdomain)
    return fail('SUBDOMAIN_MISMATCH');

  if (!options.live) return {
    ...base, status: 'offline_ready', credential_present: true,
    authenticated: false, identity_verified: false,
  };
  if (!expectedSubdomain) return fail('EXPECTED_SUBDOMAIN_REQUIRED');

  let response;
  try {
    response = await fetchImpl(`https://${subdomain}.kommo.com/api/v4/account`, {
      method: 'GET', redirect: 'error', signal: AbortSignal.timeout(15_000),
      headers: { Authorization: `Bearer ${token}`, Accept: 'application/hal+json, application/json' },
    });
  } catch {
    return fail('NETWORK_OR_TIMEOUT', { requests: 1 });
  }
  if (response.status >= 300 && response.status < 400)
    return fail('REDIRECT_REJECTED', { requests: 1 });
  if (!response.ok) return fail('HTTP_ERROR', { requests: 1, http_status: response.status });
  if (!/^application\/(?:[a-z0-9.-]+\+)?json(?:;|$)/i.test(response.headers.get('content-type') ?? ''))
    return fail('INVALID_CONTENT_TYPE', { requests: 1 });

  let account;
  try { account = await response.json(); }
  catch { return fail('INVALID_JSON', { requests: 1 }); }
  if (!account || !Number.isSafeInteger(account.id) || account.id <= 0 ||
      !validSubdomain(account.subdomain)) return fail('INVALID_ACCOUNT_SCHEMA', { requests: 1 });
  if (account.subdomain !== expectedSubdomain ||
      (expectedId !== undefined && String(account.id) !== expectedId))
    return fail('ACCOUNT_MISMATCH', { requests: 1 });

  return {
    ...base, requests: 1, status: expectedId ? 'identity_verified' : 'identity_observed',
    authenticated: true, identity_verified: Boolean(expectedId),
    account_id: account.id, subdomain: account.subdomain,
  };
}

if (process.argv[1] && import.meta.url === pathToFileURL(resolve(process.argv[1])).href) {
  const result = await runDoctor(process.argv.slice(2));
  process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);
  process.exitCode = result.status === 'failed' ? 1 : 0;
}
