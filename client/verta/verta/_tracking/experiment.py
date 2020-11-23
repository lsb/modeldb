# -*- coding: utf-8 -*-

from __future__ import print_function

import requests
import warnings

from .entity import _ModelDBEntity
from .experimentruns import ExperimentRuns

from .._protos.public.common import CommonService_pb2 as _CommonCommonService
from .._protos.public.modeldb import ExperimentService_pb2 as _ExperimentService
from .._protos.public.modeldb import CommonService_pb2 as _CommonService

from ..external import six

from .._internal_utils import (
    _utils,
)


class Experiment(_ModelDBEntity):
    """
    Object representing a machine learning Experiment.

    This class provides read/write functionality for Experiment metadata and access to its Experiment
    Runs.

    There should not be a need to instantiate this class directly; please use
    :meth:`Client.set_experiment() <verta.client.Client.set_experiment>`.

    Attributes
    ----------
    id : str
        ID of this Experiment.
    name : str
        Name of this Experiment.
    expt_runs : :class:`~verta._tracking.ExperimentRuns`
        Experiment Runs under this Experiment.

    """
    def __init__(self, conn, conf, msg):
        super(Experiment, self).__init__(conn, conf, _ExperimentService, "experiment", msg)

    def __repr__(self):
        return "<Experiment \"{}\">".format(self.name)

    @property
    def name(self):
        self._refresh_cache()
        return self._msg.name

    @property
    def expt_runs(self):
        # get runs in this Experiment
        return ExperimentRuns(self._conn, self._conf).with_experiment(self)

    @classmethod
    def _generate_default_name(cls):
        return "Expt {}".format(_utils.generate_default_name())

    def log_tag(self, tag):
        """
        Logs a tag to this Experiment.

        Parameters
        ----------
        tag : str
            Tag.

        """
        if not isinstance(tag, six.string_types):
            raise TypeError("`tag` must be a string")
        self.log_tags([tag])

    def log_tags(self, tags):
        """
        Logs multiple tags to this Experiment.

        Parameters
        ----------
        tags : list of str
            Tags.

        """
        tags = _utils.as_list_of_str(tags)

        Message = _ExperimentService.AddExperimentTags
        msg = Message(id=self.id, tags=tags)
        data = _utils.proto_to_json(msg)
        response = _utils.make_request("POST",
                                       "{}://{}/api/v1/modeldb/experiment/addExperimentTags".format(self._conn.scheme, self._conn.socket),
                                       self._conn, json=data)
        _utils.raise_for_http_error(response)

        self._clear_cache()

    def get_tags(self):
        """
        Gets all tags from this Experiment.

        Returns
        -------
        list of str
            All tags.

        """
        Message = _CommonService.GetTags
        msg = Message(id=self.id)
        data = _utils.proto_to_json(msg)
        response = _utils.make_request("GET",
                                       "{}://{}/api/v1/modeldb/experiment/getExperimentTags".format(self._conn.scheme, self._conn.socket),
                                       self._conn, params=data)
        _utils.raise_for_http_error(response)

        response_msg = _utils.json_to_proto(_utils.body_to_json(response), Message.Response)
        return response_msg.tags

    @classmethod
    def _get_proto_by_id(cls, conn, id):
        Message = _ExperimentService.GetExperimentById
        msg = Message(id=id)
        response = conn.make_proto_request("GET",
                                           "/api/v1/modeldb/experiment/getExperimentById",
                                           params=msg)

        return conn.maybe_proto_response(response, Message.Response).experiment

    @classmethod
    def _get_proto_by_name(cls, conn, name, proj_id):
        Message = _ExperimentService.GetExperimentByName
        msg = Message(project_id=proj_id, name=name)
        response = conn.make_proto_request("GET",
                                           "/api/v1/modeldb/experiment/getExperimentByName",
                                           params=msg)

        return conn.maybe_proto_response(response, Message.Response).experiment

    @classmethod
    def _create_proto_internal(cls, conn, ctx, name, desc=None, tags=None, attrs=None, date_created=None):
        Message = _ExperimentService.CreateExperiment
        msg = Message(project_id=ctx.proj.id, name=name,
                      description=desc, tags=tags, attributes=attrs)
        response = conn.make_proto_request("POST",
                                           "/api/v1/modeldb/experiment/createExperiment",
                                           body=msg)
        expt = conn.must_proto_response(response, Message.Response).experiment
        print("created new Experiment: {}".format(expt.name))
        return expt

    def delete(self):
        """
        Deletes this experiment.

        """
        request_url = "{}://{}/api/v1/modeldb/experiment/deleteExperiment".format(self._conn.scheme, self._conn.socket)
        response = requests.delete(request_url, json={'id': self.id}, headers=self._conn.auth)
        _utils.raise_for_http_error(response)
