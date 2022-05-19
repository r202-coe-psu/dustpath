from flask_restx import Namespace, Resource
from flask import request, jsonify

from flask_jwt_extended import (
    jwt_required,
    # jwt_refresh_token_required,
    create_access_token,
    create_refresh_token,
    current_user,
)

from dustpath import models
import logging

logger = logging.getLogger(__name__)


api = Namespace("auth", description="Service Authentication")


@api.route("")
class ServiceAuth(Resource):
    def get(self):
        return jsonify({"Hello": "Service Auth"})

    def post(self):
        service_id = request.json.get("service_id", None)
        secret = request.json.get("secret", None)

        try:
            service = models.Service.objects.get(id=service_id, secret=secret)
        except Exception as e:
            logger.exception(e)
            return api.abort(400, "Service not found")

        # project = service.get_project()
        if service.fix_token:
            if service.access_token:
                access_token = service.access_token
            else:
                access_token = create_access_token(
                    identity=service,
                    additional_claims=dict(project_id=str(service.project.id)),
                    expires_delta=False,
                )
                service.access_token = access_token
                service.save()
        else:
            access_token = create_access_token(
                identity=service,
                additional_claims=dict(project_id=str(service.project.id)),
            )
        refresh_token = create_refresh_token(
            identity=service, additional_claims=dict(project_id=str(service.project.id))
        )

        return jsonify(access_token=access_token, refresh_token=refresh_token)


@api.route("/refresh")
class RefreshServiceAuth(Resource):
    @jwt_required(refresh=True)
    def post(self):
        service = current_user
        # project = service.get_project()
        access_token = create_access_token(
            identity=service, additional_claims=dict(project_id=str(service.project.id))
        )

        return jsonify(access_token=access_token)
