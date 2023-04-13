from sqladmin import ModelView
from .models import (
    Run,
    ConfigTenant,
    ConfigAggregator,
    ConfigExperiment,
    ConfigUpstream,
    ConfigExecutor,
    ConfigExecutorProfile,
)


class ConfigTenantAdmin(ModelView, model=ConfigTenant):
    column_list = list(ConfigTenant.__fields__)


class ConfigAggregatorAdmin(ModelView, model=ConfigAggregator):
    column_list = list(ConfigAggregator.__fields__)


class ConfigExperimentAdmin(ModelView, model=ConfigExperiment):
    column_list = list(ConfigExperiment.__fields__)


class ConfigUpstreamAdmin(ModelView, model=ConfigUpstream):
    column_list = list(ConfigUpstream.__fields__)


class ConfigExecutorAdmin(ModelView, model=ConfigExecutor):
    column_list = list(ConfigExecutor.__fields__)


class ConfigExecutorProfileAdmin(ModelView, model=ConfigExecutorProfile):
    column_list = list(ConfigExecutorProfile.__fields__)


class RunAdmin(ModelView, model=Run):
    column_list = list(Run.__fields__)
