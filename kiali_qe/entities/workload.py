from kiali_qe.entities import EntityBase, DeploymentStatus, Requests
from kiali_qe.components.enums import HealthType


class Workload(EntityBase):

    def __init__(self, name, namespace, workload_type,
                 istio_sidecar=None, app_label=None, version_label=None, health=None):
        self.name = name
        self.namespace = namespace
        self.workload_type = workload_type
        self.istio_sidecar = istio_sidecar
        self.app_label = app_label
        self.version_label = version_label
        self.health = health

    def __str__(self):
        return 'name:{}, namespace:{}, type:{}, sidecar:{}, app:{}, version:{}, health:{}'.format(
            self.name, self.namespace, self.workload_type,
            self.istio_sidecar, self.app_label, self.version_label, self.health)

    def __repr__(self):
        return "{}({}, {}, {}, {}, {}, {}, {})".format(
            type(self).__name__, repr(self.name),
            repr(self.namespace), repr(self.workload_type),
            repr(self.istio_sidecar), repr(self.app_label),
            repr(self.version_label), repr(self.health))

    def __eq__(self, other):
        return self.is_equal(other, advanced_check=True)

    def is_equal(self, other, advanced_check=True):
        # basic check
        if not isinstance(other, Workload):
            return False
        if self.name != other.name:
            return False
        if self.namespace != other.namespace:
            return False
        if self.workload_type != other.workload_type:
            return False
        # advanced check
        if advanced_check:
            if self.istio_sidecar != other.istio_sidecar:
                return False
            if self.app_label != other.app_label:
                return False
            if self.version_label != other.version_label:
                return False
            if self.health != other.health:
                return False
        return True


class WorkloadDetails(EntityBase):

    def __init__(self, name, workload_type, created_at, resource_version,
                 istio_sidecar=False, health=None, **kwargs):
        if name is None:
            raise KeyError("'name' should not be 'None'")
        self.name = name
        self.workload_type = workload_type
        self.istio_sidecar = istio_sidecar
        self.health = health
        self.created_at = created_at
        self.resource_version = resource_version
        self.replicas = kwargs['replicas']\
            if 'replicas' in kwargs else None
        self.availableReplicas = kwargs['availableReplicas']\
            if 'availableReplicas' in kwargs else None
        self.unavailableReplicas = kwargs['unavailableReplicas']\
            if 'unavailableReplicas' in kwargs else None
        self.workload_type = kwargs['workload_type']\
            if 'workload_type' in kwargs else None
        self.created_at = kwargs['created_at']\
            if 'created_at' in kwargs else None
        self.resource_version = kwargs['resource_version']\
            if 'resource_version' in kwargs else None
        self.pods_number = kwargs['pods_number']\
            if 'pods_number' in kwargs else None
        self.services_number = kwargs['services_number']\
            if 'services_number' in kwargs else None
        self.services = kwargs['services']\
            if 'services' in kwargs else None
        self.pods = kwargs['pods']\
            if 'pods' in kwargs else None

    def __str__(self):
        return 'name:{}, type:{}, sidecar:{}, createdAt:{}, resourceVersion:{}, health{}'.format(
            self.name, self.workload_type,
            self.istio_sidecar, self.created_at, self.resource_version, self.health)

    def __repr__(self):
        return "{}({}, {}, {}, {}, {}, {})".format(
            type(self).__name__, repr(self.name), repr(self.workload_type),
            repr(self.istio_sidecar), repr(self.created_at),
            repr(self.resource_version), repr(self.health))

    def __eq__(self, other):
        return self.is_equal(other, advanced_check=True)

    def is_equal(self, other, advanced_check=True):
        # basic check
        if not isinstance(other, WorkloadDetails):
            return False
        if self.name != other.name:
            return False
        if self.workload_type != other.workload_type:
            return False
        if self.created_at != other.created_at:
            return False
        if self.resource_version != other.resource_version:
            return False
        # advanced check
        if advanced_check:
            if self.istio_sidecar != other.istio_sidecar:
                return False
            if self.health != other.health:
                return False
        return True


class WorkloadPod(EntityBase):

    def __init__(self, name, created_at, created_by,
                 istio_init_containers=None, istio_containers=None):
        self.name = name
        self.created_at = created_at
        self.created_by = created_by
        self.istio_init_containers = istio_init_containers
        self.istio_containers = istio_containers

    def __str__(self):
        return 'name:{}, created_at:{}, created_by:{},\
            istio_init_containers:{}, istio_containers:{}'.format(
            self.name, self.created_at, self.created_by,
            self.istio_init_containers, self.istio_containers)

    def __repr__(self):
        return "{}({}, {}, {}, {}, {}, {})".format(
            type(self).__name__, repr(self.name),
            repr(self.created_at), repr(self.created_by),
            repr(self.istio_init_containers), repr(self.istio_containers))

    def __eq__(self, other):
        return self.is_equal(other, advanced_check=True)

    def is_equal(self, other, advanced_check=True):
        # basic check
        if not isinstance(other, WorkloadPod):
            return False
        if self.name != other.name:
            return False
        # TODO compare multiple created at dates
        # if self.created_at != other.created_at:
        #    return False
        if self.created_by != other.created_by:
            return False
        # advanced check
        if advanced_check:
            if self.istio_init_containers != other.istio_init_containers:
                return False
            if self.istio_containers != other.istio_containers:
                return False
        return True


class WorkloadHealth(EntityBase):

    def __init__(self, deployment_status, requests):
        self.deployment_status = deployment_status
        self.requests = requests

    def __str__(self):
        return 'deployment_status:{}, requests:{}'.format(
            self.deployment_status, self.requests)

    def __repr__(self):
        return "{}({}, {}, {})".format(
            type(self).__name__,
            repr(self.deployment_status), repr(self.requests))

    def is_healthy(self):
        if self.deployment_status.is_healthy() == HealthType.NA \
                and self.requests.is_healthy() == HealthType.NA:
            return HealthType.NA
        elif self.deployment_status.is_healthy() == HealthType.FAILURE \
                or self.requests.is_healthy() == HealthType.FAILURE:
            return HealthType.FAILURE
        else:
            return HealthType.HEALTHY

    def is_equal(self, other):
        if not isinstance(other, WorkloadHealth):
            return False
        if not self.deployment_status.is_equal(other.deployment_status):
            return False
        if not self.requests.is_equal(other.requests):
            return False
        return True

    @classmethod
    def get_from_rest(cls, health):
        # update deployment status
        _deployment_status = None
        if 'deploymentStatus' in health:
            _deployment_status = DeploymentStatus(
                name=health['deploymentStatus']['name'],
                replicas=health['deploymentStatus']['replicas'],
                available=health['deploymentStatus']['available'])
            # update requests
        _r_rest = health['requests']
        _requests = Requests(
            request_count=_r_rest['requestCount'],
            request_error_count=_r_rest['requestErrorCount'])
        return WorkloadHealth(
            deployment_status=_deployment_status, requests=_requests)