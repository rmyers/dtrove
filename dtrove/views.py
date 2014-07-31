
import json
import logging
import uuid

from django.core.cache import caches
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

CACHE = caches['default']
LOG = logging.getLogger()

SERVICE_CATALOG = {
    "access": {
        "serviceCatalog": [
            {
                "endpoints": [
                    {
                        "publicURL": "http://localhost:8000/osnova/",
                        "region": "IAD",
                        "tenantId": "12345",
                    },
                ],
                "name": "cloudServersOpenStack",
                "type": "compute"
            }
        ],
        "token": {
            "expires": "2012-04-13T13:15:00.000-05:00",
            "id": "aaaaa-bbbbb-ccccc-dddd"
        },
        "user": {
            "RAX-AUTH:defaultRegion": "DFW",
            "id": "161418",
            "name": "demoauthor",
            "roles": [
                {
                    "description": "User Admin Role.",
                    "id": "3",
                    "name": "identity:user-admin"
                }
            ]
        }
    }
}

KEYPAIR = {
    "keypair": {
        "fingerprint": "1e:2c:9b:56:79:4b:45:77:f9:ca:7a:98:2c:b0:d5:3c",
        "name": "keypair-dab428fe-6186-4a14-b3de-92131f76cd39",
        "public_key": "ssh-rsa AAAAB3NzaC1yc2EAAAADAQsdHw== FAKE",
        "user_id": "fake"
    }
}


@csrf_exempt
def fake_os_auth(request, path):
    LOG.error(request.POST)
    return HttpResponse(json.dumps(SERVICE_CATALOG),
                        content_type="application/json")


@csrf_exempt
def fake_os_nova(request, path):
    if 'keypair' in path:
        return HttpResponse(json.dumps(KEYPAIR),
                            content_type="application/json")
    if 'servers' in path:
        if request.method == 'POST':
            server_id = str(uuid.uuid4())
            server = {
                "server": {
                    "security_groups": [],
                    "OS-DCF:diskConfig": "MANUAL",
                    "id": server_id,
                    "links": [],
                    "adminPass": "aabbccddeeff"
                }
            }

            return HttpResponse(json.dumps(server),
                                content_type="application/json")

        elif request.method == 'GET':
            _, server_id = path.split('/')
            key = 'fake_server:%s' % server_id
            # Make it appear to be building
            progress = CACHE.get(key, 0)
            if progress == 0:
                CACHE.set(key, 0)
            if progress < 100:
                progress = CACHE.incr(key, 10)
                status = 'BUILD'
            else:
                progress = 100
                status = 'ACTIVE'

            server = {
                "server": {
                    "accessIPv4": "10.0.0.3",
                    "addresses": {},
                    "created": "2012-08-20T21:11:09Z",
                    "flavor": {
                        "id": "1",
                        "links": []
                    },
                    "hostId": "36",
                    "id": server_id,
                    "image": {
                        "id": "70a599e0-31e7-49b7-b260-868f441e862b",
                        "links": []
                    },
                    "links": [],
                    "metadata": {},
                    "name": "new-server-test",
                    "progress": progress,
                    "status": status,
                    "tenant_id": "openstack",
                    "updated": "2012-08-20T21:11:09Z",
                    "user_id": "fake"
                }
            }

            return HttpResponse(json.dumps(server),
                                content_type="application/json")
