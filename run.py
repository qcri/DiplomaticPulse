"""
run.py
This script reads spider configurations from freebase, and distribute crawling
jobs to multiple scrapyd servers. It will run continuously and repeat at
given interval. It requires python-scrapyd-api, schedule packages.
"""
import sys
import urllib.parse
import argparse
import time
from collections import Counter
from datetime import datetime
import logging
import schedule
from diplomaticpulse.db_elasticsearch.db_es import get_url_configs
from scrapyd_api import ScrapydAPI

FORMAT = "%(message)s"
logging.basicConfig(format=FORMAT, level=logging.INFO)

class JobRaceNotification:
    subject = "jobs couldn't finish in time, scrapyd needs scale up"
    content = "Dear Diplomatic Pulse,\n\nrun.py\n\n"

def domain(url):
    o = urllib.parse.urlparse(url)
    return o.netloc

def takeJobsBalancingSplash(jobs, splashJobs):
    """
    spread slow splash spiders evenly
    """
    logging.info("TJB: %s, %s" % (len(jobs), len(splashJobs)))
    step = max(1, int(len(jobs) / max(1, len(splashJobs))))
    for i, job in enumerate(jobs):
        if i % step == 0:
            try:
                splashJob = splashJobs.pop()
                yield splashJob
            except IndexError:
                pass

        yield job

    # This loops through the remaining splash jobs and executes them.
    for i, sjob in enumerate(splashJobs):
        yield sjob

def submitJobs(options):
    configs = get_url_configs()
    counts = Counter([c['country'] for c in configs])
    logging.info('found %d configs from %d countries in database', len(configs), len(counts))

    if options.dry_run:
        logging.info('{:5s} {}'.format('COUNT', 'COUNTY'))
        for country, count in counts.most_common():
            logging.info("{:5} {}".format(count, country))

    for i, scrapydUrl in enumerate(scrapyds):
        logging.info('for scrapyd url: %s', scrapydUrl)
        logging.info('{:10.10} {}'.format('Spider', 'Url'))
        if not options.dry_run:
            api = ScrapydAPI(scrapydUrl)
            numRunningJobs = len(api.list_jobs(options.project).get('pending', []))
            logging.info("found %d pending job for url %s", numRunningJobs, scrapydUrl)
            if numRunningJobs > 0:
                logging.warning("Skipped this run! Please scale up vm or increase the interval between job runs")
                continue

        jobs = []
        splashJobs = []

        for j, config in enumerate(configs):
            if j % len(scrapyds) != i: continue
            spider = config['content_type']
            project="diplomaticpulse"
            urlToCrawl=config['url']
            jobid='{}-{}-{}'.format(
                config['country'],
                spider,
                datetime.now().isoformat().split('.')[0])
            if spider == 'javascript':
                splashJobs.append((project, spider, urlToCrawl, jobid))
            else:
                jobs.append((project, spider, urlToCrawl, jobid))

        allJobs = takeJobsBalancingSplash(jobs, splashJobs) if len(splashJobs) > 0 else jobs

        for (project, spider, url, jobid) in allJobs:
            logging.info('{:10.10} {}'.format(spider, url))
            if not options.dry_run:
                api.schedule(project=project, spider=spider, url=url, jobid=jobid)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true', default=False,
                        help='do not submit jobs')
    parser.add_argument('--delay', type=int, default=30,
                        help='delay start for n seconds')
    parser.add_argument('--every', type=int, default=5,
                        help='run spiders at x minutes interval')
    parser.add_argument('--project', type=str, default='diplomaticpulse',
                        help='the name of project on scrapyd server')
    parser.add_argument('scrapyd', type=str, nargs='+',
                        help='scrapyd url (can be multiple separated with space)')
    options = parser.parse_args()

    scrapyds = options.scrapyd
    logging.info('scrapyd servers: %s', scrapyds)

    logging.info('run all spiders every %d minutes', options.every)
    schedule.every(options.every).minutes.do(submitJobs, options)

    time.sleep(options.delay)
    submitJobs(options)
    if options.dry_run:
        sys.exit(0)

    while True:
        schedule.run_pending()
        time.sleep(1)