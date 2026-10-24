import json
import os
import re
import time
import urllib.error
import urllib.parse
import urllib.request

class APIError(Exception):
    def __init__(self,code,ambiguous=False):
        self.code=code;self.ambiguous=ambiguous
        super().__init__(f'Kommo {code}; '+('reconciliar antes de nova escrita' if ambiguous else 'sem alteração confirmada'))

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,req,fp,code,msg,headers,newurl):return None

def valid_read(path):
    return bool(re.fullmatch(r'/api/v4/(account|bots|(?:leads|contacts|companies)(?:/\d+|/custom_fields(?:/\d+)?)?|leads/pipelines(?:/\d+(?:/statuses(?:/\d+)?)?)?)',path))

def valid_write(method,path):
    return method in ('POST','PATCH') and bool(re.fullmatch(r'/api/v4/((leads|contacts|companies)/custom_fields|leads/pipelines(?:/\d+(?:/statuses(?:/\d+)?)?)?)',path))

class Client:
    def __init__(self,subdomain,token=None,transport=None,sleep=time.sleep):
        if not re.fullmatch(r'[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?',subdomain):raise APIError('invalid_subdomain')
        self.subdomain=subdomain;self.base='https://'+subdomain+'.kommo.com'
        self._token=token or os.environ.get('KOMMO_ACCESS_TOKEN')
        if not self._token or any(c.isspace() for c in self._token):raise APIError('credential_missing_or_invalid')
        self._transport=transport or self._http;self.sleep=sleep;self.calls=0
    def __repr__(self):return f'Client({self.subdomain!r}, credential=[REDACTED])'
    def _http(self,method,path,payload):
        raw=None if payload is None else json.dumps(payload).encode('utf-8')
        req=urllib.request.Request(self.base+path,data=raw,method=method,headers={'Authorization':'Bearer '+self._token,'Accept':'application/hal+json','Content-Type':'application/json'})
        try:
            with urllib.request.build_opener(NoRedirect()).open(req,timeout=15) as response:
                body=response.read(4_000_001)
                if len(body)>4_000_000:raise APIError('response_too_large',method!='GET')
                try:
                    value=json.loads(body) if body else {}
                    if not isinstance(value,dict):raise ValueError('Expected object')
                    return value
                except (ValueError,UnicodeError):raise APIError('invalid_response',method!='GET') from None
        except urllib.error.HTTPError as exc:
            raise APIError(str(exc.code),method!='GET' and exc.code>=500) from None
        except (urllib.error.URLError,TimeoutError,OSError):raise APIError('network_timeout',method!='GET') from None
    def request(self,method,path,payload=None,write_enabled=False):
        bare=path.split('?',1)[0]
        if method=='GET':
            if not valid_read(bare):raise APIError('unsupported_read_path')
            # Query construction must not allow endpoints, credentials, or redirects.
            params=urllib.parse.parse_qs(path.split('?',1)[1] if '?' in path else '',strict_parsing=True)
            if set(params)-{'page','limit','with','query'}:raise APIError('unsupported_query')
            if any(len(v)!=1 for v in params.values()):raise APIError('duplicate_query')
        elif not write_enabled or os.environ.get('KOMMO_ENABLE_WRITES')!='true' or not valid_write(method,bare) or '?' in path:
            raise APIError('writes_disabled_or_unsupported')
        for attempt in range(3 if method=='GET' else 1):
            try:
                self.calls+=1;return self._transport(method,path,payload)
            except APIError as exc:
                if method=='GET' and exc.code in ('429','500','502','503','504','network_timeout') and attempt<2:
                    self.sleep(2**attempt);continue
                raise
    def identity(self,expected_id=None):
        value=self.request('GET','/api/v4/account')
        if not isinstance(value,dict) or type(value.get('id')) is not int or value.get('subdomain')!=self.subdomain:raise APIError('account_identity_unconfirmed')
        if expected_id is not None and str(value['id'])!=str(expected_id):raise APIError('account_mismatch')
        return {key:value.get(key) for key in ('id','subdomain','name','current_user_id')}
    def collection(self,path,key,max_pages=20):
        result=[]
        for page in range(1,max_pages+1):
            value=self.request('GET',path+'?'+urllib.parse.urlencode({'limit':250,'page':page}))
            batch=value.get('_embedded',{}).get(key,[])
            if not isinstance(batch,list):raise APIError('invalid_collection')
            result.extend(batch)
            if not value.get('_links',{}).get('next'):return result
        raise APIError('pagination_limit_incomplete')
