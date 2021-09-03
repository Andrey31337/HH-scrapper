import csv

def save_to_csv(jobs):
  file = open('test.csv',mode='w')
  writer = csv.writer(file)
  writer.writerow (['title','company','company_link','link','company_www'])
  for job in jobs:
    print(job)
    writer.writerow(list(job.values()))
  return