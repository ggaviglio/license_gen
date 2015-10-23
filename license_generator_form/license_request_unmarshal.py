import datetime


class LicenseRequestUnmarshaller(object):

    @staticmethod
    def alfresco(args):
        key_map = {
            ('release_key'): 'release',
            ('field_cloud_sync', 'cloud_sync'): 'cloudsync',
            ('field_holder_name', 'holder_name'): 'h',
            ('field_end_date', 'end_date'): 'e',
            ('field_heartbeat_url', 'heartbeat_url'): 'heartbeaturl',
            ('field_ats_end_date', 'ats_end_date'): 'ats',
            ('field_max_users', 'max_users'): 'mu',
            ('field_no_heartbeat', 'no_heartbeat'): 'noheartbeat',
            ('field_license_type', 'license_type'): 'l',
            ('field_cluster_enabled', 'cluster_enabled'): 'clusterenabled',
            ('field_max_docs', 'max_docs'): 'md',
            ('field_cryptodoc_enabled', 'cryptodoc_enabled'):
                'cryptodocenabled'
        }
        return LicenseRequestUnmarshaller._unmarshal(args, key_map)

    @staticmethod
    def activiti(args):
        key_map = {
            ('field_number_of_admins', 'number_of_admins'): 'numberOfAdmins',
            ('field_holder_name', 'holder_name'): 'h',
            ('field_version', 'version'): 'v',
            ('field_end_date', 'end_date'): 'e',
            ('field_number_of_licenses', 'number_of_licenses'):
                'numberOfLicenses',
            ('field_number_of_editors', 'number_of_editors'):
                'numberOfEditors',
            ('field_number_of_processes', 'number_of_processes'):
                'numberOfProcesses',
            ('field_number_of_apps', 'number_of_apps'): 'numberOfApps',
            ('field_start_date', 'start_date'): 's',
            ('field_multi_tenant', 'multi_tenant'): 'multiTenant',
            ('field_default_tenant', 'default_tenant'): 'defaultTenant'
        }
        return LicenseRequestUnmarshaller._clean_dates(
                ['e', 's'],
                LicenseRequestUnmarshaller._unmarshal(args, key_map)
            )

    @staticmethod
    def _clean_booleans(key, value):
        boolean_fields = [
            'cloudsync',
            'noheartbeat',
            'clusterenabled',
            'cryptodocenabled',
            'multiTenant'
        ]

        if key in boolean_fields:
            return True if \
                value == '1' \
                or value == True \
                or value == 'true' \
                else False
        return value

    @staticmethod
    def _clean_dates(date_keys, args):
        for key in date_keys:
            if key in args.keys() and args[key]:
                args[key] = datetime.datetime.strptime(
                        args[key],
                        '%d/%m/%Y'
                    ).strftime('%Y%m%d')
        return args

    @staticmethod
    def _unmarshal(args, key_map):
        unmarshalled = {}
        for key, value in args.items():
            try:
                mapped_key = next(v for k, v in key_map.items() if key in k)
            except Exception as e:
                continue

            value = LicenseRequestUnmarshaller._clean_booleans(mapped_key, value)

            if value:
                unmarshalled[mapped_key] = value

        return unmarshalled
