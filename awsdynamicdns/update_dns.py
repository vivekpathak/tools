import logging
import boto3
import json
import pickle
import requests
import sys


SERIALIZE_FILE = '/tmp/ipaddress.pkl'
FORMAT = '%(asctime)-15s %(levelname)s %(message)s'
logging.basicConfig(format=FORMAT, filename='/tmp/dns.log',level=logging.INFO)


def get_public_ip():
    url = 'https://api.my-ip.io/ip'
    return requests.get(url).text


def get_old_ip():
    try:
        ipstr = pickle.load(open(SERIALIZE_FILE, 'rb'))
        return ipstr
    except:
        logging.exception("did not find saved ip")
        return None


def save_new_ip(ipstr):
    logging.info("write the ip to pickle file")
    pickle.dump(ipstr, open(SERIALIZE_FILE, 'wb'))
    logging.info("done writing the ip to pickle file")


def update_dns(domain_name, ipstr):
    client = boto3.client('route53')
    for zone in client.list_hosted_zones()['HostedZones']:
        if zone["Name"].startswith(domain_name):
            zone_id = zone['Id']
            logging.info("about to change %s %s", zone_id, ipstr)
            #zone_info = client.get_hosted_zone(Id=zone_id)
            #print(zone_info)
            #sets = client.list_resource_record_sets(HostedZoneId=zone_id)
            #print(json.dumps(sets))
            #sys.exit(0)

            client.change_resource_record_sets(
                HostedZoneId=zone_id,
                ChangeBatch={
                    'Comment': 'update dns',
                    'Changes': [
                        {
                            'Action': 'UPSERT',
                            'ResourceRecordSet': {
                                 "Name": domain_name + ".",
                                 "Type": "A",
                                 "TTL": 300,
                                 "ResourceRecords": [
                                     {
                                         "Value": ipstr
                                     }
                                 ]
                            }
                        }
                    ]
                }
            )


if __name__ == "__main__":
    ipstr = get_public_ip()
    logging.info("got public ip %s", ipstr)

    if ipstr != get_old_ip():
         update_dns("orgmeta.com", ipstr)
         save_new_ip(ipstr)

    else:
        logging.info("nothing to do")
