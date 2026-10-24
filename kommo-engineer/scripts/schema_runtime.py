"""Validate the explicitly supported JSON Schema subset used by this package.

No network/dependency. Unknown assertion keywords fail closed. This is not a
general Draft 2020-12 implementation; schemas requiring $ref/oneOf are rejected.
"""
import re
TYPES={'object':dict,'array':list,'string':str,'integer':int,'number':(int,float),'boolean':bool,'null':type(None)}
KEYS={'$schema','title','description','type','required','properties','additionalProperties','items','enum','const','minimum','minItems','minLength','pattern'}
def validate(value,schema,path='$'):
    unknown=set(schema)-KEYS
    if unknown:raise ValueError('Unsupported schema keywords: '+','.join(sorted(unknown)))
    typ=schema.get('type'); allowed=typ if isinstance(typ,list) else [typ] if typ else []
    if allowed and not any(isinstance(value,TYPES[t]) and not (isinstance(value,bool) and t in ('integer','number')) for t in allowed):
        raise ValueError(path+': invalid type')
    if 'enum' in schema and value not in schema['enum']:raise ValueError(path+': invalid enum')
    if 'const' in schema and value!=schema['const']:raise ValueError(path+': invalid constant')
    if isinstance(value,dict):
        missing=set(schema.get('required',[]))-set(value)
        if missing:raise ValueError(path+': missing '+','.join(sorted(missing)))
        props=schema.get('properties',{})
        for key,v in value.items():
            if key in props:validate(v,props[key],path+'.'+key)
            elif schema.get('additionalProperties') is False:raise ValueError(path+': unexpected '+key)
    if isinstance(value,list):
        if len(value)<schema.get('minItems',0):raise ValueError(path+': too few items')
        for i,v in enumerate(value):validate(v,schema.get('items',{}),f'{path}[{i}]')
    if isinstance(value,str):
        if len(value)<schema.get('minLength',0):raise ValueError(path+': too short')
        if 'pattern' in schema and not re.search(schema['pattern'],value):raise ValueError(path+': pattern mismatch')
    if isinstance(value,(int,float)) and 'minimum' in schema and value<schema['minimum']:raise ValueError(path+': below minimum')
