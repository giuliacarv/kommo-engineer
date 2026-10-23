import test from 'node:test';
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { runDoctor } from './connection-doctor.mjs';

const env = { KOMMO_SUBDOMAIN: 'example-only', KOMMO_TOKEN: 'synthetic-secret-for-tests' };
const live = ['--live', '--expected-subdomain', env.KOMMO_SUBDOMAIN];
const ok = account => new Response(JSON.stringify(account), {
  status: 200, headers: { 'content-type': 'application/hal+json; charset=utf-8' },
});
const account = { id: 123456, subdomain: env.KOMMO_SUBDOMAIN };
const noNetwork = async () => { assert.fail('unexpected network call'); };
function assertSafe(result) {
  const output = JSON.stringify(result);
  assert.ok(!output.includes(env.KOMMO_TOKEN));
  assert.ok(!output.includes('private-body-marker'));
  assert.equal(result.crm_writes, 0);
  assert.equal(result.write_permissions_verified, false);
}

test('offline never calls API or claims authenticated', async () => {
  const r = await runDoctor([], { env, fetchImpl: noNetwork });
  assert.equal(r.status, 'offline_ready');
  assert.equal(r.authenticated, false);
  assert.equal(r.requests, 0);
  assertSafe(r);
});

test('CLI emits sanitized JSON and fails before live network when target is absent', () => {
  const script = fileURLToPath(new URL('./connection-doctor.mjs', import.meta.url));
  for (const [args, expectedExit, expectedStatus] of [
    [[], 0, 'offline_ready'], [['--live'], 1, 'failed'],
  ]) {
    const result = spawnSync(process.execPath, [script, ...args], {
      env: { ...env, SystemRoot: process.env.SystemRoot ?? '' }, encoding: 'utf8', timeout: 5000,
    });
    assert.equal(result.status, expectedExit);
    assert.equal(result.stderr, '');
    const output = JSON.parse(result.stdout);
    assert.equal(output.status, expectedStatus);
    assert.equal(output.requests, 0);
    assertSafe(output);
  }
});

test('refuses missing credential, invalid host, mismatched target and unknown arguments before network', async () => {
  for (const [args, override, code] of [
    [live, { KOMMO_TOKEN: '' }, 'MISSING_OR_INVALID_TOKEN'],
    [live, { KOMMO_TOKEN: 'bad\nheader' }, 'MISSING_OR_INVALID_TOKEN'],
    [live, { KOMMO_SUBDOMAIN: 'evil.test/path' }, 'INVALID_SUBDOMAIN'],
    [live, { KOMMO_SUBDOMAIN: 'https://example-only.kommo.com' }, 'INVALID_SUBDOMAIN'],
    [['--live'], {}, 'EXPECTED_SUBDOMAIN_REQUIRED'],
    [['--live', '--expected-subdomain', 'other-account'], {}, 'SUBDOMAIN_MISMATCH'],
    [[...live, '--expected-account-id', 'abc'], {}, 'INVALID_EXPECTED_ACCOUNT_ID'],
    [['--token', env.KOMMO_TOKEN], {}, 'INVALID_ARGUMENTS'],
    [['--expected-subdomain'], {}, 'INVALID_ARGUMENTS'],
    [[...live, '--live'], {}, 'INVALID_ARGUMENTS'],
  ]) {
    const r = await runDoctor(args, { env: { ...env, ...override }, fetchImpl: noNetwork });
    assert.equal(r.code, code);
    assert.equal(r.requests, 0);
    assertSafe(r);
  }
});

test('live uses only the exact account GET with redirect forbidden; sanitizes account output', async () => {
  let calls = 0;
  const r = await runDoctor(live, { env, fetchImpl: async (url, options) => {
    calls++;
    assert.equal(url, 'https://example-only.kommo.com/api/v4/account');
    assert.equal(options.method, 'GET');
    assert.equal(options.redirect, 'error');
    assert.equal(options.headers.Authorization, `Bearer ${env.KOMMO_TOKEN}`);
    assert.ok(options.signal instanceof AbortSignal);
    return ok({ ...account, arbitrary_secret: env.KOMMO_TOKEN, name: 'private-body-marker' });
  } });
  assert.equal(calls, 1);
  assert.equal(r.status, 'identity_observed');
  assert.equal(r.identity_verified, false);
  assert.equal(r.account_id, account.id);
  assertSafe(r);
});

test('expected account ID is checked for success and failure, including environment config', async () => {
  const verified = await runDoctor([...live, '--expected-account-id', '123456'], {
    env, fetchImpl: async () => ok(account),
  });
  assert.equal(verified.status, 'identity_verified');
  assert.equal(verified.identity_verified, true);
  const mismatch = await runDoctor(live, {
    env: { ...env, KOMMO_EXPECTED_ACCOUNT_ID: '999999' }, fetchImpl: async () => ok(account),
  });
  assert.equal(mismatch.code, 'ACCOUNT_MISMATCH');
  const wrongSubdomain = await runDoctor(live, {
    env, fetchImpl: async () => ok({ ...account, subdomain: 'other-account' }),
  });
  assert.equal(wrongSubdomain.code, 'ACCOUNT_MISMATCH');
  for (const r of [verified, mismatch, wrongSubdomain]) assertSafe(r);
});

test('HTTP failures do not retry or emit raw bodies, headers or redirect locations', async () => {
  for (const status of [301, 401, 403, 422, 429, 500, 503]) {
    let calls = 0;
    const r = await runDoctor(live, { env, fetchImpl: async () => {
      calls++;
      return new Response(`private-body-marker ${env.KOMMO_TOKEN}`, {
        status, headers: { location: 'https://evil.test', 'content-type': 'text/html' },
      });
    } });
    assert.equal(calls, 1);
    assert.equal(r.code, status === 301 ? 'REDIRECT_REJECTED' : 'HTTP_ERROR');
    assert.equal(r.status, 'failed');
    assertSafe(r);
  }
});

test('network exceptions and invalid responses remain sanitized', async () => {
  for (const [fetchImpl, code] of [
    [async () => { throw new Error(`private-body-marker ${env.KOMMO_TOKEN}`); }, 'NETWORK_OR_TIMEOUT'],
    [async () => new Response('<html>private-body-marker</html>'), 'INVALID_CONTENT_TYPE'],
    [async () => new Response('{bad', { headers: { 'content-type': 'application/json' } }), 'INVALID_JSON'],
    [async () => ok({ id: 1 }), 'INVALID_ACCOUNT_SCHEMA'],
    [async () => ok({ ...account, id: '123456' }), 'INVALID_ACCOUNT_SCHEMA'],
    [async () => ok({ ...account, id: 0 }), 'INVALID_ACCOUNT_SCHEMA'],
  ]) {
    const r = await runDoctor(live, { env, fetchImpl });
    assert.equal(r.code, code);
    assertSafe(r);
  }
});
