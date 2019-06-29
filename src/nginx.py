"""
Provide implements of the Nginx domain.
"""
from src.constants import NGINX_LOAD_BALANCER_CONFIG_TEMPLATE


class CreationNginxLoadBalancerConfigFile:
    """
    Implements creation of Nginx load balancer config file transaction.
    """

    def __init__(self, port):
        """
        Constructor.
        """
        self.port = port

    @staticmethod
    def get_host_from_url(url):
        """
        Remove protocol and last slash from the URL.
        """
        return url.replace('https://', '').replace('/', '')

    def with_urls(self, urls):
        """
        Creation of Nginx load balancer config file with specified URLs.
        """
        upstream_server_localhosts_text = ''
        upstream_server_configs_text = ''

        for index, url in enumerate(urls):
            url_without_last_slash = url[:-1]
            host_from_url = self.get_host_from_url(url=url)

            upstream_server_configs_text += \
                f'\tserver <\n\t\tlisten 800{index};\n\n\t\tlocation / ' + \
                f'<\n\t\t\tproxy_set_header HOST {host_from_url};\n\t\t\t' + \
                f'proxy_pass {url_without_last_slash};\n\t\t>\n\t>\n\n'

            upstream_server_localhosts_text += f'\t\tserver 127.0.0.1:800{index};\n'

        nginx_load_balancer_config_file_ready_to_use = NGINX_LOAD_BALANCER_CONFIG_TEMPLATE.format(
            port=self.port,
            upstream_server_localhosts=upstream_server_localhosts_text,
            upstream_server_configs=upstream_server_configs_text,
        )

        nginx_load_balancer_config_file_ready_to_use = \
            nginx_load_balancer_config_file_ready_to_use.replace('<', '{').replace('>', '}')

        with open('nginx.conf', 'w') as nginx_config:
            nginx_config.write(nginx_load_balancer_config_file_ready_to_use)
