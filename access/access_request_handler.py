from access.models import AccessRequest
from access.serializers import AccessRequestSerializer


class AccessRequestHandler:
    def create(self, admin, data):
        # Discarding all other keys provided in the data as
        # only the following fields should be updated.
        data = {
            "admin": admin,
            "request_reason": data.get("request_reason"),
            "user_id": data["user_id"],
        }
        req = AccessRequestSerializer().create(data)
        return AccessRequestSerializer(req).data

    def get_request_list(self, query):
        data = {"pending": [], "approved": [], "rejected": []}
        requests = AccessRequest.objects.filter(**query)
        requests = AccessRequestSerializer(requests, many=True).data
        for req in requests:
            data[req.status].append(req)
        return data

    def take_decision(self, acccess_req_id, superadmin, data):
        # Discarding all other keys provided in the data as
        # only the following fields should be updated.
        data = {
            "superadmin": superadmin,
            "decision_reason": data.get("decision_reason"),
            "status": data["status"],
        }
        AccessRequest.objects.filter(uuid=acccess_req_id).update(**data)
        req = AccessRequest.objects.get(uuid=acccess_req_id)
        return AccessRequestSerializer(req).data
