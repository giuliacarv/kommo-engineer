import json
import sys
from knowledge import validate
if __name__=='__main__':
    result=validate();print(json.dumps(result,ensure_ascii=False,indent=2));sys.exit(0 if result['valid'] else 1)
