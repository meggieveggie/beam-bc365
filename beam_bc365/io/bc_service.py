""":class:`~apache_beam.transforms.ptransform.PTransform` is for reading from
and writing to relational databases. SQLAlchemy_ is used for interfacing the
databases.
.. _SQLAlchemy: https://www.sqlalchemy.org/
"""

from __future__ import division, print_function

from apache_beam import PTransform, Create, ParDo, DoFn

from beam_bc365.io.bc_service_api import BusinessCentralSource

class ReadFromService(PTransform):
    """A :class:`~apache_beam.transforms.ptransform.PTransform` for reading
    tables on relational databases.
    It outputs a :class:`~apache_beam.pvalue.PCollection` of
    ``dict:s``, each corresponding to a row in the target database table.
    Args:
        source_config (SourceConfiguration): specifies the target database.
        table_name (str): the name of the table to be read.
        query (str): the SQL query to run against the table.
    Examples:
        Reading from a table on a postgres database. ::
            import apache_beam as beam
            from apache_beam.options.pipeline_options import PipelineOptions
            from beam_bc365.io import bc_service
            service_config = bc_service.ServiceConfiguration(
                username='foo',
                service_key='api-key',
                companies=['Cranos'],
                service='G_L_ENTRY',
                instance='Sandbox',
                instance_id="2E0B815D-A1AC-491B-BD09-0876DACC2A12"
            )
            with beam.Pipeline(options=PipelineOptions()) as p:
                records = p | "Reading records from service" >>  bc_service.ReadFromService(
                    service_config=service_config,
                )
                records | 'Writing to stdout' >> beam.Map(print)
        The output will be something like ::
            {'name': 'Jan', 'num': 1}
            {'name': 'Feb', 'num': 2}
        Where "name" and "num" are the column names.
    """

    def __init__(self, service_config, *args, **kwargs):
        super(ReadFromService, self).__init__(*args, **kwargs)
        self._read_args = dict(service_config=service_config)

    def expand(self, pcoll):
        return (
            pcoll
            | Create([self._read_args])
            | ParDo(_ReadFromWebService())
        )


class _ReadFromWebService(DoFn):
    def process(self, element):
        bc_args = dict(element)
        source = BusinessCentralSource(**bc_args)
        try:
            for record in source.read_data():
                yield record
        except:
            raise

