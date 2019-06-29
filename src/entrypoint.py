"""
Provide implementation of the command line interface.
"""
import click

from src.heroku import (
    GetHerokuPipelineProductionApplicationsUrls,
    HerokuApi,
)
from src.nginx import CreationNginxLoadBalancerConfigFile


@click.group()
def cli():
    pass


@click.command()
@click.option(
    '--nginx-port',
    type=int,
    required=True,
    help='The port to the Nginx on.',
)
@click.option(
    '--heroku-api-key',
    type=str,
    required=True,
    help='The account\'s Heroku API key.',
)
@click.option(
    '--pipeline-identifier',
    type=str,
    required=True,
    help='Pipeline identifier to fetch applications for balancing.'
)
def create_load_balancer(nginx_port, heroku_api_key, pipeline_identifier):
    """
    Create Nginx load balancer config file with pipeline's production applications URLs.
    """
    print(nginx_port, heroku_api_key, pipeline_identifier)

    heroku_api = HerokuApi(
        key=heroku_api_key,
    )

    get_heroku_pipeline_production_applications_urls = GetHerokuPipelineProductionApplicationsUrls(
        heroku_api=heroku_api,
    )

    pipeline_production_applications_urls = get_heroku_pipeline_production_applications_urls.by_pipeline_identifier(
        identifier=pipeline_identifier,
    )

    CreationNginxLoadBalancerConfigFile(port=nginx_port).with_urls(urls=pipeline_production_applications_urls)


if __name__ == '__main__':
    cli.add_command(create_load_balancer)
    cli()
